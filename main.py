import pygame
import objects
import pymunk
import pymunk.pygame_util
import math
import random
import time


power = 0
# 스크린 크기 지정
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# pygame 초기화
pygame.init()

# 스크린 객체 저장
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pool Game")

# 일정한 프레임 보장
clock = pygame.time.Clock()
FPS = 60

""" Main Title """
backgroundImage = pygame.transform.scale(pygame.image.load("./data/img/background_main.png"), (1280, 720))
button1Image = pygame.transform.scale_by(pygame.image.load("./data/img/button1.png").convert_alpha(), 0.7)
button1cImage = pygame.transform.scale_by(pygame.image.load("./data/img/button1c.png").convert_alpha(), 0.7)
button2Image = pygame.transform.scale_by(pygame.image.load("./data/img/button2.png").convert_alpha(), 0.7)
button2cImage = pygame.transform.scale_by(pygame.image.load("./data/img/button2c.png").convert_alpha(), 0.7)
button3Image = pygame.transform.scale_by(pygame.image.load("./data/img/button3.png").convert_alpha(), 0.7)
button3cImage = pygame.transform.scale_by(pygame.image.load("./data/img/button3c.png").convert_alpha(), 0.7)


""" Ingame """
# pymunk 공간
space = pymunk.Space()
staticBody = space.static_body
drawOptions = pymunk.pygame_util.DrawOptions(SCREEN)


# 이미지 로딩
tableImage = pygame.image.load("./data/img/board.png").convert_alpha()
cueImage = pygame.image.load("./data/img/cue.png").convert_alpha()
backgroundImage = pygame.transform.scale(pygame.image.load("./data/img/background_ingame.png").convert_alpha(),(SCREEN_WIDTH, SCREEN_HEIGHT))
powerGaugeOuter = pygame.transform.scale_by(pygame.image.load("./data/img/power_gauge_outer.png").convert_alpha(), 0.7)
powerGaugeInner = pygame.transform.scale_by(pygame.image.load("./data/img/power_gauge_inner.png").convert_alpha(), 0.7)
powerGaugeBackground = pygame.transform.scale_by(pygame.image.load("./data/img/power_gauge_background.png").convert_alpha(), 0.7)
fontNormal = pygame.font.Font("./data/font/Pretendard-Bold.ttf", 60)
fontBold = pygame.font.Font("./data/font/Pretendard-Black.ttf", 30)
loseImage = pygame.image.load("./data/img/lose.png").convert_alpha()
winImage = pygame.image.load("./data/img/win.png").convert_alpha()

# 공 생성 함수
ballRadius = 12
def createBall(position:tuple, name:int):
    body = pymunk.Body()
    body.position = position
    shape = pymunk.Circle(body, ballRadius)
    shape.mass = 10
    shape.elasticity = 0.95

    pivot = pymunk.PivotJoint(staticBody, body, (0, 0), (0, 0))
    pivot.max_bias = 0
    pivot.max_force = 200 # 마찰

    space.add(body, shape, pivot)
    return shape


# 쿠션 생성 함수
def createCushion(poly_dims):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = ((215, 200))
    shape = pymunk.Poly(body, poly_dims)
    shape.elasticity = 0.3
    
    space.add(body, shape)

# 쿠션의 위치
cushions = [[(51, 72), (64, 89), (64, 382), (51, 404)], 
            [(73, 47), (92, 59), (382, 59), (403, 47)], 
            [(777, 47), (758, 59), (468, 59), (447, 47)], 
            [(799, 72), (786, 89), (786, 382), (799, 404)], 
            [(73, 424), (92, 410), (382, 410), (403, 424)], 
            [(777, 424), (758, 410), (468, 410), (447, 424)]]

# 구멍의 위치
pockets = [(53, 48), (53, 430), (424, 48), (424, 430), (796, 48), (796, 430)]


for cushion in cushions:
    createCushion(cushion)

