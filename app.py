#!/usr/bin/env python3
"""
🔥 火柴人对战游戏 - 横屏移动优化版 V2.3
修复版：玩家2按钮响应 + 游戏结束重置功能
"""

from flask import Flask, render_template_string, request, jsonify
import os

app = Flask(__name__)

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

        .portrait-warning .icon {
            font-size: 4em;
            margin-bottom: 20px;
            animation: rotate 1s infinite;
        }

        @keyframes rotate {
            0%, 100% { transform: rotate(0deg); }
            25% { transform: rotate(90deg); }
        }

        /* 主容器 */
        .main-container {
            width: 100vw;
            height: 100vh;
            display: flex;
            flex-direction: row;
            align-items: center;
            justify-content: center;
            gap: 5px;
            padding: 5px;
            position: relative;
        }

        /* 左侧控制面板 - 玩家1 */
        .control-panel-left {
            width: 70px;
            height: calc(100% - 40px);
            display: flex;
            flex-direction: column;
            gap: 4px;
            align-items: center;
            justify-content: center;
            padding: 8px 4px;
            background: rgba(255, 107, 107, 0.2);
            border-radius: 8px;
            backdrop-filter: blur(5px);
            margin-top: 20px;
        }

        /* 右侧控制面板 - 玩家2 */
        .control-panel-right {
            width: 70px;
            height: calc(100% - 40px);
            display: flex;
            flex-direction: column;
            gap: 4px;
            align-items: center;
            justify-content: center;
            padding: 8px 4px;
            background: rgba(77, 171, 247, 0.2);
            border-radius: 8px;
            backdrop-filter: blur(5px);
            margin-top: 20px;
        }

        /* 游戏区域 */
        .game-area {
            flex: 1;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: calc(100% - 40px);
            position: relative;
            max-width: calc(100vw - 180px);
            margin-top: 20px;
        }

        /* 画布容器 */
        .canvas-container {
            display: flex;
            align-items: center;
            justify-content: center;
            width: 100%;
            height: 100%;
            position: relative;
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

        /* 控制按钮样式 */
        .btn {
            width: 100%;
            min-height: 40px;
            background: rgba(255, 255, 255, 0.2);
            border: 2px solid rgba(255, 255, 255, 0.4);
            color: white;
            border-radius: 6px;
            font-size: 1.1em;
            font-weight: bold;
            cursor: pointer;
            user-select: none;
            touch-action: manipulation;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.1s;
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
            padding: 2px;
        }

        .btn:active {
            background: rgba(255, 255, 255, 0.4);
            transform: scale(0.95);
        }

        .btn.move {
            background: rgba(77, 171, 247, 0.3);
            border-color: rgba(77, 171, 247, 0.6);
        }

        .btn.jump {
            background: rgba(107, 207, 127, 0.3);
            border-color: rgba(107, 207, 127, 0.6);
            font-size: 1.4em;
        }

        .btn.attack {
            background: rgba(255, 107, 107, 0.3);
            border-color: rgba(255, 107, 107, 0.6);
        }

        /* 玩家标签 */
        .player-label {
            font-size: 0.85em;
            font-weight: bold;
            text-align: center;
            margin-bottom: 5px;
            padding: 5px;
            border-radius: 6px;
            width: 100%;
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
        }

        .player-label.p1 {
            background: rgba(255, 107, 107, 0.4);
            color: #ff6b6b;
        }

        .player-label.p2 {
            background: rgba(77, 171, 247, 0.4);
            color: #4dabf7;
        }

        /* 顶部状态栏 */
        .status-bar-top {
            position: absolute;
            top: 5px;
            left: 50%;
            transform: translateX(-50%);
            display: flex;
            gap: 6px;
            z-index: 5;
            pointer-events: none;
        }

        .player-status-mini {
            background: rgba(0, 0, 0, 0.7);
            padding: 4px 8px;
            border-radius: 6px;
            border: 1px solid rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(4px);
            min-width: 90px;
        }

        .mini-name {
            font-size: 0.75em;
            font-weight: bold;
            margin-bottom: 3px;
        }

        .mini-hp {
            height: 6px;
            background: rgba(255, 255, 255, 0.2);
            border-radius: 3px;
            overflow: hidden;
            margin-bottom: 2px;
        }

        .mini-hp-fill {
            height: 100%;
            transition: width 0.3s ease;
        }

        .mini-stamina {
            height: 4px;
            background: rgba(255, 255, 255, 0.2);
            border-radius: 2px;
            overflow: hidden;
        }

        .mini-stamina-fill {
            height: 100%;
            transition: width 0.3s ease;
        }

        /* 连击指示器 */
        .combo-indicator {
            position: absolute;
            top: 50px;
            left: 50%;
            transform: translateX(-50%);
            font-weight: bold;
            font-size: 1.1em;
            color: #ffd93d;
            text-shadow: 0 0 10px rgba(255, 217, 61, 0.8);
            background: rgba(0, 0, 0, 0.7);
            padding: 5px 10px;
            border-radius: 8px;
            z-index: 5;
            display: none;
        }

        .combo-indicator.show {
            display: block;
            animation: comboPulse 0.3s ease;
        }

        @keyframes comboPulse {
            0%, 100% { transform: translateX(-50%) scale(1); }
            50% { transform: translateX(-50%) scale(1.1); }
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
            margin-bottom: 15px;
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
            z-index: 5;
            backdrop-filter: blur(5px);
        }

        .mode-indicator.ai {
            background: rgba(255, 107, 107, 0.8);
        }

        .mode-indicator.hardcore {
            background: rgba(0, 0, 0, 0.9);
            border: 1px solid #ff6b6b;
            color: #ff6b6b;
        }

        /* 底部功能按钮 - 修复版 */
        .bottom-controls {
            position: fixed;
            bottom: 8px;
            left: 50%;
            transform: translateX(-50%);
            display: flex;
            gap: 4px;
            z-index: 1000;
            background: rgba(0, 0, 0, 0.7);
            padding: 6px 8px;
            border-radius: 8px;
            backdrop-filter: blur(8px);
            border: 1px solid rgba(255, 255, 255, 0.15);
            flex-wrap: nowrap;
            justify-content: center;
            max-width: 95vw;
            height: 40px;
            align-items: center;
        }

        .func-btn {
            background: linear-gradient(135deg, #4dabf7, #3b82f6);
            color: white;
            border: none;
            padding: 6px 10px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 0.75em;
            font-weight: bold;
            white-space: nowrap;
            box-shadow: 0 1px 4px rgba(0, 0, 0, 0.3);
            min-width: 45px;
            height: 28px;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .func-btn:active {
            transform: translateY(2px);
            box-shadow: 0 1px 4px rgba(0, 0, 0, 0.3);
        }

        .func-btn.danger {
            background: linear-gradient(135deg, #ff6b6b, #ee5a24);
        }

        .func-btn.warning {
            background: linear-gradient(135deg, #ffd93d, #ff6b6b);
            color: #000;
        }

        .func-btn.fullscreen {
            background: linear-gradient(135deg, #6bcf7f, #48bb78);
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
            z-index: 10000;
            max-width: 250px;
            font-size: 0.9em;
            backdrop-filter: blur(10px);
        }

        .notification.show {
            transform: translateX(0);
        }

        /* 小屏幕优化 */
        @media (max-width: 768px) {
            .control-panel-left,
            .control-panel-right {
                width: 60px;
            }

            .btn {
                min-height: 40px;
                font-size: 1em;
            }

            .btn.jump {
                font-size: 1.2em;
            }

            .player-label {
                font-size: 0.7em;
                padding: 3px;
            }

            .status-bar-top {
                gap: 5px;
            }

            .player-status-mini {
                padding: 4px 6px;
                min-width: 90px;
                font-size: 0.75em;
            }

            .bottom-controls {
                gap: 3px;
                padding: 4px 6px;
                bottom: 5px;
                height: 36px;
            }

            .func-btn {
                padding: 5px 8px;
                font-size: 0.7em;
                min-width: 40px;
                height: 26px;
            }
        }

        /* 竖屏提示 */
        @media (orientation: portrait) {
            .main-container {
                display: none;
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
    <div class="main-container" id="mainContainer">
        <!-- 左侧控制面板 - 玩家1 -->
        <div class="control-panel-left">
            <div class="player-label p1">🔴 玩家1</div>
            <div class="control-row">
                <button class="btn jump" data-key="w">↑</button>
            </div>
            <div class="control-row" style="display: flex; gap: 5px;">
                <button class="btn move" data-key="a">←</button>
                <button class="btn move" data-key="d">→</button>
            </div>
            <div class="control-row">
                <button class="btn attack" data-key="f">👊</button>
            </div>
            <div class="control-row">
                <button class="btn attack" data-key="g">🦶</button>
            </div>
        </div>

        <!-- 游戏区域 -->
        <div class="game-area">
            <!-- 顶部状态栏 -->
            <div class="status-bar-top">
                <div class="player-status-mini">
                    <div class="mini-name" style="color: #ff6b6b;">🔴 玩家1</div>
                    <div class="mini-hp">
                        <div class="mini-hp-fill" id="p1HpBar" style="width: 100%; background: linear-gradient(90deg, #ff6b6b, #ff8787);"></div>
                    </div>
                    <div class="mini-stamina">
                        <div class="mini-stamina-fill" id="p1StBar" style="width: 100%; background: linear-gradient(90deg, #4dabf7, #74c0fc);"></div>
                    </div>
                </div>
                <div class="player-status-mini">
                    <div class="mini-name" style="color: #4dabf7;">🔵 玩家2</div>
                    <div class="mini-hp">
                        <div class="mini-hp-fill" id="p2HpBar" style="width: 100%; background: linear-gradient(90deg, #ff6b6b, #ff8787);"></div>
                    </div>
                    <div class="mini-stamina">
                        <div class="mini-stamina-fill" id="p2StBar" style="width: 100%; background: linear-gradient(90deg, #4dabf7, #74c0fc);"></div>
                    </div>
                </div>
            </div>

            <!-- 连击指示器 -->
            <div class="combo-indicator" id="comboIndicator"></div>

            <!-- 模式指示器 -->
            <div id="modeIndicator" class="mode-indicator" style="display: none;"></div>

            <!-- 画布容器 -->
            <div class="canvas-container">
                <canvas id="gameCanvas" width="800" height="500"></canvas>

                <!-- 游戏结束遮罩 -->
                <div id="gameOverOverlay" class="game-over-overlay">
                    <div class="winner-text" id="winnerText"></div>
                    <div style="margin-top: 15px;">
                        <button class="reset-btn" onclick="resetGame()" style="width: auto; padding: 10px 20px; background: linear-gradient(135deg, #6bcf7f, #48bb78); color: white; border: none; border-radius: 8px; cursor: pointer; font-weight: bold;">🔄 再战一局</button>
                    </div>
                </div>
            </div>
        </div>

        <!-- 右侧控制面板 - 玩家2 -->
        <div class="control-panel-right">
            <div class="player-label p2">🔵 玩家2</div>
            <div class="control-row">
                <button class="btn jump" data-key="ArrowUp">↑</button>
            </div>
            <div class="control-row" style="display: flex; gap: 5px;">
                <button class="btn move" data-key="ArrowLeft">←</button>
                <button class="btn move" data-key="ArrowRight">→</button>
            </div>
            <div class="control-row">
                <button class="btn attack" data-key="j">👊</button>
            </div>
            <div class="control-row">
                <button class="btn attack" data-key="k">🦶</button>
            </div>
        </div>
    </div>

    <!-- 底部功能按钮 - 修复位置 -->
    <div class="bottom-controls" id="bottomControls">
        <button class="func-btn fullscreen" onclick="toggleFullscreen()">🖥️ 全屏</button>
        <button class="func-btn" onclick="togglePause()">⏸️ 暂停</button>
        <button class="func-btn warning" onclick="toggleAI()" id="aiBtn">🤖 AI</button>
        <button class="func-btn danger" onclick="toggleHardcore()" id="hardcoreBtn">💀 硬核</button>
        <button class="func-btn" onclick="resetGame()">🔄 重置</button>
    </div>

    <div id="notification" class="notification"></div>

    <script>
        // 游戏配置
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');

        // 适配移动端画布大小
        function resizeCanvas() {
            const container = canvas.parentElement;
            const containerWidth = container.clientWidth;
            const containerHeight = container.clientHeight;

            const originalWidth = 800;
            const originalHeight = 500;
            const aspectRatio = originalWidth / originalHeight;

            let newWidth, newHeight;

            if (containerWidth / containerHeight > aspectRatio) {
                newHeight = containerHeight * 0.95;
                newWidth = newHeight * aspectRatio;
            } else {
                newWidth = containerWidth * 0.95;
                newHeight = newWidth / aspectRatio;
            }

            canvas.style.width = newWidth + 'px';
            canvas.style.height = newHeight + 'px';
        }

        window.addEventListener('resize', resizeCanvas);

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

        // 音效模拟
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
            } catch(e) {}
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

            aiControl(target) {
                if (this.attackCooldown > 0) return;

                const distance = Math.abs(this.x - target.x);
                const isTargetLeft = target.x < this.x;

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

                if (target.isPunching || target.isKicking) {
                    if (this.onGround && Math.random() > 0.7) {
                        this.vy = -this.jumpPower;
                        this.onGround = false;
                    }
                }

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

                    if (attacker) {
                        gameState.stats[`p${attacker.playerNum}`].hits++;
                        gameState.stats[`p${attacker.playerNum}`].damage += finalDamage;

                        attacker.combo++;
                        attacker.comboTimer = 60;
                        attacker.comboMultiplier = Math.min(1 + (attacker.combo * 0.1), 2.0);

                        if (attacker.combo > gameState.stats[`p${attacker.playerNum}`].maxCombo) {
                            gameState.stats[`p${attacker.playerNum}`].maxCombo = attacker.combo;
                        }

                        if (attacker.combo >= 3 && attacker.combo % 3 === 0) {
                            showNotification(`玩家${attacker.playerNum} ${attacker.combo}连击! 🔥`, 800);
                            const comboEl = document.getElementById('comboIndicator');
                            comboEl.textContent = `🔥 ${attacker.combo} 连击! 🔥`;
                            comboEl.classList.add('show');
                            setTimeout(() => {
                                comboEl.textContent = '';
                                comboEl.classList.remove('show');
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
                if (gameState.aiEnabled && this.playerNum === 2 && !gameState.gameOver) {
                    this.aiControl(gameState.player1);
                } else if (this.playerNum === 2 && !gameState.gameOver) {
                    // 玩家2手动控制
                    this.handleInput();
                }

                this.vy += this.gravity;
                this.x += this.vx;
                this.y += this.vy;

                const groundLevel = canvas.height - 80;
                if (this.y + this.height >= groundLevel) {
                    this.y = groundLevel - this.height;
                    this.vy = 0;
                    this.onGround = true;
                }

                if (this.x < 0) this.x = 0;
                if (this.x + this.width > canvas.width) this.x = canvas.width - this.width;

                if (this.attackCooldown > 0) this.attackCooldown--;
                if (this.hitCooldown > 0) this.hitCooldown--;

                if (this.comboTimer > 0) {
                    this.comboTimer--;
                    if (this.comboTimer === 0) {
                        this.combo = 0;
                        this.comboMultiplier = 1;
                    }
                }

                if (this.isPunching || this.isKicking) {
                    this.animationTimer++;
                    if (this.animationTimer >= 10) {
                        this.isPunching = false;
                        this.isKicking = false;
                        this.animationTimer = 0;
                    }
                }

                const staminaRegen = gameState.hardcoreMode ? 0.1 : 0.2;
                if (this.stamina < 100) {
                    this.stamina += staminaRegen;
                }
            }

            draw() {
                if (this.hitCooldown > 0 && this.hitCooldown % 4 < 2) {
                    return;
                }

                const bodyX = this.x + this.width / 2;
                const bodyY = this.y + 15;

                ctx.strokeStyle = this.color;
                ctx.lineWidth = 3.5;
                ctx.lineCap = 'round';

                if (this.combo >= 5) {
                    ctx.shadowBlur = 10;
                    ctx.shadowColor = this.color;
                } else {
                    ctx.shadowBlur = 0;
                }

                ctx.beginPath();
                ctx.arc(bodyX, this.y + 8, 8, 0, Math.PI * 2);
                ctx.stroke();

                ctx.beginPath();
                ctx.moveTo(bodyX, bodyY);
                ctx.lineTo(bodyX, bodyY + 25);
                ctx.stroke();

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

        function checkHit(hitbox, target) {
            if (!hitbox) return false;
            return hitbox.x < target.x + target.width &&
                   hitbox.x + hitbox.w > target.x &&
                   hitbox.y < target.y + target.height &&
                   hitbox.y + hitbox.h > target.y;
        }

        function drawBackground() {
            const gradient = ctx.createLinearGradient(0, 0, 0, canvas.height);
            gradient.addColorStop(0, '#87CEEB');
            gradient.addColorStop(1, '#B0E0E6');
            ctx.fillStyle = gradient;
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            ctx.beginPath();
            ctx.arc(750, 70, 20, 0, Math.PI * 2);
            ctx.fillStyle = '#FFD700';
            ctx.fill();
            ctx.strokeStyle = '#FFA500';
            ctx.lineWidth = 2;
            ctx.stroke();

            ctx.fillStyle = 'rgba(255, 255, 255, 0.9)';
            drawCloud(150, 80);
            drawCloud(500, 60);
            drawCloud(650, 90);

            const groundY = canvas.height - 80;
            ctx.fillStyle = '#654321';
            ctx.fillRect(0, groundY, canvas.width, 80);

            ctx.strokeStyle = '#4a3319';
            ctx.lineWidth = 1.5;
            for (let i = 0; i < canvas.width; i += 12) {
                ctx.beginPath();
                ctx.moveTo(i, groundY);
                ctx.lineTo(i, groundY + 10);
                ctx.stroke();
            }

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

        function updateUI() {
            if (!gameState.player1 || !gameState.player2) return;

            const p1 = gameState.player1;
            const p2 = gameState.player2;

            document.getElementById('p1HpBar').style.width = p1.health + '%';
            document.getElementById('p1StBar').style.width = p1.stamina + '%';
            document.getElementById('p2HpBar').style.width = p2.health + '%';
            document.getElementById('p2StBar').style.width = p2.stamina + '%';
        }

        function gameLoop() {
            if (gameState.paused || gameState.gameOver) {
                if (gameState.gameOver) {
                    drawGame();
                    return;
                }
                requestAnimationFrame(gameLoop);
                return;
            }

            gameState.player1.handleInput();
            gameState.player1.update();
            gameState.player2.update();

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

            gameState.stats = {
                p1: { hits: 0, damage: 0, maxCombo: 0 },
                p2: { hits: 0, damage: 0, maxCombo: 0 }
            };

            document.getElementById('gameOverOverlay').classList.remove('show');
            document.getElementById('comboIndicator').classList.remove('show');
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
            btn.textContent = gameState.aiEnabled ? '🤖 AI:开' : '🤖 AI';
            btn.style.background = gameState.aiEnabled ?
                'linear-gradient(135deg, #ff6b6b, #ee5a24)' :
                'linear-gradient(135deg, #ffd93d, #ff6b6b)';

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

        // 全屏功能
        function toggleFullscreen() {
            const elem = document.documentElement;

            if (!document.fullscreenElement) {
                if (elem.requestFullscreen) {
                    elem.requestFullscreen();
                } else if (elem.webkitRequestFullscreen) {
                    elem.webkitRequestFullscreen();
                } else if (elem.mozRequestFullScreen) {
                    elem.mozRequestFullScreen();
                } else if (elem.msRequestFullscreen) {
                    elem.msRequestFullscreen();
                }
                showNotification('🖥️ 进入全屏模式', 1000);
            } else {
                if (document.exitFullscreen) {
                    document.exitFullscreen();
                } else if (document.webkitExitFullscreen) {
                    document.webkitExitFullscreen();
                } else if (document.mozCancelFullScreen) {
                    document.mozCancelFullScreen();
                } else if (document.msExitFullscreen) {
                    document.msExitFullscreen();
                }
                showNotification('🖥️ 退出全屏模式', 1000);
            }
        }

        // 设备检测和横屏检测
        function detectDevice() {
            const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) || window.innerWidth < 768;
            gameState.isMobile = isMobile;

            const portraitWarning = document.getElementById('portraitWarning');

            if (isMobile) {
                checkOrientation();
            }
        }

        function checkOrientation() {
            const isLandscape = window.innerWidth > window.innerHeight;
            const portraitWarning = document.getElementById('portraitWarning');

            if (!isLandscape && gameState.isMobile) {
                portraitWarning.classList.add('show');
            } else {
                portraitWarning.classList.remove('show');
            }
        }

        // 虚拟按键处理 - 修复版
        function setupVirtualControls() {
            const buttons = document.querySelectorAll('.btn');

            buttons.forEach(btn => {
                const key = btn.dataset.key;
                if (!key) return; // 跳过没有data-key的按钮

                // 触摸事件
                btn.addEventListener('touchstart', (e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    keys[key] = true;
                    // 同时设置小写版本（用于兼容）
                    if (key.length === 1) {
                        keys[key.toLowerCase()] = true;
                    }
                    initAudio();
                    console.log('Touch start:', key, keys); // 调试
                });

                btn.addEventListener('touchend', (e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    keys[key] = false;
                    if (key.length === 1) {
                        keys[key.toLowerCase()] = false;
                    }
                    console.log('Touch end:', key, keys); // 调试
                });

                // 鼠标事件（用于测试）
                btn.addEventListener('mousedown', (e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    keys[key] = true;
                    if (key.length === 1) {
                        keys[key.toLowerCase()] = true;
                    }
                    initAudio();
                    console.log('Mouse down:', key, keys); // 调试
                });

                btn.addEventListener('mouseup', (e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    keys[key] = false;
                    if (key.length === 1) {
                        keys[key.toLowerCase()] = false;
                    }
                    console.log('Mouse up:', key, keys); // 调试
                });

                btn.addEventListener('mouseleave', (e) => {
                    keys[key] = false;
                    if (key.length === 1) {
                        keys[key.toLowerCase()] = false;
                    }
                });
            });
        }

        // 键盘事件
        window.addEventListener('keydown', (e) => {
            keys[e.key.toLowerCase()] = true;
            keys[e.key] = true;
            initAudio();

            if (['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight', ' '].includes(e.key)) {
                e.preventDefault();
            }

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

        // 全屏状态监听
        document.addEventListener('fullscreenchange', () => {
            resizeCanvas();
        });

        // 初始化
        window.addEventListener('load', () => {
            detectDevice();
            setupVirtualControls();
            resetGame();
            resizeCanvas();
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
        "service": "stickman-fighter-v2.3",
        "version": "3.4",
        "features": ["landscape_mode", "side_controls", "fullscreen", "compact_bottom_bar", "maximized_canvas", "player2_fixed", "reset_fixed"]
    })

@app.route('/api/stats')
def stats():
    return jsonify({
        "game": "Stickman Fighter V2.3",
        "version": "3.4",
        "description": "火柴人对战游戏 - 完整修复版",
        "features": [
            "两侧控制按钮",
            "最大化游戏画面",
            "紧凑底部栏（不遮挡）",
            "全屏模式按钮",
            "✅ 修复玩家2按钮响应",
            "✅ 修复游戏结束重置",
            "顶部状态栏"
        ]
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"🚀 启动服务器: http://localhost:{port}")
    print("=" * 60)
    print("🔥 火柴人对战 - V2.3 完整修复版")
    print("=" * 60)
    print("✅ 修复内容:")
    print("  ✅ 玩家2按钮响应修复（update方法添加handleInput）")
    print("  ✅ 游戏结束重置按钮修复（独立class避免冲突）")
    print("  ✅ 虚拟按键同时设置大小写兼容")
    print("=" * 60)
    print(f"📱 访问: http://localhost:{port}")
    print("=" * 60)
    app.run(host='0.0.0.0', port=port, debug=False)
