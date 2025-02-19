import pygame
import cv2
import numpy as np
import random
# 在游戏初始化部分添加
def init_fonts():
    global title_font, tip_font, score_font
    
    # 尝试加载自定义字体
    font_paths = [
        "zcool.ttf",  # 自定义字体
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
video = cv2.VideoCapture("harbin_winter.mp4")
video_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
video_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

# 加载游戏素材
player_img = pygame.image.load("skier.png")
ice_img = pygame.image.load("ice_block.png")
flag_img = pygame.image.load("finish_flag.png")





# 视频帧转换函数
def get_video_frame():
    ret, frame = video.read()
    if not ret:
        video.set(cv2.CAP_PROP_POS_FRAMES, 0)
        ret, frame = video.read()
    frame = cv2.resize(frame, (WIDTH, HEIGHT))
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    return pygame.surfarray.make_surface(frame.swapaxes(0, 1))

# 玩家类
class Skier:
    def __init__(self):
        self.image = pygame.transform.scale(player_img, (60, 60))
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
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect(center=(random.randint(20, WIDTH-20), -20))
        self.speed = 5

    def move(self):
        self.rect.y += self.speed

def main():
    skier = Skier()
    obstacles = []
    score = 0
    #font = pygame.font.Font(None, 36)
    
    # 新增游戏状态变量
    game_active = False
    welcome_page = True  # 新增欢迎页面状态

    while True:
        # 获取视频背景帧
        bg_surface = get_video_frame()

        # 事件处理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                video.release()
                pygame.quit()
                return
            # if event.type == pygame.KEYDOWN :
            #     print("按键事件")
            #     if event.key==pygame.K_r :
            #         print("按R")
            #         if game_active==False:
            #     #todo
            #             game_active = True
            #             score = 0
            #             obstacles = []
            #             skier = Skier()
                
                
                
                

        # 欢迎页面逻辑
        if welcome_page:
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
            
            # 检测空格键
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                welcome_page = False
                game_active = True
                print("按下空格键")

        # 游戏进行中
        elif game_active:
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

            # 绘制游戏界面
            screen.blit(bg_surface, (0, 0))
            screen.blit(skier.image, skier.rect)
            for obstacle in obstacles:
                screen.blit(obstacle.image, obstacle.rect)
            
            # 显示得分
            score_text = tip_font.render(f"得分: {score}", True, (255, 255, 255))
            screen.blit(score_text, (10, 10))

        # 游戏结束界面
        else:
            screen.fill((0, 100, 255))
            end_text = tip_font.render(f"游戏结束！最终得分: {score}", True, (255, 255, 255))
            screen.blit(end_text, (WIDTH//2-150, HEIGHT//2))
            restart_text = tip_font.render("按空格重新开始", True, (255, 255, 255))
            screen.blit(restart_text, (WIDTH//2-100, HEIGHT//2+50))
            
            # 重新开始逻辑
            keys = pygame.key.get_pressed()
             
            if keys[pygame.K_SPACE]  :
                game_active = True
                score = 0
                obstacles = []
                skier = Skier()
                print("按下空格键")
             
    

        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()