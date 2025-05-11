import pygame
import sys
import math
import random
import os
import time

# 初始化Pygame
pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=4096)  # 设置音频参数
pygame.font.init()  # 确保字体系统初始化

# 设置窗口
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("母亲节快乐！")

# 颜色定义
PINK = (255, 192, 203)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GOLD = (255, 215, 0)
LIGHT_PINK = (255, 228, 225)
DEEP_PINK = (255, 20, 147)  # 深粉色

# 加载字体
try:
    # 尝试加载中文字体
    font_path = os.path.join(os.path.dirname(__file__), "simhei.ttf")
    if os.path.exists(font_path):
        font = pygame.font.Font(font_path, 36)
        small_font = pygame.font.Font(font_path, 24)
        lyrics_font = pygame.font.Font(font_path, 28)
    else:
        # 如果没有找到字体文件，尝试使用系统字体
        font = pygame.font.SysFont("simhei", 36)
        small_font = pygame.font.SysFont("simhei", 24)
        lyrics_font = pygame.font.SysFont("simhei", 28)
except Exception as e:
    print(f"加载字体失败: {e}")
    print("请下载 simhei.ttf 字体文件并放在程序同目录下")
    sys.exit(1)

class Heart:
    def __init__(self):
        self.reset()
        self.size = random.randint(10, 30)
        self.color = (random.randint(200, 255), random.randint(100, 200), random.randint(100, 200))

    def reset(self):
        self.x = random.randint(0, WINDOW_WIDTH)
        self.y = WINDOW_HEIGHT + 20
        self.speed = random.uniform(1, 3)

    def update(self):
        self.y -= self.speed
        if self.y < -20:
            self.reset()

    def draw(self, surface):
        points = []
        for i in range(360):
            angle = math.radians(i)
            x = self.x + self.size * 16 * math.sin(angle) ** 3
            y = self.y - self.size * (13 * math.cos(angle) - 5 * math.cos(2*angle) - 2 * math.cos(3*angle) - math.cos(4*angle))
            points.append((x, y))
        pygame.draw.polygon(surface, self.color, points)

def check_music_file():
    """检查音乐文件是否存在，如果不存在则提示用户"""
    music_file = "song1.mp3"
    if not os.path.exists(music_file):
        print(f"提示：要播放音乐，请将音乐文件命名为 '{music_file}' 并放在程序同目录下")
        print(f"当前目录: {os.path.dirname(os.path.abspath(__file__))}")
        return False
    return True

def play_music():
    """播放音乐的函数"""
    try:
        pygame.mixer.music.load("song1.mp3")
        pygame.mixer.music.set_volume(0.5)  # 设置音量为50%
        pygame.mixer.music.play(-1)  # -1表示循环播放
        return True
    except Exception as e:
        print(f"播放音乐时出错: {e}")
        return False

def main():
    clock = pygame.time.Clock()
    hearts = [Heart() for _ in range(15)]
    
    messages = [
        "亲爱的妈妈，祝您母亲节快乐！",
        "感谢您一直以来的付出和关爱",
        "愿您永远健康快乐",
        "您是我生命中最重要的人",
        "我爱您！",
        "您是我心中最温暖的阳光",
        "您的爱是我最珍贵的礼物",
        "感谢您无私的奉献",
        "您是我永远的依靠",
        "愿您永远年轻美丽",
        "您的笑容是我最大的幸福",
        "感谢您教会我成长",
        "您是我最坚强的后盾",
        "愿您每天都开开心心",
        "您是我最爱的妈妈",
        "感谢您为我付出的一切",
        "愿您永远健康平安",
        "您是我生命中最重要的人",
        "感谢您一直陪伴着我",
        "愿您永远幸福快乐",
        "您是我最温暖的港湾",
        "感谢您给予我生命",
        "愿您永远年轻漂亮",
        "您是我最亲爱的妈妈",
        "感谢您无私的爱",
        "愿您永远健康长寿",
        "您是我最敬爱的人",
        "感谢您为我遮风挡雨",
        "愿您永远开心快乐",
        "您是我最爱的母亲"
    ]
    
    current_message = 0
    message_alpha = 255
    message_timer = 0
    playing_music = False
    intro_timer = 0  # 前奏计时器
    music_start_timer = 0  # 音乐开始后的计时器
    
    # 检查音乐文件
    has_music = check_music_file()
    
    # 直接开始播放音乐
    if has_music:
        play_music()
        playing_music = True
    
    running = True
    while running:
        try:
            screen.fill(LIGHT_PINK)
            
            # 更新和绘制心形
            for heart in hearts:
                heart.update()
                heart.draw(screen)
            
            # 显示标题和祝福语
            if playing_music:
                if intro_timer < 600:  # 前奏期间
                    # 计算字体大小，从36逐渐增加到72
                    font_size = 36 + int((intro_timer / 600) * 36)
                    big_font = pygame.font.Font(font_path, font_size) if os.path.exists(font_path) else pygame.font.SysFont("simhei", font_size)
                    title = big_font.render("母亲节快乐", True, DEEP_PINK)
                    title_rect = title.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 50))
                    screen.blit(title, title_rect)
                    intro_timer += 1
                else:
                    # 前奏结束后保持大号字体
                    big_font = pygame.font.Font(font_path, 72) if os.path.exists(font_path) else pygame.font.SysFont("simhei", 72)
                    title = big_font.render("母亲节快乐", True, DEEP_PINK)
                    title_rect = title.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 50))
                    screen.blit(title, title_rect)
                    
                    # 音乐开始后的计时
                    if music_start_timer < 60:  # 等待1秒（前奏结束后）
                        music_start_timer += 1
                    else:
                        if current_message < len(messages):
                            message = lyrics_font.render(messages[current_message], True, PINK)
                            message.set_alpha(message_alpha)
                            # 将祝福语位置调整到标题下方
                            message_rect = message.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 50))
                            screen.blit(message, message_rect)
                            
                            message_timer += 1
                            # 每句祝福语显示8.5秒
                            frames = 510  # 8.5秒 * 60帧/秒
                            if message_timer >= frames:
                                message_timer = 0
                                message_alpha = 255
                                current_message += 1
                                if current_message >= len(messages):
                                    running = False  # 显示完所有祝福语后结束程序
            
            # 淡出效果
            if message_timer > 390:  # 最后2秒开始淡出
                message_alpha = max(0, message_alpha - 5)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            pygame.display.flip()
            clock.tick(60)
            
        except Exception as e:
            print(f"运行时错误: {e}")
            running = False

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main() 