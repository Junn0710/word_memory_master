# 单词记忆大师 - 艾宾浩斯遗忘曲线背单词游戏

<div align="center">
https://img.shields.io/badge/%E7%89%88%E6%9C%AC-1.0.0-8FBC8F.svg
https://img.shields.io/badge/%E5%B9%B3%E5%8F%B0-%E5%BE%AE%E4%BF%A1%E5%B0%8F%E7%A8%8B%E5%BA%8F-07C160.svg
https://img.shields.io/badge/license-MIT-FFC19E.svg
https://img.shields.io/badge/PRs-welcome-8FBC8F.svg

English | 中文

</div>

## 📖 项目简介

**单词记忆大师**是一款基于**艾宾浩斯遗忘曲线**理论的桌面背单词游戏。它将科学的记忆算法与游戏化设计相结合，让背单词变得轻松有趣。

## ✨ 核心特性

### 🎯 科学记忆算法
- **艾宾浩斯遗忘曲线**：复习间隔为 20分钟 → 1小时 → 9小时 → 1天 → 2天 → 6天 → 31天
- **智能复习系统**：自动计算每个单词的最佳复习时间
- **掌握度评估**：根据答对次数动态调整单词掌握程度

### 🎮 三种游戏模式

#### 1. 复习模式
- 基于遗忘曲线智能推送需要复习的单词
- 适合日常学习和巩固
- 自动保存学习进度

#### 2. 挑战模式 ⭐
- 90秒限时挑战
- 测试单词掌握速度
- 获得额外经验加成

#### 3. 速度模式 ⚡
- 60秒快速问答
- 仅包含简单单词
- 提升反应速度

### 🏆 游戏化系统

#### 等级成长
```
等级 1 → 解锁基础单词库
等级 3 → 解锁挑战模式和速度模式
等级 5 → 解锁中级单词库
等级 10 → 解锁高级单词库
等级 15 → 解锁专业单词库
```

#### 连击系统
- 连续答对获得连击加成
- 5连击以上获得经验倍率提升
- 最高连击记录保存

#### 经验值系统
- 学习新单词获得经验
- 复习旧单词获得经验
- 连击加成额外经验

### 📚 丰富单词库

#### 四级难度体系
- ⭐ 初级词汇（5个）
- ⭐⭐ 中级词汇（5个）
- ⭐⭐⭐ 高级词汇（5个）
- ⭐⭐⭐⭐ 专业词汇（5个）

#### 十大分类
- 动作类 | 生活类 | 职业类 | 性格类 | 外观类
- 科技类 | 情感类 | 学术类 | 艺术类 | 描述类

## 🎨 界面特色

