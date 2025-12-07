<template>
  <div class="trade">
    <el-tabs v-model="activeTab">
      <el-tab-pane label="供应信息" name="supply">
        <el-button type="primary" @click="showSupplyDialog = true">发布供应</el-button>
        <el-table :data="supplyList" style="width: 100%; margin-top: 20px;">
          <el-table-column prop="product_name" label="产品名称" />
          <el-table-column prop="quantity" label="数量" />
          <el-table-column prop="price" label="价格" />
          <el-table-column prop="region" label="地区" />
          <el-table-column prop="contact_name" label="联系人" />
          <el-table-column prop="contact_phone" label="联系电话" />
        </el-table>
      </el-tab-pane>
      
      <el-tab-pane label="需求信息" name="demand">
        <el-button type="primary" @click="showDemandDialog = true">发布需求</el-button>
        <el-table :data="demandList" style="width: 100%; margin-top: 20px;">
          <el-table-column prop="product_name" label="产品名称" />
          <el-table-column prop="quantity" label="数量" />
          <el-table-column prop="max_price" label="最高价格" />
          <el-table-column prop="region" label="地区" />
          <el-table-column prop="contact_name" label="联系人" />
          <el-table-column prop="contact_phone" label="联系电话" />
        </el-table>
      </el-tab-pane>
      
      <el-tab-pane label="交易匹配" name="match">
        <el-table :data="matchList" style="width: 100%;">
          <el-table-column prop="supply_product" label="供应产品" />
          <el-table-column prop="demand_product" label="需求产品" />
          <el-table-column prop="match_score" label="匹配度" />
          <el-table-column prop="status" label="状态" />
        </el-table>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import api from '../api'

export default {
  name: 'Trade',
  setup() {
    const activeTab = ref('supply')
    const showSupplyDialog = ref(false)
    const showDemandDialog = ref(false)
    const supplyList = ref([])
    const demandList = ref([])
    const matchList = ref([])
    
    const loadSupplies = async () => {
      try {
        const response = await api.trade.getSupplies()
        supplyList.value = response.data.data || []
      } catch (error) {
        console.error('加载供应信息失败:', error)
      }
    }
    
    const loadDemands = async () => {
      try {
        const response = await api.trade.getDemands()
        demandList.value = response.data.data || []
      } catch (error) {
        console.error('加载需求信息失败:', error)
      }
    }
    
    const loadMatches = async () => {
      try {
        const response = await api.trade.getMatches()
        matchList.value = response.data.data || []
      } catch (error) {
        console.error('加载匹配信息失败:', error)
      }
    }
    
    onMounted(() => {
      loadSupplies()
      loadDemands()
      loadMatches()
    })
    
    return {
      activeTab,
      showSupplyDialog,
      showDemandDialog,
      supplyList,
      demandList,
      matchList
    }
  }
}
</script>

<style scoped>
.trade {
  padding: 20px;
}
</style>

