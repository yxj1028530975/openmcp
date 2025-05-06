#!/bin/bash
# Docker镜像加速配置脚本

# 确认是否为root用户运行
if [ "$EUID" -ne 0 ] && [ "$(uname)" != "Darwin" ]; then
  echo "请使用sudo运行此脚本"
  exit 1
fi

# 检测操作系统类型
OS=$(uname -s)
echo "检测到操作系统: $OS"

# macOS系统处理方式
if [ "$OS" = "Darwin" ]; then
  echo "正在为macOS配置Docker镜像加速..."
  
  # 创建Docker配置目录(如果不存在)
  DOCKER_CONFIG_DIR="$HOME/.docker"
  mkdir -p "$DOCKER_CONFIG_DIR"
  
  # 检查配置文件是否存在
  CONFIG_FILE="$DOCKER_CONFIG_DIR/daemon.json"
  if [ -f "$CONFIG_FILE" ]; then
    echo "配置文件已存在，进行备份..."
    cp "$CONFIG_FILE" "${CONFIG_FILE}.bak"
  fi
  
  # 写入镜像加速配置
  cat > "$CONFIG_FILE" << EOF
{
  "registry-mirrors": [
    "https://mirror.ccs.tencentyun.com/",
    "https://registry.cn-hangzhou.aliyuncs.com",
    "https://mirror.baidubce.com",
    "https://docker.mirrors.ustc.edu.cn"
  ]
}
EOF
  
  echo "配置已写入 $CONFIG_FILE"
  echo "请在Docker Desktop的Settings中选择Apply & Restart应用配置"
  echo "或者直接重启Docker Desktop应用"
  
# Linux系统处理方式
elif [ "$OS" = "Linux" ]; then
  echo "正在为Linux配置Docker镜像加速..."
  
  # 创建Docker配置目录(如果不存在)
  mkdir -p /etc/docker
  
  # 检查配置文件是否存在
  if [ -f "/etc/docker/daemon.json" ]; then
    echo "配置文件已存在，进行备份..."
    cp /etc/docker/daemon.json /etc/docker/daemon.json.bak
  fi
  
  # 写入镜像加速配置
  cat > /etc/docker/daemon.json << EOF
{
  "registry-mirrors": [
    "https://mirror.ccs.tencentyun.com/",
    "https://registry.cn-hangzhou.aliyuncs.com",
    "https://mirror.baidubce.com",
    "https://docker.mirrors.ustc.edu.cn"
  ]
}
EOF
  
  echo "配置已写入 /etc/docker/daemon.json"
  
  # 重启Docker服务
  echo "正在重启Docker服务..."
  if command -v systemctl > /dev/null; then
    systemctl daemon-reload
    systemctl restart docker
    echo "Docker服务已重启"
  else
    service docker restart
    echo "Docker服务已重启"
  fi
  
else
  echo "不支持的操作系统类型: $OS"
  exit 1
fi

echo ""
echo "配置完成！以下国内镜像源已配置："
echo "- 腾讯云: https://mirror.ccs.tencentyun.com/"
echo "- 阿里云: https://registry.cn-hangzhou.aliyuncs.com"
echo "- 百度云: https://mirror.baidubce.com"
echo "- 中科大: https://docker.mirrors.ustc.edu.cn"
echo ""
echo "请尝试运行 'docker-compose up -d --build' 重新构建"
echo "如果仍然遇到问题，尝试直接从Alpine镜像构建:"
echo "docker pull alpine:latest"
echo "然后重新运行 docker-compose" 