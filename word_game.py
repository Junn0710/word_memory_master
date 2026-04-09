import pygame
import random
import json
import os
import math
from datetime import datetime, timedelta
import sys

# 初始化pygame
pygame.init()

# 游戏窗口设置
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("艾宾浩斯单词大冒险")

# 清新温馨的配色方案
BACKGROUND = (252, 245, 235)  # 温暖的米白色
PRIMARY = (143, 188, 143)  # 清新的草绿色
SECONDARY = (188, 210, 188)  # 淡雅的灰绿色
ACCENT = (255, 193, 158)  # 温暖的杏色
TEXT_COLOR = (80, 70, 60)  # 温暖的深棕色
CORRECT_COLOR = (129, 199, 132)  # 清新的嫩绿色
WRONG_COLOR = (229, 115, 115)  # 温柔的粉红色
WHITE = (255, 255, 245)  # 柔和的米白色
LIGHT_BLUE = (210, 230, 220)  # 清新的薄荷色
GOLD = (255, 215, 180)  # 温暖的淡金色
SILVER = (212, 212, 212)  # 柔和的银灰色
BRONZE = (205, 170, 125)  # 温暖的古铜色
PURPLE = (200, 180, 210)  # 淡雅的薰衣草色
CARD_BG = (255, 255, 250)  # 柔和的卡片背景色
SHADOW = (200, 190, 180)  # 柔和的阴影色

# 字体
title_font = pygame.font.SysFont("microsoftyahei", 56, bold=True)
word_font = pygame.font.SysFont("microsoftyahei", 72, bold=True)
button_font = pygame.font.SysFont("microsoftyahei", 36)
info_font = pygame.font.SysFont("microsoftyahei", 28)
small_font = pygame.font.SysFont("microsoftyahei", 22)

# 艾宾浩斯遗忘曲线复习间隔（分钟）
EBBINGHAUS_INTERVALS = [20, 60, 9 * 60, 24 * 60, 2 * 24 * 60, 6 * 24 * 60, 31 * 24 * 60]

# 单词数据
default_words = [
    # 初级词汇
    {"word": "abandon", "meaning": "放弃，遗弃", "example": "He abandoned his car and ran away.", "category": "动作",
     "difficulty": 1},
    {"word": "benefit", "meaning": "好处，益处", "example": "Exercise has many health benefits.", "category": "生活",
     "difficulty": 1},
    {"word": "candidate", "meaning": "候选人，申请者", "example": "There are three candidates for the position.",
     "category": "职业", "difficulty": 1},
    {"word": "diligent", "meaning": "勤奋的，刻苦的", "example": "She is a diligent student.", "category": "性格",
     "difficulty": 1},
    {"word": "elegant", "meaning": "优雅的，精美的", "example": "She wore an elegant dress to the party.",
     "category": "外观", "difficulty": 1},

    # 中级词汇
    {"word": "frugal", "meaning": "节俭的，朴素的", "example": "They lived a frugal life.", "category": "生活",
     "difficulty": 2},
    {"word": "gregarious", "meaning": "爱交际的，群居的", "example": "She is gregarious and enjoys parties.",
     "category": "性格", "difficulty": 2},
    {"word": "hinder", "meaning": "阻碍，妨碍", "example": "Bad weather hindered the construction work.",
     "category": "动作", "difficulty": 2},
    {"word": "innovative", "meaning": "创新的，革新的", "example": "The company is known for its innovative products.",
     "category": "科技", "difficulty": 2},
    {"word": "juxtapose", "meaning": "并置，并列", "example": "The exhibition juxtaposes paintings and sculptures.",
     "category": "艺术", "difficulty": 2},

    # 高级词汇
    {"word": "kaleidoscope", "meaning": "万花筒，千变万化", "example": "The market was a kaleidoscope of colors.",
     "category": "描述", "difficulty": 3},
    {"word": "lucid", "meaning": "清晰的，易懂的", "example": "He gave a lucid explanation of the theory.",
     "category": "描述", "difficulty": 3},
    {"word": "meticulous", "meaning": "一丝不苟的，细致的", "example": "She is meticulous about her work.",
     "category": "性格", "difficulty": 3},
    {"word": "nostalgia", "meaning": "怀旧，乡愁", "example": "The old song filled her with nostalgia.",
     "category": "情感", "difficulty": 3},
    {"word": "obsolete", "meaning": "过时的，废弃的", "example": "This technology is now obsolete.", "category": "科技",
     "difficulty": 3},

    # 专业词汇
    {"word": "paradigm", "meaning": "范例，模式", "example": "This discovery will change the paradigm of physics.",
     "category": "学术", "difficulty": 4},
    {"word": "quintessential", "meaning": "典型的，精髓的", "example": "He is the quintessential English gentleman.",
     "category": "描述", "difficulty": 4},
    {"word": "resilient", "meaning": "有弹性的，适应力强的", "example": "Children are often more resilient than adults.",
     "category": "性格", "difficulty": 4},
    {"word": "serendipity", "meaning": "意外发现珍奇事物的本领",
     "example": "Finding this old photo was pure serendipity.", "category": "生活", "difficulty": 4},
    {"word": "ubiquitous", "meaning": "无处不在的", "example": "Mobile phones are ubiquitous nowadays.",
     "category": "描述", "difficulty": 4},
]

