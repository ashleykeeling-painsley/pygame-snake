import pygame
import random

#variables

FPS = 10
speed = 1
score = 0

WHITE = (255,255,255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

XAXIS = 600
YAXIS = 600

grid = []

boundaries = [0,0, XAXIS, YAXIS]

blockSize = 25

snakePos = [5,5]
XChange = 1
YChange = 0

pastPos = []

# pygame setup
pygame.init()
gameWindow = pygame.display.set_mode((XAXIS, YAXIS))
clock = pygame.time.Clock()
pygame.display.set_caption("pygame movement")

# create Grid
for x in range(int(XAXIS/blockSize)):
    for y in range(int(YAXIS/blockSize)):

        grid.append([x,y])
        
#saves the current position of the snake head
def savePos(currentPos):
    # saves the last number of score positions
    # e.g. if score is 5, only the latest 5 positions are stored, the rest are removed from the list
    
    if score > 0 and len(pastPos) != score:
        pastPos.append([currentPos[0], currentPos[1]])

    elif score > 0 and len(pastPos) == score:
        pastPos.pop(0)
        pastPos.append([currentPos[0], currentPos[1]])
  
# creats a random postion for fruit
fruitPos = random.randint(0,len(grid))

def drawGrid():
    gridIndex = 0

    while gridIndex < len(grid):
        pygame.draw.rect(gameWindow, (0,0,0), (grid[gridIndex][0] * blockSize, grid[gridIndex][1] * blockSize, blockSize, blockSize), 2)
        gridIndex += 1

def drawSnake():
    #draws snake head
    pygame.draw.rect(gameWindow, RED, (snakePos[0] * blockSize, snakePos[1]*blockSize, blockSize, blockSize))

    # draws the snake body, the body lenght is dependant on the player score
    if len(pastPos) >= 1:
        if score >= 1:
            counter = -1
            while abs(counter) <= score:
                pygame.draw.rect(gameWindow, BLUE, (pastPos[counter +1][0] * blockSize, pastPos[counter+1][1] * blockSize, blockSize, blockSize))
                counter -= 1

def exitGame():
    playGame = False
    pygame.quit()
    quit()
            
# text setup
font = pygame.font.Font('freesansbold.ttf', 32)


# game loop
playGame = True

while playGame:
        
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            exitGame()
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                YChange = -speed
                XChange = 0
                
            if event.key == pygame.K_s:
                YChange = speed
                XChange = 0

            if event.key == pygame.K_a:
                XChange = -speed
                YChange = 0

            if event.key == pygame.K_d:
                XChange = speed
                YChange = 0
                
            if event.key == pygame.K_r:
                snakePos = grid[0]
    
    gameWindow.fill(WHITE)
    drawGrid()

    savePos(snakePos)
    
    # changes the direction of the snake
    snakePos[0] = snakePos[0] + XChange
    snakePos[1] = snakePos[1] + YChange
  
    # BOUNDARIE CHECK
    # needs to run function to check if the snake has been at the bounarie for more than 0.5 secs if so they loose
    if snakePos[0] == -1:
        exitGame()
        
    if snakePos[0] == XAXIS/blockSize:
        exitGame()

    if snakePos[1] == -1:
        exitGame()

    if snakePos[1] == YAXIS/blockSize:
        exitGame()

    #checks if snake head hits the snakes body
    for pos in pastPos:
        if snakePos == pos:
            exitGame()
        
    # checks if snake has eaten fruit
    if snakePos == grid[fruitPos]:
        score  += 1
        fruitPos = random.randint(0, len(grid))
        
    # SNAKE
    drawSnake()
    
    # Fruit
    pygame.draw.rect(gameWindow, GREEN, (grid[fruitPos][0] * blockSize, grid[fruitPos][1] * blockSize, blockSize, blockSize))

    # text for score
    text = font.render(str(score), True, (255,0,255))
    textRect = text.get_rect() 
    textRect.center = (blockSize/2, blockSize/2)
    gameWindow.blit(text, textRect)
    

    pygame.display.update()
    clock.tick(FPS)

