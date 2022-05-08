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
female = pygame.image.load('../female.png')
package = pygame.image.load('../package.png')
drop_off = pygame.image.load('../drop_off.jpeg')
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


# takes in lists of female and male moves from main
def pyGameGrid(f_moves, m_moves):
    pygame.init()
    SCREEN.fill(WHITE)
    # starting female coordinates
    female_x = 320
    female_y = 640
    # changes are how much the images move
    f_x_change = 0
    f_y_change = 0

    # starting male coordinates
    male_x = 320
    male_y = 0
    m_x_change = 0
    m_y_change = 0

    # 2 pick up stations initialized with 10 boxes
    pickup1 = 10
    pickup2 = 10

    # 4 drop off stations initialized empty
    dropoff1 = 0
    dropoff2 = 0
    dropoff3 = 0
    dropoff4 = 0

    while True:
        # draws the main layout of non-moving images (the board, the cell coordinates and the pickup, dropoff stations)
        drawGrid()

        # draws initial female and male starting points
        SCREEN.blit(female_agent, (female_x, female_y))
        SCREEN.blit(male_agent, (male_x, male_y))

        for event in pygame.event.get():
            # 0 to length of lists
            for i in range(0, len(f_moves)-1):
                # FEMALE DRIVER MOVE
                # move 160 in whatever direction is chosen
                if f_moves[i] == 'left':
                    f_x_change -= 160
                if f_moves[i] == 'right':
                    f_x_change += 160
                if f_moves[i] == 'up':
                    f_y_change += 160
                if f_moves[i] == 'down':
                    f_y_change -= 160
                # check for bounds of game window
                if female_x + f_x_change > 800 or female_y + f_y_change > 800:
                    female_x += 0
                    female_y += 0
                else:
                    female_x += f_x_change
                    female_y += f_y_change
                    # if in a pickup location
                    if female_x == 160 and female_y == 480:
                        for packages in range(pickup1):
                            SCREEN.blit(box, (160 + packages * 15, 15 + 480 + packages * 10))
                        pickup1 -= 1
                    if female_x == 640 and female_y == 320:
                        for packages in range(pickup2):
                            SCREEN.blit(box, (160 + packages * 15, 15 + 480 + packages * 10))
                        pickup2 -= 1
                    # if in a drop off location
                    if female_x == 0 and female_y == 0:
                        dropoff1 += 1
                        for packages in range(dropoff1):
                            SCREEN.blit(box, (160 + packages * 15, 15 + 480 + packages * 10))
                    if female_x == 640 and female_y == 0:
                        dropoff2 += 1
                        for packages in range(dropoff2):
                            SCREEN.blit(box, (160 + packages * 15, 15 + 480 + packages * 10))
                    if female_x == 320 and female_y == 320:
                        dropoff3 += 1
                        for packages in range(dropoff3):
                            SCREEN.blit(box, (160 + packages * 15, 15 + 480 + packages * 10))
                    if female_x == 640 and female_y == 640:
                        dropoff4 += 1
                        for packages in range(dropoff4):
                            SCREEN.blit(box, (160 + packages * 15, 15 + 480 + packages * 10))

                # draws female driver
                SCREEN.blit(female_agent, (female_x, female_y))

                # MALE DRIVER MOVE
                if m_moves[i] == 'left':
                    m_x_change -= 160
                if m_moves[i] == 'right':
                    m_x_change += 160
                if m_moves[i] == 'up':
                    m_y_change += 160
                if m_moves[i] == 'down':
                    m_y_change -= 160
                # check for window bounds
                if male_x + m_x_change > 800 or male_y + m_y_change > 800:
                    male_x += 0
                    male_y += 0
                else:
                    male_x += m_x_change
                    male_y += m_y_change
                    # if in pickup locations
                    if male_x == 160 and male_y == 480:
                        for packages in range(pickup1):
                            SCREEN.blit(box, (160 + packages * 15, 15 + 480 + packages * 10))
                        pickup1 -= 1
                    if male_x == 640 and male_y == 320:
                        for packages in range(pickup2):
                            SCREEN.blit(box, (160 + packages * 15, 15 + 480 + packages * 10))
                        pickup2 -= 1
                    # if in drop off locations
                    if male_x == 0 and male_y == 0:
                        dropoff1 += 1
                        for packages in range(dropoff1):
                            SCREEN.blit(box, (160 + packages * 15, 15 + 480 + packages * 10))
                    if male_x == 640 and male_y == 0:
                        dropoff2 += 1
                        for packages in range(dropoff2):
                            SCREEN.blit(box, (160 + packages * 15, 15 + 480 + packages * 10))
                    if male_x == 320 and male_y == 320:
                        dropoff3 += 1
                        for packages in range(dropoff3):
                            SCREEN.blit(box, (160 + packages * 15, 15 + 480 + packages * 10))
                    if male_x == 640 and male_y == 640:
                        dropoff4 += 1
                        for packages in range(dropoff4):
                            SCREEN.blit(box, (160 + packages * 15, 15 + 480 + packages * 10))

                # draws male driver
                SCREEN.blit(male_agent, (male_x, male_y))

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # update changes
            pygame.display.update()


def drawGrid():
    # to show cell coordinates
    number_font = pygame.font.SysFont(None, 22)  # Default font, Size 16
    number_image = number_font.render("8", True, BLACK, WHITE)  # Number 8
    row, col = 0, 0
    # drawing the grid
    for x in range(0, WINDOW_WIDTH, blockSize):
        for y in range(0, WINDOW_HEIGHT, blockSize):
            number_text = str(grid[row][col])
            rect = pygame.Rect(x, y, blockSize, blockSize)
            pygame.draw.rect(SCREEN, BLACK, rect, 1)
            # make the number from grid[row][col] into an image
            number_image = number_font.render(number_text, True, BLACK, WHITE)
            SCREEN.blit(number_image, (x, y))
            SCREEN.blit(dock, (0 + 20, 0 + 20))
            SCREEN.blit(dock, (640 + 20, 0 + 20))
            SCREEN.blit(dock, (320 + 20, 320 + 20))
            SCREEN.blit(dock, (640 + 20, 640 + 20))

            # end of row
            if row == 4:
                row = 0
            else:
                # next row
                row += 1
        # next column
        col += 1

