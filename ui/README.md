# OpenMCP UI

这是一个用于展示OpenMCP API的Vue.js界面，提供了漂亮的UI展示各种API接口。

## 功能

- 以卡片形式展示分类API
- 详细的API文档和接口说明
- 可测试各个API接口
- 响应式设计，适配移动设备和桌面设备

## 技术栈

- Vue 3
- Vue Router
- Pinia (状态管理)
- Tailwind CSS (样式)
- Axios (HTTP客户端)
- Vite (构建工具)

## 安装

```bash
# 安装依赖
npm install
```

## 开发

```bash
# 启动开发服务器
npm run dev
```

## 构建

```bash
# 构建生产版本
npm run build
```

## 预览构建结果

```bash
# 预览构建结果
npm run preview
```

## 项目结构

```
ui/
├── public/             # 静态资源
├── src/
│   ├── assets/         # 样式和图片
│   ├── components/     # 组件
│   ├── router/         # 路由配置
│   ├── stores/         # Pinia状态存储
│   ├── views/          # 页面视图
│   ├── App.vue         # 主应用组件
│   └── main.js         # 入口文件
├── index.html          # HTML模板
├── package.json        # 项目依赖
├── vite.config.js      # Vite配置
└── README.md           # 项目说明
``` 