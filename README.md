#  多语言智能日记本
一个基于Django的全栈日记应用，支持中日双语国际化，集成了Echarts数据可视化、Markdown编辑等功能。
## 项目点

### 国际化支持

- **中日双语界面**：支持简体中文和日语界面切换
- **本地化体验**：日期格式、文本方向等全面本地化
- **无缝切换**：用户可随时切换语言，不影响数据

### 智能数据可视化

- **写作统计**：月度写作频率图
- **天气分析**：日记天气分布图
- **关键词词云**：自动生成日记关键词词云

### 技术亮点

- **数据安全隔离**：完善的用户数据隔离机制
- **Markdown富文本**：优雅的Markdown写作和预览体验
- **响应式设计**：完美适配桌面和移动设备
- **实时交互**：AJAX无刷新数据更新

## 系统架构

text

```
前端层 (Bootstrap5 + jQuery + ECharts)
    ↓ AJAX/RESTful
业务层 (Django MVT + i18n国际化)
    ↓ ORM
数据层 (SQLite + Redis缓存)
```

##  核心功能

###  用户认证系统

- 邮箱验证注册（SMTP）
- 图片验证码登录（Pillow生成）
- Redis缓存验证码
- Session会话管理

###  日记管理

- 多日记本支持（用户→日记本→日记三级结构）
- Markdown编辑器（实时预览）
- 天气标签记录
- 时间轴展示

###  数据统计

- 写作频率分析（柱状图）
- 天气分布统计（饼图）
- 关键词词云生成
- ……

## 快速开始

### 环境要求

- Python 3.8+
- Django 3.2
- Redis 6.0+
### 你需要
- 在你的本地settings中配置如下
  >EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
  EMAIL_HOST = 'smtp.qq.com'
  EMAIL_PORT = 465 
  EMAIL_USE_SSL = True 
  EMAIL_HOST_USER = '你的邮箱'  
  EMAIL_HOST_PASSWORD = '你的SMTP授权码'  
  DEFAULT_FROM_EMAIL = EMAIL_HOST_USER  
- 下载并启动Redis服务
  > CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/0",  # 修改为 127.0.0.1
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {
                "max_connections": 1000,
                "encoding": 'utf-8'
            },
            # "PASSWORD": "你的密码"  # 如果您设置了密码，保留此项，
        }
    }
}
## 技术栈
### 后端技术
- **框架**: Django 3.2
- **数据库**: SQLite (支持 PostgreSQL)
- **缓存**: Redis
- **邮件服务**: SMTP
- **国际化**: Django i18n

### 前端技术
- **UI框架**: Bootstrap 5
- **交互**: jQuery
- **图表**: ECharts
- **图标**: FontAwesome
- **编辑器**: Markdown编辑器

### 后续可能完善方向
- 日记内容支持导出
- 全文搜索功能

### 作者
一个过劳的中国普通本科在校生，正在寻找一份实习机会，如果您对我的项目感兴趣，欢迎留言

