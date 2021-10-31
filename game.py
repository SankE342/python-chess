import pygame
import os

WIDTH, HEIGHT = 640, 720
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Python Chess -by SankE')

WHITE = (255, 255, 255)

FPS_CAP = 30

BOARD = pygame.transform.scale(
    pygame.image.load('./chess_board.jpg'), (WIDTH, WIDTH)
)

def draw():
    WINDOW.fill(WHITE)
    WINDOW.blit(BOARD, (0, 80))
    pygame.display.update()


def main():
    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(FPS_CAP)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        draw()
    
    pygame.quit()

if __name__ == '__main__': main()