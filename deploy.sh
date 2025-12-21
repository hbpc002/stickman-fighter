#!/bin/bash

# 火柴人对战游戏 - 云端部署脚本
# 支持多种云平台部署

set -e

echo "=========================================="
echo "   🔥 火柴人对战游戏 - 部署助手 🔥"
echo "=========================================="
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 检查 Docker 是否安装
check_docker() {
    if command -v docker &> /dev/null; then
        echo -e "${GREEN}✓${NC} Docker 已安装: $(docker --version)"
        return 0
    else
        echo -e "${RED}✗${NC} Docker 未安装，请先安装 Docker"
        return 1
    fi
}

# 检查 Docker Compose 是否安装
check_docker_compose() {
    if command -v docker-compose &> /dev/null; then
        echo -e "${GREEN}✓${NC} Docker Compose 已安装"
        return 0
    else
        echo -e "${RED}✗${NC} Docker Compose 未安装"
        return 1
    fi
}

# 本地 Docker 部署
deploy_local() {
    echo -e "${BLUE}🚀 本地 Docker 部署${NC}"
    echo ""

    if ! check_docker; then
        return 1
    fi

    echo "构建并启动容器..."
    docker-compose up -d --build

    echo ""
    echo -e "${GREEN}✓ 部署成功！${NC}"
    echo "游戏访问地址: http://localhost:5000"
    echo ""
    echo "常用命令:"
    echo "  查看日志: docker-compose logs -f"
    echo "  停止服务: docker-compose down"
    echo "  重启服务: docker-compose restart"
}

# Heroku 部署
deploy_heroku() {
    echo -e "${BLUE}☁️  Heroku 云部署${NC}"
    echo ""

    if ! command -v heroku &> /dev/null; then
        echo -e "${RED}✗${NC} 请先安装 Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli"
        return 1
    fi

    echo "步骤 1: 登录 Heroku"
    heroku login

    echo ""
    echo "步骤 2: 创建 Heroku 应用"
    read -p "输入应用名称 (留空自动生成): " app_name

    if [ -z "$app_name" ]; then
        heroku create
    else
        heroku create $app_name
    fi

    echo ""
    echo "步骤 3: 配置 Procfile"
    echo "web: python app.py" > Procfile

    echo ""
    echo "步骤 4: 部署到 Heroku"
    git init
    git add .
    git commit -m "Deploy Stickman Fighter"
    heroku git:remote -a $(heroku apps:info | grep "=== " | cut -d' ' -f2)
    git push heroku master

    echo ""
    echo -e "${GREEN}✓ 部署成功！${NC}"
    heroku open
}

# Railway 部署
deploy_railway() {
    echo -e "${BLUE}🚂 Railway 云部署${NC}"
    echo ""

    echo "Railway 部署步骤:"
    echo "1. 访问 https://railway.app"
    echo "2. 使用 GitHub 账号登录"
    echo "3. 点击 'New Project' -> 'Deploy from GitHub repo'"
    echo "4. 选择或导入此项目仓库"
    echo "5. Railway 会自动检测 Python 项目并部署"
    echo "6. 等待部署完成，获取访问 URL"
    echo ""
    echo "配置说明:"
    echo "  - Railway 会自动安装 requirements.txt 中的依赖"
    echo "  - 端口: Railway 会设置 PORT 环境变量"
    echo "  - 应用会自动启动"
    echo ""
    echo -e "${YELLOW}提示: 需要先将代码推送到 GitHub${NC}"
}

# Render 部署
deploy_render() {
    echo -e "${BLUE}🌐 Render 云部署${NC}"
    echo ""

    echo "Render 部署步骤:"
    echo "1. 访问 https://render.com"
    echo "2. 使用 GitHub 账号登录"
    echo "3. 点击 'New' -> 'Web Service'"
    echo "4. 连接 GitHub 仓库"
    echo "5. 配置 Web Service:"
    echo "   - Name: stickman-fighter"
    echo "   - Environment: Python"
    echo "   - Build Command: pip install -r requirements.txt"
    echo "   - Start Command: python app.py"
    echo "   - Port: 5000"
    echo "6. 点击 'Create Web Service'"
    echo ""
    echo -e "${YELLOW}提示: Render 提供免费的 750 小时/月${NC}"
}

# Fly.io 部署
deploy_fly() {
    echo -e "${BLUE}🚀 Fly.io 云部署${NC}"
    echo ""

    if ! command -v flyctl &> /dev/null; then
        echo -e "${RED}✗${NC} 请先安装 flyctl: curl -L https://fly.io/install.sh | sh"
        return 1
    fi

    echo "步骤 1: 登录 Fly.io"
    flyctl auth login

    echo ""
    echo "步骤 2: 创建应用"
    flyctl launch

    echo ""
    echo "步骤 3: 部署"
    flyctl deploy

    echo ""
    echo -e "${GREEN}✓ 部署成功！${NC}"
    flyctl open
}

# Vercel 部署 (需要 Python 支持)
deploy_vercel() {
    echo -e "${BLUE}⚡ Vercel 云部署${NC}"
    echo ""

    echo "Vercel 部署步骤:"
    echo "1. 访问 https://vercel.com"
    echo "2. 使用 GitHub 账号登录"
    echo "3. 点击 'Add New...' -> 'Project'"
    echo "4. 导入 GitHub 仓库"
    echo "5. 配置项目:"
    echo "   - Framework Preset: Other"
    echo "   - Build Command: (留空)"
    echo "   - Output Directory: (留空)"
    echo "   - Install Command: pip install -r requirements.txt"
    echo "   - Start Command: python app.py"
    echo "6. 点击 'Deploy'"
    echo ""
    echo -e "${YELLOW}注意: Vercel 主要用于前端，Python 支持有限${NC}"
}

