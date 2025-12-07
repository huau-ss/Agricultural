# API接口文档

## 基础信息

- 基础URL: `http://localhost:8000/api`
- 统一响应格式: `{code, msg, data}`

## 响应格式说明

### 成功响应
```json
{
  "code": 200,
  "msg": "操作成功",
  "data": {}
}
```

### 错误响应
```json
{
  "code": 400,
  "msg": "错误信息",
  "data": null
}
```

## 数据采集与清洗模块

### 1. 数据源管理

#### 获取数据源列表
- **URL**: `/data-etl/sources/`
- **方法**: `GET`
- **参数**: 
  - `source_type`: 数据源类型（web/api/file）
  - `status`: 状态（active/inactive）
  - `search`: 搜索关键词

#### 创建数据源
- **URL**: `/data-etl/sources/`
- **方法**: `POST`
- **请求体**:
```json
{
  "name": "数据源名称",
  "url": "http://example.com",
  "source_type": "web",
  "status": "active",
  "config": {}
}
```

#### 触发ETL任务
- **URL**: `/data-etl/sources/{id}/trigger_etl/`
- **方法**: `POST`

### 2. 原始数据查询

#### 获取原始数据列表
- **URL**: `/data-etl/raw-data/`
- **方法**: `GET`
- **参数**: 
  - `product_name`: 产品名称
  - `region`: 地区
  - `status`: 状态

### 3. 清洗数据查询

#### 获取清洗数据列表
- **URL**: `/data-etl/cleaned-data/`
- **方法**: `GET`
- **参数**: 
  - `product_name`: 产品名称
  - `region`: 地区

## 市场行情模块

### 1. 市场价格查询

#### 获取市场价格列表
- **URL**: `/market/prices/`
- **方法**: `GET`
- **参数**: 
  - `product_name`: 产品名称
  - `region`: 地区
  - `start_date`: 开始日期
  - `end_date`: 结束日期

#### 获取驾驶舱数据
- **URL**: `/market/prices/dashboard/`
- **方法**: `GET`
- **响应**:
```json
{
  "code": 200,
  "msg": "查询成功",
  "data": {
    "product_stats": [],
    "region_stats": [],
    "price_trend": []
  }
}
```

#### 价格对比
- **URL**: `/market/prices/price_comparison/`
- **方法**: `GET`
- **参数**: 
  - `product_name`: 产品名称（必填）
  - `regions`: 地区列表

### 2. 市场统计查询

#### 获取市场统计列表
- **URL**: `/market/statistics/`
- **方法**: `GET`
- **参数**: 
  - `product_name`: 产品名称
  - `stat_type`: 统计类型（daily/weekly/monthly）

## 价格预测模块

### 1. 预测模型管理

#### 获取模型列表
- **URL**: `/forecast/models/`
- **方法**: `GET`
- **参数**: 
  - `model_type`: 模型类型（ARIMA/LSTM/Linear）
  - `product_name`: 产品名称
  - `status`: 状态

#### 创建模型
- **URL**: `/forecast/models/`
- **方法**: `POST`
- **请求体**:
```json
{
  "model_name": "模型名称",
  "model_type": "ARIMA",
  "product_name": "产品名称",
  "region": "地区",
  "parameters": {}
}
```

#### 训练模型
- **URL**: `/forecast/models/{id}/train/`
- **方法**: `POST`

#### 执行预测
- **URL**: `/forecast/models/{id}/predict/`
- **方法**: `POST`
- **请求体**:
```json
{
  "days": 7
}
```

### 2. 预测结果查询

#### 获取预测结果列表
- **URL**: `/forecast/results/`
- **方法**: `GET`
- **参数**: 
  - `product_name`: 产品名称
  - `start_date`: 开始日期
  - `end_date`: 结束日期

#### 准确度分析
- **URL**: `/forecast/results/accuracy_analysis/`
- **方法**: `GET`
- **参数**: 
  - `product_name`: 产品名称
  - `region`: 地区

## 决策辅助模块

