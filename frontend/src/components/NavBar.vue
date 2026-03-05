<template>
  <div class="navbar-container">
    <div class="navbar-content">
      <div class="navbar-logo">
        <el-icon class="logo-icon"><TrendCharts /></el-icon>
        <span class="logo-text">农产品分析平台</span>
      </div>
      
      <el-menu
        mode="horizontal"
        :default-active="activeIndex"
        router
        class="navbar-menu"
      >
        <el-menu-item index="/">
          <el-icon><HomeFilled /></el-icon>
          <span>首页</span>
        </el-menu-item>
        <el-menu-item index="/market">
          <el-icon><TrendCharts /></el-icon>
          <span>市场行情</span>
        </el-menu-item>
        <el-menu-item index="/forecast">
          <el-icon><DataAnalysis /></el-icon>
          <span>价格预测</span>
        </el-menu-item>
        <el-menu-item index="/decision">
          <el-icon><Document /></el-icon>
          <span>决策辅助</span>
        </el-menu-item>
        <el-menu-item index="/trade">
          <el-icon><ShoppingCart /></el-icon>
          <span>供需对接</span>
        </el-menu-item>
        <el-menu-item index="/admin">
          <el-icon><Setting /></el-icon>
          <span>系统管理</span>
        </el-menu-item>
      </el-menu>
      
      <div class="navbar-right">
        <el-badge :value="unreadCount" :hidden="unreadCount === 0" class="message-badge">
          <el-button 
            :icon="Bell" 
            circle 
            @click="showMessageCenter = true"
            class="message-btn"
          />
        </el-badge>
      </div>
    </div>
    
    <MessageCenter v-model="showMessageCenter" />
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { 
  HomeFilled, 
  TrendCharts, 
  DataAnalysis, 
  Document, 
  ShoppingCart, 
  Setting,
  Bell
} from '@element-plus/icons-vue'
import MessageCenter from './MessageCenter.vue'
import api from '../api'

export default {
  name: 'NavBar',
  components: {
    HomeFilled,
    TrendCharts,
    DataAnalysis,
    Document,
    ShoppingCart,
    Setting,
    Bell,
    MessageCenter
  },
  setup() {
    const route = useRoute()
    const activeIndex = computed(() => route.path)
    const showMessageCenter = ref(false)
    const unreadCount = ref(0)
    
    const loadUnreadCount = async () => {
      try {
        const response = await api.admin.getUnreadCount()
        const resData = response.data?.data || response.data || {}
        unreadCount.value = resData.count || resData.unread_count || 0
      } catch (error) {
        console.error('获取未读消息数失败:', error)
      }
    }
    
    onMounted(() => {
      loadUnreadCount()
      // 每30秒刷新一次未读消息数
      setInterval(loadUnreadCount, 30000)
    })
    
    return {
      activeIndex,
      showMessageCenter,
      unreadCount,
      Bell
    }
  }
}
</script>

<style scoped>
.navbar-container {
  height: 64px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.navbar-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 100%;
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 24px;
}

.navbar-logo {
  display: flex;
  align-items: center;
  color: #fff;
  font-size: 20px;
  font-weight: bold;
  margin-right: 40px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.navbar-logo:hover {
  transform: scale(1.05);
}

.logo-icon {
  font-size: 28px;
  margin-right: 8px;
  color: #ffd700;
}

.logo-text {
  background: linear-gradient(45deg, #fff, #ffd700);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.navbar-menu {
  flex: 1;
  background: transparent;
  border-bottom: none;
}

.navbar-menu .el-menu-item {
  color: rgba(255, 255, 255, 0.9);
  border-bottom: 3px solid transparent;
  transition: all 0.3s ease;
  margin: 0 4px;
  border-radius: 4px 4px 0 0;
}

.navbar-menu .el-menu-item:hover {
  background-color: rgba(255, 255, 255, 0.15);
  color: #fff;
}

.navbar-menu .el-menu-item.is-active {
  background-color: rgba(255, 255, 255, 0.2);
  color: #fff;
  border-bottom-color: #ffd700;
}

.navbar-right {
  display: flex;
  align-items: center;
  margin-left: 20px;
}

.message-badge {
  cursor: pointer;
}

.message-btn {
  background: rgba(255, 255, 255, 0.2);
  border: none;
  color: #fff;
  transition: all 0.3s ease;
}

.message-btn:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: scale(1.1);
}
</style>

