<template>
  <div class="dashboard">
    <el-row :gutter="20">
      <el-col :span="24">
        <el-card>
          <template #header>
            <span>市场行情驾驶舱</span>
          </template>
          <PriceChart :data="priceTrend" title="价格趋势" />
        </el-card>
      </el-col>
    </el-row>
    
    <el-row :gutter="20" style="margin-top: 20px;">
      <el-col :span="12">
        <el-card>
          <template #header>
            <span>产品统计</span>
          </template>
          <el-table :data="productStats" style="width: 100%">
            <el-table-column prop="product_name" label="产品名称" />
            <el-table-column prop="avg_price" label="平均价格" />
            <el-table-column prop="max_price" label="最高价格" />
            <el-table-column prop="min_price" label="最低价格" />
          </el-table>
        </el-card>
      </el-col>
      
      <el-col :span="12">
        <el-card>
          <template #header>
            <span>地区统计</span>
          </template>
          <el-table :data="regionStats" style="width: 100%">
            <el-table-column prop="region" label="地区" />
            <el-table-column prop="avg_price" label="平均价格" />
            <el-table-column prop="count" label="数据量" />
          </el-table>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useStore } from 'vuex'
import PriceChart from '../components/PriceChart.vue'
import api from '../api'

export default {
  name: 'Dashboard',
  components: {
    PriceChart
  },
  setup() {
    const store = useStore()
    const priceTrend = ref([])
    const productStats = ref([])
    const regionStats = ref([])
    
    const loadDashboardData = async () => {
      try {
        const response = await api.market.getDashboard()
        const data = response.data.data
        
        priceTrend.value = data.price_trend || []
        productStats.value = data.product_stats || []
        regionStats.value = data.region_stats || []
      } catch (error) {
        console.error('加载驾驶舱数据失败:', error)
      }
    }
    
    onMounted(() => {
      loadDashboardData()
    })
    
    return {
      priceTrend,
      productStats,
      regionStats
    }
  }
}
</script>

<style scoped>
.dashboard {
  padding: 20px;
}
</style>

