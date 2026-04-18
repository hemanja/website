"""
示例数据导入脚本
运行: python init_data.py
"""
import os
import sys

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import User, Category, Product, FAQ, News
from werkzeug.security import generate_password_hash

def init_data():
    with app.app_context():
        print("🚀 开始初始化数据...")
        
        # 创建所有表
        db.create_all()
        print("✅ 数据库表创建完成")
        
        # 1. 创建管理员
        if not User.query.filter_by(username='admin').first():
            admin = User(
                username='admin',
                email='admin@ycsleeve.com',
                password_hash=generate_password_hash('admin123'),
                is_admin=True
            )
            db.session.add(admin)
            print("✅ 管理员创建完成: admin / admin123")
        
        # 2. 创建产品分类
        categories_data = [
            {'name': '玻璃纤维套管', 'name_en': 'Fiberglass Sleeves', 'slug': 'fiberglass-sleeves',
             'description': '耐高温玻璃纤维套管，适用于电机、电器绝缘保护'},
            {'name': '硅树脂套管', 'name_en': 'Silicone Fiberglass Sleeves', 'slug': 'silicone-sleeves',
             'description': '硅树脂涂覆玻纤套管，耐温-60°C~+200°C'},
            {'name': '热缩套管', 'name_en': 'Heat Shrink Tubing', 'slug': 'heat-shrink',
             'description': '聚烯烃热缩套管，2:1收缩比，阻燃'},
            {'name': '波纹管', 'name_en': 'Corrugated Tubes', 'slug': 'corrugated-tubes',
             'description': 'PP/PE波纹管，用于线束保护'},
            {'name': '硅胶管', 'name_en': 'Silicone Tubes', 'slug': 'silicone-tubes',
             'description': '食品级硅胶管，耐高温无毒'},
        ]
        
        for cat_data in categories_data:
            if not Category.query.filter_by(slug=cat_data['slug']).first():
                cat = Category(**cat_data)
                db.session.add(cat)
        print("✅ 产品分类创建完成")
        
        db.session.commit()
        
        # 3. 创建示例产品
        products_data = [
            {
                'name': '玻璃纤维套管 1kV',
                'name_en': 'Fiberglass Sleeve 1kV',
                'slug': 'fiberglass-sleeve-1kv',
                'sku': 'FGS-1KV',
                'category_slug': 'fiberglass-sleeves',
                'description': '采用优质玻璃纤维编织而成，具有良好的柔软性和介电性能。工作温度130°C，耐电压1000V。广泛应用于电机、变压器、家用电器的线圈绝缘保护。',
                'description_en': 'Made from high-quality fiberglass braiding with excellent flexibility and dielectric properties. Working temperature 130°C, voltage resistance 1000V. Widely used in motors, transformers, and household appliances.',
                'temperature_range': '-60°C ~ +130°C',
                'voltage_rating': '1kV',
                'certifications': 'UL, VDE, RoHS',
                'price': '询价',
                'min_order': '1000 meters',
                'lead_time': '7-15 days',
                'is_featured': True,
                'is_active': True
            },
            {
                'name': '硅树脂玻纤套管',
                'name_en': 'Silicone Fiberglass Sleeve',
                'slug': 'silicone-fiberglass-sleeve',
                'sku': 'SFGS-200',
                'category_slug': 'silicone-sleeves',
                'description': '在内径1-50mm的玻璃纤维套管表面涂覆硅树脂，耐温性能优异，可达200°C。适用于H级电机、电热器具的绝缘保护。',
                'description_en': 'Silicone coated fiberglass sleeve with inner diameter 1-50mm. Excellent heat resistance up to 200°C. Suitable for Class H motors and heating appliances.',
                'temperature_range': '-60°C ~ +200°C',
                'voltage_rating': '1.5kV-4kV',
                'certifications': 'UL, VDE, SGS, RoHS',
                'price': '询价',
                'min_order': '500 meters',
                'lead_time': '10-15 days',
                'is_featured': True,
                'is_active': True
            },
            {
                'name': '阻燃热缩套管 2:1',
                'name_en': 'Flame Retardant Heat Shrink Tubing 2:1',
                'slug': 'heat-shrink-tubing-2-1',
                'sku': 'HST-2-1-FR',
                'category_slug': 'heat-shrink',
                'description': '聚烯烃材质，2:1收缩比，阻燃等级VW-1。收缩温度80°C，工作温度-55°C~+125°C。适用于电线连接、绝缘保护、线束标识。',
                'description_en': 'Polyolefin material with 2:1 shrink ratio, flame retardant VW-1. Shrink temperature 80°C, working temperature -55°C to +125°C. Ideal for wire connections and insulation.',
                'temperature_range': '-55°C ~ +125°C',
                'voltage_rating': '600V',
                'certifications': 'UL, CSA',
                'price': '询价',
                'min_order': '1000 meters',
                'lead_time': '5-10 days',
                'is_featured': True,
                'is_active': True
            },
            {
                'name': 'PP波纹管 阻燃型',
                'name_en': 'PP Corrugated Tube Flame Retardant',
                'slug': 'pp-corrugated-tube-fr',
                'sku': 'PP-CORR-FR',
                'category_slug': 'corrugated-tubes',
                'description': '阻燃PP材质，耐腐蚀、绝缘性能好。用于汽车线束、机械设备电线保护。颜色可选：黑、白、灰。',
                'description_en': 'Flame retardant PP material with excellent corrosion resistance. Used for automotive wire harness and mechanical equipment protection. Available in black, white, gray.',
                'temperature_range': '-40°C ~ +90°C',
                'certifications': 'RoHS, REACH',
                'price': '询价',
                'min_order': '2000 meters',
                'lead_time': '7-12 days',
                'is_featured': False,
                'is_active': True
            },
            {
                'name': '食品级硅胶管',
                'name_en': 'Food Grade Silicone Tube',
                'slug': 'food-grade-silicone-tube',
                'sku': 'SIL-FOOD',
                'category_slug': 'silicone-tubes',
                'description': '食品级硅胶材质，无毒无味，通过FDA认证。耐温-60°C~+200°C，内径3-50mm可选。适用于食品饮料、医药、化妆品行业。',
                'description_en': 'Food grade silicone material, non-toxic and odorless, FDA certified. Temperature range -60°C to +200°C, inner diameter 3-50mm. Suitable for food, beverage, pharmaceutical and cosmetic industries.',
                'temperature_range': '-60°C ~ +200°C',
                'certifications': 'FDA, RoHS',
                'price': '询价',
                'min_order': '100 meters',
                'lead_time': '5-10 days',
                'is_featured': False,
                'is_active': True
            },
        ]
        
        for prod_data in products_data:
            if not Product.query.filter_by(slug=prod_data['slug']).first():
                category_slug = prod_data.pop('category_slug')
                category = Category.query.filter_by(slug=category_slug).first()
                if category:
                    prod = Product(**prod_data, category_id=category.id)
                    db.session.add(prod)
        print("✅ 示例产品创建完成")
        
        # 4. 创建FAQ
        faqs_data = [
            {
                'question': '你们公司是什么类型的企业？',
                'question_en': 'What type of company are you?',
                'answer': '我们是生产厂家，成立于2008年，位于佛山顺德。自有工厂3000平米，员工约80人。',
                'answer_en': 'We are a manufacturer established in 2008, located in Shunde, Foshan. Our factory covers 3000 sqm with about 80 employees.'
            },
            {
                'question': '产品是否可以定制？',
                'question_en': 'Can products be customized?',
                'answer': '可以。我们支持OEM/ODM，可根据客户要求定制尺寸、颜色、特殊性能。起订量视产品类型而定，通常为500-2000米。',
                'answer_en': 'Yes. We support OEM/ODM and can customize size, color and special performance. MOQ depends on product type, usually 500-2000 meters.'
            },
            {
                'question': '交货期需要多久？',
                'question_en': 'What is the lead time?',
                'answer': '常规产品现库存货可48小时发货。定制产品一般7-15天，急单可沟通加急。',
                'answer_en': 'Regular stock products can be shipped within 48 hours. Custom products usually take 7-15 days. Rush orders can be discussed.'
            },
            {
                'question': '可以提供样品吗？',
                'question_en': 'Can you provide samples?',
                'answer': '可以。常规产品可免费提供样品，运费可协商。特殊定制样品需先收打样费，大货后可退还。',
                'answer_en': 'Yes. Regular products can be sampled for free with negotiable shipping. Special custom samples require sampling fee, refundable upon bulk order.'
            },
            {
                'question': '你们通过哪些认证？',
                'question_en': 'What certifications do you have?',
                'answer': '我们产品通过UL、VDE、SGS、RoHS、REACH等认证。具体认证视产品型号而定，可在产品详情页查看或联系销售获取证书文件。',
                'answer_en': 'Our products are certified by UL, VDE, SGS, RoHS, REACH etc. Specific certifications vary by product model. Check product details or contact sales for certificates.'
            },
        ]
        
        for i, faq_data in enumerate(faqs_data):
            if not FAQ.query.filter_by(question=faq_data['question']).first():
                faq = FAQ(**faq_data, order=i+1, is_active=True)
                db.session.add(faq)
        print("✅ FAQ创建完成")
        
        db.session.commit()
        print("\n🎉 数据初始化完成！")
        print("=" * 50)
        print("管理后台: http://localhost:5000/admin/login")
        print("前端店铺: http://localhost:5000/")
        print("登录账号: admin / admin123")


if __name__ == '__main__':
    init_data()
