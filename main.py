import pygame
import math


class Ball():
    def __init__(self, name:int, x:float, y:float, speed:float=0.0, angle:float=0.0):
        """
        당구공을 형성하는 class입니다.
        name : 당구공의 이름을 말합니다. (int : 0~15, 0은 플레이어의 공)
        x : 현재 당구공의 x 위치를 입력합니다. (float)
        y : 현재 당구공의 y 위치를 입력합니다. (float)
        speed : 현재 당구공의 속도를 입력합니다. (float, 기본 0.0)
        angle : 현재 당구공의 각도를 입력합니다. (float, 기본 0.0)
        """
        self.name, self.x, self.y = name, x, y
        self.speed, self.angle = speed, angle
        

    def move(self):
        """
        당구공을 현재 방향과 속도대로 이동합니다.
        """
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed * (-1) # y좌표의 경우 화면 상에서 일반적인 방향의 반대 방향이므로 반대로 적어줍니다.

    def collisionWithBall(self, other):
        """
        당구공과 당구공간의 충돌을 계산합니다.
        other : 다른 공을 입력합니다. (Ball)
        return : self의 공이 충돌한 후 어떻게 될지 반환합니다. (Ball)
        """
        return Ball(self.name, self.x, self.y)
    
    def collisionWithWall(self, wall:str):
        """
        당구공과 벽의 충돌을 계산합니다. 이 연산은 반환값이 없습니다.
        wall : 벽의 방향을 입력합니다. (str : 'UP', 'RIGHT', 'DOWN', 'LEFT')
        """
        if wall == 'UP' or wall == 'DOWN':
            self.angle = -self.angle

        elif wall == 'RIGHT' or wall == 'LEFT':
            self.angle = 2*math.pi - self.angle

        else:
            raise Exception('잘못된 벽의 이름입니다.')
        
    def show(self):
        """
        화면에 x좌표, y좌표
        """