#!/usr/bin/env python3
"""
Web版本的火柴人对战游戏 - Flask服务器
"""

from flask import Flask, render_template_string, request, jsonify
import json
import os

app = Flask(__name__)

# HTML模板 - 包含Canvas和游戏逻辑
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>火柴人对战 - Stickman Fighter</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Arial', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            color: white;
            padding: 20px;
        }

        .container {
            background: rgba(0, 0, 0, 0.3);
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            backdrop-filter: blur(10px);
            max-width: 1000px;
            width: 100%;
        }

        h1 {
            text-align: center;
            margin-bottom: 20px;
            font-size: 2.5em;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
        }

        .game-area {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 20px;
        }

        #gameCanvas {
            border: 3px solid white;
            border-radius: 10px;
            background: #87CEEB;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.5);
            cursor: none;
        }

        .controls {
            background: rgba(255, 255, 255, 0.1);
            padding: 20px;
            border-radius: 10px;
            width: 100%;
        }

        .control-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 15px;
        }

        .player-controls {
            background: rgba(0, 0, 0, 0.3);
            padding: 15px;
            border-radius: 8px;
        }

        .player-controls h3 {
            margin-bottom: 10px;
            font-size: 1.2em;
        }

        .player1 h3 { color: #ff6b6b; }
        .player2 h3 { color: #4dabf7; }

        .key-list {
            list-style: none;
            font-size: 0.9em;
            line-height: 1.8;
        }

        .key {
            display: inline-block;
            background: rgba(255, 255, 255, 0.2);
            padding: 2px 8px;
            border-radius: 4px;
            font-weight: bold;
            margin-right: 5px;
        }

        .status-bar {
            display: flex;
            justify-content: space-between;
            width: 100%;
            gap: 10px;
        }

        .player-status {
            flex: 1;
            background: rgba(0, 0, 0, 0.3);
            padding: 10px;
            border-radius: 8px;
            text-align: center;
        }

        .health-bar, .stamina-bar {
            height: 20px;
            background: #333;
            border-radius: 10px;
            overflow: hidden;
            margin-top: 5px;
            border: 1px solid white;
        }

        .health-fill {
            height: 100%;
            background: linear-gradient(90deg, #ff6b6b, #ff8787);
            transition: width 0.3s;
        }

        .stamina-fill {
            height: 100%;
            background: linear-gradient(90deg, #4dabf7, #74c0fc);
            transition: width 0.3s;
        }

        .buttons {
            display: flex;
            gap: 10px;
            justify-content: center;
            margin-top: 10px;
        }

        button {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 1em;
            font-weight: bold;
            transition: transform 0.2s, box-shadow 0.2s;
        }

        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        }

        button:active {
            transform: translateY(0);
        }

        .instructions {
            background: rgba(255, 255, 255, 0.1);
            padding: 15px;
            border-radius: 8px;
            margin-top: 15px;
            font-size: 0.9em;
            line-height: 1.6;
        }

        .game-over-overlay {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: rgba(0, 0, 0, 0.9);
            padding: 40px;
            border-radius: 15px;
            text-align: center;
            display: none;
            z-index: 100;
        }

        .game-over-overlay.show {
            display: block;
        }

        .winner-text {
            font-size: 2em;
            margin-bottom: 20px;
            font-weight: bold;
        }

        @media (max-width: 768px) {
            .control-grid {
                grid-template-columns: 1fr;
            }

            h1 {
                font-size: 1.8em;
            }

            .container {
                padding: 15px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔥 火柴人对战 - Stickman Fighter 🔥</h1>

        <div class="game-area">
            <div style="position: relative;">
                <canvas id="gameCanvas" width="800" height="500"></canvas>
                <div id="gameOverOverlay" class="game-over-overlay">
                    <div class="winner-text" id="winnerText"></div>
                    <button onclick="resetGame()">重新开始</button>
                </div>
            </div>

            <div class="status-bar">
                <div class="player-status">
                    <div>玩家1 (红色) - 生命: <span id="p1Health">100</span></div>
                    <div class="health-bar">
                        <div class="health-fill" id="p1HealthBar" style="width: 100%"></div>
                    </div>
                    <div>体力: <span id="p1Stamina">100</span></div>
                    <div class="stamina-bar">
                        <div class="stamina-fill" id="p1StaminaBar" style="width: 100%"></div>
                    </div>
                </div>
                <div class="player-status">
                    <div>玩家2 (蓝色) - 生命: <span id="p2Health">100</span></div>
                    <div class="health-bar">
                        <div class="health-fill" id="p2HealthBar" style="width: 100%"></div>
                    </div>
                    <div>体力: <span id="p2Stamina">100</span></div>
                    <div class="stamina-bar">
                        <div class="stamina-fill" id="p2StaminaBar" style="width: 100%"></div>
                    </div>
                </div>
            </div>

            <div class="controls">
                <div class="control-grid">
                    <div class="player-controls player1">
                        <h3>玩家1 (红色)</h3>
                        <ul class="key-list">
                            <li><span class="key">W</span> 跳跃</li>
                            <li><span class="key">A</span> 左移</li>
                            <li><span class="key">D</span> 右移</li>
                            <li><span class="key">F</span> 出拳</li>
                            <li><span class="key">G</span> 踢腿</li>
                        </ul>
                    </div>
                    <div class="player-controls player2">
                        <h3>玩家2 (蓝色)</h3>
                        <ul class="key-list">
                            <li><span class="key">↑</span> 跳跃</li>
                            <li><span class="key">←</span> 左移</li>
                            <li><span class="key">→</span> 右移</li>
                            <li><span class="key">J</span> 出拳</li>
                            <li><span class="key">K</span> 踢腿</li>
                        </ul>
                    </div>
                </div>

                <div class="buttons">
                    <button onclick="resetGame()">🔄 重新开始</button>
                    <button onclick="togglePause()">⏸️ 暂停/继续</button>
                </div>
            </div>

            <div class="instructions">
                <strong>游戏说明：</strong> 将对手的生命值降至0即可获胜！
                出拳造成8点伤害，踢腿造成12点伤害。体力会自动恢复。
            </div>
        </div>
    </div>

    <script>
        // 游戏核心逻辑 - JavaScript版本
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');

        // 游戏状态
        let gameState = {
            player1: null,
            player2: null,
            gameOver: false,
            paused: false,
            winner: null
        };

        // 键盘状态
        const keys = {};

        // 火柴人玩家类
        class Stickman {
            constructor(x, y, color, controls, playerNum) {
                this.x = x;
                this.y = y;
                this.color = color;
                this.controls = controls;
                this.playerNum = playerNum;

                this.vx = 0;
                this.vy = 0;
                this.width = 30;
                this.height = 60;
                this.speed = 4;
                this.jumpPower = 12;
                this.gravity = 0.6;
                this.onGround = false;

                this.health = 100;
                this.stamina = 100;
                this.isPunching = false;
                this.isKicking = false;
                this.attackCooldown = 0;
                this.hitCooldown = 0;
                this.facingRight = playerNum === 2;

                this.animationTimer = 0;
            }

            handleInput() {
                this.vx = 0;

                if (keys[this.controls.left]) {
                    this.vx = -this.speed;
                    this.facingRight = false;
                }
                if (keys[this.controls.right]) {
                    this.vx = this.speed;
                    this.facingRight = true;
                }

                if (keys[this.controls.jump] && this.onGround) {
                    this.vy = -this.jumpPower;
                    this.onGround = false;
                }

                if (this.attackCooldown === 0) {
                    if (keys[this.controls.punch]) {
                        this.punch();
                    } else if (keys[this.controls.kick]) {
                        this.kick();
                    }
                }
            }

            punch() {
                if (this.stamina >= 10) {
                    this.isPunching = true;
                    this.attackCooldown = 20;
                    this.stamina -= 10;
                    this.animationTimer = 0;
                }
            }

            kick() {
                if (this.stamina >= 15) {
                    this.isKicking = true;
                    this.attackCooldown = 25;
                    this.stamina -= 15;
                    this.animationTimer = 0;
                }
            }

            takeDamage(damage) {
                if (this.hitCooldown === 0) {
                    this.health -= damage;
                    this.hitCooldown = 30;
                    if (this.health < 0) this.health = 0;
                    return true;
                }
                return false;
            }

            getAttackHitbox() {
                if (this.isPunching) {
                    const reach = 40;
                    if (this.facingRight) {
                        return { x: this.x + this.width, y: this.y + 15, w: reach, h: 30 };
                    } else {
                        return { x: this.x - reach, y: this.y + 15, w: reach, h: 30 };
                    }
                } else if (this.isKicking) {
                    const reach = 50;
                    if (this.facingRight) {
                        return { x: this.x + this.width, y: this.y + 30, w: reach, h: 40 };
                    } else {
                        return { x: this.x - reach, y: this.y + 30, w: reach, h: 40 };
                    }
                }
                return null;
            }

            update() {
                this.vy += this.gravity;
                this.x += this.vx;
                this.y += this.vy;

                // 地面碰撞
                const groundLevel = canvas.height - 80;
                if (this.y + this.height >= groundLevel) {
                    this.y = groundLevel - this.height;
                    this.vy = 0;
                    this.onGround = true;
                }

                // 边界限制
                if (this.x < 0) this.x = 0;
                if (this.x + this.width > canvas.width) this.x = canvas.width - this.width;

                // 冷却时间
                if (this.attackCooldown > 0) this.attackCooldown--;
                if (this.hitCooldown > 0) this.hitCooldown--;

                // 动画计时
                if (this.isPunching || this.isKicking) {
                    this.animationTimer++;
                    if (this.animationTimer >= 10) {
                        this.isPunching = false;
                        this.isKicking = false;
                        this.animationTimer = 0;
                    }
                }

                // 体力恢复
                if (this.stamina < 100) {
                    this.stamina += 0.2;
                }
            }

            draw() {
                // 受伤闪烁
                if (this.hitCooldown > 0 && this.hitCooldown % 4 < 2) {
                    return;
                }

                const bodyX = this.x + this.width / 2;
                const bodyY = this.y + 15;

                ctx.strokeStyle = this.color;
                ctx.lineWidth = 3;
                ctx.lineCap = 'round';

                // 头
                ctx.beginPath();
                ctx.arc(bodyX, this.y + 8, 8, 0, Math.PI * 2);
                ctx.stroke();

                // 身体
                ctx.beginPath();
                ctx.moveTo(bodyX, bodyY);
                ctx.lineTo(bodyX, bodyY + 25);
                ctx.stroke();

                // 腿
                const legOffset = (this.isKicking && this.animationTimer < 5) ? 8 : 0;
                if (this.facingRight) {
                    ctx.beginPath();
                    ctx.moveTo(bodyX, bodyY + 25);
                    ctx.lineTo(bodyX - 6, bodyY + 45 + legOffset);
                    ctx.stroke();

                    ctx.beginPath();
                    ctx.moveTo(bodyX, bodyY + 25);
                    ctx.lineTo(bodyX + 6, bodyY + 45);
                    ctx.stroke();
                } else {
                    ctx.beginPath();
                    ctx.moveTo(bodyX, bodyY + 25);
                    ctx.lineTo(bodyX + 6, bodyY + 45 + legOffset);
                    ctx.stroke();

                    ctx.beginPath();
                    ctx.moveTo(bodyX, bodyY + 25);
                    ctx.lineTo(bodyX - 6, bodyY + 45);
                    ctx.stroke();
                }

                // 手臂
                const armY = bodyY + 8;
                const punchOffset = (this.isPunching && this.animationTimer < 5) ? 12 : 0;

                if (this.facingRight) {
                    // 右臂
                    ctx.beginPath();
                    ctx.moveTo(bodyX, armY);
                    ctx.lineTo(bodyX + 12 + punchOffset, armY);
                    ctx.stroke();

                    // 左臂
                    ctx.beginPath();
                    ctx.moveTo(bodyX, armY);
                    ctx.lineTo(bodyX - 8, armY + 4);
                    ctx.stroke();
                } else {
                    // 左臂
                    ctx.beginPath();
                    ctx.moveTo(bodyX, armY);
                    ctx.lineTo(bodyX - 12 - punchOffset, armY);
                    ctx.stroke();

                    // 右臂
                    ctx.beginPath();
                    ctx.moveTo(bodyX, armY);
                    ctx.lineTo(bodyX + 8, armY + 4);
                    ctx.stroke();
                }
            }
        }

        // 检查碰撞
        function checkCollision(rect1, rect2) {
            return rect1.x < rect2.x + rect2.width &&
                   rect1.x + rect1.width > rect2.x &&
                   rect1.y < rect2.y + rect2.height &&
                   rect1.y + rect1.height > rect2.y;
        }

        function checkHit(hitbox, target) {
            if (!hitbox) return false;
            return hitbox.x < target.x + target.width &&
                   hitbox.x + hitbox.w > target.x &&
                   hitbox.y < target.y + target.height &&
                   hitbox.y + hitbox.h > target.y;
        }

        // 绘制背景
        function drawBackground() {
            // 天空
            ctx.fillStyle = '#87CEEB';
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            // 云朵
            ctx.fillStyle = 'rgba(255, 255, 255, 0.8)';
            drawCloud(100, 60);
            drawCloud(400, 50);
            drawCloud(650, 70);

            // 地面
            ctx.fillStyle = '#654321';
            const groundY = canvas.height - 80;
            ctx.fillRect(0, groundY, canvas.width, 80);

            // 地面纹理
            ctx.strokeStyle = '#4a3319';
            ctx.lineWidth = 1;
            for (let i = 0; i < canvas.width; i += 15) {
                ctx.beginPath();
                ctx.moveTo(i, groundY);
                ctx.lineTo(i, groundY + 8);
                ctx.stroke();
            }
        }

        function drawCloud(x, y) {
            ctx.beginPath();
            ctx.arc(x, y, 15, 0, Math.PI * 2);
            ctx.arc(x + 12, y - 5, 18, 0, Math.PI * 2);
            ctx.arc(x + 24, y, 15, 0, Math.PI * 2);
            ctx.fill();
        }

        // 更新UI
        function updateUI() {
            if (!gameState.player1 || !gameState.player2) return;

            document.getElementById('p1Health').textContent = Math.round(gameState.player1.health);
            document.getElementById('p1Stamina').textContent = Math.round(gameState.player1.stamina);
            document.getElementById('p1HealthBar').style.width = gameState.player1.health + '%';
            document.getElementById('p1StaminaBar').style.width = gameState.player1.stamina + '%';

            document.getElementById('p2Health').textContent = Math.round(gameState.player2.health);
            document.getElementById('p2Stamina').textContent = Math.round(gameState.player2.stamina);
            document.getElementById('p2HealthBar').style.width = gameState.player2.health + '%';
            document.getElementById('p2StaminaBar').style.width = gameState.player2.stamina + '%';
        }

        // 游戏主循环
        function gameLoop() {
            if (gameState.paused || gameState.gameOver) {
                if (gameState.gameOver) {
                    drawGame();
                    return;
                }
                requestAnimationFrame(gameLoop);
                return;
            }

            // 更新
            gameState.player1.handleInput();
            gameState.player2.handleInput();
            gameState.player1.update();
            gameState.player2.update();

            // 碰撞检测
            const hitbox1 = gameState.player1.getAttackHitbox();
            if (hitbox1) {
                const damage = gameState.player1.isPunching ? 8 : 12;
                if (checkHit(hitbox1, gameState.player2)) {
                    if (gameState.player2.takeDamage(damage)) {
                        gameState.player2.vx = gameState.player1.facingRight ? 5 : -5;
                    }
                }
            }

            const hitbox2 = gameState.player2.getAttackHitbox();
            if (hitbox2) {
                const damage = gameState.player2.isPunching ? 8 : 12;
                if (checkHit(hitbox2, gameState.player1)) {
                    if (gameState.player1.takeDamage(damage)) {
                        gameState.player1.vx = gameState.player2.facingRight ? 5 : -5;
                    }
                }
            }

            // 检查游戏结束
            if (gameState.player1.health <= 0) {
                gameState.gameOver = true;
                gameState.winner = 2;
                showGameOver();
            } else if (gameState.player2.health <= 0) {
                gameState.gameOver = true;
                gameState.winner = 1;
                showGameOver();
            }

            // 绘制
            drawGame();
            updateUI();

            requestAnimationFrame(gameLoop);
        }

        function drawGame() {
            drawBackground();

            if (gameState.player1) gameState.player1.draw();
            if (gameState.player2) gameState.player2.draw();
        }

        function showGameOver() {
            const overlay = document.getElementById('gameOverOverlay');
            const winnerText = document.getElementById('winnerText');
            const winnerColor = gameState.winner === 1 ? '#ff6b6b' : '#4dabf7';
            winnerText.innerHTML = `🎉 <span style="color: ${winnerColor}">玩家 ${gameState.winner}</span> 获胜！🎉`;
            overlay.classList.add('show');
        }

        function resetGame() {
            gameState.player1 = new Stickman(150, 200, '#ff6b6b', {
                left: 'a', right: 'd', jump: 'w', punch: 'f', kick: 'g'
            }, 1);

            gameState.player2 = new Stickman(620, 200, '#4dabf7', {
                left: 'ArrowLeft', right: 'ArrowRight', jump: 'ArrowUp', punch: 'j', kick: 'k'
            }, 2);

            gameState.gameOver = false;
            gameState.paused = false;
            gameState.winner = null;

            document.getElementById('gameOverOverlay').classList.remove('show');
            updateUI();
        }

        function togglePause() {
            gameState.paused = !gameState.paused;
        }

        // 键盘事件
        window.addEventListener('keydown', (e) => {
            keys[e.key.toLowerCase()] = true;
            keys[e.key] = true;

            // 防止方向键滚动页面
            if (['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight', ' '].includes(e.key)) {
                e.preventDefault();
            }
        });

        window.addEventListener('keyup', (e) => {
            keys[e.key.toLowerCase()] = false;
            keys[e.key] = false;
        });

        // 初始化游戏
        resetGame();
        gameLoop();
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/health')
def health():
    return jsonify({"status": "healthy", "service": "stickman-fighter"})

@app.route('/api/stats')
def stats():
    return jsonify({
        "game": "Stickman Fighter",
        "version": "1.0",
        "description": "火柴人对战小游戏 - Web版本"
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"🚀 启动服务器: http://localhost:{port}")
    print("🎮 打开浏览器访问即可开始游戏！")
    app.run(host='0.0.0.0', port=port, debug=False)
