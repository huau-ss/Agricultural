<template>
  <div class="admin">
    <el-tabs v-model="activeTab">
      <el-tab-pane label="系统日志" name="logs">
        <el-table :data="logList" style="width: 100%;">
          <el-table-column prop="log_type" label="日志类型" />
          <el-table-column prop="module" label="模块" />
          <el-table-column prop="action" label="操作" />
          <el-table-column prop="message" label="内容" />
          <el-table-column prop="created_at" label="时间" />
        </el-table>
      </el-tab-pane>
      
      <el-tab-pane label="价格预警" name="alerts">
        <el-table :data="alertList" style="width: 100%;">
          <el-table-column prop="product_name" label="产品名称" />
          <el-table-column prop="alert_type" label="预警类型" />
          <el-table-column prop="current_price" label="当前价格" />
          <el-table-column prop="change_rate" label="变化率" />
          <el-table-column prop="status" label="状态" />
        </el-table>
      </el-tab-pane>
      
      <el-tab-pane label="预警规则" name="rules">
        <el-button type="primary" @click="showRuleDialog = true">新增规则</el-button>
        <el-table :data="ruleList" style="width: 100%; margin-top: 20px;">
          <el-table-column prop="rule_name" label="规则名称" />
          <el-table-column prop="product_name" label="产品名称" />
          <el-table-column prop="alert_type" label="预警类型" />
          <el-table-column prop="threshold_value" label="阈值" />
          <el-table-column prop="is_active" label="是否启用" />
        </el-table>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import api from '../api'

export default {
  name: 'Admin',
  setup() {
    const activeTab = ref('logs')
    const showRuleDialog = ref(false)
    const logList = ref([])
    const alertList = ref([])
    const ruleList = ref([])
    
    const loadLogs = async () => {
      try {
        const response = await api.admin.getLogs()
        logList.value = response.data.data || []
      } catch (error) {
        console.error('加载日志失败:', error)
      }
    }
    
    const loadAlerts = async () => {
      try {
        const response = await api.admin.getAlerts()
        alertList.value = response.data.data || []
      } catch (error) {
        console.error('加载预警失败:', error)
      }
    }
    
    const loadRules = async () => {
      try {
        const response = await api.admin.getAlertRules()
        ruleList.value = response.data.data || []
      } catch (error) {
        console.error('加载规则失败:', error)
      }
    }
    
    onMounted(() => {
      loadLogs()
      loadAlerts()
      loadRules()
    })
    
    return {
      activeTab,
      showRuleDialog,
      logList,
      alertList,
      ruleList
    }
  }
}
</script>

<style scoped>
.admin {
  padding: 20px;
}
</style>