### 1. 利润模拟

#### 获取模拟列表
- **URL**: `/decision/profit-simulations/`
- **方法**: `GET`

#### 创建利润模拟
- **URL**: `/decision/profit-simulations/`
- **方法**: `POST`
- **请求体**:
```json
{
  "product_name": "产品名称",
  "region": "地区",
  "purchase_price": 10.0,
  "sale_price": 12.0,
  "quantity": 1000,
  "transport_cost": 500,
  "storage_cost": 200,
  "other_cost": 100
}
```

#### 批量模拟
- **URL**: `/decision/profit-simulations/batch_simulate/`
- **方法**: `POST`
- **请求体**:
```json
{
  "scenarios": [
    {
      "purchase_price": 10.0,
      "sale_price": 12.0,
      "quantity": 1000,
      "transport_cost": 500,
      "storage_cost": 200,
      "other_cost": 100
    }
  ]
}
```

### 2. 决策建议

#### 获取建议列表
- **URL**: `/decision/advices/`
- **方法**: `GET`

#### 生成建议
- **URL**: `/decision/advices/generate_advice/`
- **方法**: `POST`
- **请求体**:
```json
{
  "product_name": "产品名称",
  "region": "地区",
  "advice_type": "purchase"
}
```

## 供需对接模块

### 1. 供应信息

#### 获取供应列表
- **URL**: `/trade/supplies/`
- **方法**: `GET`
- **参数**: 
  - `product_name`: 产品名称
  - `region`: 地区
  - `status`: 状态

#### 发布供应
- **URL**: `/trade/supplies/`
- **方法**: `POST`
- **请求体**:
```json
{
  "product_name": "产品名称",
  "quantity": 1000,
  "price": 10.0,
  "region": "地区",
  "contact_name": "联系人",
  "contact_phone": "联系电话"
}
```

#### 标记完成
- **URL**: `/trade/supplies/{id}/complete/`
- **方法**: `POST`

### 2. 需求信息

#### 获取需求列表
- **URL**: `/trade/demands/`
- **方法**: `GET`

#### 发布需求
- **URL**: `/trade/demands/`
- **方法**: `POST`
- **请求体**:
```json
{
  "product_name": "产品名称",
  "quantity": 1000,
  "max_price": 12.0,
  "region": "地区",
  "contact_name": "联系人",
  "contact_phone": "联系电话"
}
```

### 3. 交易匹配

#### 获取匹配列表
- **URL**: `/trade/matches/`
- **方法**: `GET`

#### 执行匹配
- **URL**: `/trade/matches/match/`
- **方法**: `POST`
- **请求体**:
```json
{
  "supply_id": 1,
  "demand_id": 2
}
```

#### 确认匹配
- **URL**: `/trade/matches/{id}/confirm/`
- **方法**: `POST`

## 系统管理模块

### 1. 系统日志

#### 获取日志列表
- **URL**: `/admincore/logs/`
- **方法**: `GET`
- **参数**: 
  - `log_type`: 日志类型（info/warning/error/debug）
  - `module`: 模块名称

### 2. 价格预警

#### 获取预警列表
- **URL**: `/admincore/alerts/`
- **方法**: `GET`
- **参数**: 
  - `product_name`: 产品名称
  - `alert_type`: 预警类型
  - `status`: 状态

#### 处理预警
- **URL**: `/admincore/alerts/{id}/process/`
- **方法**: `POST`

#### 忽略预警
- **URL**: `/admincore/alerts/{id}/ignore/`
- **方法**: `POST`

### 3. 预警规则

#### 获取规则列表
- **URL**: `/admincore/alert-rules/`
- **方法**: `GET`

#### 创建规则
- **URL**: `/admincore/alert-rules/`
- **方法**: `POST`
- **请求体**:
```json
{
  "rule_name": "规则名称",
  "product_name": "产品名称",
  "alert_type": "price_rise",
  "threshold_type": "percentage",
  "threshold_value": 10.0,
  "is_active": true
}
```

