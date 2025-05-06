<template>
  <div class="container mx-auto px-4 py-8">
    <h1 class="text-2xl font-bold mb-6">MCP 配置文档</h1>
    
    <div class="mb-8 bg-white rounded-lg shadow-md p-6">
      <h2 class="text-xl font-bold mb-4">什么是MCP？</h2>
      <p class="text-gray-700 mb-4">
        MCP (Managed Communications Protocol) 是一个开源项目，旨在提供统一的接口配置和服务管理方案。通过简单的配置，
        您可以将多种服务整合到一起，实现统一调用。目前，OpenMCP已支持多种热门平台的数据聚合。
      </p>
    </div>
    
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
      <!-- 配置方式 -->
      <div class="bg-white rounded-lg shadow-md p-6">
        <h2 class="text-xl font-bold mb-4">配置方式</h2>
        <p class="text-gray-700 mb-4">
          MCP采用JSON格式的配置文件，您需要在以下位置创建配置文件：
        </p>
        <div class="bg-gray-100 p-3 rounded mb-4">
          <code>~/.cursor/mcp.json</code>
        </div>
        <p class="text-gray-700">
          配置文件结构如下所示，您可以根据需要添加多个MCP服务器配置：
        </p>
      </div>
      
      <!-- 配置示例 -->
      <div class="bg-white rounded-lg shadow-md p-6">
        <h2 class="text-xl font-bold mb-4">配置示例</h2>
        <div class="bg-gray-100 p-3 rounded">
          <pre class="text-sm overflow-auto">{
  "mcpServers": {
    "openmcp-sse": {
      "url": "http://127.0.0.1:8000/mcp",
      "name": "openmcp-sse"
    },
    "custom-server": {
      "url": "http://example.com/mcp",
      "name": "my-custom-mcp"
    }
  }
}</pre>
        </div>
      </div>
    </div>
    
    <div class="bg-white rounded-lg shadow-md p-6 mb-8">
      <h2 class="text-xl font-bold mb-4">支持的服务类型</h2>
      
      <div class="overflow-hidden mb-6">
        <div class="flex border-b border-gray-200 font-medium text-gray-700 bg-gray-100">
          <div class="px-4 py-2 w-1/3">服务类别</div>
          <div class="px-4 py-2 flex-1">描述</div>
          <div class="px-4 py-2 w-1/6">状态</div>
        </div>
        
        <div v-for="(category, index) in serviceCategories" :key="index" 
          class="flex border-b border-gray-200 hover:bg-gray-50">
          <div class="px-4 py-3 w-1/3 font-medium">{{ category.name }}</div>
          <div class="px-4 py-3 flex-1 text-gray-700">{{ category.description }}</div>
          <div class="px-4 py-3 w-1/6">
            <span :class="{
              'px-2 py-1 rounded-md text-xs font-medium': true,
              'bg-green-100 text-green-800': category.status === '可用',
              'bg-yellow-100 text-yellow-800': category.status === '测试中',
              'bg-red-100 text-red-800': category.status === '维护中'
            }">
              {{ category.status }}
            </span>
          </div>
        </div>
      </div>
    </div>
    
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
      <!-- 接口描述 -->
      <div class="bg-white rounded-lg shadow-md p-6">
        <h2 class="text-xl font-bold mb-4">接口描述</h2>
        <p class="text-gray-700 mb-4">
          每个MCP服务提供统一的接口格式，基本格式如下：
        </p>
        <pre class="bg-gray-100 p-3 rounded text-sm mb-4">{
  "code": 200,  // 状态码
  "message": "Success", // 消息
  "data": [...] // 数据内容
}</pre>
        <p class="text-gray-700">
          所有MCP服务都遵循相同的响应格式，确保数据处理的一致性。
        </p>
      </div>
      
      <!-- 调用示例 -->
      <div class="bg-white rounded-lg shadow-md p-6">
        <h2 class="text-xl font-bold mb-4">调用示例</h2>
        <p class="text-gray-700 mb-2">简单的JS调用示例：</p>
        <pre class="bg-gray-100 p-3 rounded text-sm mb-4">// 获取热榜数据
async function getHotData(platform) {
  const response = await fetch(
    `http://127.0.0.1:8000/${platform}`
  );
  return await response.json();
}

// 调用示例
getHotData('zhihu').then(data => {
  console.log(data);
});</pre>
      </div>
    </div>
    
    <div class="bg-white rounded-lg shadow-md p-6">
      <h2 class="text-xl font-bold mb-4">常见问题</h2>
      
      <div class="space-y-4">
        <div v-for="(faq, index) in faqs" :key="index" class="border-b border-gray-200 pb-4 last:border-0">
          <h3 class="text-lg font-medium mb-2">{{ faq.question }}</h3>
          <p class="text-gray-700">{{ faq.answer }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ApiRegistryView',
  data() {
    return {
      serviceCategories: [
        {
          name: '社交媒体',
          description: '包括知乎、微博、豆瓣等社交平台的热榜数据',
          status: '可用'
        },
        {
          name: '视频平台',
          description: 'B站、抖音、快手等视频平台的热门内容',
          status: '可用'
        },
        {
          name: '新闻资讯',
          description: '各大新闻媒体的热点新闻和资讯',
          status: '可用'
        },
        {
          name: '科技数码',
          description: 'IT之家、36氪等科技媒体的热门内容',
          status: '可用'
        },
        {
          name: '技术开发',
          description: 'CSDN、掘金、Github等开发者平台的热门内容',
          status: '可用'
        },
        {
          name: '游戏动漫',
          description: '游戏和动漫相关的热门内容和更新信息',
          status: '可用'
        },
        {
          name: '生活服务',
          description: '天气预警、地震速报等生活服务信息',
          status: '可用'
        },
        {
          name: '数据分析',
          description: '对热榜数据的分析和处理，提供数据洞察',
          status: '测试中'
        },
        {
          name: '自定义数据源',
          description: '支持用户添加自定义数据源',
          status: '开发中'
        }
      ],
      faqs: [
        {
          question: '如何添加自定义MCP服务器？',
          answer: '在配置文件中的mcpServers对象中添加新的服务器配置，指定url和name属性即可。配置文件位于~/.cursor/mcp.json。'
        },
        {
          question: 'MCP服务支持哪些平台？',
          answer: '目前支持Windows、macOS和Linux平台，只要能运行Node.js或Python环境的系统都可以使用MCP服务。'
        },
        {
          question: '如何排查MCP连接问题？',
          answer: '请检查配置文件格式是否正确，服务器URL是否可访问，以及网络连接状态。您可以使用curl或浏览器直接访问MCP服务URL来测试连接。'
        },
        {
          question: '数据更新频率是多少？',
          answer: '不同平台的数据更新频率不同，大多数热榜数据每5-15分钟更新一次，确保数据的及时性。'
        },
        {
          question: '如何贡献新的数据源？',
          answer: '您可以在Github仓库上提交Pull Request，添加新的数据源适配器。请参考项目文档中的贡献指南。'
        }
      ]
    }
  }
}
</script> 