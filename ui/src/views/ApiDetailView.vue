<template>
  <div>
    <div v-if="isLoading" class="text-center py-10">
      <p class="text-xl">加载中...</p>
    </div>
    
    <div v-else-if="error" class="text-center py-10 bg-red-50 rounded-lg border border-red-200">
      <p class="text-xl text-red-600">{{ error }}</p>
      <router-link to="/" class="mt-4 inline-block btn btn-primary">返回首页</router-link>
    </div>
    
    <template v-else-if="api">
      <div class="mb-6">
        <router-link :to="{ name: 'category', params: { category: api.category } }" class="text-blue-600 hover:underline flex items-center">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
          </svg>
          返回 {{ api.category }}
        </router-link>
      </div>
      
      <div class="bg-white rounded-lg shadow-md p-6 mb-8">
        <h1 class="text-3xl font-bold mb-2">{{ api.name }}</h1>
        <p class="text-gray-600 mb-4">{{ api.description }}</p>
        <div class="flex flex-wrap gap-2 mb-4">
          <span class="px-3 py-1 rounded-full bg-blue-100 text-blue-800 text-sm">{{ api.category }}</span>
          <span class="px-3 py-1 rounded-full bg-gray-100 text-gray-800 text-sm">{{ api.endpoints.length }} 个端点</span>
        </div>
      </div>
      
      <h2 class="text-2xl font-bold mb-4">API 端点</h2>
      
      <div class="space-y-6">
        <div v-for="(endpoint, index) in api.endpoints" :key="index" class="bg-white rounded-lg shadow-md p-6">
          <div class="flex justify-between items-start mb-4">
            <h3 class="text-xl font-semibold">{{ endpoint.name }}</h3>
            <span :class="`px-2 py-1 rounded text-white text-xs font-medium ${getMethodColor(endpoint.method)}`">
              {{ endpoint.method }}
            </span>
          </div>
          
          <p class="text-gray-600 mb-4">{{ endpoint.description }}</p>
          
          <div class="mb-4">
            <div class="text-sm font-medium text-gray-700 mb-2">路径：</div>
            <div class="bg-gray-100 p-3 rounded-md font-mono text-sm">{{ endpoint.path }}</div>
          </div>
          
          <div v-if="endpoint.params && endpoint.params.length > 0">
            <div class="text-sm font-medium text-gray-700 mb-2">参数：</div>
            <div class="overflow-x-auto">
              <table class="w-full border-collapse">
                <thead>
                  <tr class="bg-gray-100">
                    <th class="p-2 text-left text-sm">名称</th>
                    <th class="p-2 text-left text-sm">类型</th>
                    <th class="p-2 text-left text-sm">描述</th>
                    <th class="p-2 text-left text-sm" v-if="endpoint.method === 'POST'">值</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="param in endpoint.params" :key="param.name" class="border-t">
                    <td class="p-2 text-sm font-mono">{{ param.name }}</td>
                    <td class="p-2 text-sm">{{ param.type }}</td>
                    <td class="p-2 text-sm">{{ param.description }}</td>
                    <td class="p-2 text-sm" v-if="endpoint.method === 'POST'">
                      <input 
                        v-model="paramValues[endpoint.path + param.name]" 
                        :placeholder="`输入${param.name}`" 
                        class="border p-1 rounded w-full"
                      />
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
          
          <div class="mt-6 flex gap-2">
            <button 
              @click="tryEndpoint(endpoint)" 
              class="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition-colors"
              :disabled="endpointLoading === endpoint"
            >
              <span v-if="endpointLoading === endpoint">测试中...</span>
              <span v-else>测试接口</span>
            </button>
            <button 
              v-if="activeEndpoint === endpoint && apiStore.activeApiData"
              @click="toggleResponse(endpoint)"
              class="bg-gray-600 text-white px-4 py-2 rounded-md hover:bg-gray-700 transition-colors"
            >
              {{ expandedResponses[endpoint.path] ? '折叠响应' : '展开响应' }}
            </button>
          </div>
          
          <div v-if="endpointLoading === endpoint" class="mt-4 text-gray-600">
            请求中...
          </div>
          
          <div v-if="endpointErrors[endpoint.path]" class="mt-4 p-3 bg-red-50 border border-red-200 rounded-md">
            <div class="font-medium text-red-600 mb-1">请求失败：</div>
            <div class="text-red-700">{{ endpointErrors[endpoint.path] }}</div>
            <div v-if="responseErrors[endpoint.path]" class="mt-2 text-sm">
              <div class="font-medium">服务器详细错误：</div>
              <pre class="bg-red-100 p-2 rounded mt-1 overflow-x-auto">{{ JSON.stringify(responseErrors[endpoint.path], null, 2) }}</pre>
            </div>
          </div>
          
          <div v-if="activeEndpoint === endpoint && apiStore.activeApiData" class="mt-4">
            <div class="text-sm font-medium text-gray-700 mb-2">响应：</div>
            <div class="bg-gray-100 p-3 rounded-md overflow-hidden">
              <div class="flex justify-between items-center mb-2">
                <div class="text-xs text-gray-500">状态码: {{ responseStatus[endpoint.path] || 200 }} {{ responseStatusText[endpoint.path] || 'OK' }}</div>
                <button 
                  @click="copyResponse()" 
                  class="text-xs text-blue-600 hover:text-blue-800"
                >
                  复制
                </button>
              </div>
              <pre 
                v-if="expandedResponses[endpoint.path]" 
                class="overflow-x-auto text-sm"
                style="max-height: 400px; overflow-y: auto;"
              >{{ JSON.stringify(apiStore.activeApiData, null, 2) }}</pre>
              <div v-else class="text-sm cursor-pointer hover:bg-gray-200 p-2 rounded" @click="expandedResponses[endpoint.path] = true">
                点击展开查看完整响应 ({{ getResponseSize(apiStore.activeApiData) }})
              </div>
            </div>
          </div>
        </div>
      </div>
    </template>
    
    <div v-else class="text-center py-10">
      <p class="text-xl text-gray-500">未找到该API</p>
      <router-link to="/" class="mt-4 inline-block btn btn-primary">返回首页</router-link>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, onMounted, watch, reactive } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useApiStore } from '@/stores/apiStore'