# 手动部署指南
manual_deploy() {
    echo -e "${BLUE}📋 手动部署指南${NC}"
    echo ""

    echo "服务器要求:"
    echo "  - Python 3.8+"
    echo "  - 端口 5000 可用"
    echo ""

    echo "部署步骤:"
    echo "1. 上传所有文件到服务器"
    echo "2. 安装依赖:"
    echo "   pip install -r requirements.txt"
    echo ""
    echo "3. 运行应用:"
    echo "   python app.py"
    echo ""
    echo "4. 配置反向代理 (Nginx/Apache):"
    echo "   server {"
    echo "       listen 80;"
    echo "       server_name your-domain.com;"
    echo "       location / {"
    echo "           proxy_pass http://127.0.0.1:5000;"
    echo "           proxy_http_version 1.1;"
    echo "           proxy_set_header Upgrade \$http_upgrade;"
    echo "           proxy_set_header Connection 'upgrade';"
    echo "           proxy_set_header Host \$host;"
    echo "           proxy_cache_bypass \$http_upgrade;"
    echo "       }"
    echo "   }"
    echo ""
    echo "5. 使用 systemd 保持运行:"
    echo "   [Unit]"
    echo "   Description=Stickman Fighter Game"
    echo "   After=network.target"
    echo ""
    echo "   [Service]"
    echo "   User=your-user"
    echo "   WorkingDirectory=/path/to/game"
    echo "   ExecStart=/usr/bin/python3 app.py"
    echo "   Restart=always"
    echo ""
    echo "   [Install]"
    echo "   WantedBy=multi-user.target"
}

# 显示主菜单
show_menu() {
    echo -e "${GREEN}可用的部署选项:${NC}"
    echo ""
    echo "1) 🐳 本地 Docker 部署 (推荐测试)"
    echo "2) ☁️  Heroku 部署 (简单快速)"
    echo "3) 🚂 Railway 部署 (现代云平台)"
    echo "4) 🌐 Render 部署 (免费额度充足)"
    echo "5) 🚀 Fly.io 部署 (全球边缘网络)"
    echo "6) ⚡ Vercel 部署 (前端友好)"
    echo "7) 📋 手动部署指南 (自托管)"
    echo "8) 📦 查看所有文件"
    echo "9) 💡 帮助信息"
    echo "0) 退出"
    echo ""
    echo -n "请选择 (0-9): "
}

# 显示帮助
show_help() {
    echo -e "${BLUE}💡 帮助信息${NC}"
    echo ""
    echo "本项目是一个基于 Web 的火柴人对战小游戏。"
    echo ""
    echo "项目文件说明:"
    echo "  - app.py: Flask Web 应用 (主程序)"
    echo "  - stickman_fighter.py: 原始 Pygame 版本"
    echo "  - requirements.txt: Python 依赖"
    echo "  - Dockerfile: Docker 镜像配置"
    echo "  - docker-compose.yml: Docker Compose 配置"
    echo "  - deploy.sh: 部署脚本 (当前脚本)"
    echo "  - README.md: 项目说明文档"
    echo ""
    echo "游戏特点:"
    echo "  - 双人对战 (本地键盘控制)"
    echo "  - 生命值/体力系统"
    echo "  - 攻击动画和判定"
    echo "  - 跳跃和物理系统"
    echo "  - 响应式 Web 界面"
    echo ""
    echo "浏览器访问: http://localhost:5000"
    echo ""
    echo "控制键位:"
    echo "  玩家1: WASD移动, F=拳, G=脚"
    echo "  玩家2: 方向键移动, J=拳, K=脚"
}

# 显示文件列表
show_files() {
    echo -e "${BLUE}📦 项目文件列表${NC}"
    echo ""
    ls -lah
    echo ""
    echo "文件说明:"
    echo "  app.py              - Flask Web 应用"
    echo "  stickman_fighter.py - Pygame 桌面版"
    echo "  requirements.txt    - Python 依赖"
    echo "  Dockerfile          - Docker 配置"
    echo "  docker-compose.yml  - Docker Compose"
    echo "  deploy.sh           - 部署脚本"
    echo "  README.md           - 项目文档"
}

# 主循环
main() {
    while true; do
        show_menu
        read choice

        case $choice in
            1)
                deploy_local
                ;;
            2)
                deploy_heroku
                ;;
            3)
                deploy_railway
                ;;
            4)
                deploy_render
                ;;
            5)
                deploy_fly
                ;;
            6)
                deploy_vercel
                ;;
            7)
                manual_deploy
                ;;
            8)
                show_files
                ;;
            9)
                show_help
                ;;
            0)
                echo -e "${GREEN}再见！${NC}"
                exit 0
                ;;
            *)
                echo -e "${RED}无效选择，请重新输入${NC}"
                ;;
        esac

        echo ""
        read -p "按回车键继续..."
        echo ""
    done
}

# 检查参数
if [ "$1" == "local" ]; then
    deploy_local
elif [ "$1" == "help" ]; then
    show_help
else
    main
fi