# 큐 생성
class Cue():
    def __init__(self, position):
        self.originImage = cueImage
        self.angle = 0
        self.image = pygame.transform.rotate(self.originImage, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = position

    def update(self, angle):
        self.angle = angle

    def draw(self, surface):
        self.image = pygame.transform.rotate(self.originImage, self.angle)
        surface.blit(self.image, 
                     (self.rect.centerx - self.image.get_width()/2
                      , self.rect.centery - self.image.get_height()/2)
                     )



# 게임 준비
balls = []
rows = 5
ballImg = [pygame.transform.scale(pygame.image.load("./data/img/Ball"+str(i)+".png"), (ballRadius*2, ballRadius*2)) for i in range(16)]
ballNum = [11, 2, 13, 4, 5, 6, 10, 3, 14, 15, 8, 1, 7, 12, 9]
success = []
# 공 세팅
for col in range(5):
    for row in range(rows):
        pos = (420 + (col*ballRadius-2)*2, 388 + (row*(ballRadius+1))*2 + (col * ballRadius))
        newBall = createBall(pos, 1)
        balls.append(newBall)
    rows -= 1

playerBall = createBall((840, 438), 0)
backgroundColor = pygame.Color('white')
cue = Cue(playerBall.body.position)
# Main

# check game handle
isinGame = True
isShot = True
isPowering = False
powerTime = 0
isPlayerBallOut = False
gameSuccess = None
turns = 0

while isinGame:
    SCREEN.blit(backgroundImage, (0, 0))
    
    # 테이블 그리기
    SCREEN.blit(tableImage, (215, 200))

    # 공이 들어갔는가?
    for i, ball in enumerate(balls):
        for pocket in pockets:
            ballXDist = abs(ball.body.position[0]-(pocket[0]+215))
            ballYDist = abs(ball.body.position[1]-(pocket[1]+200))
            ballDist = math.sqrt(ballXDist**2 + ballYDist**2)
            if ballDist <= 20:
                space.remove(ball.body)
                success.append(ballImg[ballNum[i]])
                balls.pop(i)
                ballNum.pop(i)
    for pocket in pockets:
        playerballXDist = abs(playerBall.body.position[0]-(pocket[0]+215))
        playerballYDist = abs(playerBall.body.position[1]-(pocket[1]+200))
        playerballDist = math.sqrt(playerballXDist**2 + playerballYDist**2)
        if playerballDist <= 20:
            playerBall.body.position = (-100, -100)
            playerBall.body.velocity = [0, 0]
            turns += 3 # penalty
            isPlayerBallOut = True
    if isPlayerBallOut and isShot:
        playerBall.body.position = (840, random.randint(338, 538))
        isPlayerBallOut = False

    # 공 그리기
    for i, ball in enumerate(balls):
        SCREEN.blit(ballImg[ballNum[i]], (ball.body.position[0]-ballRadius, ball.body.position[1]-ballRadius))
    SCREEN.blit(ballImg[0], (playerBall.body.position[0]-ballRadius, playerBall.body.position[1]-ballRadius))

    # 공 이동 확인
    isShot = True
    for ball in balls:
        if int(ball.body.velocity[0])!= 0 or int(ball.body.velocity[1]) != 0:
            isShot = False
        if int(playerBall.body.velocity[0]) != 0 or int(playerBall.body.velocity[1]) != 0:
            isShot = False

    # 큐 그리기
    if isShot:
        # 큐 각도 계산하기
        mousePos = pygame.mouse.get_pos()
        cue.rect.center = playerBall.body.position
        xDistance = playerBall.body.position[0] - mousePos[0]
        yDistance = -(playerBall.body.position[1] - mousePos[1]) # y축이 반대
        cueAngle = math.degrees(math.atan2(yDistance, xDistance)) # 큐의 각도
        cue.update(cueAngle)
        cue.draw(SCREEN)

    # 게이지 그리기
    SCREEN.blit(powerGaugeBackground, (354, 135))
    SCREEN.blit(powerGaugeInner, (370, 143), pygame.Rect(0, 0, 786*power/15000*0.7, 37))
    SCREEN.blit(powerGaugeOuter, (352, 130))

    # space.debug_draw(drawOptions)
    # 힘 증가시키기
    if isPowering:
        powerTime += 1
        power = math.sin(powerTime/30) ** 4 * 15000
    elif not isPowering and isShot:
        xDir = -math.cos(math.radians(cueAngle))
        yDir = math.sin(math.radians(cueAngle))
        playerBall.body.apply_impulse_at_local_point((power * xDir, power * yDir), (0, 0))
        power = 0

    # 턴수 표시하기
    turnText = fontNormal.render(str(turns),True, (255, 255, 255))
    turnRect = turnText.get_rect()
    turnRect.centerx = 1055
    turnRect.centery = 67
    SCREEN.blit(turnText, turnRect)

    # 게임 종료
    if len(balls) != 0 and 8 not in ballNum and gameSuccess == None:
        gameSuccess = False
        for i in range(129):
            loseRect = loseImage.get_rect()
            loseRect.centerx = 640
            loseRect.centery = 360
            loseImage.set_alpha(i)
            SCREEN.blit(loseImage, loseRect)
            clock.tick(FPS)
            pygame.display.update()
        time.sleep(3)
        break
            

    elif len(balls) == 0:
        gameSuccess = True
        break

    # event 감지
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and isShot and not isPowering:
            isPowering = True
            powerTime = 0
            turns += 1
        if event.type == pygame.MOUSEBUTTONUP and isShot and isPowering:
            isPowering = False
            

        # 게임 종료    
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()


    pygame.display.update()
    clock.tick(FPS)
    space.step(1/FPS)