const route = useRoute()
const router = useRouter()
const apiStore = useApiStore()
const activeEndpoint = ref(null)
const isLoading = ref(false)
const error = ref(null)
const endpointLoading = ref(null)
const endpointErrors = reactive({}) // 存储每个端点的错误信息
const responseErrors = reactive({}) // 存储服务器返回的详细错误
const responseStatus = reactive({}) // 存储响应状态码
const responseStatusText = reactive({}) // 存储响应状态文本
const paramValues = reactive({}) // 存储POST请求的参数值
const expandedResponses = reactive({}) // 存储每个端点响应是否展开

const api = computed(() => apiStore.getApiById(route.params.apiName))

// 根据HTTP方法返回不同的颜色类
const getMethodColor = (method) => {
  const colors = {
    'GET': 'bg-green-600',
    'POST': 'bg-blue-600',
    'PUT': 'bg-yellow-600',
    'DELETE': 'bg-red-600',
    'PATCH': 'bg-purple-600'
  }
  return colors[method] || 'bg-gray-600'
}

// 计算响应数据的大小
const getResponseSize = (data) => {
  const size = JSON.stringify(data).length
  if (size < 1024) {
    return `${size} 字节`
  } else {
    return `${(size / 1024).toFixed(2)} KB`
  }
}

// 切换响应的展开/折叠状态
const toggleResponse = (endpoint) => {
  expandedResponses[endpoint.path] = !expandedResponses[endpoint.path]
}

