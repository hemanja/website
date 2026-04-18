"""
Flask主应用 - 多站点电商模板
"""
import os
import json
import uuid
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from config import Config
from models import db, User, Product, Category, Inquiry, FAQ, News, SiteConfig as SiteConfigModel
from site_configs import SiteConfig

app = Flask(__name__)
app.config.from_object(Config)

# 初始化数据库
db.init_app(app)

# 登录管理
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'admin_login'

# 全局模板上下文
@app.context_processor
def inject_site_config():
    """让所有模板都能访问site_config"""
    return dict(site_config=get_current_site_config(), now=datetime.now)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ========== 工具函数 ==========
def get_current_site_config():
    """获取当前站点配置（未来可从域名或子域名自动识别）"""
    # TODO: 根据域名自动选择站点配置
    return SiteConfig


def generate_order_no():
    """生成订单号"""
    return f"INQ{datetime.now().strftime('%Y%m%d%H%M%S')}{uuid.uuid4().hex[:4].upper()}"


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS


def save_upload(file):
    """保存上传文件"""
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        filename = f"{timestamp}_{filename}"
        filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
        file.save(filepath)
        return f"/static/uploads/{filename}"
    return None


# ========== GEO优化：生成结构化数据 ==========
def generate_organization_schema(site_config):
    """生成Organization结构化数据"""
    return {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": site_config.BRAND_NAME,
        "alternateName": site_config.BRAND_NAME_CN,
        "url": f"https://{site_config.DOMAIN}",
        "foundingDate": site_config.ESTABLISHED,
        "address": {
            "@type": "PostalAddress",
            "addressCountry": "CN",
            "addressLocality": site_config.ADDRESS_EN.split(',')[0] if site_config.ADDRESS_EN else "Foshan",
            "addressRegion": "Guangdong"
        },
        "award": site_config.CERTIFICATIONS,
        "contactPoint": [{
            "@type": "ContactPoint",
            "contactType": "sales",
            "email": site_config.EMAIL,
            "telephone": site_config.PHONE,
            "availableLanguage": ["Chinese", "English"]
        }]
    }


def generate_product_schema(product, site_config):
    """生成Product结构化数据"""
    return {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": product.name_en,
        "alternateName": product.name,
        "description": product.description_en,
        "brand": {"@type": "Brand", "name": site_config.BRAND_NAME},
        "manufacturer": {"@type": "Organization", "name": site_config.BRAND_NAME_CN},
        "category": product.category.name_en if product.category else "",
        "offers": {
            "@type": "Offer",
            "price": "Inquiry",
            "priceCurrency": "USD",
            "availability": "https://schema.org/InStock" if product.stock > 0 else "https://schema.org/PreOrder",
            "minimumOrderQuantity": product.min_order,
            "deliveryLeadTime": product.lead_time
        },
        "additionalProperty": [
            {"@type": "PropertyValue", "name": "Temperature Range", "value": product.temperature_range or "N/A"},
            {"@type": "PropertyValue", "name": "Voltage Rating", "value": product.voltage_rating or "N/A"},
            {"@type": "PropertyValue", "name": "Certifications", "value": product.certifications or "N/A"}
        ]
    }


def generate_faq_schema(faqs):
    """生成FAQ结构化数据"""
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [{
            "@type": "Question",
            "name": faq.question_en if session.get('lang') == 'en' else faq.question,
            "acceptedAnswer": {
                "@type": "Answer",
                "text": faq.answer_en if session.get('lang') == 'en' else faq.answer
            }
        } for faq in faqs]
    }


