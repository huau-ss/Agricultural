import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../views/Dashboard.vue'
import MarketPrice from '../views/MarketPrice.vue'
import Forecast from '../views/Forecast.vue'
import Decision from '../views/Decision.vue'
import Trade from '../views/Trade.vue'
import Admin from '../views/Admin.vue'

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: Dashboard
  },
  {
    path: '/market',
    name: 'MarketPrice',
    component: MarketPrice
  },
  {
    path: '/forecast',
    name: 'Forecast',
    component: Forecast
  },
  {
    path: '/decision',
    name: 'Decision',
    component: Decision
  },
  {
    path: '/trade',
    name: 'Trade',
    component: Trade
  },
  {
    path: '/admin',
    name: 'Admin',
    component: Admin
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router

