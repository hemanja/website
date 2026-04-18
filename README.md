# YC Sleeve Shop - 多站点电商模板

Shopify 级 Flask 电商模板，支持多站点部署，专为 AI 搜索引擎优化 (GEO)。

## 功能特性

- 🛍️ **产品管理** - 分类、参数、图片、认证信息
- 📦 **询价系统** - B2B 询价购物车 + 表单提交
- 🔐 **后台管理** - 产品 CRUD、询价管理
- 🌍 **多语言** - 中/英双语支持
- 🎨 **多站点** - 一键切换不同品牌/类目
- 🤖 **GEO 优化** - JSON-LD 结构化数据 (Organization/Product/FAQPage)

## 快速开始

```bash
# 克隆仓库
git clone https://github.com/YOUR_USERNAME/ycsleeve-shop.git
cd ycsleeve-shop

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 初始化数据库
python init_data.py

# 启动服务
python app.py
```

访问：
- 前端店铺: http://localhost:5000/
- 管理后台: http://localhost:5000/admin/login
- 默认账号: `admin` / `admin123`

## 多站点配置

修改 `site_config.py` 即可切换站点：

| 站点 | BRAND_NAME | PRIMARY_COLOR |
|------|------------|---------------|
| 绝缘材料 | YC INSULATION | #1a5f7a |
| 祭礼制品 | 礼缘堂 | #8B4513 |
| 高端丝袜 | 丝语 | #2F4F4F |
| 美妆工具 | 美妆工坊 | #FF69B4 |

## 项目结构

```
ycsleeve-shop/
├── app.py              # Flask 主应用
├── models.py           # SQLAlchemy 模型
├── site_config.py      # 多站点配置
├── config.py           # Flask 配置
├── init_data.py        # 初始化脚本
├── requirements.txt    # Python 依赖
├── templates/          # Jinja2 模板
│   ├── base.html
│   ├── index.html
│   ├── products.html
│   ├── product_detail.html
│   ├── contact.html
│   └── admin/
└── static/uploads/     # 产品图片
```

## GEO 优化

每个页面自动输出结构化数据：

- `Organization` - 公司信息、认证、联系方式
- `Product` - 产品参数（温度/电压/认证）
- `FAQPage` - 常见问题

这些数据专为 ChatGPT、Perplexity、Gemini 等 AI 搜索引擎优化。

## 技术栈

- **后端**: Flask 3.0 + SQLAlchemy
- **前端**: Tailwind CSS (CDN)
- **数据库**: SQLite (可切换 PostgreSQL/MySQL)
- **认证**: Flask-Login

## License

MIT
