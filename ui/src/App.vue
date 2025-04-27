<template>
  <div class="min-h-screen flex flex-col">
    <header class="bg-white shadow-md">
      <div class="container mx-auto px-4 py-4">
        <div class="flex justify-between items-center">
          <router-link to="/" class="text-2xl font-bold text-blue-600">OpenMCP API</router-link>
          <nav class="hidden md:flex space-x-6">
            <router-link to="/" class="text-gray-700 hover:text-blue-600">首页</router-link>
            <a href="https://github.com/yourusername/openmcp" target="_blank" class="text-gray-700 hover:text-blue-600">GitHub</a>
          </nav>
        </div>
      </div>
    </header>
    
    <main class="flex-grow">
      <div class="container mx-auto px-4 py-8">
        <router-view />
      </div>
    </main>
    
    <footer class="bg-gray-800 text-white py-8">
      <div class="container mx-auto px-4">
        <div class="flex flex-col md:flex-row justify-between">
          <div class="mb-6 md:mb-0">
            <h3 class="text-xl font-bold mb-4">OpenMCP API</h3>
            <p class="text-gray-400">一个开源的API集合</p>
          </div>
          <div>
            <h4 class="text-lg font-semibold mb-2">链接</h4>
            <ul class="space-y-2">
              <li><a href="https://github.com/yourusername/openmcp" class="text-gray-400 hover:text-white">GitHub</a></li>
              <li><a href="https://github.com/yourusername/openmcp/issues" class="text-gray-400 hover:text-white">问题反馈</a></li>
            </ul>
          </div>
        </div>
        <div class="border-t border-gray-700 mt-8 pt-6 text-center text-gray-500">
          <p>© {{ new Date().getFullYear() }} OpenMCP API. 保留所有权利。</p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
// App.vue不需要额外的脚本逻辑
</script> 