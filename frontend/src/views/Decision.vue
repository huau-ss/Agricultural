<template>
  <div class="decision">
    <el-card>
      <template #header>
        <span>利润模拟</span>
      </template>
      
      <el-form :model="simulationForm" label-width="120px">
        <el-form-item label="产品名称">
          <el-input v-model="simulationForm.product_name" />
        </el-form-item>
        <el-form-item label="地区">
          <el-input v-model="simulationForm.region" />
        </el-form-item>
        <el-form-item label="采购价格">
          <el-input-number v-model="simulationForm.purchase_price" :precision="2" />
        </el-form-item>
        <el-form-item label="销售价格">
          <el-input-number v-model="simulationForm.sale_price" :precision="2" />
        </el-form-item>
        <el-form-item label="数量">
          <el-input-number v-model="simulationForm.quantity" :precision="2" />
        </el-form-item>
        <el-form-item label="运输成本">
          <el-input-number v-model="simulationForm.transport_cost" :precision="2" />
        </el-form-item>
        <el-form-item label="仓储成本">
          <el-input-number v-model="simulationForm.storage_cost" :precision="2" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSimulate">计算利润</el-button>
        </el-form-item>
      </el-form>
      
      <el-card v-if="simulationResult" style="margin-top: 20px;">
        <template #header>
          <span>模拟结果</span>
        </template>
        <el-descriptions :column="2">
          <el-descriptions-item label="总成本">{{ simulationResult.total_cost }}</el-descriptions-item>
          <el-descriptions-item label="总收入">{{ simulationResult.total_revenue }}</el-descriptions-item>
          <el-descriptions-item label="利润">{{ simulationResult.profit }}</el-descriptions-item>
          <el-descriptions-item label="利润率">{{ simulationResult.profit_rate }}%</el-descriptions-item>
        </el-descriptions>
      </el-card>
    </el-card>
  </div>
</template>

<script>
import { ref } from 'vue'
import api from '../api'

export default {
  name: 'Decision',
  setup() {
    const simulationForm = ref({
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
    
    const handleSimulate = async () => {
      try {
        const response = await api.decision.createSimulation(simulationForm.value)
        simulationResult.value = response.data.data
      } catch (error) {
        console.error('模拟失败:', error)
      }
    }
    
    return {
      simulationForm,
      simulationResult,
      handleSimulate
    }
  }
}
</script>

<style scoped>
.decision {
  padding: 20px;
}
</style>

