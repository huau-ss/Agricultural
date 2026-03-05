<template>
  <div class="dashboard">
    <!-- 统计卡片 -->
    <el-row :gutter="20" class="stats-row">
      <el-col :xs="24" :sm="12" :md="6" v-for="stat in stats" :key="stat.title">
        <el-card class="stat-card" :style="{ borderTopColor: stat.color }">
          <div class="stat-content">
            <div class="stat-icon" :style="{ color: stat.color }">
              <el-icon :size="40">
                <component :is="stat.icon" />
              </el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stat.value }}</div>
              <div class="stat-title">{{ stat.title }}</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
    
    <!-- 价格趋势图 -->
    <el-row :gutter="20" style="margin-top: 20px;">
      <el-col :xs="24" :lg="16">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>价格趋势分析</span>
              <el-button-group>
                <el-button 
                  v-for="period in timePeriods" 
                  :key="period.value"
                  :type="selectedPeriod === period.value ? 'primary' : ''"
                  size="small"
                  @click="selectedPeriod = period.value; loadPriceTrend()"
                >
                  {{ period.label }}
                </el-button>
              </el-button-group>
            </div>
          </template>
          <PriceChart :data="priceTrend" title="" :height="350" />
        </el-card>
      </el-col>
      
      <el-col :xs="24" :lg="8">
        <el-card>
          <template #header>
            <span>热门产品</span>
          </template>
          <div class="hot-products">
            <div 
              v-for="(product, index) in hotProducts" 
              :key="product.id"
              class="hot-product-item"
            >
              <div class="product-rank">{{ index + 1 }}</div>
              <div class="product-info">
                <div class="product-name">{{ product.product_name }}</div>
                <div class="product-price">¥{{ product.avg_price }}/{{ product.unit }}</div>
              </div>
              <div class="product-change" :class="product.change >= 0 ? 'up' : 'down'">
                <el-icon>
                  <component :is="product.change >= 0 ? 'ArrowUp' : 'ArrowDown'" />
                </el-icon>
                {{ Math.abs(product.change) }}%
              </div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
    
    <!-- 产品统计和地区统计 -->
    <el-row :gutter="20" style="margin-top: 20px;">
      <el-col :xs="24" :lg="12">
        <el-card>
          <template #header>
            <span>产品价格统计</span>
          </template>
          <el-table :data="productStats" style="width: 100%" stripe>
            <el-table-column prop="product_name" label="产品名称" width="120" />
            <el-table-column label="价格区间" width="150">
              <template #default="scope">
                <span style="color: #67C23A;">¥{{ scope.row.min_price }}</span>
                <span style="margin: 0 8px;">-</span>
                <span style="color: #F56C6C;">¥{{ scope.row.max_price }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="avg_price" label="平均价格" width="100">
              <template #default="scope">
                <span style="font-weight: bold; color: #409EFF;">¥{{ scope.row.avg_price }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="count" label="数据量" width="80" />
          </el-table>
        </el-card>
      </el-col>
      
      <el-col :xs="24" :lg="12">
        <el-card>
          <template #header>
            <span>地区价格分布</span>
          </template>
          <div ref="regionChartContainer" style="width: 100%; height: 300px;"></div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { ref, onMounted, nextTick } from 'vue'
import { 
  TrendCharts, 
  DataAnalysis, 
  ShoppingCart, 
  Document,
  ArrowUp,
  ArrowDown
} from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import PriceChart from '../components/PriceChart.vue'
import api from '../api'
import * as echarts from 'echarts'

export default {
  name: 'Dashboard',
  components: {
    PriceChart,
    TrendCharts,
    DataAnalysis,
    ShoppingCart,
    Document,
    ArrowUp,
    ArrowDown
  },
  setup() {
    const stats = ref([
      { 
        title: '产品种类', 
        value: '0', 
        icon: 'ShoppingCart', 
        color: '#409EFF' 
      },
      { 
        title: '数据总量', 
        value: '0', 
        icon: 'DataAnalysis', 
        color: '#67C23A' 
      },
      { 
        title: '市场数量', 
        value: '0', 
        icon: 'TrendCharts', 
        color: '#E6A23C' 
      },
      { 
        title: '预警数量', 
        value: '0', 
        icon: 'Document', 
        color: '#F56C6C' 
      }
    ])
    
    const priceTrend = ref([])
    const productStats = ref([])
    const regionStats = ref([])
    const hotProducts = ref([])
    const selectedPeriod = ref('7d')
    const regionChartContainer = ref(null)
    let regionChart = null
    
    const timePeriods = [
      { label: '7天', value: '7d' },
      { label: '30天', value: '30d' },
      { label: '90天', value: '90d' },
      { label: '全部', value: 'all' }
    ]
    
    const loadDashboardData = async () => {
      try {
        const response = await api.market.getDashboard()
        // 后端返回格式: {code, msg, data}
        const data = response.data?.data || response.data || {}
        
        // 更新统计数据
        stats.value[0].value = String(data.product_count || 0)
        stats.value[1].value = String(data.total_count || 0)
        stats.value[2].value = String(data.market_count || 0)
        stats.value[3].value = String(data.alert_count || 0)
        
        // 价格趋势
        priceTrend.value = (data.price_trend || []).map(item => ({
          date: item.date || item.time,
          price: parseFloat(item.price || item.avg_price || 0)
        }))
        
        // 产品统计
        productStats.value = (data.product_stats || []).map(item => ({
          product_name: item.product_name,
          avg_price: parseFloat(item.avg_price || 0).toFixed(2),
          max_price: parseFloat(item.max_price || 0).toFixed(2),
          min_price: parseFloat(item.min_price || 0).toFixed(2),
          count: item.count || 0
        }))
        
        // 地区统计
        regionStats.value = (data.region_stats || []).map(item => ({
          region: item.region,
          avg_price: parseFloat(item.avg_price || 0).toFixed(2),
          count: item.count || 0
        }))
        
        // 热门产品（取前5个）
        hotProducts.value = (data.product_stats || [])
          .slice(0, 5)
          .map(item => ({
            id: item.product_name,
            product_name: item.product_name,
            avg_price: parseFloat(item.avg_price || 0).toFixed(2),
            unit: '元/斤',
            change: (Math.random() * 10 - 5).toFixed(2) // 模拟变化率
          }))
        
        // 绘制地区分布图
        if (regionStats.value.length > 0) {
          nextTick(() => {
            drawRegionChart()
          })
        }
      } catch (error) {
        console.error('加载驾驶舱数据失败:', error)
        ElMessage.error('加载数据失败: ' + (error.message || '未知错误'))
      }
    }
    
    const loadPriceTrend = async () => {
      try {
        // 根据选择的周期计算日期范围
        const endDate = new Date()
        let startDate = new Date()
        
        switch (selectedPeriod.value) {
          case '7d':
            startDate.setDate(endDate.getDate() - 7)
            break
          case '30d':
            startDate.setDate(endDate.getDate() - 30)
            break
          case '90d':
            startDate.setDate(endDate.getDate() - 90)
            break
          case 'all':
            startDate = null
            break
        }
        
        const params = {}
        if (startDate) {
          params.start_date = startDate.toISOString().split('T')[0]
        }
        params.end_date = endDate.toISOString().split('T')[0]
        params.page_size = 1000 // 获取足够的数据
        
        const response = await api.market.getPrices(params)
        const resData = response.data?.data || response.data || {}
        const prices = resData.results || (Array.isArray(resData) ? resData : [])
        
        // 按日期分组并计算平均价格
        const dateMap = new Map()
        prices.forEach(item => {
          const date = item.date
          if (!dateMap.has(date)) {
            dateMap.set(date, [])
          }
          dateMap.get(date).push(parseFloat(item.price || 0))
        })
        
        // 转换为图表数据格式，按日期排序
        priceTrend.value = Array.from(dateMap.entries())
          .map(([date, prices]) => ({
            date: date,
            price: prices.reduce((sum, p) => sum + p, 0) / prices.length
          }))
          .sort((a, b) => a.date.localeCompare(b.date))
      } catch (error) {
        console.error('加载价格趋势失败:', error)
        ElMessage.error('加载价格趋势失败')
      }
    }
    
    const drawRegionChart = () => {
      if (!regionChartContainer.value || regionStats.value.length === 0) {
        // 如果没有数据，显示空状态
        if (regionChartContainer.value) {
          regionChartContainer.value.innerHTML = '<div style="text-align: center; padding-top: 100px; color: #909399;">暂无数据</div>'
        }
        return
      }
      
      if (!regionChart) {
        regionChart = echarts.init(regionChartContainer.value)
      }
      
      const chartData = regionStats.value
        .filter(item => item.region && parseFloat(item.avg_price) > 0)
        .map(item => ({
          value: parseFloat(item.avg_price),
          name: item.region || '未知地区'
        }))
      
      if (chartData.length === 0) {
        regionChartContainer.value.innerHTML = '<div style="text-align: center; padding-top: 100px; color: #909399;">暂无数据</div>'
        return
      }
      
      const option = {
        tooltip: {
          trigger: 'item',
          formatter: '{b}: ¥{c} ({d}%)'
        },
        legend: {
          orient: 'vertical',
          left: 'left',
          top: 'middle',
          data: chartData.map(item => item.name)
        },
        series: [
          {
            name: '地区价格',
            type: 'pie',
            radius: ['40%', '70%'],
            avoidLabelOverlap: false,
            itemStyle: {
              borderRadius: 10,
              borderColor: '#fff',
              borderWidth: 2
            },
            label: {
              show: true,
              formatter: '{b}\n¥{c}'
            },
            emphasis: {
              label: {
                show: true,
                fontSize: 14,
                fontWeight: 'bold'
              }
            },
            data: chartData
          }
        ]
      }
      
      regionChart.setOption(option, true)
    }
    
    onMounted(() => {
      loadDashboardData()
      
      // 窗口大小改变时重新绘制图表
      window.addEventListener('resize', () => {
        if (regionChart) {
          regionChart.resize()
        }
      })
    })
    
    return {
      stats,
      priceTrend,
      productStats,
      regionStats,
      hotProducts,
      selectedPeriod,
      timePeriods,
      regionChartContainer,
      loadPriceTrend
    }
  }
}
</script>

<style scoped>
.dashboard {
  padding: 0;
}

.stats-row {
  margin-bottom: 20px;
}

.stat-card {
  border-top: 4px solid;
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

.stat-content {
  display: flex;
  align-items: center;
  padding: 10px 0;
}

.stat-icon {
  margin-right: 20px;
  opacity: 0.8;
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 28px;
  font-weight: bold;
  color: #303133;
  line-height: 1;
  margin-bottom: 8px;
}

.stat-title {
  font-size: 14px;
  color: #909399;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.hot-products {
  max-height: 350px;
  overflow-y: auto;
}

.hot-product-item {
  display: flex;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid #f0f0f0;
  transition: all 0.3s ease;
}

.hot-product-item:hover {
  background-color: #f5f7fa;
  padding-left: 8px;
}

.hot-product-item:last-child {
  border-bottom: none;
}

.product-rank {
  width: 32px;
  height: 32px;
  line-height: 32px;
  text-align: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  border-radius: 50%;
  font-weight: bold;
  margin-right: 12px;
  flex-shrink: 0;
}

.product-info {
  flex: 1;
}

.product-name {
  font-size: 14px;
  font-weight: 500;
  color: #303133;
  margin-bottom: 4px;
}

.product-price {
  font-size: 12px;
  color: #909399;
}

.product-change {
  display: flex;
  align-items: center;
  font-size: 14px;
  font-weight: bold;
  padding: 4px 8px;
  border-radius: 4px;
}

.product-change.up {
  color: #67C23A;
  background-color: #f0f9ff;
}

.product-change.down {
  color: #F56C6C;
  background-color: #fef0f0;
}

@media (max-width: 768px) {
  .card-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
}
</style>
