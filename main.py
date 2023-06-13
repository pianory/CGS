import pygame
import objects
import pymunk
import pymunk.pygame_util
import math

# 스크린 크기 지정
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# pygame 초기화
pygame.init()

# 스크린 객체 저장
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pool Game")

# pymunk 공간
space = pymunk.Space()
staticBody = space.static_body
drawOptions = pymunk.pygame_util.DrawOptions(SCREEN)

# 일정한 프레임 보장
clock = pygame.time.Clock()
FPS = 60

# 이미지 로딩
tableImage = pygame.image.load("./data/img/board.png").convert_alpha()
cueImage = pygame.image.load("./data/img/cue.png").convert_alpha()

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
    shape.elasticity = 0.75
    
    space.add(body, shape)

# 쿠션의 위치
cushions = [[(51, 72), (64, 89), (64, 382), (51, 404)], 
            [(73, 47), (92, 59), (382, 59), (403, 47)], 
            [(777, 47), (758, 59), (468, 59), (447, 47)], 
            [(799, 72), (786, 89), (786, 382), (799, 404)], 
            [(73, 424), (92, 410), (382, 410), (403, 424)], 
            [(777, 424), (758, 410), (468, 410), (447, 424)]]


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
        surface.blit(self.image, self.rect)



# 게임 준비
balls = []
rows = 5
ballImg = [pygame.transform.scale(pygame.image.load("./data/img/Ball"+str(i)+".png"), (ballRadius*2, ballRadius*2)) for i in range(16)]
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

isRunning = True

while isRunning:
    SCREEN.fill(backgroundColor)
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            playerBall.body.apply_impulse_at_local_point((-500, 0), (0, 0))

        # 게임 종료    
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    # 테이블 그리기
    SCREEN.blit(tableImage, (215, 200))

    # 공 그리기
    for i, ball in enumerate(balls):
        SCREEN.blit(ballImg[i+1], (ball.body.position[0]-ballRadius, ball.body.position[1]-ballRadius))
    SCREEN.blit(ballImg[0], (playerBall.body.position[0]-ballRadius, playerBall.body.position[1]-ballRadius))

    # 큐 그리기
    # 큐 각도 계산하기

    # cue.draw(SCREEN)

    # space.debug_draw(drawOptions)

    pygame.display.update()
    clock.tick(FPS)
    space.step(1/FPS)