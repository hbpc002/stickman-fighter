#!/bin/bash

# 🚀 火柴人对战游戏 - 快速启动脚本

echo "=========================================="
echo "   🔥 火柴人对战游戏 - 启动器"
echo "=========================================="
echo ""

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "❌ 未检测到 Python3，请先安装 Python"
    exit 1
fi

echo "✅ Python3 已安装: $(python3 --version)"

# 检查依赖
echo ""
echo "📦 检查依赖..."
if python3 -c "import flask" 2>/dev/null; then
    echo "✅ Flask 已安装"
else
    echo "❌ Flask 未安装"
    echo "正在安装依赖..."
    pip3 install -r requirements.txt
fi

echo ""
echo "🎮 选择游戏版本:"
echo "1) 标准版 (app.py) - 基础功能"
echo "2) 增强版 (app_enhanced.py) - 特殊技能+AI+音效"
echo "3) Pygame桌面版 (stickman_fighter.py) - 需要Pygame"
echo "4) 查看帮助"
echo "5) 运行测试"
echo "0) 退出"
echo ""

read -p "请选择 (0-5): " choice

case $choice in
    1)
        echo ""
        echo "🚀 启动标准版..."
        echo "访问: http://localhost:5000"
        echo "按 Ctrl+C 停止"
        echo ""
        python3 app.py
        ;;
    2)
        echo ""
        echo "🚀 启动增强版..."
        echo "访问: http://localhost:5000"
        echo "按 Ctrl+C 停止"
        echo ""
        python3 app_enhanced.py
        ;;
    3)
        echo ""
        echo "🎮 启动Pygame桌面版..."
        echo "需要安装: pip3 install pygame"
        echo "按 ESC 退出游戏"
        echo ""
        python3 stickman_fighter.py
        ;;
    4)
        echo ""
        echo "📋 游戏说明:"
        echo ""
        echo "🎮 控制键位:"
        echo "  玩家1 (红色): WASD移动, F=拳, G=踢腿, H=特殊技能"
        echo "  玩家2 (蓝色): 方向键移动, J=拳, K=踢腿, L=特殊技能"
        echo ""
        echo "⚡ 增强版特性:"
        echo "  - 连击系统 (连续攻击提升伤害)"
        echo "  - 特殊技能 (高伤害+击飞)"
        echo "  - AI对战模式 (vs 电脑)"
        echo "  - 硬核模式 (伤害翻倍)"
        echo "  - 音效系统"
        echo ""
        echo "🌐 部署选项:"
        echo "  - 本地运行: ./start.sh"
        echo "  - Docker: docker-compose up -d"
        echo "  - 云平台: ./deploy.sh"
        echo ""
        ;;
    5)
        echo ""
        echo "🔍 运行完整性测试..."
        python3 test_game.py
        ;;
    0)
        echo "👋 再见！"
        exit 0
        ;;
    *)
        echo "❌ 无效选择"
        exit 1
        ;;
esac