# ========== 前台路由 ==========
@app.route('/')
def index():
    """首页"""
    site_config = get_current_site_config()
    lang = session.get('lang', 'zh')
    
    # 获取数据
    categories = Category.query.filter_by(is_active=True).all()
    featured_products = Product.query.filter_by(is_featured=True, is_active=True).limit(8).all()
    faqs = FAQ.query.filter_by(is_active=True).order_by(FAQ.order).limit(5).all()
    
    # GEO结构化数据
    org_schema = generate_organization_schema(site_config)
    faq_schema = generate_faq_schema(faqs)
    
    return render_template('index.html',
        site_config=site_config,
        categories=categories,
        featured_products=featured_products,
        faqs=faqs,
        org_schema=org_schema,
        faq_schema=faq_schema,
        lang=lang
    )


@app.route('/lang/<lang>')
def set_language(lang):
    """切换语言"""
    if lang in ['zh', 'en']:
        session['lang'] = lang
    return redirect(request.referrer or url_for('index'))


@app.route('/products')
def products():
    """产品列表"""
    site_config = get_current_site_config()
    lang = session.get('lang', 'zh')
    
    category_slug = request.args.get('category')
    page = request.args.get('page', 1, type=int)
    per_page = 12
    
    query = Product.query.filter_by(is_active=True)
    if category_slug:
        category = Category.query.filter_by(slug=category_slug).first()
        if category:
            query = query.filter_by(category_id=category.id)
    
    products = query.order_by(Product.created_at.desc()).paginate(page=page, per_page=per_page)
    categories = Category.query.filter_by(is_active=True).all()
    
    return render_template('products.html',
        site_config=site_config,
        products=products,
        categories=categories,
        current_category=category_slug,
        lang=lang
    )


@app.route('/product/<slug>')
def product_detail(slug):
    """产品详情"""
    site_config = get_current_site_config()
    lang = session.get('lang', 'zh')
    
    product = Product.query.filter_by(slug=slug, is_active=True).first_or_404()
    product.views += 1
    db.session.commit()
    
    # 相关产品
    related = Product.query.filter_by(category_id=product.category_id, is_active=True)\
        .filter(Product.id != product.id).limit(4).all()
    
    # GEO结构化数据
    product_schema = generate_product_schema(product, site_config)
    
    return render_template('product_detail.html',
        site_config=site_config,
        product=product,
        related_products=related,
        product_schema=product_schema,
        lang=lang
    )


@app.route('/category/<slug>')
def category(slug):
    """分类页面"""
    return redirect(url_for('products', category=slug))


@app.route('/about')
def about():
    """关于我们"""
    site_config = get_current_site_config()
    lang = session.get('lang', 'zh')
    return render_template('about.html', site_config=site_config, lang=lang)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """联系我们 / 提交询价"""
    site_config = get_current_site_config()
    lang = session.get('lang', 'zh')
    
    if request.method == 'POST':
        # 保存询价
        inquiry = Inquiry(
            order_no=generate_order_no(),
            name=request.form.get('name'),
            email=request.form.get('email'),
            company=request.form.get('company'),
            phone=request.form.get('phone'),
            country=request.form.get('country'),
            message=request.form.get('message'),
            items=request.form.get('items'),  # JSON购物车数据
            ip_address=request.remote_addr,
            user_agent=request.user_agent.string[:255],
            source=request.form.get('source', 'contact_form')
        )
        db.session.add(inquiry)
        db.session.commit()
        
        flash('提交成功！我们会尽快联系您。' if lang == 'zh' else 'Submitted successfully! We will contact you soon.')
        return redirect(url_for('contact'))
    
    return render_template('contact.html', site_config=site_config, lang=lang)


@app.route('/faq')
def faq():
    """FAQ页面"""
    site_config = get_current_site_config()
    lang = session.get('lang', 'zh')
    
    faqs = FAQ.query.filter_by(is_active=True).order_by(FAQ.order).all()
    faq_schema = generate_faq_schema(faqs)
    
    return render_template('faq.html', site_config=site_config, faqs=faqs, faq_schema=faq_schema, lang=lang)


