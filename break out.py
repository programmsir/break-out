# coding: utf8
import pygame
import sys

DISPLAYWIDTH = 640
DISPLAYHEIGHT = 480

GRAY     = (100, 100, 100)
NAVYBLUE = ( 60,  60, 100)
WHITE    = (255, 255, 255)
RED      = (255,   0,   0)
GREEN    = (  0, 255,   0)
BLUE     = (  0,   0, 255)
YELLOW   = (255, 255,   0)
ORANGE   = (255, 128,   0)
PURPLE   = (255,   0, 255)
CYAN     = (  0, 255, 255)
BLACK    = (  0,   0,   0)
COMBLUE  = (233, 232, 255)

BGCOLOR = BLACK

ARRAYWIDTH = 10
ARRAYHEIGHT = 5
BLOCKGAP = 2
BLOCKWIDTH = 62
BLOCKHEIGHT = 25
PADDLEWIDTH = 100
PADDLEHEIGHT = 10

BALLSPEED = 4

class Block(pygame.sprite.Sprite):
    def __init__(self):
        self.size = [BLOCKWIDTH, BLOCKHEIGHT]
        pygame.sprite.Sprite.__init__(self)
        self.name = 'BLOCK'
        self.image = pygame.Surface(self.size)
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.name = 'BALL'
        self.moving = False
        self.image = pygame.Surface((15, 15))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.vectorx = BALLSPEED
        self.vectory = BALLSPEED * -1
        self.score = 0

    def update(self, mouseX, blocks, paddle, *args):
        if self.moving == False:
            self.rect.centerx = paddle.rect.centerx

        else:
            self.rect.y += self.vectory

            hitGroup = pygame.sprite.Group(paddle, blocks)

            spriteHitList = pygame.sprite.spritecollide(self, hitGroup, False)

            if len(spriteHitList) > 0:
                for sprite in spriteHitList:
                    if sprite.name == 'BLOCK':
                        sprite.kill()
                        self.vectorx *= -1
                        self.score += 1
                self.vectory *= -1
                self.rect.y += self.vectory

            self.rect.x += self.vectorx

            if self.rect.right > DISPLAYWIDTH:
                self.vectorx *= -1
                self.rect.right = DISPLAYWIDTH

            if self.rect.left < 0:
                self.vectorx *= -1
                self.rect.left = 0

            if self.rect.top < 0:
                self.vectory *= -1
                self.rect.top = 0

            elif self.rect.top > DISPLAYHEIGHT:
                pygame.quit()
                sys.exit()

class Paddle(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.name = 'PADDLE'
        self.image = pygame.Surface((PADDLEWIDTH, PADDLEHEIGHT))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()

    def update(self, mousex, *args):
        if self.rect.x >= 0 and self.rect.right <= DISPLAYWIDTH:
            self.rect.centerx = mousex

        if self.rect.x < 0:
            self.rect.x = 0

        elif self.rect.right > DISPLAYWIDTH:
            self.rect.right = DISPLAYWIDTH

class Game(object):
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.screen = self.makeScreen()
        self.font = pygame.font.Font(None, 32)
        self.mouseX = 0
        self.blocks = self.createBlocks()
        self.paddle = self.createPaddle()
        self.ball = self.createBall()

        self.allSprites = pygame.sprite.Group(self.blocks, self.paddle, self.ball)

    def makeScreen(self):
        pygame.display.set_caption('Arkanoid')
        screen = pygame.display.set_mode([DISPLAYWIDTH, DISPLAYHEIGHT])
        screen.fill(BGCOLOR)

        return screen

    def createBlocks(self):
        blocks = pygame.sprite.Group()
        for row in range(ARRAYHEIGHT):
            for i in range(ARRAYWIDTH):
                block = Block()
                block.rect.x = i * (BLOCKWIDTH + BLOCKGAP)
                block.rect.y = row * (BLOCKHEIGHT + BLOCKGAP)
                block.image.fill(YELLOW)
                blocks.add(block)

        return blocks

    def createPaddle(self):
        paddle = Paddle()
        paddle.rect.centerx = DISPLAYWIDTH/2
        paddle.rect.bottom = DISPLAYHEIGHT

        return paddle

    def createBall(self):
        ball = Ball()
        ball.rect.centerx = self.paddle.rect.centerx
        ball.rect.bottom = self.paddle.rect.top

        return ball

    def checkInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                self.mouseX = event.pos[0]

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.ball.moving = True

    def run(self):
        while True:
            self.screen.fill(BGCOLOR)
            score = self.font.render('Score:  ' + str(self.ball.score), 1, WHITE)
            self.screen.blit(score, [20 ,DISPLAYHEIGHT - 50])
            self.allSprites.update(self.mouseX, self.blocks, self.paddle)
            self.allSprites.draw(self.screen)
            pygame.display.update()
            pygame.time.delay(10)
            self.checkInput()

if __name__ == "__main__":
    game = Game()
    game.run()