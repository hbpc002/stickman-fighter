# 🚀 火柴人对战游戏 - 云端部署指南

## 📋 项目概览

这是一个基于 Web 的火柴人对战小游戏，使用 Python Flask 开发，支持双人在线对战。

**技术栈:**
- Python Flask (Web 框架)
- HTML5 Canvas (游戏渲染)
- JavaScript (游戏逻辑)
- Docker (容器化部署)

---

## 🎯 快速开始

### 方法 1: 本地 Docker 部署 (推荐测试)

```bash
# 1. 确保已安装 Docker 和 Docker Compose
docker --version
docker-compose --version

# 2. 使用部署脚本
./deploy.sh
# 然后选择 1 (本地 Docker 部署)

# 或手动执行
docker-compose up -d --build

# 3. 访问游戏
# 打开浏览器访问: http://localhost:5000
```

### 方法 2: 本地直接运行

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 运行应用
python app.py

# 3. 访问游戏
# 打开浏览器访问: http://localhost:5000
```

---

## ☁️ 云平台部署

### 1. Heroku (最简单)

**优点:** 部署简单，免费

```bash
# 1. 安装 Heroku CLI
# 访问: https://devcenter.heroku.com/articles/heroku-cli

# 2. 登录
heroku login

# 3. 创建应用
heroku create your-app-name

# 4. 部署
git init
git add .
git commit -m "Initial commit"
heroku git:remote -a your-app-name
git push heroku master

# 5. 打开应用
heroku open
```

**或使用部署脚本:**
```bash
./deploy.sh
# 选择 2 (Heroku 部署)
```

---

### 2. Railway (现代云平台)

**优点:** 现代化界面，GitHub 集成

1. 访问 [railway.app](https://railway.app)
2. 使用 GitHub 登录
3. 点击 "New Project" → "Deploy from GitHub repo"
4. 选择或导入此项目仓库
5. Railway 会自动检测并部署
6. 等待部署完成，获取访问 URL

**配置:**
- Railway 会自动安装 `requirements.txt` 中的依赖
- 端口: Railway 会设置 `PORT` 环境变量
- 应用会自动启动

---

### 3. Render (免费额度充足)

**优点:** 免费 750 小时/月，简单易用

1. 访问 [render.com](https://render.com)
2. 使用 GitHub 登录
3. 点击 "New" → "Web Service"
4. 连接 GitHub 仓库
5. 配置 Web Service:

| 配置项 | 值 |
|--------|------|
| Name | stickman-fighter |
| Environment | Python |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `python app.py` |
| Port | 5000 |

6. 点击 "Create Web Service"

---

### 4. Fly.io (全球边缘网络)

**优点:** 全球部署，性能优秀

```bash
# 1. 安装 flyctl
curl -L https://fly.io/install.sh | sh

# 2. 登录
flyctl auth login

# 3. 创建应用
flyctl launch

# 4. 部署
flyctl deploy

# 5. 打开应用
flyctl open
```

**或使用部署脚本:**
```bash
./deploy.sh
# 选择 5 (Fly.io 部署)
```

---

### 5. Vercel (前端友好)

**注意:** Vercel 主要用于前端，Python 支持有限

1. 访问 [vercel.com](https://vercel.com)
2. 使用 GitHub 登录
3. 导入 GitHub 仓库
4. 配置项目:

| 配置项 | 值 |
|--------|------|
| Framework Preset | Other |
| Build Command | (留空) |
| Output Directory | (留空) |
| Install Command | `pip install -r requirements.txt` |
| Start Command | `python app.py` |

5. 点击 "Deploy"

---

### 6. 自托管 (VPS/服务器)

**适用于:** 拥有自己的服务器

```bash
# 1. 上传文件到服务器
# 使用 SCP/SFTP 上传所有文件

# 2. 安装 Python 和依赖
sudo apt update
sudo apt install python3 python3-pip
pip3 install -r requirements.txt

# 3. 运行应用 (开发模式)
python3 app.py

# 4. 生产环境使用 Gunicorn
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# 5. 配置 Nginx 反向代理
sudo nano /etc/nginx/sites-available/stickman-fighter

# 添加以下配置:
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}

# 6. 启用配置并重启 Nginx
sudo ln -s /etc/nginx/sites-available/stickman-fighter /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# 7. 使用 systemd 保持应用运行
sudo nano /etc/systemd/system/stickman-fighter.service

# 添加以下配置:
[Unit]
Description=Stickman Fighter Game
After=network.target

