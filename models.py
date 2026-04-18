from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from config import Config

db = SQLAlchemy()

# 产品分类
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    name_en = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    description_en = db.Column(db.Text)
    image = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=True)
    products = db.relationship('Product', backref='category', lazy=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# 产品
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    name_en = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False)
    sku = db.Column(db.String(50), unique=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    
    # 产品详情
    description = db.Column(db.Text)
    description_en = db.Column(db.Text)
    features = db.Column(db.Text)  # JSON格式特性列表
    features_en = db.Column(db.Text)
    specifications = db.Column(db.Text)  # JSON格式规格参数
    
    # 价格与库存
    price = db.Column(db.String(50))  # 询价/报价
    min_order = db.Column(db.String(50), default='1000 meters')
    lead_time = db.Column(db.String(50), default='7-15 days')
    stock = db.Column(db.Integer, default=0)
    
    # 图片
    main_image = db.Column(db.String(255))
    images = db.Column(db.Text)  # JSON格式图片列表
    
    # 认证与参数
    certifications = db.Column(db.String(200))  # UL,VDE等
    temperature_range = db.Column(db.String(100))
    voltage_range = db.Column(db.String(100))
    voltage_rating = db.Column(db.String(100))
    
    # SEO/GEO
    meta_title = db.Column(db.String(200))
    meta_description = db.Column(db.Text)
    
    # 状态
    is_featured = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    views = db.Column(db.Integer, default=0)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# 订单/询价
class Inquiry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_no = db.Column(db.String(50), unique=True, nullable=False)
    
    # 客户信息
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(200))
    phone = db.Column(db.String(50))
    country = db.Column(db.String(100))
    address = db.Column(db.Text)
    
    # 订单内容
    items = db.Column(db.Text)  # JSON格式购物车
    message = db.Column(db.Text)
    
    # 状态
    status = db.Column(db.String(20), default='pending')  # pending, quoted, confirmed, shipped, completed
    quote_price = db.Column(db.String(100))
    quote_date = db.Column(db.DateTime)
    
    # 跟踪
    ip_address = db.Column(db.String(50))
    user_agent = db.Column(db.String(255))
    source = db.Column(db.String(100))  # 来源渠道
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# 用户/管理员
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255))
    is_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# FAQ
class FAQ(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(500), nullable=False)
    question_en = db.Column(db.String(500), nullable=False)
    answer = db.Column(db.Text, nullable=False)
    answer_en = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(100))  # 产品、订单、认证等
    order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# 公告/新闻
class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    title_en = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True)
    content = db.Column(db.Text)
    content_en = db.Column(db.Text)
    image = db.Column(db.String(255))
    is_published = db.Column(db.Boolean, default=False)
    published_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# 网站设置
class SiteConfig(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False)
    value = db.Column(db.Text)
    description = db.Column(db.String(255))
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
