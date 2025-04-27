<template>
  <div>
    <div class="mb-6">
      <router-link to="/" class="text-blue-600 hover:underline flex items-center">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
        </svg>
        返回首页
      </router-link>
    </div>
    
    <div v-if="isLoading" class="text-center py-10">
      <p class="text-xl">加载中...</p>
    </div>
    
    <div v-else-if="error" class="text-center py-10 bg-red-50 rounded-lg border border-red-200">
      <p class="text-xl text-red-600">{{ error }}</p>
      <router-link to="/" class="mt-4 inline-block btn btn-primary">返回首页</router-link>
    </div>
    
    <template v-else>
      <div v-if="category && apis.length > 0">
        <h1 class="api-category-title">{{ category }} API</h1>
        
        <div class="api-cards-grid">
          <ApiCard 
            v-for="api in apis" 
            :key="api.id" 
            :api="api" 
          />
        </div>
      </div>
      
      <div v-else class="text-center py-10">
        <p class="text-xl text-gray-500">未找到该分类或该分类下没有API</p>
        <router-link to="/" class="mt-4 inline-block btn btn-primary">返回首页</router-link>
      </div>
    </template>
  </div>
</template>

<script setup>
import { computed, ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useApiStore } from '@/stores/apiStore'
import ApiCard from '@/components/ApiCard.vue'

const route = useRoute()
const apiStore = useApiStore()
const isLoading = ref(false)
const error = ref(null)

const category = computed(() => route.params.category)
const apis = computed(() => apiStore.getApisByCategory(category.value))

// 确保API数据已加载
const loadCategoryData = async () => {
  isLoading.value = true
  error.value = null
  
  try {
    // 如果API列表为空，尝试加载
    if (apiStore.apis.length === 0) {
      await apiStore.fetchApis()
    }
  } catch (err) {
    error.value = '加载分类数据失败'
    console.error('Error loading category data:', err)
  } finally {
    isLoading.value = false
  }
}

// 当路由参数变化时重新加载
watch(() => route.params.category, loadCategoryData)

onMounted(loadCategoryData)
</script> 