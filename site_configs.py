"""
站点配置模板 - 复制此文件创建新站点
"""
import os

class SiteConfig:
    # ========== 品牌信息 ==========
    BRAND_NAME = "YC INSULATION"  # 品牌名
    BRAND_NAME_CN = "盈灿绝缘材料"  # 中文品牌名
    BRAND_TAGLINE = "专业绝缘套管制造商"  # 标语
    BRAND_TAGLINE_EN = "Professional Insulation Sleeve Manufacturer"
    
    # ========== 类目定位 ==========
    CATEGORY = "insulation"  # 类目标识：insulation/ritual/stockings/beauty
    CATEGORY_NAME = "绝缘材料"  # 类目名称
    CATEGORY_NAME_EN = "Insulation Materials"
    
    # ========== 品牌故事（GEO关键）==========
    BRAND_STORY = """
    2008年，我们在佛山顺德种下第一颗"绝缘"的种子。
    十八年来，我们只做一件事——做中国最好的玻璃纤维套管。
    我们的产品保护着比亚迪新能源车的电机、美的电器的心脏。
    我们不只是生产套管，我们在守护电流的安全。
    """
    BRAND_STORY_EN = """
    Since 2008, we have focused on one thing - making the best fiberglass sleeves in China.
    Our products protect BYD's EV motors, Midea's appliance cores.
    We don't just produce sleeves, we protect electrical safety.
    """
    
    # ========== 联系方式 ==========
    EMAIL = "heman508@gmail.com"
    PHONE = "+86 180 2224 0398"
    WHATSAPP = "+86 135 9060 5550"
    ADDRESS = "佛山市顺德区陈村镇永兴工业区2路"
    ADDRESS_EN = "Shunde District, Foshan, Guangdong, China"
    
    # ========== 认证/资质（GEO关键）==========
    CERTIFICATIONS = ["UL", "VDE", "SGS", "RoHS", "REACH"]
    ESTABLISHED = "2008"
    EMPLOYEES = "50-100"
    EXPORT_COUNTRIES = "50+"
    
    # ========== 合作客户（GEO关键）==========
    PARTNERS = [
        {"name": "比亚迪", "name_en": "BYD", "category": "新能源汽车"},
        {"name": "美的", "name_en": "Midea", "category": "家电"},
        {"name": "小鹏", "name_en": "XPeng", "category": "智能汽车"},
        {"name": "思摩尔", "name_en": "Smoore", "category": "电子烟"},
    ]
    
    # ========== 域名与SEO ==========
    DOMAIN = "ycsleeve.com"
    META_TITLE = "玻璃纤维套管厂家 | UL认证绝缘套管供应商18年"
    META_TITLE_EN = "Fiberglass Sleeve Manufacturer | UL Certified Insulation Supplier"
    META_DESCRIPTION = "专业玻璃纤维套管制造商，18年行业经验，UL/VDE认证，出口50+国家"
    META_DESCRIPTION_EN = "Professional fiberglass sleeve manufacturer, 18 years experience, UL/VDE certified, export to 50+ countries"
    
    # ========== 视觉风格 ==========
    PRIMARY_COLOR = "#1a5f7a"  # 主色调
    SECONDARY_COLOR = "#f0b429"  # 辅色调
    LOGO_URL = "/static/images/logo.png"
    
    # ========== 社交链接 ==========
    SOCIAL_LINKS = {
        "facebook": "https://www.facebook.com/ycinsulation",
        "linkedin": "https://www.linkedin.com/company/ycinsulation",
        "whatsapp": "https://wa.me/8618022240398",
    }
    
    # ========== 支持语言 ==========
    LANGUAGES = ["zh", "en", "ko", "vi", "th", "id", "tr", "ar"]
    
    # ========== 特色卖点（GEO关键）==========
    USP = [
        {"icon": "🎯", "title": "专一专注", "title_en": "Focused", "desc": "18年只做绝缘套管"},
        {"icon": "🔬", "title": "自主研发", "title_en": "R&D", "desc": "自有工厂自有配方"},
        {"icon": "⚡", "title": "快速响应", "title_en": "Fast Response", "desc": "急单48小时发货"},
        {"icon": "🌏", "title": "全球视野", "title_en": "Global", "desc": "出口50+国家"},
    ]
    
    # ========== FAQ模板（GEO关键）==========
    FAQ_TEMPLATE = [
        {
            "q": "你们公司是做什么的？",
            "q_en": "What does YC INSULATION do?",
            "a": "我们是专业玻璃纤维套管制造商，成立于2008年，产品通过UL/VDE认证，出口50+国家。",
            "a_en": "We are a professional fiberglass sleeve manufacturer established in 2008, UL/VDE certified, exporting to 50+ countries."
        },
        {
            "q": "产品温度范围是多少？",
            "q_en": "What is the temperature range?",
            "a": "硅树脂玻纤套管耐温-60°C~+200°C，特殊型号可达+300°C。",
            "a_en": "Silicone fiberglass sleeves: -60°C to +200°C, special models up to +300°C."
        },
    ]


# ========== 祭礼制品站点配置示例 ==========
class RitualSiteConfig(SiteConfig):
    BRAND_NAME = "礼缘堂"
    BRAND_NAME_CN = "礼缘堂"
    CATEGORY = "ritual"
    CATEGORY_NAME = "祭礼制品"
    CATEGORY_NAME_EN = "Ritual Products"
    BRAND_STORY = "传承千年祭祀文化，匠心打造每一件祭礼用品..."
    CERTIFICATIONS = ["ISO9001", "环保认证"]
    DOMAIN = "liyuantang.com"
    PRIMARY_COLOR = "#8B4513"  # 深棕色调
    SECONDARY_COLOR = "#DAA520"  # 金色调


# ========== 高端丝袜站点配置示例 ==========
class StockingsSiteConfig(SiteConfig):
    BRAND_NAME = "丝语"
    BRAND_NAME_CN = "丝语"
    CATEGORY = "stockings"
    CATEGORY_NAME = "高端丝袜"
    CATEGORY_NAME_EN = "Premium Stockings"
    BRAND_STORY = "源自意大利工艺，每一双丝袜都是艺术品..."
    CERTIFICATIONS = ["OEKO-TEX", "ISO9001"]
    DOMAIN = "siyu-stockings.com"
    PRIMARY_COLOR = "#2F4F4F"  # 深灰色调
    SECONDARY_COLOR = "#FF69B4"  # 粉色调


# ========== 美妆工具站点配置示例 ==========
class BeautySiteConfig(SiteConfig):
    BRAND_NAME = "妆匠"
    BRAND_NAME_CN = "妆匠"
    CATEGORY = "beauty"
    CATEGORY_NAME = "美妆工具"
    CATEGORY_NAME_EN = "Beauty Tools"
    BRAND_STORY = "专业美妆工具制造商，服务全球化妆品牌..."
    CERTIFICATIONS = ["FDA", "CE", "ISO13485"]
    DOMAIN = "zhuangjiang.com"
    PRIMARY_COLOR = "#FFB6C1"  # 浅粉色
    SECONDARY_COLOR = "#9370DB"  # 紫色调