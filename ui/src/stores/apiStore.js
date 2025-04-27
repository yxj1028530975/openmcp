import { defineStore } from 'pinia'
import axios from 'axios'

export const useApiStore = defineStore('api', {
  state: () => ({
    apis: [],
    categories: [],
    activeApiData: null,
    isLoading: false,
    error: null,
    lastStatus: null,
    lastStatusText: null
  }),
  
  getters: {
    getApisByCategory: (state) => (category) => {
      return state.apis.filter(api => api.category === category)
    },
    getApiById: (state) => (id) => {
      return state.apis.find(api => api.id === id)
    },
    getAllApis: (state) => state.apis
  },
  
  actions: {
    async fetchApis() {
      this.isLoading = true
      this.error = null
      this.lastStatus = null
      this.lastStatusText = null
      
      try {
        // 从后端获取API列表
        const response = await axios.get('/api/api-registry/apis')
        this.apis = response.data.apis || []
        
        // 保存状态码
        this.lastStatus = response.status
        this.lastStatusText = response.statusText
        
        // 从API数据中提取所有唯一的类别
        const categorySet = new Set(this.apis.map(api => api.category))
        this.categories = [...categorySet]
        
        return this.apis
      } catch (error) {
        this.error = error.message || '获取API列表失败'
        // 保存错误状态码
        if (error.response) {
          this.lastStatus = error.response.status
          this.lastStatusText = error.response.statusText
        }
        console.error('Error fetching APIs:', error)
        return []
      } finally {
        this.isLoading = false
      }
    },
    
    async fetchApiData(apiEndpoint) {
      this.isLoading = true
      this.error = null
      this.lastStatus = null
      this.lastStatusText = null
      
      try {
        const response = await axios.get(`/api${apiEndpoint}`)
        this.activeApiData = response.data
        
        // 保存状态码
        this.lastStatus = response.status
        this.lastStatusText = response.statusText
        
        return response.data
      } catch (error) {
        this.error = error.message || '获取数据失败'
        // 保存错误状态码
        if (error.response) {
          this.lastStatus = error.response.status
          this.lastStatusText = error.response.statusText
        }
        console.error('Error fetching API data:', error)
        throw error
      } finally {
        this.isLoading = false
      }
    },
    
    async sendPostRequest(apiEndpoint, data) {
      this.isLoading = true
      this.error = null
      this.lastStatus = null
      this.lastStatusText = null
      
      try {
        console.log(`发送POST请求到 /api${apiEndpoint}，数据:`, JSON.stringify(data, null, 2))
        
        // 检查请求数据格式
        if (Object.keys(data).length === 0) {
          console.error('警告: 发送空对象作为POST请求数据')
        }
        
        // 发送请求
        const response = await axios.post(`/api${apiEndpoint}`, data)
        
        console.log(`POST请求成功，状态码: ${response.status}，响应数据:`, response.data)
        this.activeApiData = response.data
        
        // 保存状态码
        this.lastStatus = response.status
        this.lastStatusText = response.statusText
        
        return response.data
      } catch (error) {
        this.error = error.message || '发送POST请求失败'
        // 保存错误状态码
        if (error.response) {
          this.lastStatus = error.response.status
          this.lastStatusText = error.response.statusText
          console.error(`POST请求错误 (${error.response.status}):`, error.response.data)
          console.error('请求路径:', apiEndpoint)
          console.error('请求数据:', data)
        } else {
          console.error('POST请求网络错误:', error.message)
        }
        console.error('完整错误信息:', error)
        throw error
      } finally {
        this.isLoading = false
      }
    },
    
    clearActiveApiData() {
      this.activeApiData = null
      this.lastStatus = null
      this.lastStatusText = null
    }
  }
}) 