<template>
  <el-dialog 
    :model-value="modelValue" 
    @update:model-value="$emit('update:modelValue', $event)"
    title="消息中心" 
    width="900px"
    @open="handleOpen"
  >
    <el-tabs v-model="activeTab">
      <el-tab-pane label="站内信" name="messages">
        <div class="message-header">
          <span>未读消息: <el-tag type="danger">{{ unreadCount }}</el-tag></span>
          <el-button size="small" @click="markAllAsRead" :disabled="unreadCount === 0">
            全部标记为已读
          </el-button>
        </div>
        <el-table :data="messageList" style="width: 100%; margin-top: 16px;" stripe>
          <el-table-column type="index" label="序号" width="60" align="center" />
          <el-table-column prop="title" label="标题" width="200" show-overflow-tooltip />
          <el-table-column prop="message_type" label="类型" width="100" align="center">
            <template #default="scope">
              <el-tag :type="getMessageTypeTag(scope.row.message_type)" size="small">
                {{ getMessageTypeText(scope.row.message_type) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="created_at" label="时间" width="160" />
          <el-table-column label="状态" width="100" align="center">
            <template #default="scope">
              <el-tag :type="scope.row.is_read ? 'info' : 'danger'" size="small">
                {{ scope.row.is_read ? '已读' : '未读' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="150" fixed="right">
            <template #default="scope">
              <el-button size="small" @click="viewMessage(scope.row)">查看</el-button>
              <el-button 
                v-if="!scope.row.is_read" 
                size="small" 
                type="primary"
                @click="markAsRead(scope.row.id)"
              >
                已读
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>
      
      <el-tab-pane label="系统公告" name="announcements">
        <el-table :data="announcementList" style="width: 100%; margin-top: 16px;" stripe>
          <el-table-column type="index" label="序号" width="60" align="center" />
          <el-table-column prop="title" label="标题" width="250" show-overflow-tooltip />
          <el-table-column prop="announcement_type" label="类型" width="120" align="center">
            <template #default="scope">
              <el-tag :type="getAnnouncementTypeTag(scope.row.announcement_type)" size="small">
                {{ scope.row.announcement_type }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="priority" label="优先级" width="100" align="center">
            <template #default="scope">
              <el-tag :type="getPriorityTag(scope.row.priority)" size="small">
                {{ getPriorityText(scope.row.priority) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="publish_at" label="发布时间" width="160" />
          <el-table-column label="操作" width="100" fixed="right">
            <template #default="scope">
              <el-button size="small" @click="viewAnnouncement(scope.row)">查看</el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>
      
      <el-tab-pane label="价格预警" name="alerts">
        <el-table :data="alertList" style="width: 100%; margin-top: 16px;" stripe>
          <el-table-column type="index" label="序号" width="60" align="center" />
          <el-table-column prop="product_name" label="产品名称" width="120" />
          <el-table-column prop="alert_type" label="预警类型" width="120" align="center">
            <template #default="scope">
              <el-tag :type="scope.row.alert_type === 'price_rise' ? 'danger' : 'success'" size="small">
                {{ scope.row.alert_type === 'price_rise' ? '价格上涨' : '价格下跌' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="current_price" label="当前价格" width="120" align="right">
            <template #default="scope">
              <span class="price-value">¥{{ parseFloat(scope.row.current_price).toFixed(2) }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="threshold_price" label="阈值价格" width="120" align="right">
            <template #default="scope">
              <span>¥{{ parseFloat(scope.row.threshold_price).toFixed(2) }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="change_rate" label="变化率" width="120" align="right">
            <template #default="scope">
              <el-tag :type="scope.row.change_rate >= 0 ? 'danger' : 'success'" size="small">
                {{ scope.row.change_rate >= 0 ? '+' : '' }}{{ parseFloat(scope.row.change_rate).toFixed(2) }}%
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="created_at" label="预警时间" width="160" />
        </el-table>
      </el-tab-pane>
    </el-tabs>
  </el-dialog>
  
  <!-- 消息详情对话框 -->
  <el-dialog v-model="showMessageDetail" :title="currentMessage?.title" width="600px">
    <div v-html="currentMessage?.content"></div>
  </el-dialog>
</template>

<script>
import { ref, onMounted, watch } from 'vue'
import { Bell } from '@element-plus/icons-vue'
import api from '../api'

export default {
  name: 'MessageCenter',
  components: {
    Bell
  },
  props: {
    modelValue: {
      type: Boolean,
      default: false
    }
  },
  emits: ['update:modelValue'],
  setup(props) {
    const showMessageDetail = ref(false)
    const activeTab = ref('messages')
    const unreadCount = ref(0)
    const messageList = ref([])
    const announcementList = ref([])
    const alertList = ref([])
    const currentMessage = ref(null)
    
    const loadMessages = async () => {
      try {
        const response = await api.admin.getMessages()
        const resData = response.data?.data || response.data || {}
        messageList.value = resData.results || (Array.isArray(resData) ? resData : [])
        unreadCount.value = resData.unread_count || 0
      } catch (error) {
        console.error('加载消息失败:', error)
      }
    }
    
    const loadAnnouncements = async () => {
      try {
        const response = await api.admin.getAnnouncements()
        const resData = response.data?.data || response.data || {}
        announcementList.value = resData.results || (Array.isArray(resData) ? resData : [])
      } catch (error) {
        console.error('加载公告失败:', error)
      }
    }
    
    const loadAlerts = async () => {
      try {
        const response = await api.admin.getAlerts({ page_size: 50 })
        const resData = response.data?.data || response.data || {}
        alertList.value = resData.results || (Array.isArray(resData) ? resData : [])
      } catch (error) {
        console.error('加载预警失败:', error)
      }
    }
    
    const getMessageTypeTag = (type) => {
      const typeMap = {
        'price_alert': 'danger',
        'system': 'info',
        'trade': 'success',
        'forecast': 'warning'
      }
      return typeMap[type] || 'info'
    }
    
    const getMessageTypeText = (type) => {
      const typeMap = {
        'price_alert': '价格预警',
        'system': '系统消息',
        'trade': '交易消息',
        'forecast': '预测消息'
      }
      return typeMap[type] || type
    }
    
    const getAnnouncementTypeTag = (type) => {
      const typeMap = {
        'system': 'info',
        'maintenance': 'warning',
        'update': 'success'
      }
      return typeMap[type] || 'info'
    }
    
    const getPriorityTag = (priority) => {
      const priorityMap = {
        'high': 'danger',
        'medium': 'warning',
        'low': 'info'
      }
      return priorityMap[priority] || 'info'
    }
    
    const getPriorityText = (priority) => {
      const priorityMap = {
        'high': '高',
        'medium': '中',
        'low': '低'
      }
      return priorityMap[priority] || priority
    }
    
    const viewMessage = (message) => {
      currentMessage.value = message
      showMessageDetail.value = true
      if (!message.is_read) {
        markAsRead(message.id)
      }
    }
    
    const markAsRead = async (messageId) => {
      try {
        await api.admin.markMessageRead(messageId)
        loadMessages()
      } catch (error) {
        console.error('标记已读失败:', error)
      }
    }
    
    const markAllAsRead = async () => {
      try {
        await api.admin.markAllMessagesRead()
        loadMessages()
      } catch (error) {
        console.error('全部标记已读失败:', error)
      }
    }
    
    const viewAnnouncement = (announcement) => {
      currentMessage.value = announcement
      showMessageDetail.value = true
    }
    
    const handleOpen = () => {
      loadMessages()
      loadAnnouncements()
      loadAlerts()
    }
    
    onMounted(() => {
      loadMessages()
      loadAnnouncements()
      // 定时刷新未读数量
      setInterval(() => {
        loadMessages()
      }, 60000) // 每分钟刷新一次
    })
    
    return {
      showMessageDetail,
      activeTab,
      unreadCount,
      messageList,
      announcementList,
      alertList,
      currentMessage,
      viewMessage,
      markAsRead,
      markAllAsRead,
      viewAnnouncement,
      getMessageTypeTag,
      getMessageTypeText,
      getAnnouncementTypeTag,
      getPriorityTag,
      getPriorityText
    }
  }
}
</script>

<style scoped>
.message-badge {
  margin-right: 20px;
}

.message-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid #ebeef5;
}

.price-value {
  font-weight: bold;
  color: #409EFF;
}
</style>

