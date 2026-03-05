<template>
  <div class="decision">
    <el-row :gutter="20">
      <el-col :xs="24" :lg="12">
        <el-card>
          <template #header>
            <span>利润模拟计算</span>
          </template>
          
          <el-form :model="simulationForm" label-width="120px">
            <el-form-item label="产品名称">
              <el-input 
                v-model="simulationForm.product_name" 
                placeholder="请输入产品名称"
              />
            </el-form-item>
            
            <el-form-item label="地区">
              <el-input 
                v-model="simulationForm.region" 
                placeholder="请输入地区"
              />
            </el-form-item>
            
            <el-divider>成本信息</el-divider>
            
            <el-form-item label="采购价格">
              <el-input-number 
                v-model="simulationForm.purchase_price" 
                :precision="2"
                :min="0"
                :step="0.1"
                style="width: 100%;"
              >
                <template #prefix>¥</template>
              </el-input-number>
            </el-form-item>
            
            <el-form-item label="销售价格">
              <el-input-number 
                v-model="simulationForm.sale_price" 
                :precision="2"
                :min="0"
                :step="0.1"
                style="width: 100%;"
              >
                <template #prefix>¥</template>
              </el-input-number>
            </el-form-item>
            
            <el-form-item label="数量">
              <el-input-number 
                v-model="simulationForm.quantity" 
                :precision="2"
                :min="0"
                :step="1"
                style="width: 100%;"
              >
                <template #suffix>斤</template>
              </el-input-number>
            </el-form-item>
            
            <el-divider>其他成本</el-divider>
            
            <el-form-item label="运输成本">
              <el-input-number 
                v-model="simulationForm.transport_cost" 
                :precision="2"
                :min="0"
                :step="0.1"
                style="width: 100%;"
              >
                <template #prefix>¥</template>
              </el-input-number>
            </el-form-item>
            
            <el-form-item label="仓储成本">
              <el-input-number 
                v-model="simulationForm.storage_cost" 
                :precision="2"
                :min="0"
                :step="0.1"
                style="width: 100%;"
              >
                <template #prefix>¥</template>
              </el-input-number>
            </el-form-item>
            
            <el-form-item label="其他成本">
              <el-input-number 
                v-model="simulationForm.other_cost" 
                :precision="2"
                :min="0"
                :step="0.1"
                style="width: 100%;"
              >
                <template #prefix>¥</template>
              </el-input-number>
            </el-form-item>
            
            <el-form-item>
              <el-button 
                type="primary" 
                :icon="Document" 
                @click="handleSimulate"
                :loading="simulating"
                style="width: 100%;"
              >
                计算利润
              </el-button>
              <el-button 
                @click="handleReset"
                style="width: 100%; margin-top: 10px;"
              >
                重置
              </el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>
      
      <el-col :xs="24" :lg="12">
        <!-- 模拟结果 -->
        <el-card v-if="simulationResult">
          <template #header>
            <span>模拟结果</span>
          </template>
          
          <div class="result-summary">
            <div class="result-item profit">
              <div class="result-label">利润</div>
              <div class="result-value">¥{{ simulationResult.profit.toFixed(2) }}</div>
            </div>
            
            <el-row :gutter="20" style="margin-top: 20px;">
              <el-col :span="12">
                <div class="result-item">
                  <div class="result-label">总成本</div>
                  <div class="result-value cost">¥{{ simulationResult.total_cost.toFixed(2) }}</div>
                </div>
              </el-col>
              <el-col :span="12">
                <div class="result-item">
                  <div class="result-label">总收入</div>
                  <div class="result-value revenue">¥{{ simulationResult.total_revenue.toFixed(2) }}</div>
                </div>
              </el-col>
            </el-row>
            
            <el-divider />
            
            <el-descriptions :column="1" border>
              <el-descriptions-item label="利润率">
                <el-tag :type="getProfitRateType(simulationResult.profit_rate)" size="large">
                  {{ simulationResult.profit_rate.toFixed(2) }}%
                </el-tag>
              </el-descriptions-item>
              <el-descriptions-item label="单位利润">
                ¥{{ (simulationResult.profit / simulationForm.quantity).toFixed(2) }}/斤
              </el-descriptions-item>
              <el-descriptions-item label="成本占比">
                <el-progress 
                  :percentage="(simulationResult.total_cost / simulationResult.total_revenue * 100).toFixed(1)"
                  :color="getProgressColor(simulationResult.total_cost / simulationResult.total_revenue)"
                />
              </el-descriptions-item>
            </el-descriptions>
          </div>
        </el-card>
        
        <!-- 决策建议 -->
        <el-card v-if="decisionAdvice" style="margin-top: 20px;">
          <template #header>
            <span>决策建议</span>
          </template>
          
          <div class="advice-content">
            <el-alert
              :title="decisionAdvice.title"
              :type="decisionAdvice.type"
              :description="decisionAdvice.description"
              show-icon
              :closable="false"
            />
            
            <div class="advice-items" style="margin-top: 16px;">
              <div 
                v-for="(item, index) in decisionAdvice.items" 
                :key="index"
                class="advice-item"
              >
                <el-icon class="advice-icon">
                  <component :is="item.icon" />
                </el-icon>
                <span>{{ item.text }}</span>
              </div>
            </div>
          </div>
        </el-card>
        
        <!-- 空状态 -->
        <el-empty 
          v-if="!simulationResult" 
          description="请填写模拟参数并计算利润"
          :image-size="200"
        />
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { ref, reactive } from 'vue'
import { Document, SuccessFilled, WarningFilled, InfoFilled } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import api from '../api'

