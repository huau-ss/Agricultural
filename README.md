# 基于时间序列预测算法的农产品产销分析与辅助决策平台

## 项目简介

本项目是一个基于时间序列预测算法的农产品产销分析与辅助决策平台，旨在通过数据采集、价格预测、利润模拟等功能，为农产品生产者和销售者提供科学的决策支持。

## 技术栈

### 后端
- Python 3.9+
- Django 4.2.7
- Django REST Framework 3.14.0
- MySQL
- Pandas、NumPy（数据处理）
- Statsmodels、Scikit-learn、TensorFlow（机器学习）

### 前端
- Vue.js 3.3.4
- Vue Router 4.2.5
- Vuex 4.1.0
- Element Plus 2.4.2
- ECharts 5.4.3
- Axios 1.6.0

### 数据采集
- Scrapy 2.11.0
- Requests 2.31.0
- BeautifulSoup4 4.12.2

## 项目结构

```
Agricultural/
├── agricultural_platform/     # Django项目配置
│   ├── settings.py            # 项目配置
│   ├── urls.py               # 主URL路由
│   └── ...
├── apps/                      # 应用模块
│   ├── data_etl/             # 数据采集与清洗
│   ├── market/               # 市场行情
│   ├── forecast/             # 价格预测
│   ├── decision/             # 决策辅助
│   ├── trade/                # 供需对接
│   └── admincore/            # 系统管理
├── utils/                     # 工具类
│   ├── response.py           # 统一响应格式
│   ├── pagination.py         # 分页工具
│   ├── logger.py             # 日志工具
│   └── ...
├── frontend/                  # Vue前端项目
│   ├── src/
│   │   ├── views/           # 页面组件
│   │   ├── components/      # 公共组件
│   │   ├── api/             # API接口
│   │   └── ...
│   └── ...
├── requirements.txt          # Python依赖
└── README.md                 # 项目说明
```

## 核心功能模块

### 1. 数据采集与清洗（data_etl）
- 支持多种数据源（网页爬虫、API接口、文件导入）
- 自动数据清洗和标准化
- ETL任务管理和监控

### 2. 市场行情可视化（market）
- 价格趋势图表展示
- 多维度统计分析
- 价格对比分析

### 3. 价格时序预测（forecast）
- ARIMA模型预测
- LSTM神经网络预测
- 线性回归预测
- 模型训练和评估

### 4. 利润模拟与决策（decision）
- 利润计算模拟
- 批量场景模拟
- 决策建议生成

### 5. 供需对接交易（trade）
- 供应信息发布
- 需求信息发布
- 智能匹配推荐

### 6. 系统管理（admincore）
- 系统日志记录
- 价格预警管理
- 用户权限管理

## 安装部署

### 环境要求
- Python 3.9+
- Node.js 14+
- MySQL 5.7+

### 后端部署

1. 克隆项目
```bash
git clone <repository-url>
cd Agricultural
```

2. 创建虚拟环境
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. 安装依赖
```bash
pip install -r requirements.txt
```

4. 配置数据库
```bash
# 创建数据库
mysql -u root -p
CREATE DATABASE agricultural_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# 修改settings.py中的数据库配置
```

5. 执行数据库迁移
```bash
python manage.py makemigrations
python manage.py migrate
```

6. 创建超级用户
```bash
python manage.py createsuperuser
```

7. 运行开发服务器
```bash
python manage.py runserver
```

### 前端部署

1. 进入前端目录
```bash
cd frontend
```

2. 安装依赖
```bash
npm install
```

3. 运行开发服务器
```bash
npm run serve
```

4. 构建生产版本
```bash
npm run build
```

## API接口文档

详见 [API_DOCUMENTATION.md](docs/API_DOCUMENTATION.md)

## 数据库文档

详见 [DATABASE_DOCUMENTATION.md](docs/DATABASE_DOCUMENTATION.md)

## 使用说明

### 数据采集
1. 在管理后台配置数据源
2. 创建ETL任务并执行
3. 查看数据采集和清洗结果

### 价格预测
1. 选择农产品和地区
2. 选择预测模型（ARIMA/LSTM/线性回归）
3. 训练模型并执行预测
4. 查看预测结果和准确度分析

### 利润模拟
1. 输入采购价格、销售价格、数量等参数
2. 输入成本信息（运输、仓储等）
3. 执行模拟计算
4. 查看利润和利润率

### 供需对接
1. 发布供应或需求信息
2. 系统自动匹配
3. 查看匹配结果并确认交易

## 开发规范

- 代码遵循PEP 8规范
- 使用统一的响应格式：`{code, msg, data}`
- API接口使用RESTful风格
- 前端组件封装化、可复用
- 所有算法脚本放在对应模块的algorithms目录

## 许可证

MIT License

## 联系方式

如有问题，请联系项目维护者。

