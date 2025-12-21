#!/usr/bin/env python3
"""
火柴人对战小游戏 (Stickman Fighter)
支持双人对战，键盘控制
"""

import pygame
import sys
import math

# 初始化
pygame.init()

# 游戏常量
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
FPS = 60

# 颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 50, 50)
BLUE = (50, 100, 255)
GREEN = (50, 200, 50)
GRAY = (150, 150, 150)
SKY_BLUE = (135, 206, 235)
GROUND_COLOR = (101, 67, 33)

# 玩家1控制 (WASD + F/G)
P1_KEYS = {
    'left': pygame.K_a,
    'right': pygame.K_d,
    'jump': pygame.K_w,
    'punch': pygame.K_f,
    'kick': pygame.K_g
}

# 玩家2控制 (方向键 + J/K)
P2_KEYS = {
    'left': pygame.K_LEFT,
    'right': pygame.K_RIGHT,
    'jump': pygame.K_UP,
    'punch': pygame.K_j,
    'kick': pygame.K_k
}

class Stickman:
    def __init__(self, x, y, color, controls, player_num):
        self.x = x
        self.y = y
        self.color = color
        self.controls = controls
        self.player_num = player_num

        # 物理属性
        self.vx = 0
        self.vy = 0
        self.width = 40
        self.height = 80
        self.speed = 5
        self.jump_power = 15
        self.gravity = 0.8
        self.on_ground = False

        # 战斗属性
        self.health = 100
        self.stamina = 100
        self.is_punching = False
        self.is_kicking = False
        self.attack_cooldown = 0
        self.hit_cooldown = 0
        self.facing_right = True

        # 动画
        self.animation_timer = 0

    def handle_input(self, keys):
        # 左右移动
        self.vx = 0
        if keys[self.controls['left']]:
            self.vx = -self.speed
            self.facing_right = False
        if keys[self.controls['right']]:
            self.vx = self.speed
            self.facing_right = True

        # 跳跃
        if keys[self.controls['jump']] and self.on_ground:
            self.vy = -self.jump_power
            self.on_ground = False

        # 攻击
        if self.attack_cooldown == 0:
            if keys[self.controls['punch']]:
                self.punch()
            elif keys[self.controls['kick']]:
                self.kick()

    def update(self):
        # 物理更新
        self.vy += self.gravity
        self.x += self.vx
        self.y += self.vy

        # 地面碰撞
        ground_level = SCREEN_HEIGHT - 100
        if self.y + self.height >= ground_level:
            self.y = ground_level - self.height
            self.vy = 0
            self.on_ground = True

        # 边界限制
        if self.x < 0:
            self.x = 0
        if self.x + self.width > SCREEN_WIDTH:
            self.x = SCREEN_WIDTH - self.width

        # 攻击冷却
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        if self.hit_cooldown > 0:
            self.hit_cooldown -= 1

        # 攻击动画计时
        if self.is_punching or self.is_kicking:
            self.animation_timer += 1
            if self.animation_timer >= 10:
                self.is_punching = False
                self.is_kicking = False
                self.animation_timer = 0

        # 恢复体力
        if self.stamina < 100:
            self.stamina += 0.2

    def punch(self):
        if self.stamina >= 10:
            self.is_punching = True
            self.attack_cooldown = 20
            self.stamina -= 10
            self.animation_timer = 0

    def kick(self):
        if self.stamina >= 15:
            self.is_kicking = True
            self.attack_cooldown = 25
            self.stamina -= 15
            self.animation_timer = 0

    def take_damage(self, damage):
        if self.hit_cooldown == 0:
            self.health -= damage
            self.hit_cooldown = 30
            if self.health < 0:
                self.health = 0
            return True
        return False

    def get_attack_hitbox(self):
        """返回攻击的判定区域"""
        if self.is_punching:
            reach = 50
            if self.facing_right:
                return (self.x + self.width, self.y + 20, reach, 40)
            else:
                return (self.x - reach, self.y + 20, reach, 40)
        elif self.is_kicking:
            reach = 60
            if self.facing_right:
                return (self.x + self.width, self.y + 40, reach, 50)
            else:
                return (self.x - reach, self.y + 40, reach, 50)
        return None

    def draw(self, screen):
        # 身体主体
        body_x = self.x + self.width // 2
        body_y = self.y + 20

        # 闪烁效果（受伤时）
        if self.hit_cooldown > 0 and self.hit_cooldown % 4 < 2:
            return

        # 头
        pygame.draw.circle(screen, self.color, (body_x, self.y + 10), 10)

        # 身体
        pygame.draw.line(screen, self.color, (body_x, body_y), (body_x, body_y + 30), 3)

        # 腿
        leg_offset = 10 if self.is_kicking and self.animation_timer < 5 else 0
        if self.facing_right:
            pygame.draw.line(screen, self.color, (body_x, body_y + 30), (body_x - 8, body_y + 50 + leg_offset), 3)
            pygame.draw.line(screen, self.color, (body_x, body_y + 30), (body_x + 8, body_y + 50), 3)
        else:
            pygame.draw.line(screen, self.color, (body_x, body_y + 30), (body_x + 8, body_y + 50 + leg_offset), 3)
            pygame.draw.line(screen, self.color, (body_x, body_y + 30), (body_x - 8, body_y + 50), 3)

        # 手臂
        arm_y = body_y + 10
        punch_offset = 15 if self.is_punching and self.animation_timer < 5 else 0
        if self.facing_right:
            # 右臂
            pygame.draw.line(screen, self.color, (body_x, arm_y), (body_x + 15 + punch_offset, arm_y), 3)
            # 左臂
            pygame.draw.line(screen, self.color, (body_x, arm_y), (body_x - 10, arm_y + 5), 3)
        else:
            # 左臂
            pygame.draw.line(screen, self.color, (body_x, arm_y), (body_x - 15 - punch_offset, arm_y), 3)
            # 右臂
            pygame.draw.line(screen, self.color, (body_x, arm_y), (body_x + 10, arm_y + 5), 3)

        # 攻击范围显示（调试用，可选）
        # hitbox = self.get_attack_hitbox()
        # if hitbox:
        #     pygame.draw.rect(screen, (255, 255, 0, 100), hitbox, 1)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("火柴人对战 - Stickman Fighter")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)

        self.reset_game()

    def reset_game(self):
        self.player1 = Stickman(200, SCREEN_HEIGHT - 180, RED, P1_KEYS, 1)
        self.player2 = Stickman(SCREEN_WIDTH - 240, SCREEN_HEIGHT - 180, BLUE, P2_KEYS, 2)
        self.game_over = False
        self.winner = None

    def check_collisions(self):
        # 检查玩家1的攻击是否击中玩家2
        hitbox1 = self.player1.get_attack_hitbox()
        if hitbox1 and not self.game_over:
            damage = 8 if self.player1.is_punching else 12
            if self.check_hit(hitbox1, self.player2):
                if self.player2.take_damage(damage):
                    # 击退效果
                    if self.player1.facing_right:
                        self.player2.vx = 5
                    else:
                        self.player2.vx = -5

        # 检查玩家2的攻击是否击中玩家1
        hitbox2 = self.player2.get_attack_hitbox()
        if hitbox2 and not self.game_over:
            damage = 8 if self.player2.is_punching else 12
            if self.check_hit(hitbox2, self.player1):
                if self.player1.take_damage(damage):
                    # 击退效果
                    if self.player2.facing_right:
                        self.player1.vx = 5
                    else:
                        self.player1.vx = -5

        # 检查游戏结束
        if not self.game_over:
            if self.player1.health <= 0:
                self.game_over = True
                self.winner = 2
            elif self.player2.health <= 0:
                self.game_over = True
                self.winner = 1

    def check_hit(self, hitbox, target):
        hx, hy, hw, hh = hitbox
        tx, ty, tw, th = target.x, target.y, target.width, target.height

        # 简单的矩形碰撞检测
        return (hx < tx + tw and hx + hw > tx and
                hy < ty + th and hy + hh > ty)

    def draw_health_bar(self, player, x, y, width, height):
        # 背景
        pygame.draw.rect(self.screen, GRAY, (x, y, width, height))
        # 血条
        health_width = int((player.health / 100) * width)
        color = RED if player.health < 30 else GREEN
        pygame.draw.rect(self.screen, color, (x, y, health_width, height))
        # 边框
        pygame.draw.rect(self.screen, BLACK, (x, y, width, height), 2)

        # 血量文字
        text = self.small_font.render(f"{int(player.health)}", True, BLACK)
        self.screen.blit(text, (x + width // 2 - 10, y + 2))

    def draw_stamina_bar(self, player, x, y, width, height):
        # 背景
        pygame.draw.rect(self.screen, GRAY, (x, y, width, height))
        # 体力条
        stamina_width = int((player.stamina / 100) * width)
        pygame.draw.rect(self.screen, BLUE, (x, y, stamina_width, height))
        # 边框
        pygame.draw.rect(self.screen, BLACK, (x, y, width, height), 1)

    def draw_ui(self):
        # 玩家1信息
        self.draw_health_bar(self.player1, 20, 20, 200, 25)
        self.draw_stamina_bar(self.player1, 20, 50, 200, 15)
        p1_text = self.font.render("P1", True, RED)
        self.screen.blit(p1_text, (230, 20))

        # 玩家2信息
        self.draw_health_bar(self.player2, SCREEN_WIDTH - 220, 20, 200, 25)
        self.draw_stamina_bar(self.player2, SCREEN_WIDTH - 220, 50, 200, 15)
        p2_text = self.font.render("P2", True, BLUE)
        self.screen.blit(p2_text, (SCREEN_WIDTH - 250, 20))

        # 控制说明
        controls_text = [
            "P1: WASD移动, F拳, G脚",
            "P2: 方向键移动, J拳, K脚",
            "R: 重新开始, ESC: 退出"
        ]
        for i, text in enumerate(controls_text):
            rendered = self.small_font.render(text, True, GRAY)
            self.screen.blit(rendered, (20, SCREEN_HEIGHT - 80 + i * 20))

    def draw_game_over(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        winner_text = self.font.render(f"玩家 {self.winner} 获胜！", True,
                                      RED if self.winner == 1 else BLUE)
        restart_text = self.font.render("按 R 重新开始", True, WHITE)

        self.screen.blit(winner_text, (SCREEN_WIDTH // 2 - winner_text.get_width() // 2,
                                      SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2,
                                       SCREEN_HEIGHT // 2 + 10))

    def draw_ground(self):
        # 地面
        ground_y = SCREEN_HEIGHT - 100
        pygame.draw.rect(self.screen, GROUND_COLOR, (0, ground_y, SCREEN_WIDTH, 100))

        # 地面纹理
        for i in range(0, SCREEN_WIDTH, 20):
            pygame.draw.line(self.screen, (80, 50, 20), (i, ground_y), (i, ground_y + 10), 1)

    def draw_background(self):
        # 天空
        self.screen.fill(SKY_BLUE)

        # 云朵
        for x in [100, 400, 700]:
            pygame.draw.circle(self.screen, WHITE, (x, 80), 20)
            pygame.draw.circle(self.screen, WHITE, (x + 15, 75), 25)
            pygame.draw.circle(self.screen, WHITE, (x + 30, 80), 20)

    def run(self):
        running = True

        while running:
            # 事件处理
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_r:
                        self.reset_game()

            # 获取按键状态
            keys = pygame.key.get_pressed()

            # 更新游戏状态
            if not self.game_over:
                self.player1.handle_input(keys)
                self.player2.handle_input(keys)
                self.player1.update()
                self.player2.update()
                self.check_collisions()

            # 绘制
            self.draw_background()
            self.draw_ground()
            self.player1.draw(self.screen)
            self.player2.draw(self.screen)
            self.draw_ui()

            if self.game_over:
                self.draw_game_over()

            # 更新显示
            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    print("火柴人对战游戏启动中...")
    print("=" * 40)
    print("玩家1控制: WASD移动, F=拳, G=脚")
    print("玩家2控制: 方向键移动, J=拳, K=脚")
    print("R = 重新开始, ESC = 退出")
    print("=" * 40)

    game = Game()
    game.run()
