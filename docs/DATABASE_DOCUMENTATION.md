# 数据库文档

## 数据库信息

- 数据库类型: MySQL
- 数据库名称: `agricultural_db`
- 字符集: utf8mb4
- 排序规则: utf8mb4_unicode_ci

## 数据表结构

### 1. 数据采集与清洗模块

#### data_source（数据源表）
| 字段名 | 类型 | 说明 | 约束 |
|--------|------|------|------|
| id | BIGINT | 主键 | PRIMARY KEY, AUTO_INCREMENT |
| name | VARCHAR(100) | 数据源名称 | NOT NULL |
| url | VARCHAR(255) | 数据源URL | NOT NULL |
| source_type | VARCHAR(50) | 数据源类型 | web/api/file |
| status | VARCHAR(20) | 状态 | active/inactive |
| config | JSON | 配置信息 | |
| created_at | DATETIME | 创建时间 | |
| updated_at | DATETIME | 更新时间 | |

#### raw_data（原始数据表）
| 字段名 | 类型 | 说明 | 约束 |
|--------|------|------|------|
| id | BIGINT | 主键 | PRIMARY KEY, AUTO_INCREMENT |
| source_id | BIGINT | 数据源ID | FOREIGN KEY |
| product_name | VARCHAR(100) | 农产品名称 | NOT NULL |
| product_category | VARCHAR(50) | 农产品类别 | |
| price | DECIMAL(10,2) | 价格 | NOT NULL |
| unit | VARCHAR(20) | 单位 | DEFAULT '元/斤' |
| market_name | VARCHAR(100) | 市场名称 | |
| region | VARCHAR(50) | 地区 | |
| date | DATE | 日期 | NOT NULL |
| raw_content | TEXT | 原始内容 | |
| status | VARCHAR(20) | 状态 | pending/cleaned/error |
| created_at | DATETIME | 采集时间 | |

**索引**:
- `idx_product_date`: (product_name, date)
- `idx_region_date`: (region, date)

#### cleaned_data（清洗数据表）
| 字段名 | 类型 | 说明 | 约束 |
|--------|------|------|------|
| id | BIGINT | 主键 | PRIMARY KEY, AUTO_INCREMENT |
| raw_data_id | BIGINT | 原始数据ID | FOREIGN KEY, UNIQUE |
| product_name | VARCHAR(100) | 农产品名称 | NOT NULL |
| product_category | VARCHAR(50) | 农产品类别 | |
| price | DECIMAL(10,2) | 价格 | NOT NULL |
| unit | VARCHAR(20) | 单位 | DEFAULT '元/斤' |
| market_name | VARCHAR(100) | 市场名称 | |
| region | VARCHAR(50) | 地区 | |
| date | DATE | 日期 | NOT NULL |
| quality_score | FLOAT | 数据质量评分 | DEFAULT 1.0 |
| cleaned_at | DATETIME | 清洗时间 | |

**索引**:
- `idx_product_date`: (product_name, date)
- `idx_region_date`: (region, date)
- `idx_date`: (date)

#### etl_task（ETL任务表）
| 字段名 | 类型 | 说明 | 约束 |
|--------|------|------|------|
| id | BIGINT | 主键 | PRIMARY KEY, AUTO_INCREMENT |
| task_name | VARCHAR(100) | 任务名称 | NOT NULL |
| source_id | BIGINT | 数据源ID | FOREIGN KEY |
| status | VARCHAR(20) | 状态 | running/success/failed |
| total_count | INT | 总记录数 | DEFAULT 0 |
| success_count | INT | 成功数 | DEFAULT 0 |
| failed_count | INT | 失败数 | DEFAULT 0 |
| error_message | TEXT | 错误信息 | |
| started_at | DATETIME | 开始时间 | |
| finished_at | DATETIME | 结束时间 | |

### 2. 市场行情模块

#### market_price（市场价格表）
| 字段名 | 类型 | 说明 | 约束 |
|--------|------|------|------|
| id | BIGINT | 主键 | PRIMARY KEY, AUTO_INCREMENT |
| product_name | VARCHAR(100) | 农产品名称 | NOT NULL |
| product_category | VARCHAR(50) | 农产品类别 | |
| price | DECIMAL(10,2) | 价格 | NOT NULL |
| unit | VARCHAR(20) | 单位 | DEFAULT '元/斤' |
| market_name | VARCHAR(100) | 市场名称 | |
| region | VARCHAR(50) | 地区 | |
| date | DATE | 日期 | NOT NULL |
| price_change | DECIMAL(10,2) | 价格变化 | |
| price_change_rate | FLOAT | 价格变化率(%) | |
| created_at | DATETIME | 创建时间 | |

