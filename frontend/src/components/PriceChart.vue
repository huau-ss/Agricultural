<template>
  <div ref="chartContainer" style="width: 100%; height: 400px;"></div>
</template>

<script>
import { ref, onMounted, watch } from 'vue'
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
    }
  },
  setup(props) {
    const chartContainer = ref(null)
    let chartInstance = null
    
    const initChart = () => {
      if (!chartContainer.value) return
      
      chartInstance = echarts.init(chartContainer.value)
      
      const option = {
        title: {
          text: props.title,
          left: 'center'
        },
        tooltip: {
          trigger: 'axis'
        },
        xAxis: {
          type: 'category',
          data: props.data.map(item => item.date)
        },
        yAxis: {
          type: 'value',
          name: '价格(元)'
        },
        series: [{
          name: '价格',
          type: 'line',
          data: props.data.map(item => item.price),
          smooth: true,
          itemStyle: {
            color: '#409EFF'
          }
        }]
      }
      
      chartInstance.setOption(option)
    }
    
    onMounted(() => {
      initChart()
    })
    
    watch(() => props.data, () => {
      if (chartInstance) {
        const option = {
          xAxis: {
            data: props.data.map(item => item.date)
          },
          series: [{
            data: props.data.map(item => item.price)
          }]
        }
        chartInstance.setOption(option)
      }
    }, { deep: true })
    
    return {
      chartContainer
    }
  }
}
</script>