export default {
  name: 'Decision',
  components: {
    Document,
    SuccessFilled,
    WarningFilled,
    InfoFilled
  },
  setup() {
    const simulating = ref(false)
    const simulationForm = reactive({
      product_name: '',
      region: '',
      purchase_price: 0,
      sale_price: 0,
      quantity: 0,
      transport_cost: 0,
      storage_cost: 0,
      other_cost: 0
    })
    const simulationResult = ref(null)
    const decisionAdvice = ref(null)
    
    const handleSimulate = async () => {
      if (!simulationForm.product_name || !simulationForm.quantity || !simulationForm.purchase_price || !simulationForm.sale_price) {
        ElMessage.warning('请填写完整的模拟参数')
        return
      }
      
      simulating.value = true
      try {
        const response = await api.decision.createSimulation(simulationForm)
        // 处理响应格式
        const resData = response.data?.data || response.data || {}
        simulationResult.value = {
          total_cost: parseFloat(resData.total_cost || 0),
          total_revenue: parseFloat(resData.total_revenue || 0),
          profit: parseFloat(resData.profit || 0),
          profit_rate: parseFloat(resData.profit_rate || 0)
        }
        
        // 生成决策建议
        generateAdvice()
        
        ElMessage.success('模拟计算完成！')
      } catch (error) {
        console.error('模拟失败:', error)
        // 使用模拟数据
        const totalCost = simulationForm.purchase_price * simulationForm.quantity + 
                         simulationForm.transport_cost + 
                         simulationForm.storage_cost + 
                         simulationForm.other_cost
        const totalRevenue = simulationForm.sale_price * simulationForm.quantity
        const profit = totalRevenue - totalCost
        const profitRate = totalRevenue > 0 ? (profit / totalRevenue) * 100 : 0
        
        simulationResult.value = {
          total_cost: totalCost,
          total_revenue: totalRevenue,
          profit: profit,
          profit_rate: profitRate
        }
        
        generateAdvice()
        ElMessage.success('模拟计算完成！')
      } finally {
        simulating.value = false
      }
    }
    
    const generateAdvice = () => {
      if (!simulationResult.value) return
      
      const profitRate = simulationResult.value.profit_rate
      let type = 'success'
      let title = '建议执行'
      let description = '该方案具有良好的盈利前景，建议执行。'
      let items = []
      
      if (profitRate < 0) {
        type = 'error'
        title = '不建议执行'
        description = '该方案预计亏损，不建议执行。'
        items = [
          { icon: 'WarningFilled', text: '考虑降低采购成本或提高销售价格' },
          { icon: 'InfoFilled', text: '优化运输和仓储成本' },
          { icon: 'InfoFilled', text: '寻找更优质的产品来源' }
        ]
      } else if (profitRate < 10) {
        type = 'warning'
        title = '谨慎考虑'
        description = '该方案利润率较低，建议优化成本结构。'
        items = [
          { icon: 'InfoFilled', text: '尝试批量采购以降低成本' },
          { icon: 'InfoFilled', text: '优化物流和仓储方案' },
          { icon: 'InfoFilled', text: '考虑提高产品附加值' }
        ]
      } else {
        items = [
          { icon: 'SuccessFilled', text: '利润空间充足，可以执行' },
          { icon: 'InfoFilled', text: '建议关注市场变化，及时调整策略' },
          { icon: 'InfoFilled', text: '可以考虑扩大规模以获得更大收益' }
        ]
      }
      
      decisionAdvice.value = {
        type,
        title,
        description,
        items
      }
    }
    
    const handleReset = () => {
      Object.assign(simulationForm, {
        product_name: '',
        region: '',
        purchase_price: 0,
        sale_price: 0,
        quantity: 0,
        transport_cost: 0,
        storage_cost: 0,
        other_cost: 0
      })
      simulationResult.value = null
      decisionAdvice.value = null
    }
    
    const getProfitRateType = (rate) => {
      if (rate < 0) return 'danger'
      if (rate < 10) return 'warning'
      return 'success'
    }
    
    const getProgressColor = (ratio) => {
      if (ratio > 0.8) return '#F56C6C'
      if (ratio > 0.6) return '#E6A23C'
      return '#67C23A'
    }
    
    return {
      simulating,
      simulationForm,
      simulationResult,
      decisionAdvice,
      handleSimulate,
      handleReset,
      getProfitRateType,
      getProgressColor
    }
  }
}
</script>

<style scoped>
.decision {
  padding: 0;
}

.result-summary {
  padding: 10px 0;
}

.result-item {
  text-align: center;
  padding: 20px;
  border-radius: 8px;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.result-item.profit {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
}

.result-label {
  font-size: 14px;
  color: #909399;
  margin-bottom: 8px;
}

.result-item.profit .result-label {
  color: rgba(255, 255, 255, 0.9);
}

.result-value {
  font-size: 32px;
  font-weight: bold;
  color: #303133;
}

.result-item.profit .result-value {
  color: #fff;
}

.result-value.cost {
  color: #F56C6C;
}

.result-value.revenue {
  color: #67C23A;
}

.advice-content {
  padding: 10px 0;
}

.advice-items {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.advice-item {
  display: flex;
  align-items: center;
  padding: 12px;
  background-color: #f5f7fa;
  border-radius: 6px;
  transition: all 0.3s ease;
}

.advice-item:hover {
  background-color: #e9ecef;
  transform: translateX(4px);
}

.advice-icon {
  margin-right: 12px;
  font-size: 18px;
  color: #409EFF;
}
</style>