**唯一约束**: (product_name, market_name, date)

**索引**:
- `idx_product_date`: (product_name, date)
- `idx_region_date`: (region, date)
- `idx_date`: (date)

#### market_statistics（市场统计表）
| 字段名 | 类型 | 说明 | 约束 |
|--------|------|------|------|
| id | BIGINT | 主键 | PRIMARY KEY, AUTO_INCREMENT |
| product_name | VARCHAR(100) | 农产品名称 | NOT NULL |
| product_category | VARCHAR(50) | 农产品类别 | |
| region | VARCHAR(50) | 地区 | |
| stat_date | DATE | 统计日期 | NOT NULL |
| stat_type | VARCHAR(20) | 统计类型 | daily/weekly/monthly |
| avg_price | DECIMAL(10,2) | 平均价格 | NOT NULL |
| max_price | DECIMAL(10,2) | 最高价格 | NOT NULL |
| min_price | DECIMAL(10,2) | 最低价格 | NOT NULL |
| price_std | DECIMAL(10,2) | 价格标准差 | |
| volume | DECIMAL(15,2) | 交易量 | |
| created_at | DATETIME | 创建时间 | |

**唯一约束**: (product_name, region, stat_date, stat_type)

**索引**:
- `idx_product_date`: (product_name, stat_date)
- `idx_region_date`: (region, stat_date)

### 3. 价格预测模块

#### forecast_model（预测模型表）
| 字段名 | 类型 | 说明 | 约束 |
|--------|------|------|------|
| id | BIGINT | 主键 | PRIMARY KEY, AUTO_INCREMENT |
| model_name | VARCHAR(100) | 模型名称 | NOT NULL, UNIQUE |
| model_type | VARCHAR(50) | 模型类型 | ARIMA/LSTM/Linear |
| product_name | VARCHAR(100) | 农产品名称 | NOT NULL |
| region | VARCHAR(50) | 地区 | |
| parameters | JSON | 模型参数 | |
| accuracy_metrics | JSON | 准确度指标 | |
| model_file_path | VARCHAR(255) | 模型文件路径 | |
| status | VARCHAR(20) | 状态 | training/ready/failed |
| created_at | DATETIME | 创建时间 | |
| updated_at | DATETIME | 更新时间 | |
| trained_at | DATETIME | 训练时间 | |

#### forecast_result（预测结果表）
| 字段名 | 类型 | 说明 | 约束 |
|--------|------|------|------|
| id | BIGINT | 主键 | PRIMARY KEY, AUTO_INCREMENT |
| model_id | BIGINT | 预测模型ID | FOREIGN KEY |
| product_name | VARCHAR(100) | 农产品名称 | NOT NULL |
| region | VARCHAR(50) | 地区 | |
| forecast_date | DATE | 预测日期 | NOT NULL |
| forecast_price | DECIMAL(10,2) | 预测价格 | NOT NULL |
| confidence_interval_lower | DECIMAL(10,2) | 置信区间下限 | |
| confidence_interval_upper | DECIMAL(10,2) | 置信区间上限 | |
| actual_price | DECIMAL(10,2) | 实际价格 | |
| error | DECIMAL(10,2) | 预测误差 | |
| created_at | DATETIME | 创建时间 | |

**索引**:
- `idx_product_date`: (product_name, forecast_date)
- `idx_region_date`: (region, forecast_date)

#### training_history（训练历史表）
| 字段名 | 类型 | 说明 | 约束 |
|--------|------|------|------|
| id | BIGINT | 主键 | PRIMARY KEY, AUTO_INCREMENT |
| model_id | BIGINT | 预测模型ID | FOREIGN KEY |
| training_data_start | DATE | 训练数据起始日期 | NOT NULL |
| training_data_end | DATE | 训练数据结束日期 | NOT NULL |
| data_count | INT | 数据量 | NOT NULL |
| training_duration | FLOAT | 训练时长(秒) | |
| accuracy_metrics | JSON | 准确度指标 | |
| status | VARCHAR(20) | 状态 | success/failed |
| error_message | TEXT | 错误信息 | |
| created_at | DATETIME | 训练时间 | |

### 4. 决策辅助模块

