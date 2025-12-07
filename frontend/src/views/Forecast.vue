<template>
  <div class="forecast">
    <el-card>
      <template #header>
        <span>价格预测</span>
      </template>
      
      <el-form :inline="true" :model="forecastForm" class="search-form">
        <el-form-item label="产品名称">
          <el-input v-model="forecastForm.product_name" placeholder="请输入产品名称" />
        </el-form-item>
        <el-form-item label="地区">
          <el-input v-model="forecastForm.region" placeholder="请输入地区" />
        </el-form-item>
        <el-form-item label="预测天数">
          <el-input-number v-model="forecastForm.days" :min="1" :max="30" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleForecast">开始预测</el-button>
        </el-form-item>
      </el-form>
      
      <PriceChart v-if="forecastData.length > 0" :data="forecastData" title="预测结果" />
      
      <el-table v-if="forecastResults.length > 0" :data="forecastResults" style="width: 100%; margin-top: 20px;">
        <el-table-column prop="forecast_date" label="预测日期" />
        <el-table-column prop="forecast_price" label="预测价格" />
        <el-table-column prop="confidence_interval_lower" label="置信区间下限" />
        <el-table-column prop="confidence_interval_upper" label="置信区间上限" />
      </el-table>
    </el-card>
  </div>
</template>

<script>
import { ref } from 'vue'
import PriceChart from '../components/PriceChart.vue'
import api from '../api'

export default {
  name: 'Forecast',
  components: {
    PriceChart
  },
  setup() {
    const forecastForm = ref({
      product_name: '',
      region: '',
      days: 7
    })
    const forecastData = ref([])
    const forecastResults = ref([])
    
    const handleForecast = async () => {
      try {
        // TODO: 调用预测API
        // const response = await api.forecast.predict(modelId, { days: forecastForm.value.days })
        // forecastResults.value = response.data.data
        
        // 示例数据
        forecastResults.value = [
          {
            forecast_date: '2024-01-01',
            forecast_price: 10.5,
            confidence_interval_lower: 9.8,
            confidence_interval_upper: 11.2
          }
        ]
        
        forecastData.value = forecastResults.value.map(item => ({
          date: item.forecast_date,
          price: parseFloat(item.forecast_price)
        }))
      } catch (error) {
        console.error('预测失败:', error)
      }
    }
    
    return {
      forecastForm,
      forecastData,
      forecastResults,
      handleForecast
    }
  }
}
</script>

<style scoped>
.forecast {
  padding: 20px;
}

.search-form {
  margin-bottom: 20px;
}
</style>

