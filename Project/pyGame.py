import pygame
import sys

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
WINDOW_HEIGHT = 800
WINDOW_WIDTH = 800

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

  for x in range(0, WINDOW_WIDTH, blockSize):
      for y in range(0, WINDOW_HEIGHT, blockSize):
          rect = pygame.Rect(x, y, blockSize, blockSize)
          pygame.draw.rect(SCREEN, BLACK, rect, 1)
          if x == 320 and y == 0:
              SCREEN.blit(male_agent, (x, y))
          if x == 320 and y == 640:
              SCREEN.blit(female_agent, (x, y))