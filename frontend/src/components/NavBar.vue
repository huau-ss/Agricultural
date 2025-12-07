<template>
  <el-menu
    mode="horizontal"
    :default-active="activeIndex"
    router
    class="navbar"
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
</template>

<script>
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import { HomeFilled, TrendCharts, DataAnalysis, Document, ShoppingCart, Setting } from '@element-plus/icons-vue'

export default {
  name: 'NavBar',
  components: {
    HomeFilled,
    TrendCharts,
    DataAnalysis,
    Document,
    ShoppingCart,
    Setting
  },
  setup() {
    const route = useRoute()
    const activeIndex = computed(() => route.path)
    
    return {
      activeIndex
    }
  }
}
</script>

<style scoped>
.navbar {
  background-color: #409EFF;
  border-bottom: none;
}

.navbar .el-menu-item {
  color: #fff;
}

.navbar .el-menu-item:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.navbar .el-menu-item.is-active {
  background-color: rgba(255, 255, 255, 0.2);
  color: #fff;
}
</style>

