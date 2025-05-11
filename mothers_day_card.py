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
DEEP_PINK = (255, 20, 147)  # 添加深粉色

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
    music_file = "周杰伦 - 听妈妈的话.mp3"
    if not os.path.exists(music_file):
        print(f"提示：要播放音乐，请将音乐文件命名为 '{music_file}' 并放在程序同目录下")
        print(f"当前目录: {os.path.dirname(os.path.abspath(__file__))}")
        return False
    return True

def play_music():
    """播放音乐的函数"""
    try:
        pygame.mixer.music.load("周杰伦 - 听妈妈的话.mp3")
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
        "我爱您！"
    ]
    
    # 歌词及其对应的显示时间（单位：秒）
    lyrics = [
      ("小朋友你是否有很多问号", 2),
("为什么别人在那看漫画", 2),
("我却在学画画对着钢琴说话", 2),
("别人在玩游戏", 0.5),
("我却靠在墙壁背我的ABC", 1),
("我说我要一台大大的飞机", 2.5),
("但却得到一台旧旧录音机", 2.5),
("为什么要听妈妈的话", 8),
("长大后你就会开始懂了这段话", 2.5),
("长大后我开始明白", 1.5),
("为什么我跑得比别人快", 0.2),
("飞得比别人高", 0.3),
("将来大家看的都是我画的漫画", 2.8),
("大家唱的都是我写的歌", 2.5),
("妈妈的辛苦不让你看见", 2),
("温暖的食谱在她心里面", 2.2),
("有空就多多握握她的手", 3),
("把手牵着一起梦游", 1.8),
("听妈妈的话别让她受伤", 9),
("想快快长大才能保护她", 9),
("美丽的白发幸福中发芽", 8.3),
("天使的魔法温暖中慈祥", 8.1)
    ]
    
    current_message = 0
    current_lyric = 0
    show_message = True
    show_lyrics = False
    message_alpha = 255
    lyric_alpha = 255
    message_timer = 0
    lyric_timer = 0
    playing_music = False
    intro_timer = 0  # 前奏计时器
    music_start_timer = 0  # 音乐开始后的计时器
    
    # 检查音乐文件
    has_music = check_music_file()
    
    running = True
    while running:
        try:
            screen.fill(LIGHT_PINK)
            
            # 更新和绘制心形
            for heart in hearts:
                heart.update()
                heart.draw(screen)
            
            # 显示消息
            if show_message:
                # 计算字体大小，从36逐渐增加到72
                font_size = 36 + int((message_timer / 180) * 36)
                message_font = pygame.font.Font(font_path, font_size) if os.path.exists(font_path) else pygame.font.SysFont("simhei", font_size)
                message = message_font.render(messages[current_message], True, PINK)
                message.set_alpha(message_alpha)
                message_rect = message.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
                screen.blit(message, message_rect)
                
                message_timer += 1
                if message_timer >= 180:  # 3秒后切换消息
                    message_timer = 0
                    message_alpha = 255
                    current_message += 1
                    if current_message >= len(messages):
                        show_message = False
                        time.sleep(2)  # 等待2秒
                        if has_music:
                            play_music()
                            playing_music = True
                            show_lyrics = True
            
            # 显示标题和歌词
            if show_lyrics and playing_music:
                if intro_timer < 600:  # 前奏期间
                    # 计算字体大小，从36逐渐增加到72
                    font_size = 36 + int((intro_timer / 600) * 36)
                    big_font = pygame.font.Font(font_path, font_size) if os.path.exists(font_path) else pygame.font.SysFont("simhei", font_size)
                    title = big_font.render("《听妈妈的话》", True, DEEP_PINK)
                    title_rect = title.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 50))
                    screen.blit(title, title_rect)
                    intro_timer += 1
                else:
                    # 前奏结束后保持大号字体
                    big_font = pygame.font.Font(font_path, 72) if os.path.exists(font_path) else pygame.font.SysFont("simhei", 72)
                    title = big_font.render("《听妈妈的话》", True, DEEP_PINK)
                    title_rect = title.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 50))
                    screen.blit(title, title_rect)
                    
                    # 音乐开始后的计时
                    if music_start_timer < 60:  # 等待1秒（前奏结束后）
                        music_start_timer += 1
                    else:
                        if current_lyric < len(lyrics):
                            lyric_text, display_time = lyrics[current_lyric]
                            lyric = lyrics_font.render(lyric_text, True, PINK)
                            lyric.set_alpha(lyric_alpha)
                            # 将歌词位置调整到标题下方
                            lyric_rect = lyric.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 50))
                            screen.blit(lyric, lyric_rect)
                            
                            lyric_timer += 1
                            # 根据每句歌词的指定时间计算帧数
                            frames = int(display_time * 60)  # 60帧/秒
                            if lyric_timer >= frames:
                                lyric_timer = 0
                                lyric_alpha = 255
                                current_lyric += 1
                                if current_lyric >= len(lyrics):
                                    running = False
            
            # 淡出效果
            if message_timer > 120:  # 最后1秒开始淡出
                message_alpha = max(0, message_alpha - 5)
            if lyric_timer > int(lyrics[current_lyric][1] * 60 * 0.7) and music_start_timer >= 60:  # 在歌词显示时间的70%处开始淡出
                lyric_alpha = max(0, lyric_alpha - 5)
            
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