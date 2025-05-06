<template>
  <div class="container mx-auto px-4 py-8">
    <div class="py-16 bg-gradient-to-r from-blue-600 to-purple-600 rounded-xl text-white mb-10">
      <div class="text-center">
        <h1 class="text-4xl font-bold mb-4">OpenMCP 项目</h1>
        <p class="text-xl max-w-3xl mx-auto">一个强大的开源MCP项目，提供统一接口配置和服务，可无缝集成热门榜单数据等多种服务。</p>
        <div class="mt-8 flex justify-center gap-4">
          <router-link to="/api-registry" class="inline-block px-6 py-3 bg-white text-blue-600 font-medium rounded-lg hover:bg-blue-50 transition">
            浏览MCP文档
          </router-link>
          <a href="http://127.0.0.1:8000/docs" target="_blank" class="inline-block px-6 py-3 bg-transparent border border-white text-white font-medium rounded-lg hover:bg-white/10 transition">
            Swagger UI
          </a>
        </div>
      </div>
    </div>
    
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">
      <div class="bg-white p-6 rounded-lg shadow-md">
        <div class="flex items-center mb-4">
          <div class="bg-blue-100 p-3 rounded-full">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
          </div>
          <h2 class="ml-4 text-xl font-bold">简单配置</h2>
        </div>
        <p class="text-gray-600">通过简单的JSON配置文件，轻松设置MCP服务，实现多服务间的无缝整合。</p>
      </div>
      
      <div class="bg-white p-6 rounded-lg shadow-md">
        <div class="flex items-center mb-4">
          <div class="bg-green-100 p-3 rounded-full">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <h2 class="ml-4 text-xl font-bold">统一接口</h2>
        </div>
        <p class="text-gray-600">将多种数据源统一到一个接口下，包括知乎、微博、B站等多平台热榜数据。</p>
      </div>
      
      <div class="bg-white p-6 rounded-lg shadow-md">
        <div class="flex items-center mb-4">
          <div class="bg-purple-100 p-3 rounded-full">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-purple-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z" />
            </svg>
          </div>
          <h2 class="ml-4 text-xl font-bold">可扩展性</h2>
        </div>
        <p class="text-gray-600">易于扩展的架构设计，可以方便地集成新的服务和数据源到MCP系统中。</p>
      </div>
    </div>
    
    <!-- MCP配置示例 -->
    <div class="bg-white rounded-lg shadow-md p-6 mb-10">
      <h2 class="text-2xl font-bold mb-4">MCP配置示例</h2>
      <div class="bg-gray-50 p-4 rounded-lg">
        <pre class="text-sm overflow-auto">{
  "mcpServers": {
      "openmcp-sse": {
        "url": "http://127.0.0.1:8000/mcp",
        "name": "openmcp-sse"
      }
  }
}</pre>
      </div>
      <p class="mt-4 text-gray-600">
        配置文件应放置在 <code>~/.cursor/mcp.json</code> 位置，MCP服务器将自动加载此配置。
      </p>
    </div>
    
    <!-- 服务状态 -->
    <div class="bg-white rounded-lg shadow-md p-6 mb-10">
      <h2 class="text-2xl font-bold mb-4">服务状态</h2>
      <div class="flex items-center">
        <div class="flex items-center mr-6">
          <div class="w-3 h-3 rounded-full bg-green-500 mr-2"></div>
          <span>MCP服务</span>
        </div>
        <div v-if="isLoading" class="text-sm text-gray-500">检查中...</div>
        <div v-else-if="apiStatus" class="flex items-center">
          <span class="text-green-600 font-medium">正常运行中</span>
          <span class="ml-2 text-sm text-gray-500">{{ apiCount }} 个服务可用</span>
        </div>
        <div v-else class="text-red-600 font-medium">
          <span>服务异常</span>
          <button @click="checkApiStatus" class="ml-2 text-sm text-blue-600">重试</button>
        </div>
      </div>
    </div>
    
    <!-- 最近更新 -->
    <div class="bg-white rounded-lg shadow-md p-6">
      <h2 class="text-2xl font-bold mb-4">最近更新</h2>
      <div class="space-y-4">
        <div class="flex">
          <div class="w-16 text-sm text-gray-500">2023-06-15</div>
          <div>
            <span class="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded">新增</span>
            <span class="ml-2">添加MCP配置文档和示例</span>
          </div>
        </div>
        <div class="flex">
          <div class="w-16 text-sm text-gray-500">2023-05-20</div>
          <div>
            <span class="bg-green-100 text-green-800 text-xs px-2 py-1 rounded">优化</span>
            <span class="ml-2">改进MCP服务注册和发现机制</span>
          </div>
        </div>
        <div class="flex">
          <div class="w-16 text-sm text-gray-500">2023-05-01</div>
          <div>
            <span class="bg-purple-100 text-purple-800 text-xs px-2 py-1 rounded">发布</span>
            <span class="ml-2">OpenMCP 1.0版本发布</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'

const isLoading = ref(false)
const apiStatus = ref(false)
const apiCount = ref(0)

const checkApiStatus = async () => {
  isLoading.value = true
  
  try {
    const response = await fetch('http://127.0.0.1:8000/mcp')
    
    if (response.ok) {
      apiStatus.value = true
      apiCount.value = 1 // MCP服务数量
    } else {
      apiStatus.value = false
    }
  } catch (err) {
    console.error('Error checking MCP status:', err)
    apiStatus.value = false
  } finally {
    isLoading.value = false
  }
}

onMounted(checkApiStatus)
</script> 