@app.route('/news')
def news():
    """新闻/公告"""
    site_config = get_current_site_config()
    lang = session.get('lang', 'zh')
    
    articles = News.query.filter_by(is_published=True).order_by(News.published_at.desc()).all()
    return render_template('news.html', site_config=site_config, articles=articles, lang=lang)


# ========== API路由 ==========
@app.route('/api/cart', methods=['POST'])
def api_cart():
    """购物车API"""
    data = request.get_json()
    session['cart'] = data.get('items', [])
    return jsonify({'success': True, 'count': len(session.get('cart', []))})


@app.route('/api/inquiry', methods=['POST'])
def api_inquiry():
    """提交询价API"""
    data = request.get_json()
    
    inquiry = Inquiry(
        order_no=generate_order_no(),
        name=data.get('name'),
        email=data.get('email'),
        company=data.get('company'),
        phone=data.get('phone'),
        country=data.get('country'),
        message=data.get('message'),
        items=json.dumps(data.get('items', [])),
        ip_address=request.remote_addr,
        source=data.get('source', 'api')
    )
    db.session.add(inquiry)
    db.session.commit()
    
    return jsonify({'success': True, 'order_no': inquiry.order_no})


# ========== 后台管理路由 ==========
@app.route('/admin')
@login_required
def admin_dashboard():
    """管理后台首页"""
    stats = {
        'products': Product.query.count(),
        'categories': Category.query.count(),
        'inquiries': Inquiry.query.filter_by(status='pending').count(),
        'orders_total': Inquiry.query.count()
    }
    recent_inquiries = Inquiry.query.order_by(Inquiry.created_at.desc()).limit(10).all()
    return render_template('admin/dashboard.html', stats=stats, recent_inquiries=recent_inquiries)


