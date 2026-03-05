<template>
  <div class="trade">
    <el-tabs v-model="activeTab" @tab-change="handleTabChange">
      <el-tab-pane label="供应信息" name="supply">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>供应信息</span>
              <el-button type="primary" :icon="Plus" @click="showSupplyDialog = true">
                发布供应
              </el-button>
            </div>
          </template>
          
          <el-table :data="supplyList" stripe v-loading="loading">
            <el-table-column type="index" label="序号" width="60" align="center" />
            <el-table-column prop="product_name" label="产品名称" width="120" />
            <el-table-column prop="product_category" label="产品类别" width="120" />
            <el-table-column prop="quantity" label="数量" width="100" align="right">
              <template #default="scope">
                {{ scope.row.quantity }} {{ scope.row.unit || '斤' }}
              </template>
            </el-table-column>
            <el-table-column prop="price" label="价格" width="120" align="right">
              <template #default="scope">
                <span class="price-value">¥{{ parseFloat(scope.row.price).toFixed(2) }}/{{ scope.row.unit || '斤' }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="region" label="地区" width="100" />
            <el-table-column prop="contact_name" label="联系人" width="100" />
            <el-table-column prop="contact_phone" label="联系电话" width="120" />
            <el-table-column prop="status" label="状态" width="100" align="center">
              <template #default="scope">
                <el-tag :type="getStatusType(scope.row.status)">
                  {{ getStatusText(scope.row.status) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="120" fixed="right">
              <template #default="scope">
                <el-button size="small" @click="viewSupply(scope.row)">查看</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-tab-pane>
      
      <el-tab-pane label="需求信息" name="demand">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>需求信息</span>
              <el-button type="primary" :icon="Plus" @click="showDemandDialog = true">
                发布需求
              </el-button>
            </div>
          </template>
          
          <el-table :data="demandList" stripe v-loading="loading">
            <el-table-column type="index" label="序号" width="60" align="center" />
            <el-table-column prop="product_name" label="产品名称" width="120" />
            <el-table-column prop="product_category" label="产品类别" width="120" />
            <el-table-column prop="quantity" label="数量" width="100" align="right">
              <template #default="scope">
                {{ scope.row.quantity }} {{ scope.row.unit || '斤' }}
              </template>
            </el-table-column>
            <el-table-column prop="max_price" label="最高价格" width="120" align="right">
              <template #default="scope">
                <span class="price-value">¥{{ parseFloat(scope.row.max_price).toFixed(2) }}/{{ scope.row.unit || '斤' }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="region" label="地区" width="100" />
            <el-table-column prop="contact_name" label="联系人" width="100" />
            <el-table-column prop="contact_phone" label="联系电话" width="120" />
            <el-table-column prop="status" label="状态" width="100" align="center">
              <template #default="scope">
                <el-tag :type="getStatusType(scope.row.status)">
                  {{ getStatusText(scope.row.status) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="120" fixed="right">
              <template #default="scope">
                <el-button size="small" @click="viewDemand(scope.row)">查看</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-tab-pane>
      
      <el-tab-pane label="智能匹配" name="match">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>交易匹配推荐</span>
              <el-button :icon="Refresh" @click="loadMatches">刷新匹配</el-button>
            </div>
          </template>
          
          <el-table :data="matchList" stripe v-loading="loading">
            <el-table-column type="index" label="序号" width="60" align="center" />
            <el-table-column prop="supply_product" label="供应产品" width="120" />
            <el-table-column prop="demand_product" label="需求产品" width="120" />
            <el-table-column prop="match_score" label="匹配度" width="120" align="center">
              <template #default="scope">
                <el-progress 
                  :percentage="parseFloat(scope.row.match_score || 0)" 
                  :color="getMatchColor(scope.row.match_score || 0)"
                />
                <div style="margin-top: 4px; font-size: 12px;">
                  {{ parseFloat(scope.row.match_score || 0).toFixed(1) }}%
                </div>
              </template>
            </el-table-column>
            <el-table-column prop="price_diff" label="价格差" width="120" align="right">
              <template #default="scope">
                <span :class="(scope.row.price_diff || 0) > 0 ? 'text-danger' : 'text-success'">
                  {{ (scope.row.price_diff || 0) > 0 ? '+' : '' }}¥{{ parseFloat(scope.row.price_diff || 0).toFixed(2) }}
                </span>
              </template>
            </el-table-column>
            <el-table-column prop="status" label="状态" width="100" align="center">
              <template #default="scope">
                <el-tag :type="getStatusType(scope.row.status)">
                  {{ getStatusText(scope.row.status) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="180" fixed="right">
              <template #default="scope">
                <el-button size="small" type="primary" @click="contactMatch(scope.row)">
                  联系
                </el-button>
                <el-button size="small" @click="viewMatch(scope.row)">详情</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-tab-pane>
    </el-tabs>
    
    <!-- 发布供应对话框 -->
    <el-dialog v-model="showSupplyDialog" title="发布供应信息" width="600px">
      <el-form :model="supplyForm" label-width="100px">
        <el-form-item label="产品名称" required>
          <el-input v-model="supplyForm.product_name" placeholder="请输入产品名称" />
        </el-form-item>
        <el-form-item label="数量" required>
          <el-input-number v-model="supplyForm.quantity" :min="0" :precision="2" style="width: 100%;" />
        </el-form-item>
        <el-form-item label="价格" required>
          <el-input-number v-model="supplyForm.price" :min="0" :precision="2" style="width: 100%;" />
        </el-form-item>
        <el-form-item label="地区" required>
          <el-input v-model="supplyForm.region" placeholder="请输入地区" />
        </el-form-item>
        <el-form-item label="联系人" required>
          <el-input v-model="supplyForm.contact_name" />
        </el-form-item>
        <el-form-item label="联系电话" required>
          <el-input v-model="supplyForm.contact_phone" />
        </el-form-item>
        <el-form-item label="备注">
          <el-input v-model="supplyForm.remark" type="textarea" :rows="3" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showSupplyDialog = false">取消</el-button>
        <el-button type="primary" @click="submitSupply">提交</el-button>
      </template>
    </el-dialog>
    
    <!-- 发布需求对话框 -->
    <el-dialog v-model="showDemandDialog" title="发布需求信息" width="600px">
      <el-form :model="demandForm" label-width="100px">
        <el-form-item label="产品名称" required>
          <el-input v-model="demandForm.product_name" placeholder="请输入产品名称" />
        </el-form-item>
        <el-form-item label="数量" required>
          <el-input-number v-model="demandForm.quantity" :min="0" :precision="2" style="width: 100%;" />
        </el-form-item>
        <el-form-item label="最高价格" required>
          <el-input-number v-model="demandForm.max_price" :min="0" :precision="2" style="width: 100%;" />
        </el-form-item>
        <el-form-item label="地区" required>
          <el-input v-model="demandForm.region" placeholder="请输入地区" />
        </el-form-item>
        <el-form-item label="联系人" required>
          <el-input v-model="demandForm.contact_name" />
        </el-form-item>
        <el-form-item label="联系电话" required>
          <el-input v-model="demandForm.contact_phone" />
        </el-form-item>
        <el-form-item label="备注">
          <el-input v-model="demandForm.remark" type="textarea" :rows="3" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showDemandDialog = false">取消</el-button>
        <el-button type="primary" @click="submitDemand">提交</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { Plus, Refresh } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import api from '../api'

export default {
  name: 'Trade',
  components: {
    Plus,
    Refresh
  },
  setup() {
    const loading = ref(false)
    const activeTab = ref('supply')
    const showSupplyDialog = ref(false)
    const showDemandDialog = ref(false)
    const supplyList = ref([])
    const demandList = ref([])
    const matchList = ref([])
    
    const supplyForm = reactive({
      product_name: '',
      product_category: '',
      quantity: 0,
      price: 0,
      unit: '斤',
      region: '',
      contact_name: '',
      contact_phone: '',
      remark: ''
    })
    
    const demandForm = reactive({
      product_name: '',
      product_category: '',
      quantity: 0,
      max_price: 0,
      unit: '斤',
      region: '',
      contact_name: '',
      contact_phone: '',
      remark: ''
    })
    
    const loadSupplies = async () => {
      loading.value = true
      try {
        const response = await api.trade.getSupplies({ page_size: 100 })
        const resData = response.data?.data || response.data || {}
        supplyList.value = resData.results || (Array.isArray(resData) ? resData : [])
        
        if (supplyList.value.length === 0) {
          ElMessage.info('暂无供应信息，请先发布供应')
        }
      } catch (error) {
        console.error('加载供应信息失败:', error)
        ElMessage.error('加载供应信息失败')
      } finally {
        loading.value = false
      }
    }
    
    const loadDemands = async () => {
      loading.value = true
      try {
        const response = await api.trade.getDemands({ page_size: 100 })
        const resData = response.data?.data || response.data || {}
        demandList.value = resData.results || (Array.isArray(resData) ? resData : [])
        
        if (demandList.value.length === 0) {
          ElMessage.info('暂无需求信息，请先发布需求')
        }
      } catch (error) {
        console.error('加载需求信息失败:', error)
        ElMessage.error('加载需求信息失败')
      } finally {
        loading.value = false
      }
    }
    
    const loadMatches = async () => {
      loading.value = true
      try {
        const response = await api.trade.getMatches({ page_size: 100 })
        const resData = response.data?.data || response.data || {}
        matchList.value = resData.results || (Array.isArray(resData) ? resData : [])
        
        if (matchList.value.length === 0) {
          ElMessage.info('暂无匹配信息，系统将自动匹配供应和需求')
        }
      } catch (error) {
        console.error('加载匹配信息失败:', error)
        ElMessage.error('加载匹配信息失败')
      } finally {
        loading.value = false
      }
    }
    
    const handleTabChange = (tab) => {
      if (tab === 'supply') {
        loadSupplies()
      } else if (tab === 'demand') {
        loadDemands()
      } else if (tab === 'match') {
        loadMatches()
      }
    }
    
    const submitSupply = async () => {
      try {
        await api.trade.createSupply(supplyForm)
        ElMessage.success('发布成功！')
        showSupplyDialog.value = false
        Object.assign(supplyForm, {
          product_name: '',
          product_category: '',
          quantity: 0,
          price: 0,
          unit: '斤',
          region: '',
          contact_name: '',
          contact_phone: '',
          remark: ''
        })
        loadSupplies()
      } catch (error) {
        console.error('发布失败:', error)
        ElMessage.error('发布失败，请稍后重试')
      }
    }
    
    const submitDemand = async () => {
      try {
        await api.trade.createDemand(demandForm)
        ElMessage.success('发布成功！')
        showDemandDialog.value = false
        Object.assign(demandForm, {
          product_name: '',
          product_category: '',
          quantity: 0,
          max_price: 0,
          unit: '斤',
          region: '',
          contact_name: '',
          contact_phone: '',
          remark: ''
        })
        loadDemands()
      } catch (error) {
        console.error('发布失败:', error)
        ElMessage.error('发布失败，请稍后重试')
      }
    }
    
    const getStatusType = (status) => {
      const statusMap = {
        'pending': 'info',
        'active': 'success',
        'completed': '',
        'cancelled': 'danger'
      }
      return statusMap[status] || 'info'
    }
    
    const getStatusText = (status) => {
      const statusMap = {
        'pending': '待审核',
        'active': '进行中',
        'completed': '已完成',
        'cancelled': '已取消'
      }
      return statusMap[status] || status
    }
    
    const getMatchColor = (score) => {
      const numScore = parseFloat(score)
      if (numScore >= 80) return '#67C23A'
      if (numScore >= 60) return '#E6A23C'
      return '#F56C6C'
    }
    
    const viewSupply = (row) => {
      ElMessage.info('查看供应详情功能开发中...')
    }
    
    const viewDemand = (row) => {
      ElMessage.info('查看需求详情功能开发中...')
    }
    
    const viewMatch = (row) => {
      ElMessage.info('查看匹配详情功能开发中...')
    }
    
    const contactMatch = (row) => {
      ElMessage.info('联系功能开发中...')
    }
    
    onMounted(() => {
      loadSupplies()
    })
    
    return {
      loading,
      activeTab,
      showSupplyDialog,
      showDemandDialog,
      supplyList,
      demandList,
      matchList,
      supplyForm,
      demandForm,
      loadSupplies,
      loadDemands,
      loadMatches,
      handleTabChange,
      submitSupply,
      submitDemand,
      getStatusType,
      getStatusText,
      getMatchColor,
      viewSupply,
      viewDemand,
      viewMatch,
      contactMatch
    }
  }
}
</script>

<style scoped>
.trade {
  padding: 0;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.price-value {
  font-weight: bold;
  color: #409EFF;
  font-size: 14px;
}

.text-danger {
  color: #F56C6C;
}

.text-success {
  color: #67C23A;
}
</style>