# 用户进度存储文件
PROGRESS_FILE = "word_progress.json"


class WordCard:
    def __init__(self, word_data, review_level=0, last_review=None, next_review=None):
        self.word = word_data["word"]
        self.meaning = word_data["meaning"]
        self.example = word_data["example"]
        self.category = word_data.get("category", "通用")
        self.difficulty = word_data.get("difficulty", 1)
        self.review_level = review_level  # 复习等级 (0-6)
        self.last_review = last_review if last_review else datetime.now()
        self.next_review = next_review if next_review else datetime.now()
        self.correct_streak = 0  # 连续答对次数
        self.mastery = 0  # 掌握度 (0-100)

    def to_dict(self):
        return {
            "word": self.word,
            "meaning": self.meaning,
            "example": self.example,
            "category": self.category,
            "difficulty": self.difficulty,
            "review_level": self.review_level,
            "last_review": self.last_review.isoformat(),
            "next_review": self.next_review.isoformat(),
            "correct_streak": self.correct_streak,
            "mastery": self.mastery
        }

    @classmethod
    def from_dict(cls, data):
        word_data = {
            "word": data["word"],
            "meaning": data["meaning"],
            "example": data["example"],
            "category": data.get("category", "通用"),
            "difficulty": data.get("difficulty", 1)
        }
        last_review = datetime.fromisoformat(data["last_review"])
        next_review = datetime.fromisoformat(data["next_review"])
        card = cls(word_data, data["review_level"], last_review, next_review)
        card.correct_streak = data.get("correct_streak", 0)
        card.mastery = data.get("mastery", 0)
        return card

    def update_review(self, remembered=True):
        self.last_review = datetime.now()

        if remembered:
            self.correct_streak += 1
            # 根据连续答对次数提高掌握度
            self.mastery = min(100, self.mastery + 10 + self.correct_streak * 2)

            # 如果记住了，进入下一复习等级
            if self.review_level < len(EBBINGHAUS_INTERVALS) - 1:
                self.review_level += 1
        else:
            self.correct_streak = 0
            self.mastery = max(0, self.mastery - 15)

            # 如果没记住，返回前一级
            if self.review_level > 0:
                self.review_level -= 1

        # 设置下一次复习时间
        interval_minutes = EBBINGHAUS_INTERVALS[self.review_level]
        self.next_review = datetime.now() + timedelta(minutes=interval_minutes)

    def is_due_for_review(self):
        return datetime.now() >= self.next_review

    def get_review_status(self):
        status_text = ["初次学习", "20分钟后", "1小时后", "9小时后", "1天后", "2天后", "6天后", "已掌握"]
        level = min(self.review_level, len(status_text) - 1)
        return status_text[level]

    def get_mastery_color(self):
        if self.mastery >= 90:
            return GOLD
        elif self.mastery >= 70:
            return SILVER
        elif self.mastery >= 50:
            return BRONZE
        else:
            return SECONDARY


