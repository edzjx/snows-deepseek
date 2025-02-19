import pygame
import cv2
import numpy as np
import random
def init_fonts():
    global title_font, tip_font, score_font
    
    # 尝试加载自定义字体
    font_paths = [
        "resources/zcool.ttf",  # 自定义字体
        "C:/Windows/Fonts/simhei.ttf",  # Windows系统字体
        "/System/Library/Fonts/STHeiti Medium.ttc"  # macOS系统字体
    ]
    
    for path in font_paths:
        try:
            title_font = pygame.font.Font(path, 72)
            tip_font = pygame.font.Font(path, 36)
            score_font = pygame.font.Font(path, 24)
            print(f"成功加载字体: {path}")
            return
        except:
            continue
    
    # 如果所有字体都加载失败
    print("警告：未能加载中文字体，将使用默认字体")
    title_font = pygame.font.Font(None, 72)
    tip_font = pygame.font.Font(None, 36)
    score_font = pygame.font.Font(None, 24)
# 初始化游戏
pygame.init()
init_fonts()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("哈尔滨冰雪大冒险")
clock = pygame.time.Clock()

# 加载视频背景
video = cv2.VideoCapture("resources/harbin_winter.mp4")  # 欢迎页面和结束页面的背景视频

# 加载图片背景
game_bg = pygame.image.load("resources/snow_bg.jpg")  # 游戏界面的背景图片
game_bg = pygame.transform.scale(game_bg, (WIDTH, HEIGHT))

# 加载游戏素材
player_img = pygame.image.load("resources/skier.png")
ice_img = pygame.image.load("resources/ice_block.png")
flag_img = pygame.image.load("resources/finish_flag.png")

# 加载背景音乐
pygame.mixer.init()
welcome_music = pygame.mixer.Sound("resources/welcome_music.mp3")  # 欢迎页面音乐
game_music = pygame.mixer.Sound("resources/game_music.mp3")        # 游戏界面音乐
end_music = pygame.mixer.Sound("resources/end_music.mp3")          # 结束页面音乐

# 设置音乐音量
welcome_music.set_volume(0.5)
game_music.set_volume(0.5)
end_music.set_volume(0.5)

# 视频帧转换函数
def get_video_frame():
    ret, frame = video.read()
    if not ret:  # 如果视频播放完毕
        video.set(cv2.CAP_PROP_POS_FRAMES, 0)  # 重置到开头
        ret, frame = video.read()
    frame = cv2.resize(frame, (WIDTH, HEIGHT))  # 调整尺寸
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # 颜色空间转换
    return pygame.surfarray.make_surface(frame.swapaxes(0, 1))  # 转为Pygame Surface

# 玩家类
class Skier:
    def __init__(self):
        self.image = pygame.transform.scale(player_img, (80, 80))
        self.rect = self.image.get_rect(center=(WIDTH//2, HEIGHT-100))
        self.speed = 8

    def move(self, direction):
        if direction == "left" and self.rect.left > 0:
            self.rect.x -= self.speed
        elif direction == "right" and self.rect.right < WIDTH:
            self.rect.x += self.speed

# 障碍物类
class Obstacle:
    def __init__(self):
        self.type = random.choice(["ice", "flag"])
        self.image = ice_img if self.type == "ice" else flag_img
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect(center=(random.randint(20, WIDTH-20), -20))
        self.speed = 5

    def move(self):
        self.rect.y += self.speed

def main():
    skier = Skier()
    obstacles = []
    score = 0
    #font = pygame.font.Font(None, 36)
    
    # 当前播放的音乐
    current_music = None
    
    # 游戏状态变量
    game_active = False
    welcome_page = True  # 初始为欢迎页面

    while True:
        # 事件处理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                video.release()
                pygame.quit()
                return

            # 检测空格键按下事件
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if welcome_page or not game_active:  # 在欢迎页面或结束页面按空格键
                    welcome_page = False
                    game_active = True
                    score = 0
                    obstacles = []
                    skier = Skier()
                    print("游戏开始！")

        # 欢迎页面
        if welcome_page:
            # 使用背景音乐
            if current_music != welcome_music:
                pygame.mixer.stop()  # 停止当前音乐
                welcome_music.play(-1)  # 循环播放欢迎音乐
                current_music = welcome_music
            
            bg_surface = get_video_frame()  # 使用视频背景
            screen.blit(bg_surface, (0, 0))
            
            # 绘制标题文字
            #title_font = pygame.font.Font(None, 72)
            title_text = title_font.render("哈尔滨冰雪大冒险", True, (255, 255, 255))
            title_rect = title_text.get_rect(center=(WIDTH//2, HEIGHT//3))
            screen.blit(title_text, title_rect)
            
            # 绘制提示文字
            #tip_font = pygame.font.Font(None, 36)
            tip_text = tip_font.render("按空格键开始游戏", True, (255, 255, 255))
            tip_rect = tip_text.get_rect(center=(WIDTH//2, HEIGHT//2))
            screen.blit(tip_text, tip_rect)

        # 游戏进行中
        elif game_active:
            # 使用背景音乐
            if current_music != game_music:
                pygame.mixer.stop()  # 停止当前音乐
                game_music.play(-1)  # 循环播放游戏音乐
                current_music = game_music
                
            # 使用图片背景
            screen.blit(game_bg, (0, 0))

            # 玩家控制
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                skier.move("left")
            if keys[pygame.K_RIGHT]:
                skier.move("right")

            # 生成障碍物
            if random.random() < 0.05:
                obstacles.append(Obstacle())

            # 更新障碍物
            for obstacle in obstacles[:]:
                obstacle.move()
                if skier.rect.colliderect(obstacle.rect):
                    if obstacle.type == "ice":
                        game_active = False
                    else:
                        score += 50
                        obstacles.remove(obstacle)
                if obstacle.rect.top > HEIGHT:
                    obstacles.remove(obstacle)
                    if obstacle.type == "ice":
                        score += 10

            # 绘制玩家和障碍物
            screen.blit(skier.image, skier.rect)
            for obstacle in obstacles:
                screen.blit(obstacle.image, obstacle.rect)
            
            # 显示得分
            score_text = tip_font.render(f"得分: {score}", True, (255, 255, 255))
            screen.blit(score_text, (10, 10))

        # 游戏结束界面
        else:
            # 使用背景音乐
            if current_music != end_music:
                pygame.mixer.stop()  # 停止当前音乐
                end_music.play(-1)  # 循环播放结束音乐
                current_music = end_music
                
            bg_surface = get_video_frame()  # 使用视频背景
            screen.blit(bg_surface, (0, 0))
            
            # 绘制结束文字
            end_text = tip_font.render(f"游戏结束！最终得分: {score}", True, (255, 255, 255))
            screen.blit(end_text, (WIDTH//2-150, HEIGHT//2))
            restart_text = tip_font.render("按空格键重新开始", True, (255, 255, 255))
            screen.blit(restart_text, (WIDTH//2-100, HEIGHT//2+50))

        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()