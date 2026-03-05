<template>
  <div ref="chartContainer" :style="{ width: '100%', height: height + 'px' }"></div>
</template>

<script>
import { ref, onMounted, watch, onBeforeUnmount, nextTick } from 'vue'
import * as echarts from 'echarts'

export default {
  name: 'PriceChart',
  props: {
    data: {
      type: Array,
      default: () => []
    },
    title: {
      type: String,
      default: '价格趋势图'
    },
    height: {
      type: Number,
      default: 400
    },
    type: {
      type: String,
      default: 'line', // line, bar, area
      validator: (value) => ['line', 'bar', 'area'].includes(value)
    }
  },
  setup(props) {
    const chartContainer = ref(null)
    let chartInstance = null
    
    const initChart = () => {
      if (!chartContainer.value) return
      
      chartInstance = echarts.init(chartContainer.value)
      updateChart()
      
      // 窗口大小改变时重新调整图表
      window.addEventListener('resize', handleResize)
    }
    
    const handleResize = () => {
      if (chartInstance) {
        chartInstance.resize()
      }
    }
    
    const updateChart = () => {
      if (!chartInstance || !props.data || props.data.length === 0) return
      
      // 处理日期格式，确保统一为 YYYY-MM-DD 格式
      const dates = props.data.map(item => {
        let date = item.date || item.time
        if (!date) return ''
        // 如果是日期对象，转换为字符串
        if (date instanceof Date) {
          date = date.toISOString().split('T')[0]
        }
        // 如果是其他格式，尝试转换
        if (typeof date === 'string' && date.includes('T')) {
          date = date.split('T')[0]
        }
        return date
      }).filter(Boolean)
      
      const prices = props.data.map(item => parseFloat(item.price) || 0)
      
      let seriesConfig = {
        name: '价格',
        type: props.type === 'bar' ? 'bar' : 'line',
        data: prices,
        smooth: props.type !== 'bar',
        itemStyle: {
          color: props.type === 'bar' ? '#409EFF' : '#667eea'
        },
        areaStyle: props.type === 'area' ? {
          color: {
            type: 'linear',
            x: 0,
            y: 0,
            x2: 0,
            y2: 1,
            colorStops: [
              { offset: 0, color: 'rgba(102, 126, 234, 0.3)' },
              { offset: 1, color: 'rgba(102, 126, 234, 0.1)' }
            ]
          }
        } : null
      }
      
      const option = {
        title: props.title ? {
          text: props.title,
          left: 'center',
          textStyle: {
            fontSize: 16,
            fontWeight: 'bold',
            color: '#303133'
          }
        } : null,
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'cross',
            label: {
              backgroundColor: '#6a7985'
            }
          },
          formatter: (params) => {
            const param = params[0]
            return `${param.name}<br/>${param.seriesName}: ¥${param.value.toFixed(2)}`
          }
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          boundaryGap: props.type === 'bar',
          data: dates,
          axisLabel: {
            rotate: dates.length > 10 ? 45 : 0,
            interval: dates.length > 20 ? Math.floor(dates.length / 10) : 0
          }
        },
        yAxis: {
          type: 'value',
          name: '价格(元)',
          axisLabel: {
            formatter: '¥{value}'
          },
          splitLine: {
            lineStyle: {
              type: 'dashed'
            }
          }
        },
        dataZoom: dates.length > 20 ? [
          {
            type: 'slider',
            start: 0,
            end: 50
          },
          {
            type: 'inside',
            start: 0,
            end: 50
          }
        ] : null,
        series: [seriesConfig]
      }
      
      chartInstance.setOption(option, true)
    }
    
    onMounted(() => {
      nextTick(() => {
        initChart()
      })
    })
    
    onBeforeUnmount(() => {
      window.removeEventListener('resize', handleResize)
      if (chartInstance) {
        chartInstance.dispose()
        chartInstance = null
      }
    })
    
    watch(() => props.data, () => {
      updateChart()
    }, { deep: true })
    
    watch(() => props.type, () => {
      updateChart()
    })
    
    return {
      chartContainer
    }
  }
}
</script>

