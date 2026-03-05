import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
api.interceptors.request.use(
  config => {
    // 可以在这里添加token等
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  response => {
    // 统一处理后端返回的 {code, msg, data} 格式
    const res = response.data
    if (res.code !== undefined) {
      // 后端使用统一响应格式
      if (res.code === 200) {
        return response // 成功，直接返回
      } else {
        // 业务错误
        const error = new Error(res.msg || '请求失败')
        error.code = res.code
        error.data = res.data
        return Promise.reject(error)
      }
    }
    // 兼容其他格式
    return response
  },
  error => {
    console.error('API错误:', error)
    // 处理HTTP错误
    if (error.response) {
      const res = error.response.data
      if (res && res.code !== undefined) {
        error.code = res.code
        error.message = res.msg || error.message
      }
    }
    return Promise.reject(error)
  }
)

export default {
  // 市场行情API
  market: {
    getPrices: (params) => api.get('/market/prices/', { params }),
    getDashboard: () => api.get('/market/prices/dashboard/'),
    getPriceComparison: (params) => api.get('/market/prices/price_comparison/', { params }),
    getStatistics: (params) => api.get('/market/statistics/', { params })
  },
  
  // 预测API
  forecast: {
    getModels: (params) => api.get('/forecast/models/', { params }),
    getResults: (params) => api.get('/forecast/results/', { params }),
    trainModel: (id) => api.post(`/forecast/models/${id}/train/`),
    predict: (id, data) => api.post(`/forecast/models/${id}/predict/`, data),
    getAccuracy: (params) => api.get('/forecast/results/accuracy_analysis/', { params })
  },
  
  // 决策API
  decision: {
    getSimulations: (params) => api.get('/decision/profit-simulations/', { params }),
    createSimulation: (data) => api.post('/decision/profit-simulations/', data),
    batchSimulate: (data) => api.post('/decision/profit-simulations/batch_simulate/', data),
    getAdvices: (params) => api.get('/decision/advices/', { params }),
    generateAdvice: (data) => api.post('/decision/advices/generate_advice/', data)
  },
  
  // 交易API
  trade: {
    getSupplies: (params) => api.get('/trade/supplies/', { params }),
    getDemands: (params) => api.get('/trade/demands/', { params }),
    getMatches: (params) => api.get('/trade/matches/', { params }),
    createSupply: (data) => api.post('/trade/supplies/', data),
    createDemand: (data) => api.post('/trade/demands/', data),
    match: (data) => api.post('/trade/matches/match/', data)
  },
  
  // 管理API
  admin: {
    getLogs: (params) => api.get('/admincore/logs/', { params }),
    getAlerts: (params) => api.get('/admincore/alerts/', { params }),
    getAlertRules: (params) => api.get('/admincore/alert-rules/', { params }),
    createAlertRule: (data) => api.post('/admincore/alert-rules/', data),
    updateAlertRule: (id, data) => api.put(`/admincore/alert-rules/${id}/`, data),
    deleteAlertRule: (id) => api.delete(`/admincore/alert-rules/${id}/`),
    getMessages: (params) => api.get('/admincore/messages/', { params }),
    getUnreadCount: () => api.get('/admincore/messages/unread_count/'),
    markMessageRead: (id) => api.post(`/admincore/messages/${id}/mark_read/`),
    markAllMessagesRead: () => api.post('/admincore/messages/mark_all_read/'),
    getAnnouncements: (params) => api.get('/admincore/announcements/', { params }),
    getAlertSubscriptions: (params) => api.get('/admincore/alert-subscriptions/', { params }),
    createAlertSubscription: (data) => api.post('/admincore/alert-subscriptions/', data),
    updateAlertSubscription: (id, data) => api.put(`/admincore/alert-subscriptions/${id}/`, data),
    deleteAlertSubscription: (id) => api.delete(`/admincore/alert-subscriptions/${id}/`)
  }
}

