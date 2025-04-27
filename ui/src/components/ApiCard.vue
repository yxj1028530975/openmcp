<template>
  <div class="card group hover:border-blue-500" :class="{ 'border-2 border-blue-500': isActive, 'border border-transparent': !isActive }">
    <div class="card-title">{{ api.name }}</div>
    <div class="card-desc">{{ api.description }}</div>
    <div class="flex justify-between items-center">
      <span class="text-xs text-gray-500">{{ api.endpoints.length }} 个接口</span>
      <router-link :to="`/api/${api.id}`" class="btn btn-primary text-sm">查看详情</router-link>
    </div>
  </div>
</template>

<script setup>
import { defineProps, computed } from 'vue'
import { useRoute } from 'vue-router'

const props = defineProps({
  api: {
    type: Object,
    required: true
  }
})

const route = useRoute()
const isActive = computed(() => route.params.apiName === props.api.id)
</script> 