#### profit_simulation（利润模拟表）
| 字段名 | 类型 | 说明 | 约束 |
|--------|------|------|------|
| id | BIGINT | 主键 | PRIMARY KEY, AUTO_INCREMENT |
| product_name | VARCHAR(100) | 农产品名称 | NOT NULL |
| region | VARCHAR(50) | 地区 | |
| purchase_price | DECIMAL(10,2) | 采购价格 | NOT NULL |
| sale_price | DECIMAL(10,2) | 销售价格 | NOT NULL |
| quantity | DECIMAL(15,2) | 数量 | NOT NULL |
| unit | VARCHAR(20) | 单位 | DEFAULT '斤' |
| transport_cost | DECIMAL(10,2) | 运输成本 | DEFAULT 0.00 |
| storage_cost | DECIMAL(10,2) | 仓储成本 | DEFAULT 0.00 |
| other_cost | DECIMAL(10,2) | 其他成本 | DEFAULT 0.00 |
| total_cost | DECIMAL(15,2) | 总成本 | NOT NULL |
| total_revenue | DECIMAL(15,2) | 总收入 | NOT NULL |
| profit | DECIMAL(15,2) | 利润 | NOT NULL |
| profit_rate | FLOAT | 利润率(%) | NOT NULL |
| simulation_date | DATE | 模拟日期 | NOT NULL |
| created_at | DATETIME | 创建时间 | |

#### decision_advice（决策建议表）
| 字段名 | 类型 | 说明 | 约束 |
|--------|------|------|------|
| id | BIGINT | 主键 | PRIMARY KEY, AUTO_INCREMENT |
| product_name | VARCHAR(100) | 农产品名称 | NOT NULL |
| region | VARCHAR(50) | 地区 | |
| advice_type | VARCHAR(50) | 建议类型 | purchase/sale/storage/transport |
| advice_content | TEXT | 建议内容 | NOT NULL |
| confidence | FLOAT | 置信度 | DEFAULT 0.0 |
| factors | JSON | 影响因素 | |
| created_at | DATETIME | 创建时间 | |

### 5. 供需对接模块

#### supply_info（供应信息表）
| 字段名 | 类型 | 说明 | 约束 |
|--------|------|------|------|
| id | BIGINT | 主键 | PRIMARY KEY, AUTO_INCREMENT |
| product_name | VARCHAR(100) | 农产品名称 | NOT NULL |
| product_category | VARCHAR(50) | 农产品类别 | |
| quantity | DECIMAL(15,2) | 供应数量 | NOT NULL |
| unit | VARCHAR(20) | 单位 | DEFAULT '斤' |
| price | DECIMAL(10,2) | 价格 | NOT NULL |
| region | VARCHAR(50) | 地区 | |
| contact_name | VARCHAR(50) | 联系人 | NOT NULL |
| contact_phone | VARCHAR(20) | 联系电话 | NOT NULL |
| description | TEXT | 描述 | |
| status | VARCHAR(20) | 状态 | active/completed/cancelled |
| created_at | DATETIME | 发布时间 | |
| updated_at | DATETIME | 更新时间 | |
| expire_at | DATETIME | 过期时间 | |

**索引**:
- `idx_product_status`: (product_name, status)
- `idx_region_status`: (region, status)

#### demand_info（需求信息表）
| 字段名 | 类型 | 说明 | 约束 |
|--------|------|------|------|
| id | BIGINT | 主键 | PRIMARY KEY, AUTO_INCREMENT |
| product_name | VARCHAR(100) | 农产品名称 | NOT NULL |
| product_category | VARCHAR(50) | 农产品类别 | |
| quantity | DECIMAL(15,2) | 需求数量 | NOT NULL |
| unit | VARCHAR(20) | 单位 | DEFAULT '斤' |
| max_price | DECIMAL(10,2) | 最高价格 | |
| region | VARCHAR(50) | 地区 | |
| contact_name | VARCHAR(50) | 联系人 | NOT NULL |
| contact_phone | VARCHAR(20) | 联系电话 | NOT NULL |
| description | TEXT | 描述 | |
| status | VARCHAR(20) | 状态 | active/completed/cancelled |
| created_at | DATETIME | 发布时间 | |
| updated_at | DATETIME | 更新时间 | |
| expire_at | DATETIME | 过期时间 | |

**索引**:
- `idx_product_status`: (product_name, status)
- `idx_region_status`: (region, status)

#### trade_match（交易匹配表）
| 字段名 | 类型 | 说明 | 约束 |
|--------|------|------|------|
| id | BIGINT | 主键 | PRIMARY KEY, AUTO_INCREMENT |
| supply_id | BIGINT | 供应信息ID | FOREIGN KEY |
| demand_id | BIGINT | 需求信息ID | FOREIGN KEY |
| match_score | FLOAT | 匹配度 | NOT NULL |
| status | VARCHAR(20) | 状态 | pending/confirmed/completed/cancelled |
| created_at | DATETIME | 匹配时间 | |
| confirmed_at | DATETIME | 确认时间 | |