### 清新温馨配色
- **主色调**：草绿色 (#8FBC8F) - 清新自然
- **背景色**：米白色 (#FCF5EB) - 温暖舒适
- **强调色**：杏色 (#FFC19E) - 柔和温暖

### 视觉设计
- 圆润的卡片设计
- 柔和的阴影效果
- 流畅的动画过渡
- 友好的视觉反馈

## 🚀 快速开始

### 系统要求

- **操作系统**：Windows 7+ / macOS 10.12+ / Linux
- **Python版本**：3.7 或更高版本
- **依赖库**：pygame 2.0+

### 安装步骤

1. **克隆项目**

```bash
git clone https://github.com/yourusername/word-memory-master.git
cd word-memory-master
```

2. **安装依赖**

```bash
pip install pygame
```

3. **运行游戏**

```bash
python word_game.py
```

### 游戏控制

| 按键 | 功能 |
|------|------|
| 鼠标左键 | 点击按钮进行选择 |
| 空格键 | 显示释义 / 标记"记住了" |
| F键 | 标记"忘记了" |
| ESC键 | 返回主菜单 |
| C键 | 打开单词收藏 |

## 📖 游戏玩法

### 学习流程

1. **主菜单选择模式**
   - 复习模式：日常学习
   - 挑战模式：限时挑战
   - 速度模式：快速练习

2. **单词学习**
   ```
   显示单词 → 尝试回忆 → 显示释义 → 选择记忆情况
   ```

3. **复习安排**
   - 记住：推迟复习时间
   - 忘记：提前复习时间
   - 系统自动调整复习间隔

### 掌握度系统

每个单词都有掌握度百分比：
- **0-30%**：新手 - 需要重点复习
- **31-60%**：入门 - 初步掌握
- **61-90%**：熟练 - 基本掌握
- **91-100%**：精通 - 完全掌握

## 🛠 技术实现

### 技术栈

- **开发语言**：Python 3.7+
- **图形框架**：Pygame 2.0
- **数据存储**：JSON文件
- **架构模式**：面向对象

### 核心算法

#### 复习间隔计算

```python
# 艾宾浩斯遗忘曲线复习间隔（分钟）
EBBINGHAUS_INTERVALS = [20, 60, 540, 1440, 2880, 8640, 44640]

def update_review(self, remembered=True):
    if remembered:
        self.review_level = min(self.review_level + 1, 6)
        self.mastery = min(100, self.mastery + 10 + self.correct_streak * 2)
    else:
        self.review_level = max(self.review_level - 1, 0)
        self.mastery = max(0, self.mastery - 15)
    
    interval = EBBINGHAUS_INTERVALS[self.review_level]
    self.next_review = datetime.now() + timedelta(minutes=interval)
```

#### 经验值计算

```python
def add_exp(self, amount):
    self.exp += amount * self.streak_multiplier
    if self.exp >= self.exp_to_next_level:
        self.exp -= self.exp_to_next_level
        self.level += 1
        self.exp_to_next_level = int(self.exp_to_next_level * 1.5)
        return True
    return False
```

## 📁 项目结构

```
word-memory-master/
│
├── word_game.py           # 主游戏文件
├── word_progress.json     # 学习进度数据（自动生成）
├── requirements.txt       # 依赖包列表
├── README.md             # 项目说明
│
├── screenshots/          # 截图文件夹
│   ├── menu.png
│   ├── game.png
│   └── result.png
│
└── docs/                 # 文档文件夹
    ├── 使用说明.md
    └── 开发文档.md
```

## 🎯 功能演示

### 主菜单
- 显示玩家等级和经验
- 四种游戏模式选择
- 学习进度统计
- 艾宾浩斯曲线说明

### 游戏界面
- 顶部状态栏（分数、连击、进度）
- 单词卡片（渐变背景）
- 掌握度显示
- 分类和难度标识

### 结果界面
- 准确率统计
- 评级系统（S/A/B/C/D）
- 经验获得显示
- 掌握度分布图表

## 📊 数据存储

### 单词数据结构

```json
{
  "word": "example",
  "meaning": "例子",
  "example": "This is an example.",
  "category": "生活",
  "difficulty": 1,
  "review_level": 3,
  "mastery": 75,
  "last_review": "2024-01-15T10:30:00",
  "next_review": "2024-01-16T10:30:00",
  "correct_streak": 5
}
```

### 用户数据结构

```json
{
  "level": 5,
  "exp": 250,
  "exp_to_next_level": 300,
  "max_combo": 12
}
```

## 🔧 自定义配置

### 添加新单词

编辑 `word_game.py` 中的 `default_words` 列表：

```python
default_words = [
    {
        "word": "your_word",
        "meaning": "你的释义",
        "example": "你的例句",
        "category": "分类",
        "difficulty": 1  # 1-4
    },
    # 更多单词...
]
```

### 修改配色

在 `word_game.py` 顶部修改颜色常量：

```python
BACKGROUND = (252, 245, 235)  # 背景色
PRIMARY = (143, 188, 143)     # 主色调
ACCENT = (255, 193, 158)      # 强调色
```

## 🤝 贡献指南

欢迎贡献代码！以下是参与方式：

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📝 更新日志

### v2.0.0 (2024-01-15)
- ✨ 新增三种游戏模式
- ✨ 新增等级和经验系统
- ✨ 新增连击系统
- 🎨 全新清新温馨界面
- 📊 新增学习统计图表
- 🐛 修复文本换行问题

### v1.0.0 (2024-01-01)
- 🎉 首次发布
- 📚 基础单词学习功能
- 🔄 艾宾浩斯复习算法
- 💾 本地进度保存

## ⭐ Star History

如果这个项目对你有帮助，欢迎 star ⭐️

---

<div align="center">

**让记忆单词成为一种享受，而不是负担！**

Made with ❤️ by Word Memory Master Team

</div>
