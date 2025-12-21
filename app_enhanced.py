#!/usr/bin/env python3
"""
增强版火柴人对战游戏 - Flask服务器
包含音效提示、连击系统、特殊技能等增强功能
"""

from flask import Flask, render_template_string, request, jsonify
import os
import time

app = Flask(__name__)

# 增强版HTML模板
ENHANCED_HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🔥 火柴人对战 - 增强版</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
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
            padding: 15px;
            overflow-x: hidden;
        }

        .container {
            background: rgba(0, 0, 0, 0.4);
            border-radius: 20px;
            padding: 25px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
            backdrop-filter: blur(15px);
            max-width: 1100px;
            width: 100%;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }

        .header {
            text-align: center;
            margin-bottom: 20px;
            position: relative;
        }

        h1 {
            font-size: 2.5em;
            margin-bottom: 5px;
            text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.5);
            background: linear-gradient(45deg, #ff6b6b, #ffd93d, #6bcf7f);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .version-badge {
            display: inline-block;
            background: linear-gradient(45deg, #ff6b6b, #ff8e53);
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 0.8em;
            font-weight: bold;
            margin-top: 5px;
        }

        .game-area {
            display: flex;
            flex-direction: column;
            gap: 20px;
        }

        .canvas-container {
            position: relative;
            display: flex;
            justify-content: center;
        }

        #gameCanvas {
            border: 3px solid rgba(255, 255, 255, 0.3);
            border-radius: 12px;
            background: linear-gradient(180deg, #87CEEB 0%, #B0E0E6 100%);
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.6);
            cursor: none;
            max-width: 100%;
            height: auto;
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
            border: 2px solid rgba(255, 255, 255, 0.3);
            min-width: 300px;
        }

        .game-over-overlay.show {
            display: block;
            animation: popIn 0.3s ease-out;
        }

        @keyframes popIn {
            0% { transform: translate(-50%, -50%) scale(0.5); opacity: 0; }
            100% { transform: translate(-50%, -50%) scale(1); opacity: 1; }
        }

        .winner-text {
            font-size: 2.2em;
            margin-bottom: 20px;
            font-weight: bold;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8);
        }

        .status-bar {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin: 10px 0;
        }

        .player-status {
            background: rgba(0, 0, 0, 0.4);
            padding: 15px;
            border-radius: 10px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }

        .player-status h3 {
            margin-bottom: 8px;
            font-size: 1.1em;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .player1 h3 { color: #ff6b6b; }
        .player2 h3 { color: #4dabf7; }

        .stat-row {
            margin: 5px 0;
            font-size: 0.95em;
        }

        .health-bar, .stamina-bar, .combo-bar {
            height: 18px;
            background: rgba(0, 0, 0, 0.5);
            border-radius: 9px;
            overflow: hidden;
            margin-top: 4px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            position: relative;
        }

        .health-fill {
            height: 100%;
            background: linear-gradient(90deg, #ff6b6b, #ff8787);
            transition: width 0.3s ease;
            box-shadow: 0 0 10px rgba(255, 107, 107, 0.5);
        }

        .stamina-fill {
            height: 100%;
            background: linear-gradient(90deg, #4dabf7, #74c0fc);
            transition: width 0.3s ease;
            box-shadow: 0 0 10px rgba(77, 171, 247, 0.5);
        }

        .combo-fill {
            height: 100%;
            background: linear-gradient(90deg, #ffd93d, #ff6b6b);
            transition: width 0.3s ease;
            box-shadow: 0 0 10px rgba(255, 217, 61, 0.5);
        }

        .combo-indicator {
            text-align: center;
            font-weight: bold;
            font-size: 1.2em;
            color: #ffd93d;
            text-shadow: 0 0 10px rgba(255, 217, 61, 0.8);
            height: 25px;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .controls {
            background: rgba(0, 0, 0, 0.3);
            padding: 20px;
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }

        .control-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin-bottom: 15px;
        }

        .player-controls {
            background: rgba(255, 255, 255, 0.05);
            padding: 15px;
            border-radius: 8px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }

        .player-controls h3 {
            margin-bottom: 10px;
            font-size: 1.1em;
            font-weight: bold;
        }

        .key-list {
            list-style: none;
            font-size: 0.9em;
            line-height: 1.9;
        }

        .key {
            display: inline-block;
            background: rgba(255, 255, 255, 0.2);
            padding: 2px 8px;
            border-radius: 4px;
            font-weight: bold;
            margin-right: 6px;
            min-width: 24px;
            text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.3);
        }

        .buttons {
            display: flex;
            gap: 10px;
            justify-content: center;
            flex-wrap: wrap;
        }

        button {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border: none;
            padding: 12px 20px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 1em;
            font-weight: bold;
            transition: all 0.2s;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }

        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.4);
            background: linear-gradient(135deg, #764ba2, #667eea);
        }

        button:active {
            transform: translateY(0);
        }

        button.danger {
            background: linear-gradient(135deg, #ff6b6b, #ee5a24);
        }

        button.danger:hover {
            background: linear-gradient(135deg, #ee5a24, #ff6b6b);
        }

        .instructions {
            background: rgba(255, 255, 255, 0.1);
            padding: 15px;
            border-radius: 8px;
            margin-top: 15px;
            font-size: 0.9em;
            line-height: 1.6;
            border: 1px solid rgba(255, 255, 255, 0.15);
        }

        .instructions strong {
            color: #ffd93d;
        }

        .tips {
            background: rgba(255, 217, 61, 0.1);
            padding: 10px;
            border-radius: 6px;
            margin-top: 10px;
            font-size: 0.85em;
            border-left: 3px solid #ffd93d;
        }

        .stats-panel {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 10px;
            margin-top: 10px;
            font-size: 0.85em;
        }

        .stat-item {
            background: rgba(0, 0, 0, 0.3);
            padding: 8px;
            border-radius: 6px;
            text-align: center;
        }

        .stat-value {
            font-size: 1.3em;
            font-weight: bold;
            color: #ffd93d;
        }

        @media (max-width: 768px) {
            .control-grid {
                grid-template-columns: 1fr;
            }

            .status-bar {
                grid-template-columns: 1fr;
            }

            h1 {
                font-size: 1.8em;
            }

            .container {
                padding: 15px;
            }

            .game-over-overlay {
                padding: 25px;
                min-width: 250px;
            }

            .winner-text {
                font-size: 1.6em;
            }
        }

        .notification {
            position: fixed;
            top: 20px;
            right: 20px;
            background: rgba(0, 0, 0, 0.9);
            padding: 15px 20px;
            border-radius: 8px;
            border-left: 4px solid #ffd93d;
            transform: translateX(400px);
            transition: transform 0.3s ease;
            z-index: 1000;
            max-width: 300px;
        }

        .notification.show {
            transform: translateX(0);
        }

        .sound-toggle {
            position: absolute;
            top: 10px;
            right: 10px;
            background: rgba(0, 0, 0, 0.5);
            border: 1px solid rgba(255, 255, 255, 0.3);
            padding: 8px 12px;
            border-radius: 6px;
            font-size: 0.9em;
            cursor: pointer;
        }

        .combo-animation {
            animation: comboShake 0.3s ease;
        }

        @keyframes comboShake {
            0%, 100% { transform: translateX(0); }
            25% { transform: translateX(-5px); }
            75% { transform: translateX(5px); }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔥 火柴人对战 - Stickman Fighter 🔥</h1>
            <span class="version-badge">⚡ 增强版 v2.0</span>
            <button class="sound-toggle" onclick="toggleSound()">🔊 音效: <span id="soundStatus">开</span></button>
        </div>

        <div class="game-area">
            <div class="canvas-container">
                <canvas id="gameCanvas" width="900" height="550"></canvas>
                <div id="gameOverOverlay" class="game-over-overlay">
                    <div class="winner-text" id="winnerText"></div>
                    <div class="stats-panel" id="finalStats"></div>
                    <div style="margin-top: 20px;">
                        <button onclick="resetGame()">🔄 再战一局</button>
                    </div>
                </div>
            </div>

            <div class="status-bar">
                <div class="player-status player1">
                    <h3>🔴 玩家1 (红色)</h3>
                    <div class="stat-row">生命: <span id="p1Health">100</span></div>
                    <div class="health-bar">
                        <div class="health-fill" id="p1HealthBar" style="width: 100%"></div>
                    </div>
                    <div class="stat-row">体力: <span id="p1Stamina">100</span></div>
                    <div class="stamina-bar">
                        <div class="stamina-fill" id="p1StaminaBar" style="width: 100%"></div>
                    </div>
                    <div class="stat-row">连击: <span id="p1Combo">0</span></div>
                    <div class="combo-bar">
                        <div class="combo-fill" id="p1ComboBar" style="width: 0%"></div>
                    </div>
                </div>

                <div class="player-status player2">
                    <h3>🔵 玩家2 (蓝色)</h3>
                    <div class="stat-row">生命: <span id="p2Health">100</span></div>
                    <div class="health-bar">
                        <div class="health-fill" id="p2HealthBar" style="width: 100%"></div>
                    </div>
                    <div class="stat-row">体力: <span id="p2Stamina">100</span></div>
                    <div class="stamina-bar">
                        <div class="stamina-fill" id="p2StaminaBar" style="width: 100%"></div>
                    </div>
                    <div class="stat-row">连击: <span id="p2Combo">0</span></div>
                    <div class="combo-bar">
                        <div class="combo-fill" id="p2ComboBar" style="width: 0%"></div>
                    </div>
                </div>
            </div>

            <div class="combo-indicator" id="comboIndicator"></div>

            <div class="controls">
                <div class="control-grid">
                    <div class="player-controls player1">
                        <h3>玩家1 控制</h3>
                        <ul class="key-list">
                            <li><span class="key">W</span> 跳跃</li>
                            <li><span class="key">A</span> 左移</li>
                            <li><span class="key">D</span> 右移</li>
                            <li><span class="key">F</span> 出拳 (8伤害)</li>
                            <li><span class="key">G</span> 踢腿 (12伤害)</li>
                            <li><span class="key">H</span> 特殊技能 (30伤害)</li>
                        </ul>
                    </div>
                    <div class="player-controls player2">
                        <h3>玩家2 控制</h3>
                        <ul class="key-list">
                            <li><span class="key">↑</span> 跳跃</li>
                            <li><span class="key">←</span> 左移</li>
                            <li><span class="key">→</span> 右移</li>
                            <li><span class="key">J</span> 出拳 (8伤害)</li>
                            <li><span class="key">K</span> 踢腿 (12伤害)</li>
                            <li><span class="key">L</span> 特殊技能 (30伤害)</li>
                        </ul>
                    </div>
                </div>

                <div class="buttons">
                    <button onclick="resetGame()">🔄 重新开始</button>
                    <button onclick="togglePause()">⏸️ 暂停/继续</button>
                    <button onclick="toggleAI()" id="aiBtn">🤖 AI对战</button>
                    <button class="danger" onclick="toggleHardcore()">💀 硬核模式</button>
                </div>

                <div class="instructions">
                    <strong>🎯 游戏说明：</strong> 将对手的生命值降至0即可获胜！
                    <div class="tips">
                        💡 <strong>技巧：</strong> 连续攻击可累积连击！连击越高伤害越高！
                        特殊技能需要50点体力，造成30点伤害并击飞对手！
                        硬核模式下伤害翻倍，体力恢复减半！
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div id="notification" class="notification"></div>

    <script>
        // 增强版游戏核心逻辑
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');

        // 游戏配置
        const CONFIG = {
            canvas: { width: 900, height: 550 },
            physics: { gravity: 0.6, groundOffset: 80 },
            combat: {
                punch: { damage: 8, stamina: 10, cooldown: 20, reach: 40 },
                kick: { damage: 12, stamina: 15, cooldown: 25, reach: 50 },
                special: { damage: 30, stamina: 50, cooldown: 60, reach: 70 }
            },
            player: {
                width: 35, height: 65, speed: 4.5, jumpPower: 13,
                health: 100, stamina: 100, hitCooldown: 30
            }
        };

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
            stats: {
                p1: { hits: 0, damage: 0, maxCombo: 0 },
                p2: { hits: 0, damage: 0, maxCombo: 0 }
            }
        };

        // 键盘状态
        const keys = {};

        // 音效模拟（使用Web Audio API）
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();

        function playSound(type) {
            if (!gameState.soundEnabled) return;

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
                case 'special':
                    oscillator.frequency.value = 300;
                    gainNode.gain.setValueAtTime(0.2, audioContext.currentTime);
                    gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.3);
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
        }

        // 显示通知
        function showNotification(message, duration = 2000) {
            const notif = document.getElementById('notification');
            notif.textContent = message;
            notif.classList.add('show');
            setTimeout(() => {
                notif.classList.remove('show');
            }, duration);
        }

        // 火柴人玩家类（增强版）
        class Stickman {
            constructor(x, y, color, controls, playerNum) {
                this.x = x;
                this.y = y;
                this.color = color;
                this.controls = controls;
                this.playerNum = playerNum;

                // 物理属性
                this.vx = 0;
                this.vy = 0;
                this.width = CONFIG.player.width;
                this.height = CONFIG.player.height;
                this.speed = CONFIG.player.speed;
                this.jumpPower = CONFIG.player.jumpPower;
                this.gravity = CONFIG.physics.gravity;
                this.onGround = false;

                // 战斗属性
                this.health = CONFIG.player.health;
                this.stamina = CONFIG.player.stamina;
                this.isPunching = false;
                this.isKicking = false;
                this.isSpecial = false;
                this.attackCooldown = 0;
                this.hitCooldown = 0;
                this.facingRight = playerNum === 2;

                // 连击系统
                this.combo = 0;
                this.comboTimer = 0;
                this.comboMultiplier = 1;

                // 动画
                this.animationTimer = 0;

                // 硬核模式
                this.hardcore = false;
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
                    playSound('punch'); // 跳跃音效
                }

                if (this.attackCooldown === 0) {
                    if (keys[this.controls.punch]) {
                        this.punch();
                    } else if (keys[this.controls.kick]) {
                        this.kick();
                    } else if (keys[this.controls.special]) {
                        this.specialAttack();
                    }
                }
            }

            // AI控制
            aiControl(target) {
                if (this.attackCooldown > 0) return;

                const distance = Math.abs(this.x - target.x);
                const isTargetLeft = target.x < this.x;

                // 移动逻辑
                if (distance > 100) {
                    if (isTargetLeft) {
                        this.vx = -this.speed;
                        this.facingRight = false;
                    } else {
                        this.vx = this.speed;
                        this.facingRight = true;
                    }
                } else if (distance < 50) {
                    // 太近了，后退
                    if (isTargetLeft) {
                        this.vx = this.speed;
                        this.facingRight = true;
                    } else {
                        this.vx = -this.speed;
                        this.facingRight = false;
                    }
                }

                // 跳跃躲避攻击
                if (target.isPunching || target.isKicking) {
                    if (this.onGround && Math.random() > 0.7) {
                        this.vy = -this.jumpPower;
                        this.onGround = false;
                    }
                }

                // 攻击逻辑
                if (distance < 80 && this.stamina > 20) {
                    if (this.stamina >= 50 && Math.random() > 0.8) {
                        this.specialAttack();
                    } else if (Math.random() > 0.5) {
                        this.punch();
                    } else {
                        this.kick();
                    }
                }
            }

            punch() {
                if (this.stamina >= CONFIG.combat.punch.stamina) {
                    this.isPunching = true;
                    this.attackCooldown = CONFIG.combat.punch.cooldown;
                    this.stamina -= CONFIG.combat.punch.stamina;
                    this.animationTimer = 0;
                    playSound('punch');
                }
            }

            kick() {
                if (this.stamina >= CONFIG.combat.kick.stamina) {
                    this.isKicking = true;
                    this.attackCooldown = CONFIG.combat.kick.cooldown;
                    this.stamina -= CONFIG.combat.kick.stamina;
                    this.animationTimer = 0;
                    playSound('kick');
                }
            }

            specialAttack() {
                if (this.stamina >= CONFIG.combat.special.stamina) {
                    this.isSpecial = true;
                    this.attackCooldown = CONFIG.combat.special.cooldown;
                    this.stamina -= CONFIG.combat.special.stamina;
                    this.animationTimer = 0;
                    playSound('special');
                    showNotification(`玩家${this.playerNum} 发动特殊技能! 💥`, 1000);
                }
            }

            takeDamage(damage, attacker = null) {
                if (this.hitCooldown === 0) {
                    const finalDamage = this.hardcore ? damage * 2 : damage;
                    this.health -= finalDamage;
                    this.hitCooldown = CONFIG.player.hitCooldown;

                    if (this.health < 0) this.health = 0;

                    // 更新统计
                    if (attacker) {
                        gameState.stats[`p${attacker.playerNum}`].hits++;
                        gameState.stats[`p${attacker.playerNum}`].damage += finalDamage;

                        // 连击系统
                        attacker.combo++;
                        attacker.comboTimer = 60; // 1秒
                        attacker.comboMultiplier = Math.min(1 + (attacker.combo * 0.1), 2.0);

                        if (attacker.combo > gameState.stats[`p${attacker.playerNum}`].maxCombo) {
                            gameState.stats[`p${attacker.playerNum}`].maxCombo = attacker.combo;
                        }

                        // 连击提示
                        if (attacker.combo >= 3 && attacker.combo % 3 === 0) {
                            showNotification(`玩家${attacker.playerNum} ${attacker.combo}连击! 🔥`, 800);
                            document.getElementById('comboIndicator').textContent = `🔥 ${attacker.combo} 连击! 🔥`;
                            document.getElementById('comboIndicator').classList.add('combo-animation');
                            setTimeout(() => {
                                document.getElementById('comboIndicator').classList.remove('combo-animation');
                                document.getElementById('comboIndicator').textContent = '';
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
                    const reach = CONFIG.combat.punch.reach;
                    return this.facingRight
                        ? { x: this.x + this.width, y: this.y + 15, w: reach, h: 30 }
                        : { x: this.x - reach, y: this.y + 15, w: reach, h: 30 };
                } else if (this.isKicking) {
                    const reach = CONFIG.combat.kick.reach;
                    return this.facingRight
                        ? { x: this.x + this.width, y: this.y + 30, w: reach, h: 40 }
                        : { x: this.x - reach, y: this.y + 30, w: reach, h: 40 };
                } else if (this.isSpecial) {
                    const reach = CONFIG.combat.special.reach;
                    return this.facingRight
                        ? { x: this.x + this.width, y: this.y + 10, w: reach, h: 50 }
                        : { x: this.x - reach, y: this.y + 10, w: reach, h: 50 };
                }
                return null;
            }

            update() {
                // AI控制
                if (gameState.aiEnabled && this.playerNum === 2 && !gameState.gameOver) {
                    this.aiControl(gameState.player1);
                }

                // 物理更新
                this.vy += this.gravity;
                this.x += this.vx;
                this.y += this.vy;

                // 地面碰撞
                const groundLevel = canvas.height - CONFIG.physics.groundOffset;
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
                if (this.isPunching || this.isKicking || this.isSpecial) {
                    this.animationTimer++;
                    if (this.animationTimer >= 10) {
                        this.isPunching = false;
                        this.isKicking = false;
                        this.isSpecial = false;
                        this.animationTimer = 0;
                    }
                }

                // 体力恢复
                const staminaRegen = this.hardcore ? 0.1 : 0.2;
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
                const bodyY = this.y + 20;

                ctx.strokeStyle = this.color;
                ctx.lineWidth = 3.5;
                ctx.lineCap = 'round';

                // 特殊技能效果
                if (this.isSpecial) {
                    ctx.shadowBlur = 15;
                    ctx.shadowColor = this.color;
                } else {
                    ctx.shadowBlur = 0;
                }

                // 头
                ctx.beginPath();
                ctx.arc(bodyX, this.y + 10, 9, 0, Math.PI * 2);
                ctx.stroke();

                // 身体
                ctx.beginPath();
                ctx.moveTo(bodyX, bodyY);
                ctx.lineTo(bodyX, bodyY + 28);
                ctx.stroke();

                // 腿
                const legOffset = (this.isKicking && this.animationTimer < 5) ? 10 : 0;
                if (this.facingRight) {
                    ctx.beginPath();
                    ctx.moveTo(bodyX, bodyY + 28);
                    ctx.lineTo(bodyX - 7, bodyY + 50 + legOffset);
                    ctx.stroke();

                    ctx.beginPath();
                    ctx.moveTo(bodyX, bodyY + 28);
                    ctx.lineTo(bodyX + 7, bodyY + 50);
                    ctx.stroke();
                } else {
                    ctx.beginPath();
                    ctx.moveTo(bodyX, bodyY + 28);
                    ctx.lineTo(bodyX + 7, bodyY + 50 + legOffset);
                    ctx.stroke();

                    ctx.beginPath();
                    ctx.moveTo(bodyX, bodyY + 28);
                    ctx.lineTo(bodyX - 7, bodyY + 50);
                    ctx.stroke();
                }

                // 手臂
                const armY = bodyY + 10;
                const punchOffset = (this.isPunching && this.animationTimer < 5) ? 15 : 0;
                const specialOffset = (this.isSpecial && this.animationTimer < 5) ? 20 : 0;

                if (this.facingRight) {
                    // 右臂
                    ctx.beginPath();
                    ctx.moveTo(bodyX, armY);
                    ctx.lineTo(bodyX + 13 + punchOffset + specialOffset, armY);
                    ctx.stroke();

                    // 左臂
                    ctx.beginPath();
                    ctx.moveTo(bodyX, armY);
                    ctx.lineTo(bodyX - 9, armY + 5);
                    ctx.stroke();
                } else {
                    // 左臂
                    ctx.beginPath();
                    ctx.moveTo(bodyX, armY);
                    ctx.lineTo(bodyX - 13 - punchOffset - specialOffset, armY);
                    ctx.stroke();

                    // 右臂
                    ctx.beginPath();
                    ctx.moveTo(bodyX, armY);
                    ctx.lineTo(bodyX + 9, armY + 5);
                    ctx.stroke();
                }

                // 重置阴影
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

        // 背景绘制
        function drawBackground() {
            // 天空渐变
            const gradient = ctx.createLinearGradient(0, 0, 0, canvas.height);
            gradient.addColorStop(0, '#87CEEB');
            gradient.addColorStop(1, '#B0E0E6');
            ctx.fillStyle = gradient;
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            // 云朵
            ctx.fillStyle = 'rgba(255, 255, 255, 0.9)';
            drawCloud(150, 80);
            drawCloud(500, 60);
            drawCloud(750, 90);

            // 太阳
            ctx.beginPath();
            ctx.arc(800, 80, 25, 0, Math.PI * 2);
            ctx.fillStyle = '#FFD700';
            ctx.fill();
            ctx.strokeStyle = '#FFA500';
            ctx.lineWidth = 2;
            ctx.stroke();

            // 地面
            const groundY = canvas.height - CONFIG.physics.groundOffset;
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

        // UI更新
        function updateUI() {
            if (!gameState.player1 || !gameState.player2) return;

            const p1 = gameState.player1;
            const p2 = gameState.player2;

            // 玩家1
            document.getElementById('p1Health').textContent = Math.round(p1.health);
            document.getElementById('p1Stamina').textContent = Math.round(p1.stamina);
            document.getElementById('p1Combo').textContent = p1.combo;
            document.getElementById('p1HealthBar').style.width = p1.health + '%';
            document.getElementById('p1StaminaBar').style.width = p1.stamina + '%';
            document.getElementById('p1ComboBar').style.width = Math.min(p1.combo * 10, 100) + '%';

            // 玩家2
            document.getElementById('p2Health').textContent = Math.round(p2.health);
            document.getElementById('p2Stamina').textContent = Math.round(p2.stamina);
            document.getElementById('p2Combo').textContent = p2.combo;
            document.getElementById('p2HealthBar').style.width = p2.health + '%';
            document.getElementById('p2StaminaBar').style.width = p2.stamina + '%';
            document.getElementById('p2ComboBar').style.width = Math.min(p2.combo * 10, 100) + '%';
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
                let damage = 0;
                if (gameState.player1.isPunching) damage = CONFIG.combat.punch.damage;
                else if (gameState.player1.isKicking) damage = CONFIG.combat.kick.damage;
                else if (gameState.player1.isSpecial) damage = CONFIG.combat.special.damage;

                // 连击加成
                damage = Math.floor(damage * gameState.player1.comboMultiplier);

                if (checkHit(hitbox1, gameState.player2)) {
                    if (gameState.player2.takeDamage(damage, gameState.player1)) {
                        // 击退效果
                        const knockback = gameState.player1.isSpecial ? 8 :
                                        (gameState.player1.isKicking ? 5 : 3);
                        gameState.player2.vx = gameState.player1.facingRight ? knockback : -knockback;

                        // 硬核模式特殊效果
                        if (gameState.hardcoreMode && gameState.player1.isSpecial) {
                            gameState.player2.vy = -8; // 击飞
                        }
                    }
                }
            }

            const hitbox2 = gameState.player2.getAttackHitbox();
            if (hitbox2) {
                let damage = 0;
                if (gameState.player2.isPunching) damage = CONFIG.combat.punch.damage;
                else if (gameState.player2.isKicking) damage = CONFIG.combat.kick.damage;
                else if (gameState.player2.isSpecial) damage = CONFIG.combat.special.damage;

                // 连击加成
                damage = Math.floor(damage * gameState.player2.comboMultiplier);

                if (checkHit(hitbox2, gameState.player1)) {
                    if (gameState.player1.takeDamage(damage, gameState.player2)) {
                        const knockback = gameState.player2.isSpecial ? 8 :
                                        (gameState.player2.isKicking ? 5 : 3);
                        gameState.player1.vx = gameState.player2.facingRight ? knockback : -knockback;

                        if (gameState.hardcoreMode && gameState.player2.isSpecial) {
                            gameState.player1.vy = -8;
                        }
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
            const finalStats = document.getElementById('finalStats');

            const winnerColor = gameState.winner === 1 ? '#ff6b6b' : '#4dabf7';
            const winnerName = gameState.winner === 1 ? '玩家1' : '玩家2';

            winnerText.innerHTML = `🎉 <span style="color: ${winnerColor}">${winnerName}</span> 获胜！🎉`;

            // 显示最终统计
            const stats = gameState.stats[`p${gameState.winner}`];
            const loserStats = gameState.stats[`p${gameState.winner === 1 ? 2 : 1}`];

            finalStats.innerHTML = `
                <div class="stat-item">
                    <div>胜者命中</div>
                    <div class="stat-value">${stats.hits}</div>
                </div>
                <div class="stat-item">
                    <div>胜者伤害</div>
                    <div class="stat-value">${stats.damage}</div>
                </div>
                <div class="stat-item">
                    <div>最高连击</div>
                    <div class="stat-value">${stats.maxCombo}</div>
                </div>
                <div class="stat-item">
                    <div>对手伤害</div>
                    <div class="stat-value">${loserStats.damage}</div>
                </div>
            `;

            overlay.classList.add('show');
        }

        function resetGame() {
            const health = gameState.hardcoreMode ? 75 : 100;
            const stamina = gameState.hardcoreMode ? 80 : 100;

            gameState.player1 = new Stickman(200, 250, '#ff6b6b', {
                left: 'a', right: 'd', jump: 'w', punch: 'f', kick: 'g', special: 'h'
            }, 1);
            gameState.player1.hardcore = gameState.hardcoreMode;
            gameState.player1.health = health;
            gameState.player1.stamina = stamina;

            gameState.player2 = new Stickman(650, 250, '#4dabf7', {
                left: 'ArrowLeft', right: 'ArrowRight', jump: 'ArrowUp', punch: 'j', kick: 'k', special: 'l'
            }, 2);
            gameState.player2.hardcore = gameState.hardcoreMode;
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
            updateUI();

            if (gameState.aiEnabled) {
                showNotification('AI模式已启用！', 1500);
            }
            if (gameState.hardcoreMode) {
                showNotification('💀 硬核模式开启！伤害翻倍！', 1500);
            }
        }

        function togglePause() {
            gameState.paused = !gameState.paused;
            showNotification(gameState.paused ? '⏸️ 游戏暂停' : '▶️ 游戏继续', 1000);
        }

        function toggleSound() {
            gameState.soundEnabled = !gameState.soundEnabled;
            document.getElementById('soundStatus').textContent = gameState.soundEnabled ? '开' : '关';
            showNotification(`音效: ${gameState.soundEnabled ? '开启' : '关闭'}`, 1000);
        }

        function toggleAI() {
            gameState.aiEnabled = !gameState.aiEnabled;
            const btn = document.getElementById('aiBtn');
            btn.textContent = gameState.aiEnabled ? '🤖 AI: 开启' : '🤖 AI对战';
            btn.style.background = gameState.aiEnabled ?
                'linear-gradient(135deg, #ff6b6b, #ee5a24)' :
                'linear-gradient(135deg, #667eea, #764ba2)';
            showNotification(`AI对战: ${gameState.aiEnabled ? '开启' : '关闭'}`, 1500);
        }

        function toggleHardcore() {
            gameState.hardcoreMode = !gameState.hardcoreMode;
            showNotification(
                gameState.hardcoreMode ? '💀 硬核模式已开启！' : '✨ 普通模式已恢复',
                1500
            );
        }

        // 键盘事件
        window.addEventListener('keydown', (e) => {
            keys[e.key.toLowerCase()] = true;
            keys[e.key] = true;

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

        // 初始化游戏
        resetGame();
        gameLoop();

        // 页面加载完成提示
        window.addEventListener('load', () => {
            showNotification('🎮 游戏加载完成！按 R 重新开始', 2000);
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(ENHANCED_HTML_TEMPLATE)

@app.route('/enhanced')
def enhanced():
    return render_template_string(ENHANCED_HTML_TEMPLATE)

@app.route('/classic')
def classic():
    # 原始版本
    return render_template_string(ENHANCED_HTML_TEMPLATE)

@app.route('/api/health')
def health():
    return jsonify({
        "status": "healthy",
        "service": "stickman-fighter-enhanced",
        "version": "2.0",
        "features": ["enhanced_graphics", "combo_system", "special_attacks", "ai_mode", "hardcore_mode", "sound_effects"]
    })

@app.route('/api/stats')
def stats():
    return jsonify({
        "game": "Stickman Fighter Enhanced",
        "version": "2.0",
        "description": "火柴人对战游戏 - 增强版",
        "features": [
            "双人对战",
            "连击系统",
            "特殊技能",
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
                "attack": "F=拳, G=踢腿, H=特殊技能"
            },
            "player2": {
                "move": "↑/←/→",
                "attack": "J=拳, K=踢腿, L=特殊技能"
            },
            "global": {
                "pause": "ESC",
                "reset": "R",
                "toggle_ai": "点击AI按钮",
                "toggle_hardcore": "点击硬核按钮"
            }
        },
        "game_mechanics": {
            "punch": "8伤害, 消耗10体力",
            "kick": "12伤害, 消耗15体力",
            "special": "30伤害, 消耗50体力, 击飞效果",
            "combo": "连续攻击提升伤害(最高2倍)",
            "hardcore": "伤害翻倍, 体力恢复减半"
        }
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"🚀 启动增强版服务器: http://localhost:{port}")
    print("🎮 增强版特性:")
    print("  - 连击系统")
    print("  - 特殊技能")
    print("  - AI对战")
    print("  - 硬核模式")
    print("  - 音效系统")
    print("  - 增强图形")
    print("")
    print("💡 提示: 访问 / 可玩增强版")
    app.run(host='0.0.0.0', port=port, debug=False)
