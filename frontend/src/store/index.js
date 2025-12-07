import { createStore } from 'vuex'
import api from '../api'

export default createStore({
  state: {
    user: null,
    marketData: [],
    forecastData: []
  },
  mutations: {
    SET_USER(state, user) {
      state.user = user
    },
    SET_MARKET_DATA(state, data) {
      state.marketData = data
    },
    SET_FORECAST_DATA(state, data) {
      state.forecastData = data
    }
  },
  actions: {
    async fetchMarketData({ commit }, params) {
      try {
        const response = await api.market.getPrices(params)
        commit('SET_MARKET_DATA', response.data.data)
        return response.data
      } catch (error) {
        console.error('获取市场数据失败:', error)
        throw error
      }
    },
    async fetchForecastData({ commit }, params) {
      try {
        const response = await api.forecast.getResults(params)
        commit('SET_FORECAST_DATA', response.data.data)
        return response.data
      } catch (error) {
        console.error('获取预测数据失败:', error)
        throw error
      }
    }
  }
})

