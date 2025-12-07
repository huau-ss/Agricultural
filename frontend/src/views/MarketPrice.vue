<template>
  <div class="market-price">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>市场价格查询</span>
          <el-button type="primary" @click="loadData">刷新</el-button>
        </div>
      </template>
      
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="产品名称">
          <el-input v-model="searchForm.product_name" placeholder="请输入产品名称" />
        </el-form-item>
        <el-form-item label="地区">
          <el-input v-model="searchForm.region" placeholder="请输入地区" />
        </el-form-item>
        <el-form-item label="开始日期">
          <el-date-picker v-model="searchForm.start_date" type="date" placeholder="选择日期" />
        </el-form-item>
        <el-form-item label="结束日期">
          <el-date-picker v-model="searchForm.end_date" type="date" placeholder="选择日期" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">查询</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
      
      <PriceChart :data="chartData" title="价格趋势图" />
      
      <el-table :data="tableData" style="width: 100%; margin-top: 20px;">
        <el-table-column prop="product_name" label="产品名称" />
        <el-table-column prop="region" label="地区" />
        <el-table-column prop="market_name" label="市场名称" />
        <el-table-column prop="price" label="价格" />
        <el-table-column prop="unit" label="单位" />
        <el-table-column prop="date" label="日期" />
        <el-table-column prop="price_change_rate" label="变化率(%)" />
      </el-table>
    </el-card>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useStore } from 'vuex'
import PriceChart from '../components/PriceChart.vue'
import api from '../api'

export default {
  name: 'MarketPrice',
  components: {
    PriceChart
  },
  setup() {
    const store = useStore()
    const searchForm = ref({
      product_name: '',
      region: '',
      start_date: '',
      end_date: ''
    })
    const tableData = ref([])
    const chartData = ref([])
    
    const loadData = async () => {
      try {
        const params = {}
        if (searchForm.value.product_name) {
          params.product_name = searchForm.value.product_name
        }
        if (searchForm.value.region) {
          params.region = searchForm.value.region
        }
        if (searchForm.value.start_date) {
          params.start_date = searchForm.value.start_date
        }
        if (searchForm.value.end_date) {
          params.end_date = searchForm.value.end_date
        }
        
        const response = await api.market.getPrices(params)
        tableData.value = response.data.data || []
        
        // 准备图表数据
        chartData.value = tableData.value.map(item => ({
          date: item.date,
          price: parseFloat(item.price)
        }))
      } catch (error) {
        console.error('加载数据失败:', error)
      }
    }
    
    const handleSearch = () => {
      loadData()
    }
    
    const handleReset = () => {
      searchForm.value = {
        product_name: '',
        region: '',
        start_date: '',
        end_date: ''
      }
      loadData()
    }
    
    onMounted(() => {
      loadData()
    })
    
    return {
      searchForm,
      tableData,
      chartData,
      loadData,
      handleSearch,
      handleReset
    }
  }
}
</script>

<style scoped>
.market-price {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.search-form {
  margin-bottom: 20px;
}
</style>