// 复制响应到剪贴板
const copyResponse = () => {
  const responseText = JSON.stringify(apiStore.activeApiData, null, 2)
  navigator.clipboard.writeText(responseText)
    .then(() => {
      alert('已复制到剪贴板')
    })
    .catch(err => {
      console.error('复制失败:', err)
    })
}

// 确保API数据已加载
const checkApiData = async () => {
  isLoading.value = true
  error.value = null
  
  try {
    // 如果API列表为空，尝试加载
    if (apiStore.apis.length === 0) {
      await apiStore.fetchApis()
    }
    
    // 如果加载后仍然找不到当前API，可能是无效ID
    if (!api.value) {
      error.value = '未找到该API'
    }
  } catch (err) {
    error.value = '加载API数据失败'
    console.error('Error loading API data:', err)
  } finally {
    isLoading.value = false
  }
}

// 测试端点
const tryEndpoint = async (endpoint) => {
  activeEndpoint.value = endpoint
  endpointLoading.value = endpoint
  delete endpointErrors[endpoint.path] // 清除之前的错误
  delete responseErrors[endpoint.path] // 清除之前的错误详情
  delete responseStatus[endpoint.path] // 清除之前的状态码
  delete responseStatusText[endpoint.path] // 清除之前的状态文本
  apiStore.clearActiveApiData()
  
  try {
    // 根据HTTP方法使用不同的请求方式
    if (endpoint.method === 'POST') {
      // 构建请求参数
      const requestData = {}
      
      // 特殊处理天气API的城市名查询
      if (endpoint.path === '/weather/get_weather/cityname') {
        // 从输入中获取城市名
        const cityKey = endpoint.path + 'cityname'
        if (paramValues[cityKey] && paramValues[cityKey].trim() !== '') {
          requestData.cityname = paramValues[cityKey].trim()
          console.log('天气API请求数据:', requestData)
        } else {
          throw new Error('城市名不能为空')
        }
      } 
      // 通用参数处理
      else if (endpoint.params && endpoint.params.length > 0) {
        endpoint.params.forEach(param => {
          const key = endpoint.path + param.name
          if (paramValues[key] !== undefined && paramValues[key] !== '') {
            // 根据参数类型转换值
            if (param.type === 'number') {
              requestData[param.name] = Number(paramValues[key])
            } else {
              requestData[param.name] = paramValues[key]
            }
          }
        })
      }
      
      console.log('POST请求数据:', requestData)
      
      // 发起POST请求
      const response = await apiStore.sendPostRequest(endpoint.path, requestData)
      responseStatus[endpoint.path] = apiStore.lastStatus
      responseStatusText[endpoint.path] = apiStore.lastStatusText
    } else {
      // 对于GET请求继续使用现有方法
      const response = await apiStore.fetchApiData(endpoint.path)
      responseStatus[endpoint.path] = apiStore.lastStatus
      responseStatusText[endpoint.path] = apiStore.lastStatusText
    }
    
    // 默认展开响应
    expandedResponses[endpoint.path] = true
  } catch (err) {
    endpointErrors[endpoint.path] = err.message || '请求失败，请检查网络连接'
    console.error('Error fetching endpoint data:', err)
    
    // 保存服务器返回的错误详情
    if (err.response && err.response.data) {
      responseErrors[endpoint.path] = err.response.data
      responseStatus[endpoint.path] = err.response.status
      responseStatusText[endpoint.path] = err.response.statusText
    }
  } finally {
    endpointLoading.value = null
  }
}

// 当路由参数变化时重新检查
watch(() => route.params.apiName, checkApiData)

onMounted(checkApiData)
</script>

<style scoped>
/* 添加淡入淡出效果 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* 自定义滚动条样式 */
pre::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

pre::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

pre::-webkit-scrollbar-thumb {
  background: #ddd;
  border-radius: 4px;
}

pre::-webkit-scrollbar-thumb:hover {
  background: #ccc;
}
</style> 