### 6. 系统管理模块

#### system_log（系统日志表）
| 字段名 | 类型 | 说明 | 约束 |
|--------|------|------|------|
| id | BIGINT | 主键 | PRIMARY KEY, AUTO_INCREMENT |
| log_type | VARCHAR(50) | 日志类型 | info/warning/error/debug |
| module | VARCHAR(100) | 模块 | NOT NULL |
| action | VARCHAR(100) | 操作 | NOT NULL |
| message | TEXT | 日志内容 | NOT NULL |
| user_id | BIGINT | 用户ID | FOREIGN KEY |
| ip_address | VARCHAR(45) | IP地址 | |
| created_at | DATETIME | 创建时间 | |

**索引**:
- `idx_log_type_date`: (log_type, created_at)
- `idx_module_date`: (module, created_at)

#### price_alert（价格预警表）
| 字段名 | 类型 | 说明 | 约束 |
|--------|------|------|------|
| id | BIGINT | 主键 | PRIMARY KEY, AUTO_INCREMENT |
| product_name | VARCHAR(100) | 农产品名称 | NOT NULL |
| region | VARCHAR(50) | 地区 | |
| alert_type | VARCHAR(50) | 预警类型 | price_rise/price_fall/price_abnormal |
| threshold | DECIMAL(10,2) | 阈值 | NOT NULL |
| current_price | DECIMAL(10,2) | 当前价格 | NOT NULL |
| change_rate | FLOAT | 变化率(%) | NOT NULL |
| status | VARCHAR(20) | 状态 | pending/processed/ignored |
| message | TEXT | 预警信息 | NOT NULL |
| created_at | DATETIME | 创建时间 | |
| processed_at | DATETIME | 处理时间 | |

**索引**:
- `idx_product_status`: (product_name, status)
- `idx_alert_type_status`: (alert_type, status)

#### alert_rule（预警规则表）
| 字段名 | 类型 | 说明 | 约束 |
|--------|------|------|------|
| id | BIGINT | 主键 | PRIMARY KEY, AUTO_INCREMENT |
| rule_name | VARCHAR(100) | 规则名称 | NOT NULL |
| product_name | VARCHAR(100) | 农产品名称 | |
| region | VARCHAR(50) | 地区 | |
| alert_type | VARCHAR(50) | 预警类型 | price_rise/price_fall/price_abnormal |
| threshold_type | VARCHAR(50) | 阈值类型 | absolute/percentage |
| threshold_value | DECIMAL(10,2) | 阈值 | NOT NULL |
| is_active | BOOLEAN | 是否启用 | DEFAULT TRUE |
| created_at | DATETIME | 创建时间 | |
| updated_at | DATETIME | 更新时间 | |

#### user_permission（用户权限表）
| 字段名 | 类型 | 说明 | 约束 |
|--------|------|------|------|
| id | BIGINT | 主键 | PRIMARY KEY, AUTO_INCREMENT |
| user_id | BIGINT | 用户ID | FOREIGN KEY, UNIQUE |
| role | VARCHAR(50) | 角色 | admin/analyst/trader/viewer |
| permissions | JSON | 权限配置 | |
| created_at | DATETIME | 创建时间 | |
| updated_at | DATETIME | 更新时间 | |

## 数据库关系图

```
data_source (1) ----< (N) raw_data
raw_data (1) ----< (1) cleaned_data
cleaned_data (N) ----< (N) market_price

forecast_model (1) ----< (N) forecast_result
forecast_model (1) ----< (N) training_history

supply_info (1) ----< (N) trade_match
demand_info (1) ----< (N) trade_match

user (1) ----< (1) user_permission
user (1) ----< (N) system_log
```

## 数据字典

### 状态枚举值

- **数据源状态**: `active`（启用）, `inactive`（禁用）
- **原始数据状态**: `pending`（待清洗）, `cleaned`（已清洗）, `error`（清洗失败）
- **ETL任务状态**: `running`（运行中）, `success`（成功）, `failed`（失败）
- **模型状态**: `training`（训练中）, `ready`（就绪）, `failed`（训练失败）
- **供应/需求状态**: `active`（有效）, `completed`（已完成）, `cancelled`（已取消）
- **匹配状态**: `pending`（待确认）, `confirmed`（已确认）, `completed`（已完成）, `cancelled`（已取消）
- **预警状态**: `pending`（待处理）, `processed`（已处理）, `ignored`（已忽略）
- **日志类型**: `info`（信息）, `warning`（警告）, `error`（错误）, `debug`（调试）

