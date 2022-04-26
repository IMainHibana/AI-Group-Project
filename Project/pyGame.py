import pygame
import sys
import numpy as np

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
WINDOW_HEIGHT = 800
WINDOW_WIDTH = 800
ROWS = 5  # ROWS IN WORLD
COLS = 5  # COLUMNS IN WORLD
blockSize = 160  # Set the size of the grid block
male = pygame.image.load('male.jpeg')
female = pygame.image.load('female.png')
package = pygame.image.load('package.png')
drop_off = pygame.image.load('drop_off.jpeg')
IMG_SIZE = (100, 100)
male_agent = pygame.transform.scale(male, IMG_SIZE)
female_agent = pygame.transform.scale(female, IMG_SIZE)
box = pygame.transform.scale(package, (30, 30))
dock = pygame.transform.scale(drop_off, (130, 130))
SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
CLOCK = pygame.time.Clock()

# our grid as a 2d array
grid = np.zeros((ROWS, COLS), dtype='i,i')
for i in range(0, ROWS):
    for j in range(0, COLS):
        grid[i][j] = (i+1, j+1)


def pyGameGrid(moves):
    pygame.init()
    SCREEN.fill(WHITE)
    female_x = 320
    female_y = 640
    f_x_change = 0
    f_y_change = 0

    while True:
        pyGrid()
        SCREEN.blit(female_agent, (female_x, female_y))
        for f_moves in moves:
            if f_moves == 'left':
                f_x_change -= 160
            if f_moves == 'right':
                f_x_change += 160
            if f_moves == 'up':
                f_y_change += 160
            if f_moves == 'down':
                f_y_change -= 160
            if female_x + f_x_change > 800 or female_y + f_y_change > 800:
                female_x += 0
                female_y += 0
            else:
                female_x += f_x_change
                female_y += f_y_change
            SCREEN.blit(female_agent, (female_x, female_y))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()


def pyGrid():
    number_font = pygame.font.SysFont(None, 22)  # Default font, Size 16
    number_image = number_font.render("8", True, BLACK, WHITE)  # Number 8
    row, col = 0, 0
    for x in range(0, WINDOW_WIDTH, blockSize):
        for y in range(0, WINDOW_HEIGHT, blockSize):
            number_text = str(grid[row][col])
            rect = pygame.Rect(x, y, blockSize, blockSize)
            pygame.draw.rect(SCREEN, BLACK, rect, 1)
            # make the number from grid[row][col] into an image
            number_image = number_font.render(number_text, True, BLACK, WHITE)
            SCREEN.blit(number_image, (x, y))
            SCREEN.blit(dock, (20, 20))
            SCREEN.blit(dock, (640 + 20, 0 + 20))
            SCREEN.blit(dock, (320 + 20, 320 + 20))
            SCREEN.blit(dock, (640 + 20, 640 + 20))

            for packages in range(10):
                SCREEN.blit(box, (160 + packages * 15, 15 + 480 + packages * 10))

            for packages in range(10):
                SCREEN.blit(box, (640 + packages * 15, 15 + 320 + packages * 10))

            SCREEN.blit(male_agent, (320 + 30, 0 + 30))

            if row == 4:
                row = 0
            else:
                row += 1
        col += 1

