@[TOC](体验用ai做了个python小游戏)

# 写在前面

最近ai确实比较火。各种生成式AI，包括文字、图片、视频。之前听说ai生产代码能力比较强，一直想试试。所以及就有了本问

# 使用的工具
deepinseek ：用来生成python代码
即梦：用来生成图片素材
Remove.bg：用来对生成的图片素材去除背景
pixabay.com：用来下载音乐素材

#游戏建立步骤
##1.设立游戏建立背景
![在这里插入图片描述](https://i-blog.csdnimg.cn/img_convert/2bebf10d779c753c84ceaa7f83ff6ffd.png#pic_center)

我使用了深度思考
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/0b22c8037bea4549814c8ae3b6ac366b.png)
整个深度思索的过程，让我了解到deepseek为啥选择pygame库，为啥选择收集物品得分的模式。主要是我前面的提示词：小学生。我觉得符合我预期。

很快他就生成了python代码

```python
import pygame
import random

# 初始化游戏
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("哈尔滨冰雪大冒险")
clock = pygame.time.Clock()

# 加载哈尔滨元素素材
bg = pygame.image.load("snow_bg.jpg")  # 冰雪大世界背景
player_img = pygame.image.load("skier.png")  # 滑雪运动员
ice_img = pygame.image.load("ice_block.png")  # 冰障碍物
flag_img = pygame.image.load("finish_flag.png")  # 终点旗

# 颜色定义
WHITE = (255, 255, 255)
BLUE = (0, 100, 255)

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

# 游戏主循环
def main():
    skier = Skier()
    obstacles = []
    score = 0
    font = pygame.font.Font(None, 36)
    game_active = True

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        if game_active:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                skier.move("left")
            if keys[pygame.K_RIGHT]:
                skier.move("right")

            # 生成障碍物
            if random.random() < 0.05:  # 5%概率生成
                obstacles.append(Obstacle())

            # 移动障碍物
            for obstacle in obstacles:
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

            # 更新界面
            screen.blit(bg, (0, 0))
            screen.blit(skier.image, skier.rect)
            for obstacle in obstacles:
                screen.blit(obstacle.image, obstacle.rect)

            # 显示得分
            score_text = font.render(f"得分: {score}", True, WHITE)
            screen.blit(score_text, (10, 10))
        else:
            # 游戏结束界面
            screen.fill(BLUE)
            end_text = font.render("游戏结束！最终得分: " + str(score), True, WHITE)
            screen.blit(end_text, (WIDTH//2-150, HEIGHT//2))
            restart_text = font.render("按R重新开始", True, WHITE)
            screen.blit(restart_text, (WIDTH//2-100, HEIGHT//2+50))

            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                game_active = True
                score = 0
                obstacles = []
                skier = Skier()

        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()

```
代码的完整度非常好，拷贝图片素材基本就可以运行了。代码中有注释，方便阅读代码。他还给出了后续的建议。游戏就是避障，然后接住游戏元素得分。碰到障碍物游戏结束，提示分数，提示按R键继续游戏。逻辑比较简单。
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/5467a1c88a9a4786bf3de00463a79344.png)
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/0a09768a4cc7428caccbd69868f6e5ea.png)
## 2.增加功能
在这个基础上，我对deepseek提了一些要求，或者觉得有问题的让他解决。总体上都解决了。而且效果我认为满意。
### 1.要求增加视频作为背景。
因为pygame是不支持视频元素的。我 看看deepseek怎么解决的哦，他比较了opencv和moviepy库，在小学生这个条件下，给出opencv更适合。这段深度思考部分，我觉得给出moviepy和opencv的比较逻辑有点欠缺。但是实际的思路还是比较清晰的使用第三方库从视频中取帧，然后绘制到pygame的surface上。

它还贴心的给出了如何安装opencv库，怎么引用素材
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/9e4577ed0a504e918860f03896c4fb01.png)
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/0f62368a02514cb2925fc2eef1a40437.png)
### 2.我让增加了一个欢迎页面。
它的思路，通过设置变量，把游戏过程分为欢迎页，游戏进行中，游戏结束3个状态。逻辑没毛病。还贴心的提供修改说明和建议。
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/8e73efe0b31344199145fad0a6a32266.png)
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/3e93074d11224a97955c3f3612ea16cc.png)
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/037b4c07227b4cd78f67b52c564590d9.png)
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/3f84c1abb1db4232811ea56300a3dacb.png)
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/6c7f19ba090e48718bec9c29d87c416c.png)
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/9ba1e97665464780b77ad29476048571.png)
### 3.我发现中文显示有问题。
提出了问题，deepseek也给出可行的解决方案，我使用了他给的方案2 ，因为自定义字体可以使得游戏画面更优。还贴心的给出了注意事项。
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/c607ddfe26b64600b9e991b66ff3d1dc.png)
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/a001ec0abcd94027b6e8b2e1d35dfe31.png)
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/e84954fdabc6435d94b7c8570391a781.png)
### 4.我提出了背景修改意见，欢迎页面和结束页面背景是视频，游戏页面背景是静态图片。
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/02da55a8073c4256a7b97f63dc6b7926.png)
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/52dda3f0f88d41d680490bb43f3ba235.png)
### 5.提出增加更多游戏元素。
deepseek增加了加速道具，护盾道具，磁铁道具，减速道具。
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/c9c55d5861974ed6bf62ce241a2a8b93.png)
# 总结：
deepseek的代码输出能力完全没有问题，对于需求的分析也很精确。给出的修改提示和建议也非常有用。我的结论，deepseek完全可以作为生产力工具给程序员提供更快的代码输出，也可以帮助程序员学习新的知识点，通过项目一点点增加功能打磨代码。

最后给出我最终的代码（我没有加上更多元素）

链接: [https://github.com/edzjx/snows-deepseek](https://github.com/edzjx/snows-deepseek )


![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/ad2b038292994e65aee4b2238b5ba124.png)
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/182406ae0ef54ad39a770256832d2233.png)
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/d2d38e9fc3744ff8a2f8d00e19e36f10.png)
