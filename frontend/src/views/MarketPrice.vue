<template>
  <div class="market-price">
    <el-card>
      <template #header>
        <div class="card-header">
          <span class="page-title">市场价格查询</span>
          <el-button type="primary" :icon="Refresh" @click="loadData" :loading="loading">
            刷新数据
          </el-button>
        </div>
      </template>
      
      <!-- 搜索表单 -->
      <el-card class="search-card" shadow="never">
        <el-form :inline="true" :model="searchForm" class="search-form" label-width="80px">
          <el-form-item label="产品名称">
            <el-input 
              v-model="searchForm.product_name" 
              placeholder="请输入产品名称"
              clearable
              style="width: 200px;"
            />
          </el-form-item>
          <el-form-item label="地区">
            <el-select 
              v-model="searchForm.region" 
              placeholder="请选择地区"
              clearable
              filterable
              style="width: 150px;"
            >
              <el-option 
                v-for="region in regionOptions" 
                :key="region" 
                :label="region" 
                :value="region"
              />
            </el-select>
          </el-form-item>
          <el-form-item label="日期范围">
            <el-date-picker
              v-model="dateRange"
              type="daterange"
              range-separator="至"
              start-placeholder="开始日期"
              end-placeholder="结束日期"
              format="YYYY-MM-DD"
              value-format="YYYY-MM-DD"
              @change="handleDateRangeChange"
            />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" :icon="Search" @click="handleSearch">查询</el-button>
            <el-button :icon="RefreshLeft" @click="handleReset">重置</el-button>
            <el-button :icon="Download" @click="handleExport">导出</el-button>
          </el-form-item>
        </el-form>
      </el-card>
      
      <!-- 价格趋势图 -->
      <el-card v-if="chartData.length > 0" style="margin-top: 20px;">
        <template #header>
          <span>价格趋势图</span>
        </template>
        <PriceChart :data="chartData" :height="350" type="area" />
      </el-card>
      
      <!-- 数据表格 -->
      <el-card style="margin-top: 20px;">
        <template #header>
          <div class="table-header">
            <span>价格数据列表</span>
            <div>
              <span class="data-count">共 {{ total }} 条数据</span>
            </div>
          </div>
        </template>
        
        <el-table 
          :data="tableData" 
          style="width: 100%"
          stripe
          v-loading="loading"
          @sort-change="handleSortChange"
        >
          <el-table-column type="index" label="序号" width="60" align="center" />
          <el-table-column prop="product_name" label="产品名称" width="120" sortable="custom" />
          <el-table-column prop="product_category" label="产品类别" width="120" />
          <el-table-column prop="region" label="地区" width="100" sortable="custom" />
          <el-table-column prop="market_name" label="市场名称" width="180" show-overflow-tooltip />
          <el-table-column prop="price" label="价格" width="100" sortable="custom" align="right">
            <template #default="scope">
              <span class="price-value">¥{{ parseFloat(scope.row.price).toFixed(2) }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="unit" label="单位" width="80" align="center" />
          <el-table-column prop="date" label="日期" width="120" sortable="custom" />
          <el-table-column prop="price_change_rate" label="变化率" width="120" align="right">
            <template #default="scope">
              <el-tag 
                :type="getChangeTagType(scope.row.price_change_rate)"
                size="small"
              >
                <el-icon style="margin-right: 4px;">
                  <component :is="scope.row.price_change_rate >= 0 ? 'ArrowUp' : 'ArrowDown'" />
                </el-icon>
                {{ formatChangeRate(scope.row.price_change_rate) }}
              </el-tag>
            </template>
          </el-table-column>
        </el-table>
        
        <!-- 分页 -->
        <div class="pagination-container">
          <el-pagination
            v-model:current-page="pagination.page"
            v-model:page-size="pagination.pageSize"
            :page-sizes="[10, 20, 50, 100]"
            :total="total"
            layout="total, sizes, prev, pager, next, jumper"
            @size-change="handleSizeChange"
            @current-change="handlePageChange"
          />
        </div>
      </el-card>
    </el-card>
  </div>
</template>

<script>
import { ref, reactive, onMounted, computed } from 'vue'
import { 
  Search, 
  Refresh, 
  RefreshLeft, 
  Download,
  ArrowUp,
  ArrowDown
} from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import PriceChart from '../components/PriceChart.vue'
import api from '../api'

export default {
  name: 'MarketPrice',
  components: {
    PriceChart,
    Search,
    Refresh,
    RefreshLeft,
    Download,
    ArrowUp,
    ArrowDown
  },
  setup() {
    const loading = ref(false)
    const searchForm = reactive({
      product_name: '',
      region: '',
      start_date: '',
      end_date: ''
    })
    const dateRange = ref([])
    const tableData = ref([])
    const chartData = ref([])
    const regionOptions = ref([])
    const total = ref(0)
    const pagination = reactive({
      page: 1,
      pageSize: 20
    })
    const sortParams = reactive({
      ordering: ''
    })
    
    const loadData = async () => {
      loading.value = true
      try {
        const params = {
          page: pagination.page,
          page_size: pagination.pageSize
        }
        
        // 添加搜索条件
        if (searchForm.product_name) {
          params.product_name = searchForm.product_name
        }
        if (searchForm.region) {
          params.region = searchForm.region
        }
        if (searchForm.start_date) {
          params.start_date = searchForm.start_date
        }
        if (searchForm.end_date) {
          params.end_date = searchForm.end_date
        }
        
        if (sortParams.ordering) {
          params.ordering = sortParams.ordering
        }
        
        const response = await api.market.getPrices(params)
        // 处理分页响应格式: {code, msg, data: {results, count, ...}}
        const resData = response.data?.data || response.data || {}
        
        if (resData.results) {
          // 分页格式
          tableData.value = resData.results
          total.value = resData.count || resData.results.length
        } else if (Array.isArray(resData)) {
          // 数组格式
          tableData.value = resData
          total.value = resData.length
        } else {
          tableData.value = []
          total.value = 0
        }
        
        // 准备图表数据（按日期分组并计算平均价格）
        const dateMap = new Map()
        tableData.value.forEach(item => {
          const date = item.date
          if (!dateMap.has(date)) {
            dateMap.set(date, [])
          }
          dateMap.get(date).push(parseFloat(item.price || 0))
        })
        
        // 转换为图表数据格式，按日期排序
        chartData.value = Array.from(dateMap.entries())
          .map(([date, prices]) => ({
            date: date,
            price: prices.reduce((sum, p) => sum + p, 0) / prices.length
          }))
          .sort((a, b) => {
            // 确保日期格式正确排序
            return new Date(a.date) - new Date(b.date)
          })
        
        // 提取地区选项（从所有数据中提取，不仅仅是当前页）
        if (tableData.value.length > 0) {
          const regions = [...new Set(tableData.value.map(item => item.region).filter(Boolean))]
          regionOptions.value = regions.sort()
        }
      } catch (error) {
        console.error('加载数据失败:', error)
        ElMessage.error('加载数据失败: ' + (error.message || '未知错误'))
      } finally {
        loading.value = false
      }
    }
    
    const handleSearch = () => {
      pagination.page = 1
      loadData()
    }
    
    const handleReset = () => {
      searchForm.product_name = ''
      searchForm.region = ''
      searchForm.start_date = ''
      searchForm.end_date = ''
      dateRange.value = []
      pagination.page = 1
      sortParams.ordering = ''
      loadData()
    }
    
    const handleDateRangeChange = (dates) => {
      if (dates && dates.length === 2) {
        searchForm.start_date = dates[0]
        searchForm.end_date = dates[1]
      } else {
        searchForm.start_date = ''
        searchForm.end_date = ''
      }
    }
    
    const handleSortChange = ({ prop, order }) => {
      if (order === 'ascending') {
        sortParams.ordering = prop
      } else if (order === 'descending') {
        sortParams.ordering = `-${prop}`
      } else {
        sortParams.ordering = ''
      }
      loadData()
    }
    
    const handleSizeChange = () => {
      pagination.page = 1
      loadData()
    }
    
    const handlePageChange = () => {
      loadData()
    }
    
    const handleExport = () => {
      ElMessage.info('导出功能开发中...')
    }
    
    const getChangeTagType = (rate) => {
      if (!rate) return 'info'
      const numRate = parseFloat(rate)
      if (numRate > 0) return 'danger'
      if (numRate < 0) return 'success'
      return 'info'
    }
    
    const formatChangeRate = (rate) => {
      if (!rate) return '0.00%'
      const numRate = parseFloat(rate)
      return `${numRate >= 0 ? '+' : ''}${numRate.toFixed(2)}%`
    }
    
    onMounted(() => {
      loadData()
    })
    
    return {
      loading,
      searchForm,
      dateRange,
      tableData,
      chartData,
      regionOptions,
      total,
      pagination,
      loadData,
      handleSearch,
      handleReset,
      handleDateRangeChange,
      handleSortChange,
      handleSizeChange,
      handlePageChange,
      handleExport,
      getChangeTagType,
      formatChangeRate
    }
  }
}
</script>

<style scoped>
.market-price {
  padding: 0;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.page-title {
  font-size: 18px;
  font-weight: bold;
  color: #303133;
}

.search-card {
  margin-bottom: 20px;
  background-color: #f8f9fa;
}

.search-form {
  margin: 0;
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.data-count {
  color: #909399;
  font-size: 14px;
}

.price-value {
  font-weight: bold;
  color: #409EFF;
  font-size: 15px;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

@media (max-width: 768px) {
  .search-form {
    display: flex;
    flex-direction: column;
  }
  
  .card-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
}
</style>
