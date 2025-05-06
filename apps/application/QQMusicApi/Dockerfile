FROM python:3.9-slim

WORKDIR /app

# 安装依赖
RUN pip install --no-cache-dir fastapi uvicorn qqmusic-api-python

# 复制应用代码
COPY ./QQMusic_api.py .

# 设置环境变量
ENV PORT=8001
ENV HOST=0.0.0.0

# 暴露端口
EXPOSE 8001

# 启动服务
CMD ["python", "QQMusic_api.py"] 