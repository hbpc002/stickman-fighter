# 🔥 火柴人对战游戏 (Stickman Fighter)

一个基于 Web 的火柴人对战小游戏，支持双人在线对战！

> 🎮 **在线试玩**: [点击查看部署地址](#部署指南) | 📚 **详细文档**: [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

## ✨ 特性

- 🎯 **双人对战** - 本地键盘控制，支持双人同屏对战
- 🌐 **Web版本** - 基于 HTML5 Canvas，浏览器直接运行
- ⚡ **实时战斗** - 流畅的物理系统和攻击判定
- 🎨 **精美界面** - 响应式设计，适配各种设备
- 🐳 **容器化** - 支持 Docker 一键部署
- ☁️ **多平台** - 支持 7+ 云平台部署

## 🚀 快速开始

### 方式1: 本地运行 (最简单)

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 运行游戏
python app.py

# 3. 浏览器访问
# 打开: http://localhost:5000
```

### 方式2: Docker 部署

```bash
# 1. 启动服务
docker-compose up -d --build

# 2. 访问游戏
# 打开: http://localhost:5000
```

### 方式3: 云平台部署

```bash
# 使用部署助手
./deploy.sh
# 选择: Heroku / Railway / Render / Fly.io 等
```

## 🎮 游戏控制

| 玩家1 (红色) | 玩家2 (蓝色) |
|-------------|-------------|
| `W` - 跳跃 | `↑` - 跳跃 |
| `A` - 左移 | `←` - 左移 |
| `D` - 右移 | `→` - 右移 |
| `F` - 出拳 | `J` - 出拳 |
| `G` - 踢腿 | `K` - 踢腿 |

**其他操作:**
- `R` - 重新开始
- `ESC` - 暂停/继续

## 🎯 游戏机制

### 战斗系统
- **出拳**: 消耗 10 体力，造成 8 点伤害
- **踢腿**: 消耗 15 体力，造成 12 点伤害
- **体力恢复**: 自动缓慢恢复
- **受伤无敌**: 0.5秒无敌时间
- **击退效果**: 攻击会击退对手

### 物理系统
- 真实重力模拟
- 跳跃和地面碰撞
- 边界限制

### UI 显示
- 生命值条 (红色)
- 体力条 (蓝色)
- 实时数值显示

## 📁 项目结构

```
.
├── app.py                    # Flask Web 应用 (主程序)
├── stickman_fighter.py       # Pygame 桌面版 (可选)
├── requirements.txt          # Python 依赖
├── Dockerfile               # Docker 镜像配置
├── docker-compose.yml       # Docker 编排
├── deploy.sh                # 一键部署脚本
├── Procfile                 # Heroku 配置
├── VERCEL.json              # Vercel 配置
├── README.md                # 本文件
├── DEPLOYMENT_GUIDE.md      # 详细部署指南
├── 快速开始.md              # 快速启动指南
└── .gitignore               # Git 忽略文件
```

## 🐳 Docker 支持

### 构建和运行
```bash
# 构建镜像
docker build -t stickman-fighter .

# 运行容器
docker run -p 5000:5000 stickman-fighter

# 或使用 docker-compose
docker-compose up -d --build
```

### 常用命令
```bash
docker-compose logs -f      # 查看日志
docker-compose down         # 停止服务
docker-compose restart      # 重启服务
```

## ☁️ 支持的云平台

| 平台 | 难度 | 费用 | 状态 |
|------|------|------|------|
| **Heroku** | ⭐⭐ | 免费 | ✅ 支持 |
| **Railway** | ⭐⭐ | 免费/付费 | ✅ 支持 |
| **Render** | ⭐⭐ | 免费750h/月 | ✅ 支持 |
| **Fly.io** | ⭐⭐⭐ | 免费/付费 | ✅ 支持 |
| **Vercel** | ⭐⭐ | 免费 | ✅ 支持 |
| **自托管** | ⭐⭐⭐⭐ | 服务器费用 | ✅ 支持 |
| **Docker** | ⭐⭐ | 免费 | ✅ 支持 |

详细部署指南: [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

## 🔧 API 端点

应用提供以下 API 端点:

- `GET /` - 游戏主界面
- `GET /api/health` - 健康检查
- `GET /api/stats` - 游戏统计信息

## 🛠️ 技术栈

- **后端**: Python Flask
- **前端**: HTML5 Canvas + JavaScript
- **部署**: Docker / 云平台
- **测试**: 本地浏览器

## 📊 性能优化

- ✅ 轻量级 Canvas 渲染
- ✅ 高效的碰撞检测
- ✅ 优化的动画循环
- ✅ 响应式设计

## 🎯 使用场景

- 🏠 **家庭娱乐** - 双人同屏对战
- 🎓 **教学演示** - 游戏开发入门
- 💻 **编程学习** - Python + Web 开发
- 🚀 **项目展示** - 云部署演示

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📝 开发计划

- [ ] 添加音效系统
- [ ] AI 对战模式
- [ ] 联机对战功能
- [ ] 更多角色皮肤
- [ ] 排行榜系统
- [ ] 移动端触控支持

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 🙏 致谢

- 感谢 Pygame 和 Flask 社区
- 感谢所有贡献者的支持

---

**🎮 开始游戏**: `python app.py`

**📚 更多信息**: 查看 [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) 或 [快速开始.md](快速开始.md)

**🌟 如果这个项目对你有帮助，请给个 Star！**