class WordGame:
    def __init__(self):
        self.word_cards = []
        self.current_card_index = 0
        self.game_state = "menu"  # menu, game, result, collection
        self.score = 0
        self.total_reviewed = 0
        self.show_meaning = False
        self.game_mode = "review"  # review, challenge, speedrun
        self.combo = 0  # 连击数
        self.max_combo = 0
        self.streak_multiplier = 1.0
        self.time_limit = 60  # 挑战模式时间限制（秒）
        self.time_left = self.time_limit
        self.last_time = pygame.time.get_ticks()
        self.level = 1
        self.exp = 0
        self.exp_to_next_level = 100
        self.unlocked_categories = ["初级"]
        self.load_progress()

    def load_progress(self):
        # 加载用户进度或使用默认单词
        if os.path.exists(PROGRESS_FILE):
            try:
                with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.word_cards = [WordCard.from_dict(card_data) for card_data in data]
                print(f"已加载 {len(self.word_cards)} 个单词的进度")
            except Exception as e:
                print(f"加载进度失败: {e}, 使用默认单词")
                self.initialize_default_words()
        else:
            self.initialize_default_words()

    def initialize_default_words(self):
        self.word_cards = [WordCard(word_data) for word_data in default_words]

    def save_progress(self):
        try:
            data = [card.to_dict() for card in self.word_cards]
            with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存进度失败: {e}")

    def get_due_cards(self):
        # 获取需要复习的卡片
        return [card for card in self.word_cards if card.is_due_for_review()]

    def add_exp(self, amount):
        self.exp += amount * self.streak_multiplier
        if self.exp >= self.exp_to_next_level:
            self.exp -= self.exp_to_next_level
            self.level += 1
            self.exp_to_next_level = int(self.exp_to_next_level * 1.5)
            # 解锁新分类
            if self.level >= 5 and "中级" not in self.unlocked_categories:
                self.unlocked_categories.append("中级")
            if self.level >= 10 and "高级" not in self.unlocked_categories:
                self.unlocked_categories.append("高级")
            if self.level >= 15 and "专业" not in self.unlocked_categories:
                self.unlocked_categories.append("专业")
            return True
        return False

    def start_game(self, mode="review"):
        self.game_mode = mode
        due_cards = self.get_due_cards()

        if mode == "review":
            if not due_cards:
                # 如果没有需要复习的卡片，随机选择一些
                due_cards = random.sample(self.word_cards, min(10, len(self.word_cards)))

            # 如果卡片太少，使用所有卡片
            if len(due_cards) < 5:
                due_cards = self.word_cards[:10] if len(self.word_cards) >= 10 else self.word_cards

        elif mode == "challenge":
            # 挑战模式：混合所有单词
            due_cards = self.word_cards.copy()
            self.time_left = 90  # 挑战模式90秒
            self.score = 0

        elif mode == "speedrun":
            # 速度模式：只使用简单单词
            easy_cards = [card for card in self.word_cards if card.difficulty <= 2]
            due_cards = easy_cards[:20] if len(easy_cards) >= 20 else easy_cards
            self.time_left = 60  # 速度模式60秒
            self.score = 0

        self.game_cards = due_cards.copy()
        random.shuffle(self.game_cards)
        self.current_card_index = 0
        self.total_reviewed = len(self.game_cards)
        self.show_meaning = False
        self.game_state = "game"
        self.combo = 0
        self.streak_multiplier = 1.0
        self.last_time = pygame.time.get_ticks()

    def next_card(self, remembered=True):
        if self.current_card_index < len(self.game_cards):
            current_card = self.game_cards[self.current_card_index]
            current_card.update_review(remembered)

            if remembered:
                self.score += 1
                self.combo += 1
                self.max_combo = max(self.max_combo, self.combo)

                # 连击奖励
                if self.combo >= 5:
                    self.streak_multiplier = 1.0 + (self.combo // 5) * 0.2

                # 经验值奖励
                exp_gained = current_card.difficulty * 10
                level_up = self.add_exp(exp_gained)

            else:
                self.combo = 0
                self.streak_multiplier = 1.0

            self.current_card_index += 1
            self.show_meaning = False

            # 如果所有卡片都复习完了，进入结果界面
            if self.current_card_index >= len(self.game_cards):
                self.game_state = "result"
                self.save_progress()

    def update_timer(self):
        current_time = pygame.time.get_ticks()
        elapsed = (current_time - self.last_time) / 1000.0
        self.last_time = current_time

        if self.game_mode in ["challenge", "speedrun"]:
            self.time_left -= elapsed

            if self.time_left <= 0:
                self.time_left = 0
                self.game_state = "result"
                self.save_progress()

    def draw_menu(self):
        screen.fill(BACKGROUND)

        # 清新的装饰元素 - 简单的圆形图案
        for i in range(8):
            x = random.randint(50, WIDTH - 50)
            y = random.randint(50, HEIGHT - 50)
            size = random.randint(30, 80)
            alpha = random.randint(20, 50)
            color = (*PRIMARY, alpha)
            s = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            pygame.draw.circle(s, color, (size, size), size)
            screen.blit(s, (int(x - size), int(y - size)))

        # 标题
        title = title_font.render("单词大冒险", True, PRIMARY)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 60))

        subtitle = info_font.render("基于艾宾浩斯遗忘曲线的记忆游戏", True, SECONDARY)
        screen.blit(subtitle, (WIDTH // 2 - subtitle.get_width() // 2, 120))

        # 玩家信息卡片
        info_card = pygame.Rect(WIDTH // 2 - 250, 180, 500, 140)
        pygame.draw.rect(screen, CARD_BG, info_card, border_radius=20)
        pygame.draw.rect(screen, SHADOW, info_card, 2, border_radius=20)

        info_y = 200
        player_info = [
            f"等级: {self.level}",
            f"经验: {self.exp}/{self.exp_to_next_level}",
            f"最高连击: {self.max_combo}",
            f"已解锁分类: {', '.join(self.unlocked_categories)}"
        ]

        for i, info in enumerate(player_info):
            info_text = info_font.render(info, True, TEXT_COLOR)
            screen.blit(info_text, (WIDTH // 2 - info_text.get_width() // 2, info_y + i * 30))

        # 游戏模式选择
        modes_y = 360
        modes = [
            ("复习模式", "按遗忘曲线复习单词", "review"),
            ("挑战模式", "限时挑战，测试单词掌握", "challenge"),
            ("速度模式", "快速回答简单单词", "speedrun"),
            ("单词收藏", "查看已掌握的单词", "collection")
        ]

        mode_buttons = []
        for i, (title, desc, mode) in enumerate(modes):
            button_rect = pygame.Rect(WIDTH // 2 - 250, modes_y + i * 100, 500, 80)
            mode_buttons.append((button_rect, mode))

            # 按钮颜色
            if mode in ["challenge", "speedrun"] and self.level < 3:
                color = (220, 210, 200)  # 温暖的灰色
                text_color = (150, 140, 130)
            else:
                color = PRIMARY
                text_color = WHITE

            # 按钮阴影
            shadow_rect = button_rect.copy()
            shadow_rect.x += 3
            shadow_rect.y += 3
            pygame.draw.rect(screen, SHADOW, shadow_rect, border_radius=15)

            # 按钮主体
            pygame.draw.rect(screen, color, button_rect, border_radius=15)

            # 按钮标题
            title_text = button_font.render(title, True, text_color)
            screen.blit(title_text, (button_rect.x + 20, button_rect.y + 15))

            # 按钮描述
            desc_text = small_font.render(desc, True, text_color if text_color != WHITE else LIGHT_BLUE)
            screen.blit(desc_text, (button_rect.x + 20, button_rect.y + 50))

            # 如果未解锁，显示锁图标
            if mode in ["challenge", "speedrun"] and self.level < 3:
                lock_text = small_font.render("🔒 需要等级3", True, text_color)
                screen.blit(lock_text, (button_rect.right - 120, button_rect.y + 30))

        # 进度条
        progress_width = 600
        progress_height = 20
        progress_x = (WIDTH - progress_width) // 2
        progress_y = 750

        due_cards = self.get_due_cards()

        # 进度条背景
        pygame.draw.rect(screen, LIGHT_BLUE, (progress_x, progress_y, progress_width, progress_height),
                         border_radius=10)

        # 进度条填充
        total_progress = (len(self.word_cards) - len(due_cards)) / len(self.word_cards) if self.word_cards else 0
        fill_width = int(progress_width * total_progress)
        pygame.draw.rect(screen, PRIMARY, (progress_x, progress_y, fill_width, progress_height), border_radius=10)

        progress_text = info_font.render(f"今日进度: {len(self.word_cards) - len(due_cards)}/{len(self.word_cards)}",
                                         True, TEXT_COLOR)
        screen.blit(progress_text, (WIDTH // 2 - progress_text.get_width() // 2, progress_y - 30))

        return mode_buttons

    def draw_game(self):
        screen.fill(BACKGROUND)

        # 更新计时器
        self.update_timer()

        if self.current_card_index >= len(self.game_cards):
            return []

        current_card = self.game_cards[self.current_card_index]

        # 顶部状态栏
        status_bar = pygame.Rect(0, 0, WIDTH, 70)
        pygame.draw.rect(screen, PRIMARY, status_bar)

        # 分数和连击
        score_text = info_font.render(f"分数: {self.score}", True, WHITE)
        screen.blit(score_text, (20, 20))

        if self.combo >= 3:
            combo_text = info_font.render(f"🔥 连击: {self.combo} x{self.streak_multiplier:.1f}", True, GOLD)
            screen.blit(combo_text, (WIDTH // 2 - combo_text.get_width() // 2, 20))

        # 计时器（仅限挑战模式）
        if self.game_mode in ["challenge", "speedrun"]:
            time_text = info_font.render(f"⏱️ 时间: {int(self.time_left)}秒", True, WHITE)
            screen.blit(time_text, (WIDTH - 180, 20))

        # 进度
        progress_text = info_font.render(f"📚 进度: {self.current_card_index + 1}/{len(self.game_cards)}", True, WHITE)
        screen.blit(progress_text, (WIDTH - 280, 20))

        # 单词卡片 - 清新风格
        card_rect = pygame.Rect(WIDTH // 2 - 400, 120, 800, 500)

        # 卡片阴影
        shadow_rect = card_rect.copy()
        shadow_rect.x += 5
        shadow_rect.y += 5
        pygame.draw.rect(screen, SHADOW, shadow_rect, border_radius=25)

        # 卡片背景
        pygame.draw.rect(screen, CARD_BG, card_rect, border_radius=25)
        pygame.draw.rect(screen, PRIMARY, card_rect, 3, border_radius=25)

        # 装饰花边
        for i in range(4):
            x = card_rect.x + 20 + i * (card_rect.width - 40) // 3
            pygame.draw.circle(screen, LIGHT_BLUE, (x, card_rect.y + 30), 5)
            pygame.draw.circle(screen, LIGHT_BLUE, (x, card_rect.bottom - 30), 5)

        # 单词
        word_text = word_font.render(current_card.word, True, PRIMARY)
        screen.blit(word_text, (WIDTH // 2 - word_text.get_width() // 2, 200))

        # 分类和难度
        category_text = info_font.render(f"📖 {current_card.category}  |  {'⭐' * current_card.difficulty}", True,
                                         SECONDARY)
        screen.blit(category_text, (WIDTH // 2 - category_text.get_width() // 2, 290))

        # 复习状态
        status_text = info_font.render(f"📅 {current_card.get_review_status()}  |  🎯 掌握度: {current_card.mastery}%",
                                       True, SECONDARY)
        screen.blit(status_text, (WIDTH // 2 - status_text.get_width() // 2, 340))

        # 显示释义按钮
        if not self.show_meaning:
            show_button = pygame.Rect(WIDTH // 2 - 150, 480, 300, 60)

            # 按钮阴影
            show_shadow = show_button.copy()
            show_shadow.x += 2
            show_shadow.y += 2
            pygame.draw.rect(screen, SHADOW, show_shadow, border_radius=12)

            # 按钮主体
            pygame.draw.rect(screen, ACCENT, show_button, border_radius=12)
            show_text = button_font.render("📖 显示释义", True, WHITE)
            screen.blit(show_text, (WIDTH // 2 - show_text.get_width() // 2, 495))

            # 返回按钮
            back_button = pygame.Rect(30, 30, 100, 40)
            pygame.draw.rect(screen, LIGHT_BLUE, back_button, border_radius=8)
            back_text = small_font.render("🏠 返回", True, TEXT_COLOR)
            screen.blit(back_text, (back_button.x + 15, back_button.y + 10))

            return [show_button, back_button]
        else:
            # 显示释义
            meaning_text = button_font.render(current_card.meaning, True, ACCENT)
            screen.blit(meaning_text, (WIDTH // 2 - meaning_text.get_width() // 2, 400))

            # 例句
            example_text = f"💬 例句: {current_card.example}"
            example_lines = self.wrap_text(example_text, info_font, 700)
            for i, line in enumerate(example_lines):
                line_surface = info_font.render(line, True, TEXT_COLOR)
                screen.blit(line_surface, (WIDTH // 2 - line_surface.get_width() // 2, 460 + i * 35))

            # 记住和忘记按钮
            remember_button = pygame.Rect(WIDTH // 2 - 320, 580, 280, 60)
            forget_button = pygame.Rect(WIDTH // 2 + 40, 580, 280, 60)

            # 记住按钮阴影
            remember_shadow = remember_button.copy()
            remember_shadow.x += 2
            remember_shadow.y += 2
            pygame.draw.rect(screen, SHADOW, remember_shadow, border_radius=12)
            pygame.draw.rect(screen, CORRECT_COLOR, remember_button, border_radius=12)

            # 忘记按钮阴影
            forget_shadow = forget_button.copy()
            forget_shadow.x += 2
            forget_shadow.y += 2
            pygame.draw.rect(screen, SHADOW, forget_shadow, border_radius=12)
            pygame.draw.rect(screen, WRONG_COLOR, forget_button, border_radius=12)

            remember_text = button_font.render("✓ 记住了 (空格键)", True, WHITE)
            forget_text = button_font.render("✗ 忘记了 (F键)", True, WHITE)

            screen.blit(remember_text, (remember_button.x + 35, remember_button.y + 15))
            screen.blit(forget_text, (forget_button.x + 35, forget_button.y + 15))

            # 返回按钮
            back_button = pygame.Rect(30, 30, 100, 40)
            pygame.draw.rect(screen, LIGHT_BLUE, back_button, border_radius=8)
            back_text = small_font.render("🏠 返回", True, TEXT_COLOR)
            screen.blit(back_text, (back_button.x + 15, back_button.y + 10))

            return [remember_button, forget_button, back_button]

    def draw_result(self):
        screen.fill(BACKGROUND)

        # 标题
        title = title_font.render("🎉 挑战完成! 🎉", True, PRIMARY)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 60))

        # 结果卡片
        result_card = pygame.Rect(WIDTH // 2 - 350, 140, 700, 550)

        # 卡片阴影
        shadow_rect = result_card.copy()
        shadow_rect.x += 5
        shadow_rect.y += 5
        pygame.draw.rect(screen, SHADOW, shadow_rect, border_radius=25)

        # 卡片背景
        pygame.draw.rect(screen, CARD_BG, result_card, border_radius=25)
        pygame.draw.rect(screen, PRIMARY, result_card, 3, border_radius=25)

        # 分数
        percentage = int((self.score / self.total_reviewed) * 100) if self.total_reviewed > 0 else 0

        # 评级
        if percentage >= 90:
            grade = "S级 大师"
            grade_color = GOLD
            emoji = "🏆"
        elif percentage >= 80:
            grade = "A级 优秀"
            grade_color = SILVER
            emoji = "🌟"
        elif percentage >= 70:
            grade = "B级 良好"
            grade_color = BRONZE
            emoji = "⭐"
        elif percentage >= 60:
            grade = "C级 及格"
            grade_color = SECONDARY
            emoji = "📚"
        else:
            grade = "D级 需努力"
            grade_color = WRONG_COLOR
            emoji = "💪"

        grade_text = word_font.render(f"{emoji} {grade}", True, grade_color)
        screen.blit(grade_text, (WIDTH // 2 - grade_text.get_width() // 2, 200))

        # 详情
        details_y = 300
        details = [
            f"📊 准确率: {percentage}% ({self.score}/{self.total_reviewed})",
            f"🔥 最高连击: {self.max_combo}",
            f"✨ 经验获得: {int(self.exp)}",
            f"🎮 游戏模式: {'复习模式' if self.game_mode == 'review' else '挑战模式' if self.game_mode == 'challenge' else '速度模式'}"
        ]

        for i, detail in enumerate(details):
            detail_text = info_font.render(detail, True, TEXT_COLOR)
            screen.blit(detail_text, (WIDTH // 2 - detail_text.get_width() // 2, details_y + i * 45))

        # 掌握度分布
        mastery_y = 500
        mastery_title = info_font.render("📈 单词掌握度分布:", True, SECONDARY)
        screen.blit(mastery_title, (WIDTH // 2 - mastery_title.get_width() // 2, mastery_y))

        mastery_levels = [0, 0, 0, 0]  # 0-30%, 31-60%, 61-90%, 91-100%
        for card in self.word_cards:
            if card.mastery <= 30:
                mastery_levels[0] += 1
            elif card.mastery <= 60:
                mastery_levels[1] += 1
            elif card.mastery <= 90:
                mastery_levels[2] += 1
            else:
                mastery_levels[3] += 1

        bar_width = 500
        bar_height = 25
        bar_x = (WIDTH - bar_width) // 2
        bar_y = mastery_y + 50

        colors = [WRONG_COLOR, SECONDARY, CORRECT_COLOR, GOLD]
        labels = ["新手", "入门", "熟练", "精通"]

        for i in range(4):
            if self.word_cards:
                ratio = mastery_levels[i] / len(self.word_cards)
            else:
                ratio = 0

            # 进度条
            bar_segment_width = int(bar_width * ratio)
            pygame.draw.rect(screen, colors[i], (bar_x, bar_y + i * 45, bar_segment_width, bar_height), border_radius=5)
            pygame.draw.rect(screen, TEXT_COLOR, (bar_x, bar_y + i * 45, bar_width, bar_height), 2, border_radius=5)

            # 标签
            label_text = small_font.render(f"{labels[i]}: {mastery_levels[i]}个 ({ratio * 100:.1f}%)", True, TEXT_COLOR)
            screen.blit(label_text, (bar_x + bar_width + 20, bar_y + i * 45 + 5))

        # 返回按钮
        back_button = pygame.Rect(WIDTH // 2 - 150, 700, 300, 60)

        # 按钮阴影
        back_shadow = back_button.copy()
        back_shadow.x += 2
        back_shadow.y += 2
        pygame.draw.rect(screen, SHADOW, back_shadow, border_radius=15)

        # 按钮主体
        pygame.draw.rect(screen, PRIMARY, back_button, border_radius=15)

        back_text = button_font.render("🏠 返回主菜单", True, WHITE)
        screen.blit(back_text, (WIDTH // 2 - back_text.get_width() // 2, 715))

        return [back_button]

    def draw_collection(self):
        screen.fill(BACKGROUND)

        # 标题
        title = title_font.render("📚 我的单词收藏", True, PRIMARY)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 40))

        # 统计卡片
        mastered = len([c for c in self.word_cards if c.mastery >= 90])
        total = len(self.word_cards)

        stats_card = pygame.Rect(WIDTH // 2 - 200, 100, 400, 70)
        pygame.draw.rect(screen, CARD_BG, stats_card, border_radius=15)
        pygame.draw.rect(screen, PRIMARY, stats_card, 2, border_radius=15)

        stats_text = info_font.render(f"✨ 已精通 {mastered}/{total} 个单词 ({mastered / total * 100:.1f}%)", True,
                                      TEXT_COLOR)
        screen.blit(stats_text, (WIDTH // 2 - stats_text.get_width() // 2, 120))

        # 单词列表
        list_y = 200
        cards_per_page = 8

        # 显示前8个单词作为示例
        display_cards = self.word_cards[:min(cards_per_page, len(self.word_cards))]

        for i, card in enumerate(display_cards):
            card_y = list_y + i * 70

            # 卡片背景
            card_rect = pygame.Rect(100, card_y, WIDTH - 200, 65)
            pygame.draw.rect(screen, CARD_BG, card_rect, border_radius=12)
            pygame.draw.rect(screen, card.get_mastery_color(), card_rect, 2, border_radius=12)

            # 单词
            word_text = info_font.render(card.word, True, PRIMARY)
            screen.blit(word_text, (120, card_y + 18))

            # 释义
            meaning_text = small_font.render(card.meaning, True, SECONDARY)
            screen.blit(meaning_text, (350, card_y + 22))

            # 掌握度
            mastery_text = small_font.render(f"🎯 掌握度: {card.mastery}%", True, card.get_mastery_color())
            screen.blit(mastery_text, (WIDTH - 280, card_y + 22))

            # 复习状态
            status_text = small_font.render(f"📅 {card.get_review_status()}", True, TEXT_COLOR)
            screen.blit(status_text, (WIDTH - 150, card_y + 22))

        # 提示信息
        if len(self.word_cards) > cards_per_page:
            hint_text = info_font.render(
                f"... 还有 {len(self.word_cards) - cards_per_page} 个单词未显示，继续学习解锁更多内容", True, SECONDARY)
            screen.blit(hint_text, (WIDTH // 2 - hint_text.get_width() // 2, list_y + cards_per_page * 70 + 30))

        # 返回按钮
        back_button = pygame.Rect(50, 50, 100, 40)
        pygame.draw.rect(screen, LIGHT_BLUE, back_button, border_radius=8)
        back_text = small_font.render("🏠 返回", True, TEXT_COLOR)
        screen.blit(back_text, (back_button.x + 25, back_button.y + 10))

        return [back_button]

    def wrap_text(self, text, font, max_width):
        """文本换行"""
        words = text.split()
        lines = []
        current_line = []

        for word in words:
            # 测试添加当前单词后行的宽度
            test_line = ' '.join(current_line + [word])
            test_surface = font.render(test_line, True, TEXT_COLOR)

            if test_surface.get_width() <= max_width:
                current_line.append(word)
            else:
                # 如果当前行不为空，保存它
                if current_line:
                    lines.append(' '.join(current_line))
                # 开始新行
                current_line = [word]

        # 添加最后一行
        if current_line:
            lines.append(' '.join(current_line))

        return lines

    def draw(self):
        if self.game_state == "menu":
            return self.draw_menu()
        elif self.game_state == "game":
            return self.draw_game()
        elif self.game_state == "result":
            return self.draw_result()
        elif self.game_state == "collection":
            return self.draw_collection()

    def handle_click(self, pos):
        if self.game_state == "menu":
            mode_buttons = self.draw()
            for button_rect, mode in mode_buttons:
                if button_rect.collidepoint(pos):
                    if mode in ["challenge", "speedrun"] and self.level < 3:
                        continue  # 未解锁
                    elif mode == "collection":
                        self.game_state = "collection"
                    else:
                        self.start_game(mode)

        elif self.game_state == "game":
            buttons = self.draw()

            if not self.show_meaning:
                if len(buttons) >= 2:
                    show_button, back_button = buttons[0], buttons[1]
                    if show_button.collidepoint(pos):
                        self.show_meaning = True
                    elif back_button.collidepoint(pos):
                        self.game_state = "menu"
            else:
                if len(buttons) >= 3:
                    remember_button, forget_button, back_button = buttons[0], buttons[1], buttons[2]
                    if remember_button.collidepoint(pos):
                        self.next_card(remembered=True)
                    elif forget_button.collidepoint(pos):
                        self.next_card(remembered=False)
                    elif back_button.collidepoint(pos):
                        self.game_state = "menu"

        elif self.game_state == "result":
            back_button = self.draw()[0]
            if back_button.collidepoint(pos):
                self.game_state = "menu"

        elif self.game_state == "collection":
            buttons = self.draw()
            back_button = buttons[0]
            if back_button.collidepoint(pos):
                self.game_state = "menu"


def main():
    game = WordGame()
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.save_progress()
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # 左键点击
                    game.handle_click(event.pos)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game.game_state = "menu"
                elif event.key == pygame.K_SPACE and game.game_state == "game":
                    if game.show_meaning:
                        game.next_card(remembered=True)
                    else:
                        game.show_meaning = True
                elif event.key == pygame.K_f and game.game_state == "game" and game.show_meaning:
                    game.next_card(remembered=False)
                elif event.key == pygame.K_c and game.game_state == "menu":
                    game.game_state = "collection"

        # 绘制界面
        game.draw()

        # 更新显示
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()