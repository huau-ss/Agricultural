<template>
  <el-badge :value="unreadCount" :hidden="unreadCount === 0" class="message-badge">
    <el-button :icon="Bell" circle @click="showMessageDialog = true" />
  </el-badge>
  
  <el-dialog v-model="showMessageDialog" title="消息中心" width="800px">
    <el-tabs v-model="activeTab">
      <el-tab-pane label="站内信" name="messages">
        <el-table :data="messageList" style="width: 100%">
          <el-table-column prop="title" label="标题" />
          <el-table-column prop="message_type" label="类型" />
          <el-table-column prop="created_at" label="时间" />
          <el-table-column label="状态">
            <template #default="scope">
              <el-tag :type="scope.row.is_read ? 'info' : 'danger'">
                {{ scope.row.is_read ? '已读' : '未读' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作">
            <template #default="scope">
              <el-button size="small" @click="viewMessage(scope.row)">查看</el-button>
              <el-button 
                v-if="!scope.row.is_read" 
                size="small" 
                type="primary"
                @click="markAsRead(scope.row.id)"
              >
                标记已读
              </el-button>
            </template>
          </el-table-column>
        </el-table>
        
        <div style="margin-top: 20px;">
          <el-button @click="markAllAsRead">全部标记为已读</el-button>
        </div>
      </el-tab-pane>
      
      <el-tab-pane label="系统公告" name="announcements">
        <el-table :data="announcementList" style="width: 100%">
          <el-table-column prop="title" label="标题" />
          <el-table-column prop="announcement_type" label="类型" />
          <el-table-column prop="priority" label="优先级" />
          <el-table-column prop="publish_at" label="发布时间" />
          <el-table-column label="操作">
            <template #default="scope">
              <el-button size="small" @click="viewAnnouncement(scope.row)">查看</el-button>
            </template>
          </el-table-column>
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
import { ref, onMounted } from 'vue'
import { Bell } from '@element-plus/icons-vue'
import api from '../api'

export default {
  name: 'MessageCenter',
  components: {
    Bell
  },
  setup() {
    const showMessageDialog = ref(false)
    const showMessageDetail = ref(false)
    const activeTab = ref('messages')
    const unreadCount = ref(0)
    const messageList = ref([])
    const announcementList = ref([])
    const currentMessage = ref(null)
    
    const loadMessages = async () => {
      try {
        const response = await api.admin.getMessages()
        messageList.value = response.data.data.results || []
        unreadCount.value = response.data.data.unread_count || 0
      } catch (error) {
        console.error('加载消息失败:', error)
      }
    }
    
    const loadAnnouncements = async () => {
      try {
        const response = await api.admin.getAnnouncements()
        announcementList.value = response.data.data || []
      } catch (error) {
        console.error('加载公告失败:', error)
      }
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
    
    onMounted(() => {
      loadMessages()
      loadAnnouncements()
      // 定时刷新未读数量
      setInterval(() => {
        loadMessages()
      }, 60000) // 每分钟刷新一次
    })
    
    return {
      showMessageDialog,
      showMessageDetail,
      activeTab,
      unreadCount,
      messageList,
      announcementList,
      currentMessage,
      viewMessage,
      markAsRead,
      markAllAsRead,
      viewAnnouncement
    }
  }
}
</script>

<style scoped>
.message-badge {
  margin-right: 20px;
}
</style>