@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """管理员登录"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('admin_dashboard'))
        flash('用户名或密码错误')
    
    return render_template('admin/login.html')


@app.route('/admin/logout')
@login_required
def admin_logout():
    logout_user()
    return redirect(url_for('admin_login'))


# ========== 产品管理 ==========
@app.route('/admin/products')
@login_required
def admin_products():
    """产品列表"""
    products = Product.query.order_by(Product.created_at.desc()).all()
    return render_template('admin/products.html', products=products)


@app.route('/admin/product/add', methods=['GET', 'POST'])
@login_required
def admin_product_add():
    """添加产品"""
    categories = Category.query.all()
    
    if request.method == 'POST':
        # 处理图片上传
        main_image = None
        if 'main_image' in request.files:
            main_image = save_upload(request.files['main_image'])
        
        product = Product(
            name=request.form.get('name'),
            name_en=request.form.get('name_en'),
            slug=request.form.get('slug'),
            sku=request.form.get('sku'),
            category_id=request.form.get('category_id'),
            description=request.form.get('description'),
            description_en=request.form.get('description_en'),
            features=request.form.get('features'),
            features_en=request.form.get('features_en'),
            specifications=request.form.get('specifications'),
            price=request.form.get('price'),
            min_order=request.form.get('min_order'),
            lead_time=request.form.get('lead_time'),
            stock=request.form.get('stock', 0, type=int),
            main_image=main_image,
            certifications=request.form.get('certifications'),
            temperature_range=request.form.get('temperature_range'),
            voltage_range=request.form.get('voltage_range'),
            voltage_rating=request.form.get('voltage_rating'),
            meta_title=request.form.get('meta_title'),
            meta_description=request.form.get('meta_description'),
            is_featured='is_featured' in request.form,
            is_active='is_active' in request.form
        )
        db.session.add(product)
        db.session.commit()
        flash('产品添加成功')
        return redirect(url_for('admin_products'))
    
    return render_template('admin/product_form.html', categories=categories, product=None)


@app.route('/admin/product/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def admin_product_edit(id):
    """编辑产品"""
    product = Product.query.get_or_404(id)
    categories = Category.query.all()
    
    if request.method == 'POST':
        # 处理图片上传
        if 'main_image' in request.files and request.files['main_image'].filename:
            product.main_image = save_upload(request.files['main_image'])
        
        product.name = request.form.get('name')
        product.name_en = request.form.get('name_en')
        product.slug = request.form.get('slug')
        product.sku = request.form.get('sku')
        product.category_id = request.form.get('category_id')
        product.description = request.form.get('description')
        product.description_en = request.form.get('description_en')
        product.features = request.form.get('features')
        product.features_en = request.form.get('features_en')
        product.specifications = request.form.get('specifications')
        product.price = request.form.get('price')
        product.min_order = request.form.get('min_order')
        product.lead_time = request.form.get('lead_time')
        product.stock = request.form.get('stock', 0, type=int)
        product.certifications = request.form.get('certifications')
        product.temperature_range = request.form.get('temperature_range')
        product.voltage_range = request.form.get('voltage_range')
        product.voltage_rating = request.form.get('voltage_rating')
        product.meta_title = request.form.get('meta_title')
        product.meta_description = request.form.get('meta_description')
        product.is_featured = 'is_featured' in request.form
        product.is_active = 'is_active' in request.form
        
        db.session.commit()
        flash('产品更新成功')
        return redirect(url_for('admin_products'))
    
    return render_template('admin/product_form.html', categories=categories, product=product)


@app.route('/admin/product/<int:id>/delete', methods=['POST'])
@login_required
def admin_product_delete(id):
    """删除产品"""
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    flash('产品已删除')
    return redirect(url_for('admin_products'))


# ========== 分类管理 ==========
@app.route('/admin/categories')
@login_required
def admin_categories():
    """分类列表"""
    categories = Category.query.all()
    return render_template('admin/categories.html', categories=categories)


@app.route('/admin/category/add', methods=['GET', 'POST'])
@login_required
def admin_category_add():
    """添加分类"""
    if request.method == 'POST':
        image = None
        if 'image' in request.files:
            image = save_upload(request.files['image'])
        
        category = Category(
            name=request.form.get('name'),
            name_en=request.form.get('name_en'),
            slug=request.form.get('slug'),
            description=request.form.get('description'),
            description_en=request.form.get('description_en'),
            image=image
        )
        db.session.add(category)
        db.session.commit()
        flash('分类添加成功')
        return redirect(url_for('admin_categories'))
    
    return render_template('admin/category_form.html', category=None)


# ========== 询价管理 ==========
@app.route('/admin/inquiries')
@login_required
def admin_inquiries():
    """询价列表"""
    status = request.args.get('status')
    query = Inquiry.query
    if status:
        query = query.filter_by(status=status)
    inquiries = query.order_by(Inquiry.created_at.desc()).all()
    return render_template('admin/inquiries.html', inquiries=inquiries, current_status=status)


@app.route('/admin/inquiry/<int:id>')
@login_required
def admin_inquiry_detail(id):
    """询价详情"""
    inquiry = Inquiry.query.get_or_404(id)
    return render_template('admin/inquiry_detail.html', inquiry=inquiry)


# ========== 初始化数据库 ==========
def init_db():
    """初始化数据库"""
    with app.app_context():
        db.create_all()
        
        # 创建默认管理员
        if not User.query.filter_by(username='admin').first():
            admin = User(
                username='admin',
                email='admin@ycsleeve.com',
                password_hash=generate_password_hash('admin123'),
                is_admin=True
            )
            db.session.add(admin)
            db.session.commit()
            print("默认管理员创建成功: admin / admin123")


# ========== 运行 ==========
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        # 创建默认管理员
        if not User.query.first():
            admin = User(
                username='admin',
                email='admin@ycsleeve.com',
                password_hash=generate_password_hash('admin123'),
                is_admin=True
            )
            db.session.add(admin)
            db.session.commit()
            print("默认管理员: admin / admin123")
    
    app.run(debug=True, host='0.0.0.0', port=5000)