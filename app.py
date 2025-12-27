#!/usr/bin/env python3
"""
🔥 火柴人对战游戏 - V2.6 创意武器系统版
新增：6种独特武器 + 特殊效果 + 自动掉落机制
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
    <title>🔥 火柴人对战 - 武器系统版 V2.6</title>
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
            width: 85px;
            height: calc(100% - 45px);
            display: flex;
            flex-direction: column;
            gap: 6px;
            align-items: center;
            justify-content: center;
            padding: 10px 6px;
            background: rgba(255, 107, 107, 0.25);
            border-radius: 10px;
            backdrop-filter: blur(6px);
            margin-top: 25px;
            border: 1px solid rgba(255, 107, 107, 0.3);
        }

        /* 右侧控制面板 - 玩家2 */
        .control-panel-right {
            width: 85px;
            height: calc(100% - 45px);
            display: flex;
            flex-direction: column;
            gap: 6px;
            align-items: center;
            justify-content: center;
            padding: 10px 6px;
            background: rgba(77, 171, 247, 0.25);
            border-radius: 10px;
            backdrop-filter: blur(6px);
            margin-top: 25px;
            border: 1px solid rgba(77, 171, 247, 0.3);
        }

        /* 游戏区域 */
        .game-area {
            flex: 1;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: calc(100% - 45px);
            position: relative;
            max-width: calc(100vw - 210px);
            margin-top: 25px;
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
            min-height: 48px;
            background: rgba(255, 255, 255, 0.25);
            border: 2px solid rgba(255, 255, 255, 0.5);
            color: white;
            border-radius: 8px;
            font-size: 1.2em;
            font-weight: bold;
            cursor: pointer;
            user-select: none;
            touch-action: manipulation;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.1s;
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
            padding: 4px;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.3);
        }

        .btn:active {
            background: rgba(255, 255, 255, 0.5);
            transform: scale(0.95);
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
        }

        .btn.move {
            background: rgba(77, 171, 247, 0.3);
            border-color: rgba(77, 171, 247, 0.6);
        }

        .btn.jump {
            background: rgba(107, 207, 127, 0.35);
            border-color: rgba(107, 207, 127, 0.7);
            font-size: 1.4em;
            min-height: 52px;
        }

        .btn.attack {
            background: rgba(255, 107, 107, 0.35);
            border-color: rgba(255, 107, 107, 0.7);
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

        /* 武器状态指示器 */
        .weapon-status {
            position: absolute;
            top: 90px;
            left: 50%;
            transform: translateX(-50%);
            background: rgba(0, 0, 0, 0.8);
            padding: 6px 12px;
            border-radius: 8px;
            z-index: 5;
            display: none;
            font-size: 0.9em;
            border: 1px solid rgba(255, 255, 255, 0.2);
            backdrop-filter: blur(5px);
        }

        .weapon-status.show {
            display: block;
            animation: fadeIn 0.3s ease;
        }

        .weapon-status .weapon-name {
            font-weight: bold;
            margin-right: 5px;
        }

        .weapon-status .weapon-durability {
            color: #ffd93d;
            font-size: 0.85em;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateX(-50%) translateY(-5px); }
            to { opacity: 1; transform: translateX(-50%) translateY(0); }
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

        /* 重置按钮 */
        .reset-btn {
            width: auto;
            padding: 12px 24px;
            background: linear-gradient(135deg, #6bcf7f, #48bb78);
            color: white;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            font-weight: bold;
            font-size: 1em;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
            transition: all 0.2s;
            touch-action: manipulation;
        }

        .reset-btn:active {
            transform: translateY(2px);
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.3);
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
            max-width: 300px;
            font-size: 0.9em;
            backdrop-filter: blur(10px);
            white-space: pre-wrap;
            line-height: 1.4;
        }

        .notification.show {
            transform: translateX(0);
        }

        /* 小屏幕优化 */
        @media (max-width: 768px) {
            .control-panel-left,
            .control-panel-right {
                width: 70px;
                gap: 5px;
                padding: 8px 4px;
            }

            .btn {
                min-height: 44px;
                font-size: 1.1em;
                padding: 3px;
            }

            .btn.jump {
                font-size: 1.3em;
                min-height: 48px;
            }

            .player-label {
                font-size: 0.7em;
                padding: 3px;
            }

            .status-bar-top {
                gap: 4px;
            }

            .player-status-mini {
                padding: 3px 5px;
                min-width: 80px;
                font-size: 0.7em;
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

            .game-area {
                max-width: calc(100vw - 180px);
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

            <!-- 武器状态指示器 -->
            <div class="weapon-status" id="weaponStatus"></div>

            <!-- 模式指示器 -->
            <div id="modeIndicator" class="mode-indicator" style="display: none;"></div>

            <!-- 画布容器 -->
            <div class="canvas-container">
                <canvas id="gameCanvas" width="800" height="500"></canvas>

                <!-- 游戏结束遮罩 -->
                <div id="gameOverOverlay" class="game-over-overlay">
                    <div class="winner-text" id="winnerText"></div>
                    <div style="margin-top: 15px;">
                        <button id="resetButton" class="reset-btn">🔄 再战一局</button>
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
        <button class="func-btn fullscreen" id="fullscreenBtn">🖥️ 全屏</button>
        <button class="func-btn" id="pauseBtn">⏸️ 暂停</button>
        <button class="func-btn warning" id="aiBtn">🤖 AI</button>
        <button class="func-btn danger" id="hardcoreBtn">💀 硬核</button>
        <button class="func-btn" id="resetBtn">🔄 重置</button>
        <button class="func-btn" id="weaponsBtn">⚔️ 武器</button>
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
            weapons: [], // 武器数组
            weaponDropTimer: 0, // 武器掉落计时器
            stats: {
                p1: { hits: 0, damage: 0, maxCombo: 0, weaponsCollected: 0 },
                p2: { hits: 0, damage: 0, maxCombo: 0, weaponsCollected: 0 }
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
                    case 'weapon_pickup':
                        oscillator.frequency.value = 600;
                        gainNode.gain.setValueAtTime(0.2, audioContext.currentTime);
                        gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.2);
                        break;
                    case 'weapon_drop':
                        oscillator.frequency.value = 200;
                        gainNode.gain.setValueAtTime(0.15, audioContext.currentTime);
                        gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.15);
                        break;
                    case 'weapon_special':
                        oscillator.frequency.value = 800;
                        gainNode.gain.setValueAtTime(0.18, audioContext.currentTime);
                        gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.3);
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

        // 武器系统 - 创意武器类
        class Weapon {
            constructor(x, y) {
                this.x = x;
                this.y = y;
                this.width = 20;
                this.height = 20;
                this.vx = (Math.random() - 0.5) * 2;
                this.vy = -3; // 向上抛出
                this.gravity = 0.3;
                this.onGround = false;
                this.lifetime = 300; // 存在时间（帧）

                // 随机选择武器类型
                const types = [
                    { name: '火焰剑', emoji: '🔥', color: '#ff4500', damage: 15, special: 'burn', durability: 5 },
                    { name: '闪电锤', emoji: '⚡', color: '#ffd700', damage: 20, special: 'knockback', durability: 4 },
                    { name: '冰霜弓', emoji: '🧊', color: '#00bfff', damage: 12, special: 'slow', durability: 6 },
                    { name: '钻石匕首', emoji: '💎', color: '#00ffff', damage: 25, special: 'crit', durability: 3 },
                    { name: '战斧', emoji: '🪓', color: '#8b4513', damage: 22, special: 'stun', durability: 4 },
                    { name: '回旋镖', emoji: '🎯', color: '#ff1493', damage: 18, special: 'boomerang', durability: 5 }
                ];

                const type = types[Math.floor(Math.random() * types.length)];
                this.name = type.name;
                this.emoji = type.emoji;
                this.color = type.color;
                this.baseDamage = type.damage;
                this.special = type.special;
                this.durability = type.durability;
                this.maxDurability = type.durability;
            }

            update() {
                if (!this.onGround) {
                    this.vy += this.gravity;
                    this.x += this.vx;
                    this.y += this.vy;

                    // 地面碰撞
                    const groundLevel = canvas.height - 80;
                    if (this.y + this.height >= groundLevel) {
                        this.y = groundLevel - this.height;
                        this.vy = 0;
                        this.vx = 0;
                        this.onGround = true;
                    }

                    // 边界限制
                    if (this.x < 0) this.x = 0;
                    if (this.x + this.width > canvas.width) this.x = canvas.width - this.width;
                }

                this.lifetime--;
            }

            draw() {
                // 绘制武器光效
                ctx.save();
                ctx.shadowBlur = 15;
                ctx.shadowColor = this.color;

                // 武器主体
                ctx.fillStyle = this.color;
                ctx.font = '20px Arial';
                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';
                ctx.fillText(this.emoji, this.x + this.width/2, this.y + this.height/2);

                // 耐久度指示器
                if (this.durability > 0) {
                    const barWidth = 20;
                    const barHeight = 3;
                    const durabilityRatio = this.durability / this.maxDurability;

                    ctx.fillStyle = 'rgba(0, 0, 0, 0.5)';
                    ctx.fillRect(this.x, this.y - 6, barWidth, barHeight);

                    ctx.fillStyle = durabilityRatio > 0.5 ? '#00ff00' : durabilityRatio > 0.25 ? '#ffff00' : '#ff0000';
                    ctx.fillRect(this.x, this.y - 6, barWidth * durabilityRatio, barHeight);
                }

                ctx.restore();
            }

            isExpired() {
                return this.lifetime <= 0;
            }
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

                // 武器系统
                this.weapon = null; // 当前装备的武器
                this.isUsingWeapon = false; // 是否正在使用武器
                this.burnTicks = 0; // 燃烧效果计数
                this.slowTicks = 0; // 减速效果计数
                this.stunTicks = 0; // 眩晕效果计数
            }

            // 拾取武器
            pickUpWeapon(weapon) {
                this.weapon = weapon;
                this.weapon.durability = weapon.durability; // 重置耐久
                showNotification(`玩家${this.playerNum} 拾取了 ${weapon.name} ${weapon.emoji}`, 1200);
                playSound('weapon_pickup');
                gameState.stats[`p${this.playerNum}`].weaponsCollected++;
            }

            // 使用武器攻击
            useWeapon() {
                if (!this.weapon || this.weapon.durability <= 0) {
                    this.weapon = null;
                    return null;
                }

                if (this.stamina < 15) return null;

                this.isUsingWeapon = true;
                this.attackCooldown = 25;
                this.stamina -= 15;
                this.animationTimer = 0;
                playSound('weapon_special');

                // 武器耐久减少
                this.weapon.durability--;

                // 武器耗尽提示
                if (this.weapon.durability <= 0) {
                    showNotification(`${this.weapon.name} 耗尽!`, 800);
                    this.weapon = null;
                }

                return this.weapon;
            }

            // 应用特殊效果
            applySpecialEffect(special) {
                switch(special) {
                    case 'burn':
                        this.burnTicks = 60; // 持续2秒
                        break;
                    case 'slow':
                        this.slowTicks = 90; // 持续3秒
                        break;
                    case 'stun':
                        this.stunTicks = 40; // 持续1.3秒
                        break;
                    case 'knockback':
                        // 击退在伤害计算时处理
                        break;
                    case 'crit':
                        // 暴击在伤害计算时处理
                        break;
                }
            }

            // 处理特殊效果
            handleSpecialEffects() {
                // 燃烧伤害
                if (this.burnTicks > 0) {
                    if (this.burnTicks % 20 === 0) { // 每0.67秒造成1点伤害
                        this.health -= 1;
                        if (this.health < 0) this.health = 0;
                    }
                    this.burnTicks--;
                }

                // 减速
                if (this.slowTicks > 0) {
                    this.slowTicks--;
                }

                // 眩晕
                if (this.stunTicks > 0) {
                    this.stunTicks--;
                    return true; // 眩晕中，无法行动
                }

                return false;
            }

            handleInput() {
                // 眩晕检查
                if (this.handleSpecialEffects()) {
                    this.vx = 0;
                    return;
                }

                this.vx = 0;

                // 减速效果
                let speedMultiplier = this.slowTicks > 0 ? 0.5 : 1;

                if (keys[this.controls.left]) {
                    this.vx = -this.speed * speedMultiplier;
                    this.facingRight = false;
                }
                if (keys[this.controls.right]) {
                    this.vx = this.speed * speedMultiplier;
                    this.facingRight = true;
                }

                if (keys[this.controls.jump] && this.onGround) {
                    this.vy = -this.jumpPower;
                    this.onGround = false;
                    playSound('punch');
                }

                if (this.attackCooldown === 0) {
                    // 优先使用武器攻击（如果装备了武器）
                    if (this.weapon && keys[this.controls.punch]) {
                        this.useWeapon();
                    } else if (keys[this.controls.punch]) {
                        this.punch();
                    } else if (keys[this.controls.kick]) {
                        this.kick();
                    }
                }
            }

            aiControl(target) {
                // 眩晕检查
                if (this.handleSpecialEffects()) {
                    this.vx = 0;
                    return;
                }

                if (this.attackCooldown > 0) return;

                const distance = Math.abs(this.x - target.x);
                const isTargetLeft = target.x < this.x;

                // 减速效果
                let speedMultiplier = this.slowTicks > 0 ? 0.5 : 1;

                if (distance > 80) {
                    if (isTargetLeft) {
                        this.vx = -this.speed * speedMultiplier;
                        this.facingRight = false;
                    } else {
                        this.vx = this.speed * speedMultiplier;
                        this.facingRight = true;
                    }
                } else if (distance < 40) {
                    if (isTargetLeft) {
                        this.vx = this.speed * speedMultiplier;
                        this.facingRight = true;
                    } else {
                        this.vx = -this.speed * speedMultiplier;
                        this.facingRight = false;
                    }
                }

                if (target.isPunching || target.isKicking || target.isUsingWeapon) {
                    if (this.onGround && Math.random() > 0.7) {
                        this.vy = -this.jumpPower;
                        this.onGround = false;
                    }
                }

                if (distance < 70 && this.stamina > 20) {
                    // AI优先使用武器
                    if (this.weapon && Math.random() > 0.3) {
                        this.useWeapon();
                    } else if (Math.random() > 0.5) {
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

            takeDamage(damage, attacker = null, weapon = null) {
                if (this.hitCooldown === 0) {
                    let finalDamage = gameState.hardcoreMode ? damage * 2 : damage;

                    // 武器特殊效果处理
                    if (weapon) {
                        // 暴击效果
                        if (weapon.special === 'crit' && Math.random() > 0.7) {
                            finalDamage = Math.floor(finalDamage * 2);
                            showNotification(`💥 暴击! ${finalDamage} 伤害`, 600);
                        }

                        // 应用特殊效果
                        this.applySpecialEffect(weapon.special);

                        // 击退效果
                        if (weapon.special === 'knockback' && attacker) {
                            const knockback = attacker.facingRight ? 8 : -8;
                            this.vx = knockback;
                        }
                    }

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
                } else if (this.isUsingWeapon) {
                    // 武器攻击范围更大
                    const reach = 60;
                    return this.facingRight
                        ? { x: this.x + this.width, y: this.y + 10, w: reach, h: 40 }
                        : { x: this.x - reach, y: this.y + 10, w: reach, h: 40 };
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

                // 处理武器动画
                if (this.isPunching || this.isKicking || this.isUsingWeapon) {
                    this.animationTimer++;
                    if (this.animationTimer >= 10) {
                        this.isPunching = false;
                        this.isKicking = false;
                        this.isUsingWeapon = false;
                        this.animationTimer = 0;
                    }
                }

                // 武器拾取检测
                if (!gameState.gameOver) {
                    for (let i = gameState.weapons.length - 1; i >= 0; i--) {
                        const weapon = gameState.weapons[i];
                        if (weapon.onGround) {
                            // 碰撞检测
                            if (this.x < weapon.x + weapon.width &&
                                this.x + this.width > weapon.x &&
                                this.y < weapon.y + weapon.height &&
                                this.y + this.height > weapon.y) {

                                this.pickUpWeapon(weapon);
                                gameState.weapons.splice(i, 1);
                                break;
                            }
                        }
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

                // 特殊效果视觉提示
                let drawColor = this.color;
                let glowSize = 0;

                if (this.burnTicks > 0) {
                    drawColor = '#ff4500';
                    glowSize = 8;
                }
                if (this.slowTicks > 0) {
                    drawColor = '#00bfff';
                    glowSize = 8;
                }
                if (this.stunTicks > 0) {
                    drawColor = '#ffff00';
                    glowSize = 10;
                }
                if (this.combo >= 5) {
                    glowSize = Math.max(glowSize, 10);
                }

                ctx.strokeStyle = drawColor;
                ctx.lineWidth = 3.5;
                ctx.lineCap = 'round';

                if (glowSize > 0) {
                    ctx.shadowBlur = glowSize;
                    ctx.shadowColor = drawColor;
                } else {
                    ctx.shadowBlur = 0;
                }

                // 绘制火柴人
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
                const weaponOffset = (this.isUsingWeapon && this.animationTimer < 5) ? 15 : 0;

                if (this.facingRight) {
                    ctx.beginPath();
                    ctx.moveTo(bodyX, armY);
                    ctx.lineTo(bodyX + 12 + punchOffset + weaponOffset, armY);
                    ctx.stroke();

                    ctx.beginPath();
                    ctx.moveTo(bodyX, armY);
                    ctx.lineTo(bodyX - 8, armY + 4);
                    ctx.stroke();
                } else {
                    ctx.beginPath();
                    ctx.moveTo(bodyX, armY);
                    ctx.lineTo(bodyX - 12 - punchOffset - weaponOffset, armY);
                    ctx.stroke();

                    ctx.beginPath();
                    ctx.moveTo(bodyX, armY);
                    ctx.lineTo(bodyX + 8, armY + 4);
                    ctx.stroke();
                }

                // 绘制装备的武器
                if (this.weapon) {
                    ctx.save();
                    ctx.font = '16px Arial';
                    ctx.textAlign = 'center';
                    ctx.textBaseline = 'middle';
                    ctx.shadowBlur = 8;
                    ctx.shadowColor = this.weapon.color;

                    let weaponX = bodyX;
                    let weaponY = bodyY + 8;

                    if (this.isUsingWeapon && this.animationTimer < 5) {
                        // 攻击时武器前伸
                        if (this.facingRight) {
                            weaponX += 18;
                        } else {
                            weaponX -= 18;
                        }
                    } else {
                        // 非攻击时在身侧
                        if (this.facingRight) {
                            weaponX += 10;
                        } else {
                            weaponX -= 10;
                        }
                    }

                    ctx.fillText(this.weapon.emoji, weaponX, weaponY);
                    ctx.restore();
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

            // 更新武器状态显示
            const weaponStatus = document.getElementById('weaponStatus');

            // 检查两个玩家的武器
            const weapons = [];
            if (p1.weapon) weapons.push({ player: '玩家1', color: '#ff6b6b', weapon: p1.weapon });
            if (p2.weapon) weapons.push({ player: '玩家2', color: '#4dabf7', weapon: p2.weapon });

            if (weapons.length > 0) {
                if (weapons.length === 1) {
                    const w = weapons[0];
                    weaponStatus.innerHTML = `<span class="weapon-name" style="color: ${w.color}">${w.player} ${w.weapon.emoji} ${w.weapon.name}</span><span class="weapon-durability">耐久: ${w.weapon.durability}/${w.weapon.maxDurability}</span>`;
                } else {
                    // 两个玩家都有武器，显示两个
                    weaponStatus.innerHTML = weapons.map(w =>
                        `<span style="color: ${w.color}">${w.player} ${w.weapon.emoji}</span>`
                    ).join(' ');
                }
                weaponStatus.classList.add('show');
            } else {
                weaponStatus.classList.remove('show');
            }
        }

        function gameLoop() {
            // 总是绘制游戏，即使在暂停或游戏结束状态
            drawGame();

            // 检查游戏状态，确保玩家存在
            if (!gameState.player1 || !gameState.player2) {
                requestAnimationFrame(gameLoop);
                return;
            }

            if (gameState.paused) {
                // 暂停时仍然显示状态
                updateUI();
                requestAnimationFrame(gameLoop);
                return;
            }

            if (gameState.gameOver) {
                // 游戏结束时仍然显示状态
                updateUI();
                requestAnimationFrame(gameLoop);
                return;
            }

            // 只有在游戏进行中才更新逻辑
            gameState.player1.handleInput();
            gameState.player1.update();
            gameState.player2.update();

            // 武器掉落系统
            gameState.weaponDropTimer++;
            if (gameState.weaponDropTimer > 300 && Math.random() > 0.97) { // 每5-10秒随机掉落
                const x = Math.random() * (canvas.width - 100) + 50;
                const y = 100;
                gameState.weapons.push(new Weapon(x, y));
                gameState.weaponDropTimer = 0;
                playSound('weapon_drop');
                showNotification('✨ 武器掉落!', 800);
            }

            // 更新武器
            for (let i = gameState.weapons.length - 1; i >= 0; i--) {
                const weapon = gameState.weapons[i];
                weapon.update();

                if (weapon.isExpired()) {
                    gameState.weapons.splice(i, 1);
                }
            }

            // 玩家1攻击检测
            const hitbox1 = gameState.player1.getAttackHitbox();
            if (hitbox1) {
                let damage = 8;
                let weapon = null;

                if (gameState.player1.isPunching) {
                    damage = 8;
                } else if (gameState.player1.isKicking) {
                    damage = 12;
                } else if (gameState.player1.isUsingWeapon && gameState.player1.weapon) {
                    damage = gameState.player1.weapon.baseDamage;
                    weapon = gameState.player1.weapon;
                }

                damage = Math.floor(damage * gameState.player1.comboMultiplier);

                if (checkHit(hitbox1, gameState.player2)) {
                    if (gameState.player2.takeDamage(damage, gameState.player1, weapon)) {
                        if (gameState.player1.isKicking) {
                            const knockback = gameState.player1.facingRight ? 5 : 3;
                            gameState.player2.vx = gameState.player1.facingRight ? knockback : -knockback;
                        }
                    }
                }
            }

            // 玩家2攻击检测
            const hitbox2 = gameState.player2.getAttackHitbox();
            if (hitbox2) {
                let damage = 8;
                let weapon = null;

                if (gameState.player2.isPunching) {
                    damage = 8;
                } else if (gameState.player2.isKicking) {
                    damage = 12;
                } else if (gameState.player2.isUsingWeapon && gameState.player2.weapon) {
                    damage = gameState.player2.weapon.baseDamage;
                    weapon = gameState.player2.weapon;
                }

                damage = Math.floor(damage * gameState.player2.comboMultiplier);

                if (checkHit(hitbox2, gameState.player1)) {
                    if (gameState.player1.takeDamage(damage, gameState.player2, weapon)) {
                        if (gameState.player2.isKicking) {
                            const knockback = gameState.player2.isKicking ? 5 : 3;
                            gameState.player1.vx = gameState.player2.facingRight ? knockback : -knockback;
                        }
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

            updateUI();

            requestAnimationFrame(gameLoop);
        }

        function drawGame() {
            // 确保canvas和context存在
            if (!canvas || !ctx) {
                console.log('❌ Canvas或Context未准备好');
                return;
            }

            // 清空画布
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // 绘制背景
            drawBackground();

            // 绘制掉落的武器
            if (gameState.weapons && gameState.weapons.length > 0) {
                gameState.weapons.forEach(weapon => {
                    if (weapon && weapon.draw) {
                        weapon.draw();
                    }
                });
            }

            // 绘制玩家
            if (gameState.player1 && gameState.player1.draw) {
                gameState.player1.draw();
            }

            if (gameState.player2 && gameState.player2.draw) {
                gameState.player2.draw();
            }
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

            // 确保canvas尺寸正确
            if (canvas.width === 0 || canvas.height === 0) {
                console.log('⚠️ Canvas尺寸异常，尝试修复...');
                resizeCanvas();
            }

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

            // 重置武器系统
            gameState.weapons = [];
            gameState.weaponDropTimer = 0;

            gameState.stats = {
                p1: { hits: 0, damage: 0, maxCombo: 0, weaponsCollected: 0 },
                p2: { hits: 0, damage: 0, maxCombo: 0, weaponsCollected: 0 }
            };

            // 立即更新UI
            const overlay = document.getElementById('gameOverOverlay');
            const comboIndicator = document.getElementById('comboIndicator');
            if (overlay) overlay.classList.remove('show');
            if (comboIndicator) comboIndicator.classList.remove('show');

            updateUI();

            // 显示通知
            if (gameState.aiEnabled) {
                showNotification('🤖 AI对战模式已启用！', 1500);
            }
            if (gameState.hardcoreMode) {
                showNotification('💀 硬核模式开启！伤害翻倍！', 1500);
            }

            showNotification('🔄 游戏重置！武器将在5-10秒后随机掉落', 2000);

            console.log('✅ 游戏重置完成');
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

        // 显示武器系统说明
        function showWeaponsInfo() {
            // 分段显示，避免通知框过大
            showNotification('⚔️ 创意武器系统说明 (1/3)', 1500);

            setTimeout(() => {
                showNotification('🔥 火焰剑 - 15伤害 + 燃烧
⚡ 闪电锤 - 20伤害 + 击退
🧊 冰霜弓 - 12伤害 + 减速
💎 钻石匕首 - 25伤害 + 暴击
🪓 战斧 - 22伤害 + 重击
🎯 回旋镖 - 18伤害 + 特效', 2000);
            }, 1600);

            setTimeout(() => {
                showNotification('🎯 机制：每5-10秒掉落
🎯 靠近自动拾取
🎯 F/J键使用武器
🎯 武器有耐久度
💡 顶部显示武器状态', 2500);
            }, 3700);
        }

        // 全屏功能
        function toggleFullscreen() {
            try {
                // 首先初始化音频（需要用户交互）
                initAudio();

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
            } catch(e) {
                showNotification('⚠️ 全屏功能需要用户交互', 1500);
                console.log('Fullscreen error:', e);
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

        // 重置按钮事件监听器
        function setupResetButton() {
            const resetBtn = document.getElementById('resetButton');
            if (resetBtn) {
                // 触摸事件
                resetBtn.addEventListener('touchstart', (e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    initAudio();
                    resetGame();
                });

                // 鼠标点击事件
                resetBtn.addEventListener('click', (e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    initAudio();
                    resetGame();
                });

                // 鼠标按下效果
                resetBtn.addEventListener('mousedown', (e) => {
                    e.preventDefault();
                    e.stopPropagation();
                });
            }
        }

        // 设置底部功能按钮事件
        function setupBottomButtons() {
            // 全屏按钮
            const fullscreenBtn = document.getElementById('fullscreenBtn');
            if (fullscreenBtn) {
                fullscreenBtn.addEventListener('click', (e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    toggleFullscreen();
                });
                fullscreenBtn.addEventListener('touchstart', (e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    toggleFullscreen();
                });
            }

            // 暂停按钮
            const pauseBtn = document.getElementById('pauseBtn');
            if (pauseBtn) {
                pauseBtn.addEventListener('click', (e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    initAudio();
                    togglePause();
                });
                pauseBtn.addEventListener('touchstart', (e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    initAudio();
                    togglePause();
                });
            }

            // AI按钮
            const aiBtn = document.getElementById('aiBtn');
            if (aiBtn) {
                aiBtn.addEventListener('click', (e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    initAudio();
                    toggleAI();
                });
                aiBtn.addEventListener('touchstart', (e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    initAudio();
                    toggleAI();
                });
            }

            // 硬核按钮
            const hardcoreBtn = document.getElementById('hardcoreBtn');
            if (hardcoreBtn) {
                hardcoreBtn.addEventListener('click', (e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    initAudio();
                    toggleHardcore();
                });
                hardcoreBtn.addEventListener('touchstart', (e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    initAudio();
                    toggleHardcore();
                });
            }

            // 重置按钮（底部）
            const resetBtn = document.getElementById('resetBtn');
            if (resetBtn) {
                resetBtn.addEventListener('click', (e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    initAudio();
                    resetGame();
                });
                resetBtn.addEventListener('touchstart', (e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    initAudio();
                    resetGame();
                });
            }

            // 武器信息按钮
            const weaponsBtn = document.getElementById('weaponsBtn');
            if (weaponsBtn) {
                weaponsBtn.addEventListener('click', (e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    initAudio();
                    showWeaponsInfo();
                });
                weaponsBtn.addEventListener('touchstart', (e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    initAudio();
                    showWeaponsInfo();
                });
            }
        }

        // 初始化
        window.addEventListener('load', () => {
            console.log('🎮 游戏初始化开始...');

            detectDevice();
            setupVirtualControls();
            setupResetButton();
            setupBottomButtons();

            // 确保canvas准备好
            const canvas = document.getElementById('gameCanvas');
            if (canvas && canvas.getContext) {
                console.log('✅ Canvas准备就绪');
                console.log('Canvas尺寸:', canvas.width, 'x', canvas.height);

                // 先调整大小，再重置游戏
                resizeCanvas();
                resetGame();

                // 开始游戏循环
                gameLoop();
                showNotification('🎮 游戏加载完成！按 R 重新开始', 2000);
                console.log('🎉 游戏初始化完成');
            } else {
                console.log('❌ Canvas未找到或不支持');
                showNotification('❌ 初始化失败：Canvas未找到', 3000);
            }
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
        "service": "stickman-fighter-v2.6-weapon",
        "version": "2.6",
        "features": ["landscape_mode", "side_controls", "fullscreen", "larger_buttons", "game_loop_continuous", "player2_fixed", "reset_fixed", "weapon_system", "special_effects"]
    })

@app.route('/api/stats')
def stats():
    return jsonify({
        "game": "Stickman Fighter V2.6",
        "version": "2.6",
        "description": "火柴人对战游戏 - 创意武器系统版",
        "features": [
            "✅ 创意武器系统（6种独特武器）",
            "✅ 武器特殊效果（燃烧、击退、减速、暴击、眩晕）",
            "✅ 自动掉落机制（每5-10秒）",
            "✅ 武器耐久度系统",
            "✅ 武器状态UI显示",
            "✅ 侧边控制面板",
            "✅ 全屏模式",
            "✅ 游戏循环永不停止"
        ],
        "weapon_types": [
            "🔥 火焰剑 - 燃烧效果",
            "⚡ 闪电锤 - 击退+眩晕",
            "🧊 冰霜弓 - 减速效果",
            "💎 钻石匕首 - 暴击",
            "🪓 战斧 - 重击",
            "🎯 回旋镖 - 特殊效果"
        ]
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"🚀 启动服务器: http://localhost:{port}")
    print("=" * 70)
    print("🔥 火柴人对战 - V2.6 创意武器系统版")
    print("=" * 70)
    print("⚔️ 新增武器系统:")
    print("  🔥 火焰剑 - 燃烧持续伤害")
    print("  ⚡ 闪电锤 - 击退+眩晕")
    print("  🧊 冰霜弓 - 减速效果")
    print("  💎 钻石匕首 - 高暴击")
    print("  🪓 战斧 - 重击")
    print("  🎯 回旋镖 - 特殊效果")
    print("=" * 70)
    print("🎯 游戏机制:")
    print("  ✅ 武器每5-10秒自动掉落")
    print("  ✅ 靠近自动拾取")
    print("  ✅ 耐久度系统")
    print("  ✅ 特殊效果可视化")
    print("=" * 70)
    print(f"📱 访问: http://localhost:{port}")
    print("💡 按 ⚔️ 武器 按钮查看详细说明")
    print("=" * 70)
    app.run(host='0.0.0.0', port=port, debug=False)