[Service]
User=your-user
WorkingDirectory=/path/to/game
ExecStart=/usr/bin/python3 /path/to/game/app.py
Restart=always

[Install]
WantedBy=multi-user.target

# 8. 启动服务
sudo systemctl enable stickman-fighter
sudo systemctl start stickman-fighter
sudo systemctl status stickman-fighter
```

---

## 🐳 Docker 详细说明

### Dockerfile 说明

```dockerfile
FROM python:3.11-slim          # 使用精简版 Python 镜像
WORKDIR /app                   # 设置工作目录
COPY requirements.txt .        # 复制依赖文件
RUN pip install -r requirements.txt  # 安装依赖
COPY . .                       # 复制应用代码
EXPOSE 5000                    # 暴露端口
CMD ["python", "app.py"]       # 启动命令
```

### docker-compose.yml 说明

```yaml
version: '3.8'
services:
  stickman-fighter:
    build: .                    # 从当前目录构建
    container_name: stickman-fighter
    ports:
      - "5000:5000"            # 端口映射
    environment:
      - PORT=5000              # 环境变量
    restart: unless-stopped    # 自动重启
    healthcheck:               # 健康检查
      test: ["CMD", "curl", "-f", "http://localhost:5000/api/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

### Docker 常用命令

```bash
# 构建并启动
docker-compose up -d --build

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down

# 重启服务
docker-compose restart

# 查看状态
docker-compose ps

# 进入容器
docker exec -it stickman-fighter bash
```

---

## 🔧 环境变量

应用支持以下环境变量:

| 变量名 | 默认值 | 说明 |
|--------|--------|------|
| `PORT` | 5000 | Web 服务端口 |
| `FLASK_APP` | app.py | Flask 应用入口 |

---

## 🎮 游戏访问

部署成功后，访问:

```
http://your-app-url.com
```

**控制键位:**

| 玩家 | 移动 | 跳跃 | 出拳 | 踢腿 |
|------|------|------|------|------|
| 玩家1 (红色) | WASD | W | F | G |
| 玩家2 (蓝色) | 方向键 | ↑ | J | K |

**其他操作:**
- `R` - 重新开始
- `ESC` - 暂停/继续

---

## 📊 监控和维护

### 健康检查

应用提供健康检查 API:

```bash
# 检查服务状态
curl http://your-app-url.com/api/health

# 获取统计信息
curl http://your-app-url.com/api/stats
```

### 日志查看

```bash
# Docker 环境
docker-compose logs -f

# 系统服务
sudo journalctl -u stickman-fighter -f

# 直接运行
tail -f app.log
```

---

## 🛠️ 故障排除

### 问题 1: 端口被占用

```bash
# 查看端口占用
lsof -i :5000

# 或使用不同端口
PORT=8080 python app.py
```

### 问题 2: 依赖安装失败

```bash
# 升级 pip
pip install --upgrade pip

# 使用国内镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 问题 3: Docker 构建失败

```bash
# 清理缓存并重建
docker system prune -a
docker-compose build --no-cache
```

### 问题 4: 应用崩溃

```bash
# 检查 Python 版本
python --version

# 检查依赖
pip list | grep -E "flask|pygame"

# 手动测试
python -c "import flask; import pygame; print('OK')"
```

---

## 📝 部署检查清单

- [ ] 选择部署平台
- [ ] 准备 GitHub 仓库 (如需要)
- [ ] 配置环境变量
- [ ] 测试本地运行
- [ ] 执行部署
- [ ] 验证应用访问
- [ ] 配置自定义域名 (可选)
- [ ] 设置监控和告警 (可选)
- [ ] 配置 SSL 证书 (可选)

---

## 🎯 推荐部署方案

| 场景 | 推荐方案 | 原因 |
|------|----------|------|
| 快速测试 | 本地 Docker | 简单快速，无需配置 |
| 个人项目 | Heroku/Railway | 免费，部署简单 |
| 生产环境 | Render/Fly.io | 稳定，性能好 |
| 企业应用 | 自托管 + Docker | 完全控制，数据安全 |

---

## 📞 获取帮助

如果遇到问题:

1. 查看本指南的故障排除部分
2. 检查云平台文档
3. 查看应用日志获取详细错误信息
4. 确保所有依赖正确安装

---

**祝部署顺利！🎮**

如需使用部署脚本，只需运行:
```bash
./deploy.sh
```
然后按照菜单选择即可！
