<template>
  <div class="forecast">
    <el-row :gutter="20">
      <el-col :xs="24" :lg="8">
        <el-card>
          <template #header>
            <span>预测配置</span>
          </template>
          
          <el-form :model="forecastForm" label-width="100px" label-position="top">
            <el-form-item label="产品名称">
              <el-input 
                v-model="forecastForm.product_name" 
                placeholder="请输入产品名称（如：土豆、苹果、白菜等）"
                clearable
                style="width: 100%;"
              >
                <template #prefix>
                  <el-icon><Search /></el-icon>
                </template>
              </el-input>
              <div style="margin-top: 8px; font-size: 12px; color: #909399;">
                <span>热门产品：</span>
                <el-tag 
                  v-for="product in hotProducts" 
                  :key="product"
                  size="small"
                  style="margin-right: 8px; cursor: pointer;"
                  @click="forecastForm.product_name = product"
                >
                  {{ product }}
                </el-tag>
              </div>
            </el-form-item>
            
            <el-form-item label="地区">
              <el-select 
                v-model="forecastForm.region" 
                placeholder="请选择地区"
                filterable
                clearable
                style="width: 100%;"
              >
                <el-option 
                  v-for="region in regionOptions" 
                  :key="region" 
                  :label="region" 
                  :value="region"
                />
              </el-select>
            </el-form-item>
            
            <el-form-item label="预测模型">
              <el-select 
                v-model="forecastForm.model_type" 
                placeholder="请选择预测模型"
                style="width: 100%;"
              >
                <el-option label="ARIMA模型" value="arima" />
                <el-option label="LSTM神经网络" value="lstm" />
                <el-option label="线性回归" value="linear" />
              </el-select>
            </el-form-item>
            
            <el-form-item label="预测天数">
              <el-slider 
                v-model="forecastForm.days" 
                :min="1" 
                :max="30" 
                :step="1"
                show-stops
                show-input
              />
            </el-form-item>
            
            <el-form-item>
              <el-button 
                type="primary" 
                :icon="DataAnalysis" 
                @click="handleForecast" 
                :loading="forecasting"
                style="width: 100%;"
              >
                开始预测
              </el-button>
            </el-form-item>
          </el-form>
          
          <!-- 模型信息 -->
          <el-divider />
          <div v-if="modelInfo" class="model-info">
            <h4>模型信息</h4>
            <el-descriptions :column="1" size="small" border>
              <el-descriptions-item label="模型名称">{{ modelInfo.model_name }}</el-descriptions-item>
              <el-descriptions-item label="准确度">{{ modelInfo.accuracy }}%</el-descriptions-item>
              <el-descriptions-item label="训练时间">{{ modelInfo.trained_at }}</el-descriptions-item>
            </el-descriptions>
          </div>
        </el-card>
      </el-col>
      
      <el-col :xs="24" :lg="16">
        <!-- 预测结果图表 -->
        <el-card v-if="forecastData.length > 0">
          <template #header>
            <div class="card-header">
              <span>预测结果趋势</span>
              <el-button-group>
                <el-button 
                  :icon="TrendCharts" 
                  @click="chartType = 'line'"
                  :type="chartType === 'line' ? 'primary' : ''"
                >
                  折线图
                </el-button>
                <el-button 
                  :icon="DataAnalysis" 
                  @click="chartType = 'bar'"
                  :type="chartType === 'bar' ? 'primary' : ''"
                >
                  柱状图
                </el-button>
              </el-button-group>
            </div>
          </template>
          <PriceChart :data="forecastData" :type="chartType" :height="400" />
        </el-card>
        
        <!-- 预测结果表格 -->
        <el-card v-if="forecastResults.length > 0" style="margin-top: 20px;">
          <template #header>
            <span>预测结果详情</span>
          </template>
          
          <el-table :data="forecastResults" stripe>
            <el-table-column type="index" label="序号" width="60" align="center" />
            <el-table-column prop="forecast_date" label="预测日期" width="120" />
            <el-table-column prop="forecast_price" label="预测价格" width="120" align="right">
              <template #default="scope">
                <span class="price-value">¥{{ parseFloat(scope.row.forecast_price).toFixed(2) }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="confidence_interval_lower" label="置信区间下限" width="140" align="right">
              <template #default="scope">
                <span style="color: #67C23A;">¥{{ parseFloat(scope.row.confidence_interval_lower).toFixed(2) }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="confidence_interval_upper" label="置信区间上限" width="140" align="right">
              <template #default="scope">
                <span style="color: #F56C6C;">¥{{ parseFloat(scope.row.confidence_interval_upper).toFixed(2) }}</span>
              </template>
            </el-table-column>
            <el-table-column label="置信区间" width="200">
              <template #default="scope">
                <el-progress 
                  :percentage="100"
                  :format="() => `${parseFloat(scope.row.confidence_interval_lower).toFixed(2)} - ${parseFloat(scope.row.confidence_interval_upper).toFixed(2)}`"
                  :color="getConfidenceColor(scope.row)"
                />
              </template>
            </el-table-column>
          </el-table>
        </el-card>
        
        <!-- 空状态 -->
        <el-empty 
          v-if="!forecasting && forecastResults.length === 0" 
          description="请配置预测参数并开始预测"
          :image-size="200"
        />
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { DataAnalysis, TrendCharts, Search } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import PriceChart from '../components/PriceChart.vue'
import api from '../api'

export default {
  name: 'Forecast',
  components: {
    PriceChart,
    DataAnalysis,
    TrendCharts
  },
  setup() {
    const forecasting = ref(false)
    const forecastForm = reactive({
      product_name: '',
      region: '',
      model_type: 'arima',
      days: 7
    })
    const forecastData = ref([])
    const forecastResults = ref([])
    const modelInfo = ref(null)
    const regionOptions = ref([])
    const chartType = ref('line')
    const hotProducts = ref(['土豆', '苹果', '白菜', '萝卜', '西红柿', '黄瓜', '香蕉', '橙子'])
    
    const loadOptions = async () => {
      try {
        // 加载地区选项和热门产品
        const priceResponse = await api.market.getPrices({ page_size: 100 })
        const resData = priceResponse.data?.data || priceResponse.data || {}
        const prices = resData.results || (Array.isArray(resData) ? resData : [])
        
        // 更新热门产品（从实际数据中获取）
        const products = [...new Set(prices.map(item => item.product_name).filter(Boolean))]
        if (products.length > 0) {
          hotProducts.value = products.slice(0, 8)
        }
        
        const regions = [...new Set(prices.map(item => item.region).filter(Boolean))]
        regionOptions.value = regions.sort()
      } catch (error) {
        console.error('加载选项失败:', error)
        // 使用默认热门产品
      }
    }
    
    const handleForecast = async () => {
      if (!forecastForm.product_name || !forecastForm.model_type) {
        ElMessage.warning('请填写完整的预测参数')
        return
      }
      
      forecasting.value = true
      try {
        // TODO: 调用实际的预测API
        // 1. 先获取或创建模型
        // 2. 然后进行预测
        
        // 模拟预测结果
        await new Promise(resolve => setTimeout(resolve, 2000))
        
        const mockResults = []
        const today = new Date()
        for (let i = 1; i <= forecastForm.days; i++) {
          const date = new Date(today)
          date.setDate(date.getDate() + i)
          const basePrice = 10 + Math.random() * 5
          mockResults.push({
            forecast_date: date.toISOString().split('T')[0],
            forecast_price: basePrice.toFixed(2),
            confidence_interval_lower: (basePrice * 0.9).toFixed(2),
            confidence_interval_upper: (basePrice * 1.1).toFixed(2)
          })
        }
        
        forecastResults.value = mockResults
        forecastData.value = mockResults.map(item => ({
          date: item.forecast_date,
          price: parseFloat(item.forecast_price)
        }))
        
        modelInfo.value = {
          model_name: forecastForm.model_type.toUpperCase() + '模型',
          accuracy: (85 + Math.random() * 10).toFixed(2),
          trained_at: new Date().toLocaleString()
        }
        
        ElMessage.success('预测完成！')
      } catch (error) {
        console.error('预测失败:', error)
        ElMessage.error('预测失败，请稍后重试')
      } finally {
        forecasting.value = false
      }
    }
    
    const getConfidenceColor = (row) => {
      const range = parseFloat(row.confidence_interval_upper) - parseFloat(row.confidence_interval_lower)
      const price = parseFloat(row.forecast_price)
      const ratio = range / price
      
      if (ratio < 0.1) return '#67C23A'
      if (ratio < 0.2) return '#E6A23C'
      return '#F56C6C'
    }
    
    onMounted(() => {
      loadOptions()
    })
    
    return {
      forecasting,
      forecastForm,
      forecastData,
      forecastResults,
      modelInfo,
      hotProducts,
      regionOptions,
      chartType,
      handleForecast,
      getConfidenceColor,
      DataAnalysis,
      TrendCharts,
      Search
    }
  }
}
</script>

<style scoped>
.forecast {
  padding: 0;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.model-info {
  margin-top: 20px;
}

.model-info h4 {
  margin-bottom: 12px;
  color: #303133;
}

.price-value {
  font-weight: bold;
  color: #409EFF;
  font-size: 15px;
}
</style>

