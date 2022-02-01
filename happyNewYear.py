import pygame
import random
import time
import threading
import math

Circles = []
GRAVITY = 9.81
FRAME = 0.07


class circle:
    def __init__(
        self, x: float, y: float, velocityX: float, velocityY: float, size: int
    ):
        self.x = x
        self.y = y
        self.velocityX = velocityX
        self.velocityY = velocityY
        self.color = [random.randint(0, 245) for i in range(3)]
        self.size = size
        self.threat = threading.Thread(target=self.timeCounter)
        self.threat.start()
        self.Switch = False

    def move(self):
        self.x += self.velocityX * FRAME
        self.y -= self.velocityY * FRAME
        self.velocityY -= FRAME * GRAVITY
        if self.y > 600:
            self.velocityY = -self.velocityY
            if self.Switch == True:

                Circles.remove(self)
                self.size = 0

    def display(self, screen: pygame.Surface):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.size)

    def explosion(self):
        if self.size > 5:
            Circles.remove(self)
            ballsNumber = random.randint(5, 7)
            raid = math.pi * 2 / ballsNumber + math.pi / random.randint(3, 6)
            length = abs(self)
            for addCir in range(1, ballsNumber + 1):
                yVelocity = math.sin(raid * addCir) * length
                xVelocity = math.cos(raid * addCir) * length
                Circles.append(
                    circle(
                        self.x,
                        self.y,
                        yVelocity,
                        xVelocity,
                        int(self.size / 1.5),
                    )
                )
        else:
            self.Switch = True

    def timeCounter(self):
        time.sleep(1.5)
        self.explosion()

    def __abs__(self):
        return math.sqrt(self.velocityY ** 2 + self.velocityX ** 2)


def moveBalls(screen: pygame.Surface):
    for ball in Circles:
        ball.move()
        ball.display(screen)


def main():
    run = True
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    while run:
        screen.fill((0, 0, 0))
        for eve in pygame.event.get():
            if eve.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                Circles.append(circle(pos[0], pos[1], 0, 90, 20))
            if eve.type == pygame.QUIT:
                run = False
                pygame.quit()
        moveBalls(screen)
        pygame.display.flip()


if __name__ == "__main__":
    main()
