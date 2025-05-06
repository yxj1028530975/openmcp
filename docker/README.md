# OpenMCP Docker部署指南

本目录包含了OpenMCP项目的Docker部署相关文件，帮助您快速部署整个应用栈。

## 目录结构

- `Dockerfile.backend` - 后端API服务的Dockerfile
- `Dockerfile.frontend` - 前端UI服务的Dockerfile
- `nginx.conf` - Nginx配置文件，用于前端部署
- `docker-compose.yml` - Docker Compose配置文件，定义了整个应用栈

## 环境变量配置

Docker Compose配置使用了环境变量，提供了默认值，因此即使不创建环境变量文件也能正常运行。如果您需要自定义配置，可以创建一个`.env`文件在docker目录中：

```ini
# 后端服务配置
BACKEND_PORT=8000
BACKEND_CORS_ORIGINS=["http://localhost","http://localhost:80"]

# 前端服务配置
FRONTEND_PORT=80
API_BASE_URL=http://localhost:8000

# DailyHotApi服务配置
DAILYHOT_API_PORT=6688
DAILYHOT_API_URL=http://dailyhot-api:6688

# 其他配置
TIMEZONE=Asia/Shanghai
```

## 部署步骤

1. 确保已安装Docker和Docker Compose
   
   ```bash
   docker --version
   docker-compose --version
   ```

2. (可选) 创建环境变量文件
   
   ```bash
   # 在docker目录下创建.env文件
   cat > .env << EOF
   # 后端服务配置
   BACKEND_PORT=8000
   BACKEND_CORS_ORIGINS=["http://localhost","http://localhost:80"]
   
   # 前端服务配置
   FRONTEND_PORT=80
   API_BASE_URL=http://localhost:8000
   
   # DailyHotApi服务配置
   DAILYHOT_API_PORT=6688
   DAILYHOT_API_URL=http://dailyhot-api:6688
   
   # 其他配置
   TIMEZONE=Asia/Shanghai
   EOF
   ```

3. 构建并启动服务
   
   ```bash
   # 从docker目录下运行
   docker-compose up -d
   ```

4. 验证服务
   
   - 前端UI服务: http://localhost:80
   - 后端API服务: http://localhost:8000/docs
   - 热榜API服务: http://localhost:6688

## Docker Compose命令参考

```bash
# 启动所有服务
docker-compose up -d

# 仅启动后端服务
docker-compose up -d backend

# 重新构建并启动服务
docker-compose up -d --build

# 停止所有服务
docker-compose down

# 停止并删除所有容器和网络
docker-compose down -v

# 查看服务状态
docker-compose ps

# 进入容器内部(例如进入后端容器)
docker-compose exec backend bash
```

## 开发模式部署

针对开发环境，docker-compose.yml已配置后端代码目录为卷挂载，这意味着当您修改本地代码时，容器内的应用会自动更新。

要查看后端日志以监控应用状态：

```bash
docker-compose logs -f backend
```

## 常见问题

### 如何自定义端口？

修改`.env`文件中的对应端口配置，或者直接在运行docker-compose命令时传入环境变量：

```bash
BACKEND_PORT=9000 FRONTEND_PORT=8080 docker-compose up -d
```

### 遇到构建超时问题？

如果构建时出现网络超时问题，可以尝试以下解决方案：

1. 使用国内Docker镜像源，在`/etc/docker/daemon.json`中添加：

```json
{
  "registry-mirrors": [
    "https://registry.cn-hangzhou.aliyuncs.com"
  ]
}
```

2. 重启Docker服务

```bash
sudo systemctl restart docker
```

### 如何查看日志？

```bash
# 查看特定服务的日志
docker-compose logs backend
docker-compose logs frontend
docker-compose logs dailyhot-api

# 实时查看日志
docker-compose logs -f

# 查看最近100行日志
docker-compose logs --tail=100
```

### 如何更新到最新版本？

```bash
# 拉取最新代码
git pull

# 重新构建并启动服务
docker-compose up -d --build
```

### 如何配置MCP客户端？

在容器化环境中使用OpenMCP，您需要更新MCP配置文件中的URL地址。根据您的部署方式，选择合适的配置：

- 本地开发环境:
```json
{
  "mcpServers": {
    "openmcp-sse": {
      "url": "http://localhost:8000/mcp",
      "name": "openmcp-sse"
    }
  }
}
```

- 生产环境(使用域名):
```json
{
  "mcpServers": {
    "openmcp-sse": {
      "url": "https://yourdomain.com/mcp",
      "name": "openmcp-sse"
    }
  }
}
```

## 进阶配置

### 性能优化

- **后端服务**: 可以调整uvicorn的工作进程数和线程数
```yaml
CMD ["uvicorn", "apps.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

- **Nginx配置**: 可以调整工作进程数和连接数，在nginx.conf中添加
```
worker_processes auto;
worker_connections 1024;
```

### 使用外部数据源

如果您需要将热榜API服务替换为外部数据源，请修改`.env`文件中的`DAILYHOT_API_URL`变量，并删除`docker-compose.yml`中的`dailyhot-api`服务部分。

### 生产环境部署建议

对于生产环境，建议额外配置：

1. **HTTPS支持**: 更新Nginx配置，添加SSL证书
2. **环境隔离**: 为开发、测试和生产环境使用不同的docker-compose文件
3. **资源限制**: 在docker-compose.yml中添加资源限制
```yaml
services:
  backend:
    # ...
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
```
4. **监控和日志**: 集成Prometheus、Grafana和ELK等工具
5. **数据持久化**: 配置适当的卷挂载，保存重要数据 