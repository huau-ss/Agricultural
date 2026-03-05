<template>
  <div class="admin">
    <el-tabs v-model="activeTab" @tab-change="handleTabChange">
      <el-tab-pane label="系统日志" name="logs">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>系统日志</span>
              <el-button :icon="Refresh" @click="loadLogs" :loading="loading">刷新</el-button>
            </div>
          </template>
          <el-table :data="logList" style="width: 100%;" stripe v-loading="loading">
            <el-table-column type="index" label="序号" width="60" align="center" />
            <el-table-column prop="log_type" label="日志类型" width="100" align="center">
              <template #default="scope">
                <el-tag :type="getLogTypeTag(scope.row.log_type)" size="small">
                  {{ getLogTypeText(scope.row.log_type) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="module" label="模块" width="120" />
            <el-table-column prop="action" label="操作" width="150" />
            <el-table-column prop="message" label="内容" show-overflow-tooltip />
            <el-table-column prop="user" label="用户" width="100">
              <template #default="scope">
                {{ scope.row.user?.username || '-' }}
              </template>
            </el-table-column>
            <el-table-column prop="ip_address" label="IP地址" width="120" />
            <el-table-column prop="created_at" label="时间" width="160" />
          </el-table>
        </el-card>
      </el-tab-pane>
      
      <el-tab-pane label="价格预警" name="alerts">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>价格预警</span>
              <el-button :icon="Refresh" @click="loadAlerts" :loading="loading">刷新</el-button>
            </div>
          </template>
          <el-table :data="alertList" style="width: 100%;" stripe v-loading="loading">
            <el-table-column type="index" label="序号" width="60" align="center" />
            <el-table-column prop="product_name" label="产品名称" width="120" />
            <el-table-column prop="region" label="地区" width="100" />
            <el-table-column prop="alert_type" label="预警类型" width="120" align="center">
              <template #default="scope">
                <el-tag :type="scope.row.alert_type === 'price_rise' ? 'danger' : 'success'" size="small">
                  {{ scope.row.alert_type === 'price_rise' ? '价格上涨' : '价格下跌' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="current_price" label="当前价格" width="120" align="right">
              <template #default="scope">
                <span class="price-value">¥{{ parseFloat(scope.row.current_price || 0).toFixed(2) }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="threshold_price" label="阈值价格" width="120" align="right">
              <template #default="scope">
                <span>¥{{ parseFloat(scope.row.threshold_price || 0).toFixed(2) }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="change_rate" label="变化率" width="120" align="right">
              <template #default="scope">
                <el-tag :type="scope.row.change_rate >= 0 ? 'danger' : 'success'" size="small">
                  {{ scope.row.change_rate >= 0 ? '+' : '' }}{{ parseFloat(scope.row.change_rate || 0).toFixed(2) }}%
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="status" label="状态" width="100" align="center">
              <template #default="scope">
                <el-tag :type="getStatusTag(scope.row.status)" size="small">
                  {{ getStatusText(scope.row.status) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="created_at" label="预警时间" width="160" />
          </el-table>
        </el-card>
      </el-tab-pane>
      
      <el-tab-pane label="预警规则" name="rules">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>预警规则</span>
              <div>
                <el-button type="primary" :icon="Plus" @click="showRuleDialog = true">新增规则</el-button>
                <el-button :icon="Refresh" @click="loadRules" :loading="loading">刷新</el-button>
              </div>
            </div>
          </template>
          <el-table :data="ruleList" style="width: 100%;" stripe v-loading="loading">
            <el-table-column type="index" label="序号" width="60" align="center" />
            <el-table-column prop="rule_name" label="规则名称" width="150" />
            <el-table-column prop="product_name" label="产品名称" width="120" />
            <el-table-column prop="region" label="地区" width="100" />
            <el-table-column prop="alert_type" label="预警类型" width="120" align="center">
              <template #default="scope">
                <el-tag :type="scope.row.alert_type === 'price_rise' ? 'danger' : 'success'" size="small">
                  {{ scope.row.alert_type === 'price_rise' ? '价格上涨' : '价格下跌' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="threshold_value" label="阈值" width="120" align="right">
              <template #default="scope">
                {{ scope.row.threshold_value }} {{ scope.row.threshold_type === 'percentage' ? '%' : '元' }}
              </template>
            </el-table-column>
            <el-table-column prop="is_active" label="是否启用" width="100" align="center">
              <template #default="scope">
                <el-tag :type="scope.row.is_active ? 'success' : 'info'" size="small">
                  {{ scope.row.is_active ? '启用' : '禁用' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="created_at" label="创建时间" width="160" />
            <el-table-column label="操作" width="120" fixed="right">
              <template #default="scope">
                <el-button size="small" @click="editRule(scope.row)">编辑</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-tab-pane>
    </el-tabs>
    
    <!-- 新增/编辑规则对话框 -->
    <el-dialog 
      v-model="showRuleDialog" 
      :title="editingRule ? '编辑规则' : '新增规则'" 
      width="600px"
    >
      <el-form :model="ruleForm" label-width="100px">
        <el-form-item label="规则名称" required>
          <el-input v-model="ruleForm.rule_name" placeholder="请输入规则名称" />
        </el-form-item>
        <el-form-item label="产品名称" required>
          <el-input v-model="ruleForm.product_name" placeholder="请输入产品名称" />
        </el-form-item>
        <el-form-item label="地区">
          <el-input v-model="ruleForm.region" placeholder="请输入地区（可选）" />
        </el-form-item>
        <el-form-item label="预警类型" required>
          <el-select v-model="ruleForm.alert_type" style="width: 100%;">
            <el-option label="价格上涨" value="price_rise" />
            <el-option label="价格下跌" value="price_fall" />
          </el-select>
        </el-form-item>
        <el-form-item label="阈值类型" required>
          <el-select v-model="ruleForm.threshold_type" style="width: 100%;">
            <el-option label="百分比" value="percentage" />
            <el-option label="绝对值" value="absolute" />
          </el-select>
        </el-form-item>
        <el-form-item label="阈值" required>
          <el-input-number v-model="ruleForm.threshold_value" :min="0" :precision="2" style="width: 100%;" />
        </el-form-item>
        <el-form-item label="是否启用">
          <el-switch v-model="ruleForm.is_active" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showRuleDialog = false">取消</el-button>
        <el-button type="primary" @click="saveRule">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { Refresh, Plus } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import api from '../api'

export default {
  name: 'Admin',
  components: {
    Refresh,
    Plus
  },
  setup() {
    const loading = ref(false)
    const activeTab = ref('logs')
    const showRuleDialog = ref(false)
    const editingRule = ref(null)
    const logList = ref([])
    const alertList = ref([])
    const ruleList = ref([])
    
    const ruleForm = reactive({
      rule_name: '',
      product_name: '',
      region: '',
      alert_type: 'price_rise',
      threshold_type: 'percentage',
      threshold_value: 10,
      is_active: true
    })
    
    const loadLogs = async () => {
      loading.value = true
      try {
        const response = await api.admin.getLogs({ page_size: 100 })
        const resData = response.data?.data || response.data || {}
        logList.value = resData.results || (Array.isArray(resData) ? resData : [])
        
        if (logList.value.length === 0) {
          ElMessage.info('暂无系统日志')
        }
      } catch (error) {
        console.error('加载日志失败:', error)
        ElMessage.error('加载日志失败')
      } finally {
        loading.value = false
      }
    }
    
    const loadAlerts = async () => {
      loading.value = true
      try {
        const response = await api.admin.getAlerts({ page_size: 100 })
        const resData = response.data?.data || response.data || {}
        alertList.value = resData.results || (Array.isArray(resData) ? resData : [])
        
        if (alertList.value.length === 0) {
          ElMessage.info('暂无价格预警')
        }
      } catch (error) {
        console.error('加载预警失败:', error)
        ElMessage.error('加载预警失败')
      } finally {
        loading.value = false
      }
    }
    
    const loadRules = async () => {
      loading.value = true
      try {
        const response = await api.admin.getAlertRules({ page_size: 100 })
        const resData = response.data?.data || response.data || {}
        ruleList.value = resData.results || (Array.isArray(resData) ? resData : [])
        
        if (ruleList.value.length === 0) {
          ElMessage.info('暂无预警规则，请创建规则')
        }
      } catch (error) {
        console.error('加载规则失败:', error)
        ElMessage.error('加载规则失败')
      } finally {
        loading.value = false
      }
    }
    
    const handleTabChange = (tab) => {
      if (tab === 'logs') {
        loadLogs()
      } else if (tab === 'alerts') {
        loadAlerts()
      } else if (tab === 'rules') {
        loadRules()
      }
    }
    
    const getLogTypeTag = (type) => {
      const typeMap = {
        'info': '',
        'warning': 'warning',
        'error': 'danger',
        'debug': 'info'
      }
      return typeMap[type] || 'info'
    }
    
    const getLogTypeText = (type) => {
      const typeMap = {
        'info': '信息',
        'warning': '警告',
        'error': '错误',
        'debug': '调试'
      }
      return typeMap[type] || type
    }
    
    const getStatusTag = (status) => {
      const statusMap = {
        'pending': 'warning',
        'processed': 'success',
        'ignored': 'info'
      }
      return statusMap[status] || 'info'
    }
    
    const getStatusText = (status) => {
      const statusMap = {
        'pending': '待处理',
        'processed': '已处理',
        'ignored': '已忽略'
      }
      return statusMap[status] || status
    }
    
    const editRule = (rule) => {
      editingRule.value = rule
      Object.assign(ruleForm, {
        rule_name: rule.rule_name,
        product_name: rule.product_name,
        region: rule.region,
        alert_type: rule.alert_type,
        threshold_type: rule.threshold_type,
        threshold_value: parseFloat(rule.threshold_value),
        is_active: rule.is_active
      })
      showRuleDialog.value = true
    }
    
    const saveRule = async () => {
      try {
        if (editingRule.value) {
          await api.admin.updateAlertRule(editingRule.value.id, ruleForm)
          ElMessage.success('更新成功')
        } else {
          await api.admin.createAlertRule(ruleForm)
          ElMessage.success('创建成功')
        }
        showRuleDialog.value = false
        editingRule.value = null
        Object.assign(ruleForm, {
          rule_name: '',
          product_name: '',
          region: '',
          alert_type: 'price_rise',
          threshold_type: 'percentage',
          threshold_value: 10,
          is_active: true
        })
        loadRules()
      } catch (error) {
        console.error('保存规则失败:', error)
        ElMessage.error('保存失败')
      }
    }
    
    onMounted(() => {
      loadLogs()
    })
    
    return {
      loading,
      activeTab,
      showRuleDialog,
      editingRule,
      logList,
      alertList,
      ruleList,
      ruleForm,
      loadLogs,
      loadAlerts,
      loadRules,
      handleTabChange,
      getLogTypeTag,
      getLogTypeText,
      getStatusTag,
      getStatusText,
      editRule,
      saveRule
    }
  }
}
</script>

<style scoped>
.admin {
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
}
</style>

