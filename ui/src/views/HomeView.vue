<template>
  <div>
    <div class="py-10 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg text-white mb-10">
      <div class="text-center">
        <h1 class="text-4xl font-bold mb-4">OpenMCP API</h1>
        <p class="text-xl max-w-3xl mx-auto">一个强大的开源API集合，提供多种服务接口，包括天气信息和热门榜单数据。</p>
      </div>
    </div>
    
    <div v-if="isLoading" class="text-center py-10">
      <p class="text-xl">加载中...</p>
    </div>
    
    <div v-else-if="error" class="text-center py-10 bg-red-50 rounded-lg border border-red-200">
      <p class="text-xl text-red-600">{{ error }}</p>
      <button @click="loadApis" class="mt-4 btn btn-primary">重试</button>
    </div>
    
    <template v-else>
      <div v-if="categories.length === 0" class="text-center py-10">
        <p class="text-xl text-gray-500">暂无API数据</p>
      </div>
      
      <div v-for="category in categories" :key="category" class="api-category">
        <h2 class="api-category-title">{{ category }}</h2>
        <div class="api-cards-grid">
          <ApiCard 
            v-for="api in getApisByCategory(category)" 
            :key="api.id" 
            :api="api" 
          />
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useApiStore } from '@/stores/apiStore'
import ApiCard from '@/components/ApiCard.vue'

const apiStore = useApiStore()
const categories = computed(() => apiStore.categories)
const isLoading = ref(false)
const error = ref(null)

const getApisByCategory = (category) => apiStore.getApisByCategory(category)

const loadApis = async () => {
  isLoading.value = true
  error.value = null
  
  try {
    await apiStore.fetchApis()
  } catch (err) {
    error.value = '无法加载API数据，请稍后重试'
    console.error('Error loading APIs:', err)
  } finally {
    isLoading.value = false
  }
}

onMounted(loadApis)
</script> 