#!/usr/bin/env python3
"""
🔥 火柴人对战游戏 - 增强创意版
支持手机端虚拟按键，全新特效，更多创意功能
"""

from flask import Flask, render_template_string, request, jsonify
import os

app = Flask(__name__)

# 增强版HTML模板 - 包含手机端虚拟按键
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>🔥 火柴人对战 - 创意增强版</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            -webkit-tap-highlight-color: transparent;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            color: white;
            padding: 10px;
            overflow-x: hidden;
            touch-action: manipulation;
        }

        .container {
            background: rgba(0, 0, 0, 0.4);
            border-radius: 20px;
            padding: 15px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
            backdrop-filter: blur(15px);
            max-width: 1000px;
            width: 100%;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }

        .header {
            text-align: center;
            margin-bottom: 15px;
            position: relative;
        }

        h1 {
            font-size: 2em;
            margin-bottom: 5px;
            text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.5);
            background: linear-gradient(45deg, #ff6b6b, #ffd93d, #6bcf7f);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .device-badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 0.75em;
            font-weight: bold;
            margin-top: 5px;
            background: rgba(255, 255, 255, 0.2);
        }

        .game-area {
            display: flex;
            flex-direction: column;
            gap: 15px;
        }

        .canvas-container {
            position: relative;
            display: flex;
            justify-content: center;
            width: 100%;
        }

        #gameCanvas {
            border: 3px solid rgba(255, 255, 255, 0.3);
            border-radius: 12px;
            background: linear-gradient(180deg, #87CEEB 0%, #B0E0E6 100%);
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.6);
            max-width: 100%;
            height: auto;
            display: block;
        }

        .game-over-overlay {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: rgba(0, 0, 0, 0.95);
            padding: 30px;
            border-radius: 15px;
            text-align: center;
            display: none;
            z-index: 100;
            border: 2px solid rgba(255, 255, 255, 0.3);
            min-width: 280px;
            animation: popIn 0.3s ease-out;
        }

        .game-over-overlay.show {
            display: block;
        }

        @keyframes popIn {
            0% { transform: translate(-50%, -50%) scale(0.5); opacity: 0; }
            100% { transform: translate(-50%, -50%) scale(1); opacity: 1; }
        }

        .winner-text {
            font-size: 1.8em;
            margin-bottom: 15px;
            font-weight: bold;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8);
        }

        .status-bar {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            margin: 5px 0;
        }

        .player-status {
            background: rgba(0, 0, 0, 0.4);
            padding: 10px;
            border-radius: 10px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }

        .player-status h3 {
            margin-bottom: 5px;
            font-size: 0.9em;
            display: flex;
            align-items: center;
            gap: 5px;
        }

        .player1 h3 { color: #ff6b6b; }
        .player2 h3 { color: #4dabf7; }

        .stat-row {
            margin: 3px 0;
            font-size: 0.85em;
        }

        .health-bar, .stamina-bar {
            height: 15px;
            background: rgba(0, 0, 0, 0.5);
            border-radius: 8px;
            overflow: hidden;
            margin-top: 3px;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }

        .health-fill {
            height: 100%;
            background: linear-gradient(90deg, #ff6b6b, #ff8787);
            transition: width 0.3s ease;
            box-shadow: 0 0 8px rgba(255, 107, 107, 0.5);
        }

        .stamina-fill {
            height: 100%;
            background: linear-gradient(90deg, #4dabf7, #74c0fc);
            transition: width 0.3s ease;
            box-shadow: 0 0 8px rgba(77, 171, 247, 0.5);
        }

        .controls {
            background: rgba(0, 0, 0, 0.3);
            padding: 15px;
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }

        .control-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            margin-bottom: 15px;
        }

        .player-controls {
            background: rgba(255, 255, 255, 0.05);
            padding: 12px;
            border-radius: 8px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }

        .player-controls h3 {
            margin-bottom: 8px;
            font-size: 0.95em;
            font-weight: bold;
        }

        .key-list {
            list-style: none;
            font-size: 0.8em;
            line-height: 1.8;
        }

        .key {
            display: inline-block;
            background: rgba(255, 255, 255, 0.2);
            padding: 2px 6px;
            border-radius: 4px;
            font-weight: bold;
            margin-right: 4px;
            min-width: 20px;
            text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.3);
        }

        .buttons {
            display: flex;
            gap: 8px;
            justify-content: center;
            flex-wrap: wrap;
        }

        button {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border: none;
            padding: 10px 16px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 0.9em;
            font-weight: bold;
            transition: all 0.2s;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
            border: 1px solid rgba(255, 255, 255, 0.2);
            flex: 1;
            min-width: 100px;
        }

        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 16px rgba(0, 0, 0, 0.4);
        }

        button:active {
            transform: translateY(0);
        }

        button.danger {
            background: linear-gradient(135deg, #ff6b6b, #ee5a24);
        }

        .instructions {
            background: rgba(255, 255, 255, 0.1);
            padding: 12px;
            border-radius: 8px;
            margin-top: 10px;
            font-size: 0.85em;
            line-height: 1.6;
            border: 1px solid rgba(255, 255, 255, 0.15);
        }

        .instructions strong {
            color: #ffd93d;
        }

        /* 虚拟按键 - 仅在移动端显示 */
        .virtual-controls {
            display: none;
            margin-top: 10px;
            gap: 10px;
            flex-direction: column;
        }

        .virtual-controls.show {
            display: flex;
        }

        .virtual-row {
            display: flex;
            gap: 8px;
            justify-content: center;
            width: 100%;
        }

        .virtual-btn {
            background: rgba(255, 255, 255, 0.2);
            border: 2px solid rgba(255, 255, 255, 0.4);
            color: white;
            padding: 15px;
            border-radius: 12px;
            font-size: 1.2em;
            font-weight: bold;
            cursor: pointer;
            user-select: none;
            touch-action: manipulation;
            flex: 1;
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 50px;
            transition: all 0.1s;
        }

        .virtual-btn:active {
            background: rgba(255, 255, 255, 0.4);
            transform: scale(0.95);
        }

        .virtual-btn.attack {
            background: linear-gradient(135deg, #ff6b6b, #ee5a24);
            border-color: #ff6b6b;
        }

        .virtual-btn.jump {
            background: linear-gradient(135deg, #6bcf7f, #48bb78);
            border-color: #6bcf7f;
        }

        .virtual-btn.move {
            background: linear-gradient(135deg, #4dabf7, #3b82f6);
            border-color: #4dabf7;
        }

        .virtual-btn.special {
            background: linear-gradient(135deg, #ffd93d, #ff6b6b);
            border-color: #ffd93d;
            color: #000;
        }

        .notification {
            position: fixed;
            top: 20px;
            right: 20px;
            background: rgba(0, 0, 0, 0.9);
            padding: 12px 18px;
            border-radius: 8px;
            border-left: 4px solid #ffd93d;
            transform: translateX(400px);
            transition: transform 0.3s ease;
            z-index: 1000;
            max-width: 280px;
            font-size: 0.9em;
        }

        .notification.show {
            transform: translateX(0);
        }

        .combo-indicator {
            text-align: center;
            font-weight: bold;
            font-size: 1.1em;
            color: #ffd93d;
            text-shadow: 0 0 10px rgba(255, 217, 61, 0.8);
            height: 25px;
            display: flex;
            align-items: center;
            justify-content: center;
            animation: comboShake 0.3s ease;
        }

        @keyframes comboShake {
            0%, 100% { transform: translateX(0); }
            25% { transform: translateX(-5px); }
            75% { transform: translateX(5px); }
        }

        /* 响应式设计 */
        @media (max-width: 768px) {
            .control-grid {
                grid-template-columns: 1fr;
            }

            .status-bar {
                grid-template-columns: 1fr;
            }

            h1 {
                font-size: 1.5em;
            }

            .container {
                padding: 10px;
            }

            .game-over-overlay {
                padding: 20px;
                min-width: 240px;
            }

            .winner-text {
                font-size: 1.4em;
            }

            button {
                padding: 8px 12px;
                font-size: 0.85em;
            }

            .virtual-btn {
                padding: 12px;
                font-size: 1em;
                min-height: 45px;
            }
        }

        /* 模式指示器 */
        .mode-indicator {
            position: absolute;
            top: 10px;
            left: 10px;
            background: rgba(0, 0, 0, 0.7);
            padding: 6px 12px;
            border-radius: 6px;
            font-size: 0.8em;
            font-weight: bold;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }

        .mode-indicator.ai {
            background: rgba(255, 107, 107, 0.8);
        }

        .mode-indicator.hardcore {
            background: rgba(0, 0, 0, 0.9);
            border-color: #ff6b6b;
            color: #ff6b6b;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔥 火柴人对战 - 创意增强版 🔥</h1>
            <span class="device-badge" id="deviceBadge">检测中...</span>
        </div>

        <div class="game-area">
            <div class="canvas-container">
                <canvas id="gameCanvas" width="800" height="500"></canvas>
                <div id="gameOverOverlay" class="game-over-overlay">
                    <div class="winner-text" id="winnerText"></div>
                    <div style="margin-top: 15px;">
                        <button onclick="resetGame()">🔄 再战一局</button>
                    </div>
                </div>
                <div id="modeIndicator" class="mode-indicator" style="display: none;"></div>
            </div>

            <div class="status-bar">
                <div class="player-status player1">
                    <h3>🔴 玩家1</h3>
                    <div class="stat-row">生命: <span id="p1Health">100</span></div>
                    <div class="health-bar">
                        <div class="health-fill" id="p1HealthBar" style="width: 100%"></div>
                    </div>
                    <div class="stat-row">体力: <span id="p1Stamina">100</span></div>
                    <div class="stamina-bar">
                        <div class="stamina-fill" id="p1StaminaBar" style="width: 100%"></div>
                    </div>
                </div>

                <div class="player-status player2">
                    <h3>🔵 玩家2</h3>
                    <div class="stat-row">生命: <span id="p2Health">100</span></div>
                    <div class="health-bar">
                        <div class="health-fill" id="p2HealthBar" style="width: 100%"></div>
                    </div>
                    <div class="stat-row">体力: <span id="p2Stamina">100</span></div>
                    <div class="stamina-bar">
                        <div class="stamina-fill" id="p2StaminaBar" style="width: 100%"></div>
                    </div>
                </div>
            </div>

            <div class="combo-indicator" id="comboIndicator"></div>

            <div class="controls">
                <div class="control-grid">
                    <div class="player-controls player1">
                        <h3>玩家1 控制</h3>
                        <ul class="key-list">
                            <li><span class="key">W</span> 跳跃 <span class="key">A/D</span> 移动</li>
                            <li><span class="key">F</span> 出拳 <span class="key">G</span> 踢腿</li>
                        </ul>
                    </div>
                    <div class="player-controls player2">
                        <h3>玩家2 控制</h3>
                        <ul class="key-list">
                            <li><span class="key">↑</span> 跳跃 <span class="key">←/→</span> 移动</li>
                            <li><span class="key">J</span> 出拳 <span class="key">K</span> 踢腿</li>
                        </ul>
                    </div>
                </div>

                <div class="buttons">
                    <button onclick="resetGame()">🔄 重新开始</button>
                    <button onclick="togglePause()">⏸️ 暂停</button>
                    <button onclick="toggleAI()" id="aiBtn">🤖 AI对战</button>
                    <button class="danger" onclick="toggleHardcore()" id="hardcoreBtn">💀 硬核</button>
                </div>

                <!-- 虚拟按键 - 手机端显示 -->
                <div id="virtualControls" class="virtual-controls">
                    <div style="text-align: center; margin-bottom: 5px; font-size: 0.9em; opacity: 0.8;">
                        📱 虚拟按键模式
                    </div>
                    <!-- 玩家1 虚拟按键 -->
                    <div style="font-size: 0.85em; opacity: 0.9; margin-top: 5px;">玩家1 (红色)</div>
                    <div class="virtual-row">
                        <div class="virtual-btn move" data-key="a">←</div>
                        <div class="virtual-btn jump" data-key="w">↑</div>
                        <div class="virtual-btn move" data-key="d">→</div>
                    </div>
                    <div class="virtual-row">
                        <div class="virtual-btn attack" data-key="f">👊</div>
                        <div class="virtual-btn attack" data-key="g">🦶</div>
                    </div>

                    <!-- 玩家2 虚拟按键 -->
                    <div style="font-size: 0.85em; opacity: 0.9; margin-top: 10px;">玩家2 (蓝色)</div>
                    <div class="virtual-row">
                        <div class="virtual-btn move" data-key="ArrowLeft">←</div>
                        <div class="virtual-btn jump" data-key="ArrowUp">↑</div>
                        <div class="virtual-btn move" data-key="ArrowRight">→</div>
                    </div>
                    <div class="virtual-row">
                        <div class="virtual-btn attack" data-key="j">👊</div>
                        <div class="virtual-btn attack" data-key="k">🦶</div>
                    </div>
                </div>
            </div>

            <div class="instructions">
                <strong>🎯 游戏说明：</strong> 将对手的生命值降至0即可获胜！
                <div style="margin-top: 5px; opacity: 0.9;">
                    💡 <strong>技巧：</strong> 连续攻击可累积连击！体力会自动恢复。
                    硬核模式下伤害翻倍，体力恢复减半！
                </div>
            </div>
        </div>
    </div>

    <div id="notification" class="notification"></div>

    <script>
        // 游戏配置
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');

        // 适配移动端画布大小
        function resizeCanvas() {
            const container = canvas.parentElement;
            const containerWidth = container.clientWidth - 10;
            const maxWidth = 800;
            const scale = Math.min(1, containerWidth / maxWidth);
            canvas.style.width = (800 * scale) + 'px';
            canvas.style.height = (500 * scale) + 'px';
        }
        window.addEventListener('resize', resizeCanvas);
        resizeCanvas();

        // 游戏状态
        let gameState = {
            player1: null,
            player2: null,
            gameOver: false,
            paused: false,
            winner: null,
            soundEnabled: true,
            aiEnabled: false,
            hardcoreMode: false,
            isMobile: false,
            stats: {
                p1: { hits: 0, damage: 0, maxCombo: 0 },
                p2: { hits: 0, damage: 0, maxCombo: 0 }
            }
        };

        // 键盘/触摸状态
        const keys = {};

        // 音效模拟（Web Audio API）
        let audioContext = null;

        function initAudio() {
            if (!audioContext) {
                audioContext = new (window.AudioContext || window.webkitAudioContext)();
            }
        }

        function playSound(type) {
            if (!gameState.soundEnabled || !audioContext) return;

            try {
                const oscillator = audioContext.createOscillator();
                const gainNode = audioContext.createGain();

                oscillator.connect(gainNode);
                gainNode.connect(audioContext.destination);

                switch(type) {
                    case 'punch':
                        oscillator.frequency.value = 150;
                        gainNode.gain.setValueAtTime(0.1, audioContext.currentTime);
                        gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.1);
                        break;
                    case 'kick':
                        oscillator.frequency.value = 80;
                        gainNode.gain.setValueAtTime(0.15, audioContext.currentTime);
                        gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.15);
                        break;
                    case 'hit':
                        oscillator.frequency.value = 100;
                        gainNode.gain.setValueAtTime(0.12, audioContext.currentTime);
                        gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.1);
                        break;
                    case 'win':
                        oscillator.frequency.value = 400;
                        gainNode.gain.setValueAtTime(0.15, audioContext.currentTime);
                        gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.5);
                        break;
                }

                oscillator.start(audioContext.currentTime);
                oscillator.stop(audioContext.currentTime + 0.5);
            } catch(e) {
                // 静默处理音频错误
            }
        }

        // 显示通知
        function showNotification(message, duration = 1500) {
            const notif = document.getElementById('notification');
            notif.textContent = message;
            notif.classList.add('show');
            setTimeout(() => {
                notif.classList.remove('show');
            }, duration);
        }

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

                this.combo = 0;
                this.comboTimer = 0;
                this.comboMultiplier = 1;

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
                    playSound('punch');
                }

                if (this.attackCooldown === 0) {
                    if (keys[this.controls.punch]) {
                        this.punch();
                    } else if (keys[this.controls.kick]) {
                        this.kick();
                    }
                }
            }

            // AI控制
            aiControl(target) {
                if (this.attackCooldown > 0) return;

                const distance = Math.abs(this.x - target.x);
                const isTargetLeft = target.x < this.x;

                // 移动逻辑
                if (distance > 80) {
                    if (isTargetLeft) {
                        this.vx = -this.speed;
                        this.facingRight = false;
                    } else {
                        this.vx = this.speed;
                        this.facingRight = true;
                    }
                } else if (distance < 40) {
                    if (isTargetLeft) {
                        this.vx = this.speed;
                        this.facingRight = true;
                    } else {
                        this.vx = -this.speed;
                        this.facingRight = false;
                    }
                }

                // 跳跃躲避
                if (target.isPunching || target.isKicking) {
                    if (this.onGround && Math.random() > 0.7) {
                        this.vy = -this.jumpPower;
                        this.onGround = false;
                    }
                }

                // 攻击逻辑
                if (distance < 70 && this.stamina > 20) {
                    if (Math.random() > 0.5) {
                        this.punch();
                    } else {
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
                    playSound('punch');
                }
            }

            kick() {
                if (this.stamina >= 15) {
                    this.isKicking = true;
                    this.attackCooldown = 25;
                    this.stamina -= 15;
                    this.animationTimer = 0;
                    playSound('kick');
                }
            }

            takeDamage(damage, attacker = null) {
                if (this.hitCooldown === 0) {
                    const finalDamage = gameState.hardcoreMode ? damage * 2 : damage;
                    this.health -= finalDamage;
                    this.hitCooldown = 30;

                    if (this.health < 0) this.health = 0;

                    // 更新统计
                    if (attacker) {
                        gameState.stats[`p${attacker.playerNum}`].hits++;
                        gameState.stats[`p${attacker.playerNum}`].damage += finalDamage;

                        // 连击系统
                        attacker.combo++;
                        attacker.comboTimer = 60;
                        attacker.comboMultiplier = Math.min(1 + (attacker.combo * 0.1), 2.0);

                        if (attacker.combo > gameState.stats[`p${attacker.playerNum}`].maxCombo) {
                            gameState.stats[`p${attacker.playerNum}`].maxCombo = attacker.combo;
                        }

                        // 连击提示
                        if (attacker.combo >= 3 && attacker.combo % 3 === 0) {
                            showNotification(`玩家${attacker.playerNum} ${attacker.combo}连击! 🔥`, 800);
                            const comboEl = document.getElementById('comboIndicator');
                            comboEl.textContent = `🔥 ${attacker.combo} 连击! 🔥`;
                            comboEl.style.display = 'flex';
                            setTimeout(() => {
                                comboEl.textContent = '';
                                comboEl.style.display = 'none';
                            }, 800);
                        }
                    }

                    playSound('hit');
                    return true;
                }
                return false;
            }

            getAttackHitbox() {
                if (this.isPunching) {
                    const reach = 40;
                    return this.facingRight
                        ? { x: this.x + this.width, y: this.y + 15, w: reach, h: 30 }
                        : { x: this.x - reach, y: this.y + 15, w: reach, h: 30 };
                } else if (this.isKicking) {
                    const reach = 50;
                    return this.facingRight
                        ? { x: this.x + this.width, y: this.y + 30, w: reach, h: 40 }
                        : { x: this.x - reach, y: this.y + 30, w: reach, h: 40 };
                }
                return null;
            }

            update() {
                // AI控制
                if (gameState.aiEnabled && this.playerNum === 2 && !gameState.gameOver) {
                    this.aiControl(gameState.player1);
                }

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

                // 连击计时
                if (this.comboTimer > 0) {
                    this.comboTimer--;
                    if (this.comboTimer === 0) {
                        this.combo = 0;
                        this.comboMultiplier = 1;
                    }
                }

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
                const staminaRegen = gameState.hardcoreMode ? 0.1 : 0.2;
                if (this.stamina < 100) {
                    this.stamina += staminaRegen;
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
                ctx.lineWidth = 3.5;
                ctx.lineCap = 'round';

                // 特殊效果
                if (this.combo >= 5) {
                    ctx.shadowBlur = 10;
                    ctx.shadowColor = this.color;
                } else {
                    ctx.shadowBlur = 0;
                }

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
                    ctx.beginPath();
                    ctx.moveTo(bodyX, armY);
                    ctx.lineTo(bodyX + 12 + punchOffset, armY);
                    ctx.stroke();

                    ctx.beginPath();
                    ctx.moveTo(bodyX, armY);
                    ctx.lineTo(bodyX - 8, armY + 4);
                    ctx.stroke();
                } else {
                    ctx.beginPath();
                    ctx.moveTo(bodyX, armY);
                    ctx.lineTo(bodyX - 12 - punchOffset, armY);
                    ctx.stroke();

                    ctx.beginPath();
                    ctx.moveTo(bodyX, armY);
                    ctx.lineTo(bodyX + 8, armY + 4);
                    ctx.stroke();
                }

                ctx.shadowBlur = 0;
            }
        }

        // 碰撞检测
        function checkHit(hitbox, target) {
            if (!hitbox) return false;
            return hitbox.x < target.x + target.width &&
                   hitbox.x + hitbox.w > target.x &&
                   hitbox.y < target.y + target.height &&
                   hitbox.y + hitbox.h > target.y;
        }

        // 绘制背景
        function drawBackground() {
            // 天空渐变
            const gradient = ctx.createLinearGradient(0, 0, 0, canvas.height);
            gradient.addColorStop(0, '#87CEEB');
            gradient.addColorStop(1, '#B0E0E6');
            ctx.fillStyle = gradient;
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            // 太阳
            ctx.beginPath();
            ctx.arc(750, 70, 20, 0, Math.PI * 2);
            ctx.fillStyle = '#FFD700';
            ctx.fill();
            ctx.strokeStyle = '#FFA500';
            ctx.lineWidth = 2;
            ctx.stroke();

            // 云朵
            ctx.fillStyle = 'rgba(255, 255, 255, 0.9)';
            drawCloud(150, 80);
            drawCloud(500, 60);
            drawCloud(650, 90);

            // 地面
            const groundY = canvas.height - 80;
            ctx.fillStyle = '#654321';
            ctx.fillRect(0, groundY, canvas.width, 80);

            // 地面纹理
            ctx.strokeStyle = '#4a3319';
            ctx.lineWidth = 1.5;
            for (let i = 0; i < canvas.width; i += 12) {
                ctx.beginPath();
                ctx.moveTo(i, groundY);
                ctx.lineTo(i, groundY + 10);
                ctx.stroke();
            }

            // 地面阴影
            ctx.fillStyle = 'rgba(0, 0, 0, 0.2)';
            ctx.fillRect(0, groundY + 10, canvas.width, 70);
        }

        function drawCloud(x, y) {
            ctx.beginPath();
            ctx.arc(x, y, 18, 0, Math.PI * 2);
            ctx.arc(x + 15, y - 6, 22, 0, Math.PI * 2);
            ctx.arc(x + 30, y, 18, 0, Math.PI * 2);
            ctx.fill();
        }

        // 更新UI
        function updateUI() {
            if (!gameState.player1 || !gameState.player2) return;

            const p1 = gameState.player1;
            const p2 = gameState.player2;

            document.getElementById('p1Health').textContent = Math.round(p1.health);
            document.getElementById('p1Stamina').textContent = Math.round(p1.stamina);
            document.getElementById('p1HealthBar').style.width = p1.health + '%';
            document.getElementById('p1StaminaBar').style.width = p1.stamina + '%';

            document.getElementById('p2Health').textContent = Math.round(p2.health);
            document.getElementById('p2Stamina').textContent = Math.round(p2.stamina);
            document.getElementById('p2HealthBar').style.width = p2.health + '%';
            document.getElementById('p2StaminaBar').style.width = p2.stamina + '%';
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
            gameState.player1.update();
            gameState.player2.update();

            // 碰撞检测
            const hitbox1 = gameState.player1.getAttackHitbox();
            if (hitbox1) {
                let damage = gameState.player1.isPunching ? 8 : 12;
                damage = Math.floor(damage * gameState.player1.comboMultiplier);

                if (checkHit(hitbox1, gameState.player2)) {
                    if (gameState.player2.takeDamage(damage, gameState.player1)) {
                        const knockback = gameState.player1.isKicking ? 5 : 3;
                        gameState.player2.vx = gameState.player1.facingRight ? knockback : -knockback;
                    }
                }
            }

            const hitbox2 = gameState.player2.getAttackHitbox();
            if (hitbox2) {
                let damage = gameState.player2.isPunching ? 8 : 12;
                damage = Math.floor(damage * gameState.player2.comboMultiplier);

                if (checkHit(hitbox2, gameState.player1)) {
                    if (gameState.player1.takeDamage(damage, gameState.player2)) {
                        const knockback = gameState.player2.isKicking ? 5 : 3;
                        gameState.player1.vx = gameState.player2.facingRight ? knockback : -knockback;
                    }
                }
            }

            // 检查游戏结束
            if (gameState.player1.health <= 0) {
                gameState.gameOver = true;
                gameState.winner = 2;
                showGameOver();
                playSound('win');
            } else if (gameState.player2.health <= 0) {
                gameState.gameOver = true;
                gameState.winner = 1;
                showGameOver();
                playSound('win');
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
            const winnerName = gameState.winner === 1 ? '玩家1' : '玩家2';

            winnerText.innerHTML = `🎉 <span style="color: ${winnerColor}">${winnerName}</span> 获胜！🎉`;
            overlay.classList.add('show');
        }

        function resetGame() {
            const health = gameState.hardcoreMode ? 75 : 100;
            const stamina = gameState.hardcoreMode ? 80 : 100;

            gameState.player1 = new Stickman(150, 200, '#ff6b6b', {
                left: 'a', right: 'd', jump: 'w', punch: 'f', kick: 'g'
            }, 1);
            gameState.player1.health = health;
            gameState.player1.stamina = stamina;

            gameState.player2 = new Stickman(620, 200, '#4dabf7', {
                left: 'ArrowLeft', right: 'ArrowRight', jump: 'ArrowUp', punch: 'j', kick: 'k'
            }, 2);
            gameState.player2.health = health;
            gameState.player2.stamina = stamina;

            gameState.gameOver = false;
            gameState.paused = false;
            gameState.winner = null;

            // 重置统计
            gameState.stats = {
                p1: { hits: 0, damage: 0, maxCombo: 0 },
                p2: { hits: 0, damage: 0, maxCombo: 0 }
            };

            document.getElementById('gameOverOverlay').classList.remove('show');
            document.getElementById('comboIndicator').textContent = '';
            document.getElementById('comboIndicator').style.display = 'none';
            updateUI();

            if (gameState.aiEnabled) {
                showNotification('🤖 AI对战模式已启用！', 1500);
            }
            if (gameState.hardcoreMode) {
                showNotification('💀 硬核模式开启！伤害翻倍！', 1500);
            }
        }

        function togglePause() {
            gameState.paused = !gameState.paused;
            showNotification(gameState.paused ? '⏸️ 游戏暂停' : '▶️ 游戏继续', 1000);
        }

        function toggleAI() {
            gameState.aiEnabled = !gameState.aiEnabled;
            const btn = document.getElementById('aiBtn');
            btn.textContent = gameState.aiEnabled ? '🤖 AI: 开启' : '🤖 AI对战';
            btn.style.background = gameState.aiEnabled ?
                'linear-gradient(135deg, #ff6b6b, #ee5a24)' :
                'linear-gradient(135deg, #667eea, #764ba2)';

            updateModeIndicator();
            showNotification(`AI对战: ${gameState.aiEnabled ? '开启' : '关闭'}`, 1500);
        }

        function toggleHardcore() {
            gameState.hardcoreMode = !gameState.hardcoreMode;
            const btn = document.getElementById('hardcoreBtn');
            btn.style.background = gameState.hardcoreMode ?
                'linear-gradient(135deg, #000, #ff6b6b)' :
                'linear-gradient(135deg, #ff6b6b, #ee5a24)';

            updateModeIndicator();
            showNotification(
                gameState.hardcoreMode ? '💀 硬核模式已开启！' : '✨ 普通模式已恢复',
                1500
            );
        }

        function updateModeIndicator() {
            const indicator = document.getElementById('modeIndicator');
            if (gameState.aiEnabled || gameState.hardcoreMode) {
                let text = '';
                if (gameState.aiEnabled) text += '🤖 AI ';
                if (gameState.hardcoreMode) text += '💀 硬核';
                indicator.textContent = text;
                indicator.style.display = 'block';
                indicator.className = 'mode-indicator ' + (gameState.aiEnabled ? 'ai' : '') + (gameState.hardcoreMode ? ' hardcore' : '');
            } else {
                indicator.style.display = 'none';
            }
        }

        // 设备检测
        function detectDevice() {
            const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) || window.innerWidth < 768;
            gameState.isMobile = isMobile;

            const badge = document.getElementById('deviceBadge');
            const virtualControls = document.getElementById('virtualControls');

            if (isMobile) {
                badge.textContent = '📱 手机端';
                badge.style.background = 'linear-gradient(45deg, #ff6b6b, #ff8e53)';
                virtualControls.classList.add('show');
                showNotification('📱 检测到手机端，已启用虚拟按键！', 2000);
            } else {
                badge.textContent = '💻 电脑端';
                badge.style.background = 'linear-gradient(45deg, #4dabf7, #74c0fc)';
            }
        }

        // 虚拟按键处理
        function setupVirtualControls() {
            const buttons = document.querySelectorAll('.virtual-btn');

            buttons.forEach(btn => {
                // 触摸事件
                btn.addEventListener('touchstart', (e) => {
                    e.preventDefault();
                    const key = btn.dataset.key;
                    keys[key] = true;
                    initAudio(); // 用户交互时初始化音频
                });

                btn.addEventListener('touchend', (e) => {
                    e.preventDefault();
                    const key = btn.dataset.key;
                    keys[key] = false;
                });

                // 鼠标事件（用于测试）
                btn.addEventListener('mousedown', (e) => {
                    e.preventDefault();
                    const key = btn.dataset.key;
                    keys[key] = true;
                    initAudio();
                });

                btn.addEventListener('mouseup', (e) => {
                    e.preventDefault();
                    const key = btn.dataset.key;
                    keys[key] = false;
                });

                btn.addEventListener('mouseleave', (e) => {
                    const key = btn.dataset.key;
                    keys[key] = false;
                });
            });
        }

        // 键盘事件
        window.addEventListener('keydown', (e) => {
            keys[e.key.toLowerCase()] = true;
            keys[e.key] = true;
            initAudio(); // 用户交互时初始化音频

            // 防止方向键滚动页面
            if (['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight', ' '].includes(e.key)) {
                e.preventDefault();
            }

            // 快捷键
            if (e.key === 'Escape') togglePause();
            if (e.key === 'r' || e.key === 'R') resetGame();
        });

        window.addEventListener('keyup', (e) => {
            keys[e.key.toLowerCase()] = false;
            keys[e.key] = false;
        });

        // 初始化
        window.addEventListener('load', () => {
            detectDevice();
            setupVirtualControls();
            resetGame();
            gameLoop();
            showNotification('🎮 游戏加载完成！按 R 重新开始', 2000);
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/health')
def health():
    return jsonify({
        "status": "healthy",
        "service": "stickman-fighter-enhanced",
        "version": "2.0",
        "features": ["mobile_support", "virtual_controls", "combo_system", "ai_mode", "hardcore_mode", "sound_effects"]
    })

@app.route('/api/stats')
def stats():
    return jsonify({
        "game": "Stickman Fighter Enhanced",
        "version": "2.0",
        "description": "火柴人对战游戏 - 创意增强版",
        "features": [
            "双人对战",
            "手机端支持",
            "虚拟按键",
            "连击系统",
            "AI对战模式",
            "硬核模式",
            "音效系统",
            "增强图形"
        ]
    })

@app.route('/api/help')
def help():
    return jsonify({
        "controls": {
            "player1": {
                "move": "W/A/D",
                "attack": "F=拳, G=踢腿"
            },
            "player2": {
                "move": "↑/←/→",
                "attack": "J=拳, K=踢腿"
            },
            "global": {
                "pause": "ESC",
                "reset": "R",
                "toggle_ai": "点击AI按钮",
                "toggle_hardcore": "点击硬核按钮"
            }
        },
        "mobile": {
            "virtual_controls": "自动显示在手机端",
            "touch": "点击虚拟按钮进行操作"
        },
        "game_mechanics": {
            "punch": "8伤害, 消耗10体力",
            "kick": "12伤害, 消耗15体力",
            "combo": "连续攻击提升伤害(最高2倍)",
            "hardcore": "伤害翻倍, 体力恢复减半"
        }
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"🚀 启动服务器: http://localhost:{port}")
    print("=" * 60)
    print("🔥 火柴人对战 - 创意增强版")
    print("=" * 60)
    print("🎮 特性:")
    print("  ✅ 手机端支持 + 虚拟按键")
    print("  ✅ 连击系统")
    print("  ✅ AI对战模式")
    print("  ✅ 硬核模式")
    print("  ✅ 音效系统")
    print("  ✅ 增强图形")
    print("=" * 60)
    print(f"📱 访问: http://localhost:{port}")
    print("=" * 60)
    app.run(host='0.0.0.0', port=port, debug=False)
