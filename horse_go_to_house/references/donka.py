import pygame
from pygame.locals import *
import sys

def play_se():
    pass

def main():

    pygame.init()
    pygame.display.set_caption("pygame太鼓の達人試作")
    screen = pygame.display.set_mode((500,500))
    clock = pygame.time.Clock()

    pygame.mixer.quit()
    pygame.mixer.pre_init(buffer=128)
    pygame.mixer.init()
    se_dong = pygame.mixer.Sound("fail.wav")
    se_ka = pygame.mixer.Sound("correct.wav")

    while True:

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_f:
                        se_dong.play()
                    if event.key == K_j:
                        se_dong.play()
                    if event.key == K_d:
                        se_ka.play()
                    if event.key == K_k:
                        se_ka.play()
            screen.fill((0,0,0))


            pygame.display.update()
            clock.tick(30)

if __name__ == "__main__":
    main()