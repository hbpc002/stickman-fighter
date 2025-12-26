#!/usr/bin/env python3
"""
🔥 火柴人对战游戏 - 横屏移动优化版
专为手机端优化的横屏显示，透明虚拟按键覆盖在画面上方
"""

from flask import Flask, render_template_string, request, jsonify
import os

app = Flask(__name__)

# 横屏优化版HTML模板 - 透明虚拟按键在画面上方
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <title>🔥 火柴人对战 - 横屏版</title>
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
            overflow: hidden;
            touch-action: manipulation;
            height: 100vh;
            width: 100vw;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        /* 横屏提示 */
        .portrait-warning {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.95);
            z-index: 9999;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            color: white;
            text-align: center;
            padding: 20px;
        }

        .portrait-warning.show {
            display: flex;
        }

        .portrait-warning h2 {
            font-size: 2em;
            margin-bottom: 20px;
            color: #ffd93d;
        }

        .portrait-warning p {
            font-size: 1.2em;
            opacity: 0.8;
        }

        .portrait-warning .icon {
            font-size: 4em;
            margin-bottom: 20px;
            animation: rotate 1s infinite;
        }

        @keyframes rotate {
            0%, 100% { transform: rotate(0deg); }
            25% { transform: rotate(90deg); }
        }

        /* 主容器 - 横屏优化 */
        .main-container {
            width: 100vw;
            height: 100vh;
            display: flex;
            flex-direction: row;
            align-items: center;
            justify-content: center;
            padding: 10px;
            gap: 10px;
        }

        /* 游戏区域容器 */
        .game-section {
            flex: 1;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            max-width: 70%;
            height: 100%;
            position: relative;
        }

        /* 画布容器 - 相对定位用于放置透明按键 */
        .canvas-wrapper {
            position: relative;
            display: flex;
            align-items: center;
            justify-content: center;
            width: 100%;
            height: 100%;
            max-height: 80vh;
        }

        #gameCanvas {
            border: 3px solid rgba(255, 255, 255, 0.3);
            border-radius: 12px;
            background: linear-gradient(180deg, #87CEEB 0%, #B0E0E6 100%);
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.6);
            max-width: 100%;
            max-height: 100%;
            display: block;
        }

        /* 透明虚拟按键 - 覆盖在画面上方 */
        .transparent-virtual-controls {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 10;
            display: none;
        }

        .transparent-virtual-controls.show {
            display: block;
        }

        /* 按键区域 - 上半部分 */
        .control-overlay-top {
            position: absolute;
            top: 10px;
            left: 50%;
            transform: translateX(-50%);
            width: 90%;
            display: flex;
            flex-direction: column;
            gap: 8px;
            pointer-events: auto;
        }

        .control-row {
            display: flex;
            gap: 8px;
            justify-content: center;
            width: 100%;
        }

        /* 透明按钮样式 */
        .transparent-btn {
            background: rgba(255, 255, 255, 0.15);
            border: 2px solid rgba(255, 255, 255, 0.3);
            color: white;
            padding: 12px 16px;
            border-radius: 10px;
            font-size: 1.1em;
            font-weight: bold;
            cursor: pointer;
            user-select: none;
            touch-action: manipulation;
            display: flex;
            align-items: center;
            justify-content: center;
            min-width: 50px;
            transition: all 0.1s;
            backdrop-filter: blur(5px);
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
            flex: 1;
            max-width: 80px;
        }

        .transparent-btn:active {
            background: rgba(255, 255, 255, 0.35);
            transform: scale(0.95);
        }

        .transparent-btn.attack {
            background: rgba(255, 107, 107, 0.25);
            border-color: rgba(255, 107, 107, 0.5);
        }

        .transparent-btn.attack:active {
            background: rgba(255, 107, 107, 0.5);
        }

        .transparent-btn.jump {
            background: rgba(107, 207, 127, 0.25);
            border-color: rgba(107, 207, 127, 0.5);
        }

        .transparent-btn.jump:active {
            background: rgba(107, 207, 127, 0.5);
        }

        .transparent-btn.move {
            background: rgba(77, 171, 247, 0.25);
            border-color: rgba(77, 171, 247, 0.5);
        }

        .transparent-btn.move:active {
            background: rgba(77, 171, 247, 0.5);
        }

        /* 玩家标签 */
        .player-label {
            font-size: 0.75em;
            opacity: 0.8;
            text-align: center;
            margin-bottom: 2px;
            font-weight: bold;
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.8);
        }

        .player-label.p1 { color: #ff6b6b; }
        .player-label.p2 { color: #4dabf7; }

        /* 侧边信息面板 */
        .side-panel {
            width: 280px;
            display: flex;
            flex-direction: column;
            gap: 10px;
            height: 100%;
            overflow-y: auto;
            padding: 10px;
            background: rgba(0, 0, 0, 0.3);
            border-radius: 12px;
            backdrop-filter: blur(10px);
        }

        .header {
            text-align: center;
            padding: 10px;
            background: rgba(0, 0, 0, 0.4);
            border-radius: 8px;
        }

        h1 {
            font-size: 1.3em;
            margin-bottom: 5px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
            background: linear-gradient(45deg, #ff6b6b, #ffd93d, #6bcf7f);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .device-badge {
            display: inline-block;
            padding: 3px 8px;
            border-radius: 8px;
            font-size: 0.7em;
            font-weight: bold;
            background: rgba(255, 255, 255, 0.2);
        }

        .status-bar {
            display: flex;
            flex-direction: column;
            gap: 8px;
        }

        .player-status {
            background: rgba(0, 0, 0, 0.4);
            padding: 8px;
            border-radius: 8px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }

        .player-status h3 {
            margin-bottom: 4px;
            font-size: 0.85em;
            display: flex;
            align-items: center;
            gap: 5px;
        }

        .player1 h3 { color: #ff6b6b; }
        .player2 h3 { color: #4dabf7; }

        .stat-row {
            margin: 2px 0;
            font-size: 0.75em;
        }

        .health-bar, .stamina-bar {
            height: 12px;
            background: rgba(0, 0, 0, 0.5);
            border-radius: 6px;
            overflow: hidden;
            margin-top: 2px;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }

        .health-fill {
            height: 100%;
            background: linear-gradient(90deg, #ff6b6b, #ff8787);
            transition: width 0.3s ease;
            box-shadow: 0 0 6px rgba(255, 107, 107, 0.5);
        }

        .stamina-fill {
            height: 100%;
            background: linear-gradient(90deg, #4dabf7, #74c0fc);
            transition: width 0.3s ease;
            box-shadow: 0 0 6px rgba(77, 171, 247, 0.5);
        }

        .combo-indicator {
            text-align: center;
            font-weight: bold;
            font-size: 0.9em;
            color: #ffd93d;
            text-shadow: 0 0 8px rgba(255, 217, 61, 0.8);
            height: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: rgba(0, 0, 0, 0.3);
            border-radius: 6px;
            padding: 4px;
        }

        .controls {
            background: rgba(0, 0, 0, 0.3);
            padding: 8px;
            border-radius: 8px;
            display: flex;
            flex-direction: column;
            gap: 8px;
        }

        .buttons {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 6px;
        }

        button {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border: none;
            padding: 8px 10px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 0.75em;
            font-weight: bold;
            transition: all 0.2s;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
            border: 1px solid rgba(255, 255, 255, 0.2);
            white-space: nowrap;
        }

        button:hover {
            transform: translateY(-1px);
            box-shadow: 0 3px 10px rgba(0, 0, 0, 0.4);
        }

        button:active {
            transform: translateY(0);
        }

        button.danger {
            background: linear-gradient(135deg, #ff6b6b, #ee5a24);
        }

        .instructions {
            background: rgba(255, 255, 255, 0.1);
            padding: 8px;
            border-radius: 6px;
            font-size: 0.7em;
            line-height: 1.5;
            border: 1px solid rgba(255, 255, 255, 0.15);
        }

        .instructions strong {
            color: #ffd93d;
        }

        /* 游戏结束遮罩 */
        .game-over-overlay {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: rgba(0, 0, 0, 0.95);
            padding: 20px;
            border-radius: 12px;
            text-align: center;
            display: none;
            z-index: 100;
            border: 2px solid rgba(255, 255, 255, 0.3);
            min-width: 240px;
            animation: popIn 0.3s ease-out;
            pointer-events: auto;
        }

        .game-over-overlay.show {
            display: block;
        }

        @keyframes popIn {
            0% { transform: translate(-50%, -50%) scale(0.5); opacity: 0; }
            100% { transform: translate(-50%, -50%) scale(1); opacity: 1; }
        }

        .winner-text {
            font-size: 1.4em;
            margin-bottom: 12px;
            font-weight: bold;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8);
        }

        /* 模式指示器 */
        .mode-indicator {
            position: absolute;
            top: 10px;
            left: 10px;
            background: rgba(0, 0, 0, 0.7);
            padding: 4px 8px;
            border-radius: 6px;
            font-size: 0.7em;
            font-weight: bold;
            border: 1px solid rgba(255, 255, 255, 0.2);
            z-index: 5;
        }

        .mode-indicator.ai {
            background: rgba(255, 107, 107, 0.8);
        }

        .mode-indicator.hardcore {
            background: rgba(0, 0, 0, 0.9);
            border-color: #ff6b6b;
            color: #ff6b6b;
        }

        /* 通知 */
        .notification {
            position: fixed;
            top: 20px;
            right: 20px;
            background: rgba(0, 0, 0, 0.9);
            padding: 10px 15px;
            border-radius: 8px;
            border-left: 4px solid #ffd93d;
            transform: translateX(400px);
            transition: transform 0.3s ease;
            z-index: 1000;
            max-width: 250px;
            font-size: 0.85em;
        }

        .notification.show {
            transform: translateX(0);
        }

        /* 横屏适配 */
        @media (orientation: landscape) and (max-width: 1024px) {
            .side-panel {
                width: 220px;
            }

            h1 {
                font-size: 1.1em;
            }

            .transparent-btn {
                padding: 10px 12px;
                font-size: 1em;
                min-width: 45px;
            }
        }

        /* 竖屏优化 */
        @media (orientation: portrait) {
            .main-container {
                flex-direction: column;
            }

            .side-panel {
                width: 100%;
                max-height: 30vh;
            }

            .game-section {
                max-width: 100%;
                max-height: 60vh;
            }
        }

        /* 小屏幕优化 */
        @media (max-width: 600px) {
            .side-panel {
                width: 100%;
                max-height: 25vh;
            }

            .game-section {
                max-width: 100%;
                max-height: 60vh;
            }

            h1 {
                font-size: 1em;
            }

            .buttons {
                grid-template-columns: 1fr;
            }

            button {
                font-size: 0.7em;
                padding: 6px 8px;
            }
        }
    </style>
</head>
<body>
    <!-- 横屏提示 -->
    <div id="portraitWarning" class="portrait-warning">
        <div class="icon">📱</div>
        <h2>请旋转设备</h2>
        <p>为了获得最佳游戏体验</p>
        <p>请将设备切换到横屏模式</p>
    </div>

    <!-- 主容器 -->
    <div class="main-container">
        <!-- 游戏区域 -->
        <div class="game-section">
            <div class="canvas-wrapper">
                <canvas id="gameCanvas" width="800" height="500"></canvas>

                <!-- 透明虚拟按键 - 覆盖在画面上方 -->
                <div id="transparentVirtualControls" class="transparent-virtual-controls">
                    <div class="control-overlay-top">
                        <!-- 玩家1 按键 -->
                        <div class="player-label p1">🔴 玩家1</div>
                        <div class="control-row">
                            <div class="transparent-btn move" data-key="a">←</div>
                            <div class="transparent-btn jump" data-key="w">↑</div>
                            <div class="transparent-btn move" data-key="d">→</div>
                        </div>
                        <div class="control-row">
                            <div class="transparent-btn attack" data-key="f">👊</div>
                            <div class="transparent-btn attack" data-key="g">🦶</div>
                        </div>

                        <!-- 玩家2 按键 -->
                        <div class="player-label p2" style="margin-top: 8px;">🔵 玩家2</div>
                        <div class="control-row">
                            <div class="transparent-btn move" data-key="ArrowLeft">←</div>
                            <div class="transparent-btn jump" data-key="ArrowUp">↑</div>
                            <div class="transparent-btn move" data-key="ArrowRight">→</div>
                        </div>
                        <div class="control-row">
                            <div class="transparent-btn attack" data-key="j">👊</div>
                            <div class="transparent-btn attack" data-key="k">🦶</div>
                        </div>
                    </div>
                </div>

                <!-- 游戏结束遮罩 -->
                <div id="gameOverOverlay" class="game-over-overlay">
                    <div class="winner-text" id="winnerText"></div>
                    <div style="margin-top: 15px;">
                        <button onclick="resetGame()">🔄 再战一局</button>
                    </div>
                </div>

                <!-- 模式指示器 -->
                <div id="modeIndicator" class="mode-indicator" style="display: none;"></div>
            </div>
        </div>

        <!-- 侧边信息面板 -->
        <div class="side-panel">
            <div class="header">
                <h1>🔥 火柴人对战</h1>
                <span class="device-badge" id="deviceBadge">检测中...</span>
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
                <div class="buttons">
                    <button onclick="resetGame()">🔄 重新开始</button>
                    <button onclick="togglePause()">⏸️ 暂停</button>
                    <button onclick="toggleAI()" id="aiBtn">🤖 AI对战</button>
                    <button class="danger" onclick="toggleHardcore()" id="hardcoreBtn">💀 硬核</button>
                </div>

                <div class="instructions">
                    <strong>🎯 游戏说明：</strong><br>
                    将对手生命降至0获胜！
                    <br><br>
                    <strong>💡 技巧：</strong><br>
                    连续攻击累积连击，伤害最高2倍！
                    <br><br>
                    <strong>📱 手机端：</strong><br>
                    虚拟按键透明显示在画面上方
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
            const wrapper = canvas.parentElement;
            const wrapperWidth = wrapper.clientWidth;
            const wrapperHeight = wrapper.clientHeight;

            const originalWidth = 800;
            const originalHeight = 500;
            const aspectRatio = originalWidth / originalHeight;

            let newWidth, newHeight;

            if (wrapperWidth / wrapperHeight > aspectRatio) {
                // 容器更宽，以高度为准
                newHeight = wrapperHeight * 0.95;
                newWidth = newHeight * aspectRatio;
            } else {
                // 容器更高，以宽度为准
                newWidth = wrapperWidth * 0.95;
                newHeight = newWidth / aspectRatio;
            }

            canvas.style.width = newWidth + 'px';
            canvas.style.height = newHeight + 'px';
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

            winnerText.innerHTML = `🎉 <span style=\"color: ${winnerColor}\">${winnerName}</span> 获胜！🎉`;
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

        // 设备检测和横屏检测
        function detectDevice() {
            const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) || window.innerWidth < 768;
            gameState.isMobile = isMobile;

            const badge = document.getElementById('deviceBadge');
            const virtualControls = document.getElementById('transparentVirtualControls');
            const portraitWarning = document.getElementById('portraitWarning');

            if (isMobile) {
                badge.textContent = '📱 手机端';
                badge.style.background = 'linear-gradient(45deg, #ff6b6b, #ff8e53)';
                virtualControls.classList.add('show');
                showNotification('📱 检测到手机端，已启用透明虚拟按键！', 2000);

                // 检查横屏
                checkOrientation();
            } else {
                badge.textContent = '💻 电脑端';
                badge.style.background = 'linear-gradient(45deg, #4dabf7, #74c0fc)';
            }
        }

        // 横屏检测
        function checkOrientation() {
            const isLandscape = window.innerWidth > window.innerHeight;
            const portraitWarning = document.getElementById('portraitWarning');

            if (!isLandscape && gameState.isMobile) {
                portraitWarning.classList.add('show');
            } else {
                portraitWarning.classList.remove('show');
            }
        }

        // 虚拟按键处理
        function setupVirtualControls() {
            const buttons = document.querySelectorAll('.transparent-btn');

            buttons.forEach(btn => {
                // 触摸事件
                btn.addEventListener('touchstart', (e) => {
                    e.preventDefault();
                    const key = btn.dataset.key;
                    keys[key] = true;
                    initAudio();
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
            initAudio();

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

        // 窗口大小改变时检测横屏
        window.addEventListener('resize', () => {
            if (gameState.isMobile) {
                checkOrientation();
            }
            resizeCanvas();
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
        "service": "stickman-fighter-landscape",
        "version": "3.0",
        "features": ["landscape_mode", "transparent_controls", "mobile_optimized", "virtual_buttons_on_canvas"]
    })

@app.route('/api/stats')
def stats():
    return jsonify({
        "game": "Stickman Fighter Landscape Edition",
        "version": "3.0",
        "description": "火柴人对战游戏 - 横屏移动优化版",
        "features": [
            "横屏模式优化",
            "透明虚拟按键覆盖在画面上方",
            "手机端专用布局",
            "自动横屏检测",
            "连击系统",
            "AI对战模式",
            "硬核模式"
        ]
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"🚀 启动服务器: http://localhost:{port}")
    print("=" * 60)
    print("🔥 火柴人对战 - 横屏移动优化版")
    print("=" * 60)
    print("🎮 特性:")
    print("  ✅ 横屏模式优化")
    print("  ✅ 透明虚拟按键（覆盖在画面上方）")
    print("  ✅ 手机端专用布局")
    print("  ✅ 自动横屏检测提示")
    print("  ✅ 连击系统 + AI对战 + 硬核模式")
    print("=" * 60)
    print(f"📱 访问: http://localhost:{port}")
    print("=" * 60)
    app.run(host='0.0.0.0', port=port, debug=False)
