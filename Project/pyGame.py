import pygame
import sys
import numpy as np

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
WINDOW_HEIGHT = 800
WINDOW_WIDTH = 800
ROWS = 5   #ROWS IN WORLD
COLS = 5 #COLUMNS IN WORLD

# our grid as a 2d array
grid = np.zeros((ROWS, COLS), dtype='i,i')
for i in range(0, ROWS):
    for j in range(0, COLS):
        grid[i][j] = (i+1, j+1)

def pyGameGrid():
  global SCREEN, CLOCK
  pygame.init()
  SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
  CLOCK = pygame.time.Clock()
  SCREEN.fill(WHITE)

  while True:
      drawGrid()
      for event in pygame.event.get():
          if event.type == pygame.QUIT:
              pygame.quit()
              sys.exit()

      pygame.display.update()


def drawGrid():
    blockSize = 160 #Set the size of the grid block
    male = pygame.image.load('male.jpeg')
    female = pygame.image.load('female.png')
    IMG_SIZE = (160,160)
    male_agent = pygame.transform.scale(male, IMG_SIZE)
    female_agent = pygame.transform.scale(female, IMG_SIZE)
    number_font = pygame.font.SysFont(None, 22)  # Default font, Size 16
    number_image = number_font.render("8", True, BLACK, WHITE)  # Number 8
    row,col = 0, 0
    for x in range(0, WINDOW_WIDTH, blockSize):
        for y in range(0, WINDOW_HEIGHT, blockSize):
            number_text = str(grid[row][col])
            rect = pygame.Rect(x, y, blockSize, blockSize)
            pygame.draw.rect(SCREEN, BLACK, rect, 1)
            # make the number from grid[row][col] into an image
            number_image = number_font.render(number_text, True, BLACK, WHITE)
            SCREEN.blit(number_image, (x,y))
            if row == 4:
                row = 0
            else:
                row += 1
        col += 1
