import pygame
import random
pygame.init()

win = pygame.display.set_mode((1500,800))
pygame.display.set_caption("Asteroids!")
clock = pygame.time.Clock()



default = pygame.image.load('player_ship.png')
default = pygame.transform.rotate(default, -90)
default = pygame.transform.scale(default, (60,60))
rock = pygame.image.load('asteroid.png')
rock = pygame.transform.scale(rock, (60,60))


bg = pygame.image.load('bg.jpg')
bg = pygame.transform.scale(bg, (1500, 800))
clock = pygame.time.Clock()
bulletSound = pygame.mixer.Sound('shoot.wav')
hitSound = pygame.mixer.Sound('hit.wav')
music = pygame.mixer.music.load('music.mp3')
pygame.mixer.music.play(-1)




class player(object):
    def __init__(self, x, y, height, width):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.damage = 10
        self.vel = 1
        self.hitbox = (self.x + 20, self.y, 60,60)

    def draw(self, win):
        self.hitbox = (self.x, self.y, 60, 60)
        #pygame.draw.rect(win, (255,0,0), self.hitbox, 2)
        win.blit(default, (self.x, self.y))

    def hit(self):
        self.x = 200
        self.y = 400
        font1 = pygame.font.SysFont('comicsans', 50)
        text = font1.render('-1 Life, ' + str(lives-1) + ' more left', 1, (255,0,0))
        win.blit(text, (250 - (text.get_width()/2),200))
        pygame.display.update()
        asteroid_1.x = 1600
        asteroid_1.y = random.randint(50,750)
        i = 0
        while i < 300:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 301
                    pygame.quit()
        asteroid_1.x = 1600


class enemy(object):
    def __init__(self,x, y, height, width):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.vel = 0.5
        self.health = 4
        self.hitbox = (self.x + 20, self.y, 60, 60)
        self.visible = True

    def draw(self, win):
        self.move()
        self.hitbox = (self.x, self.y, 60, 60)
        #pygame.draw.rect(win, (255,0,0), self.hitbox, 2)
        win.blit(rock, (self.x,self.y))

    def move(self):
        self.x-=self.vel

    def hit(self):
        hitSound.play()
        if self.health > 0:
            self.health-=1
        else:
            self.x = 1600
            self.y =random.randint(50,750)
            self.health = 4


class projectile(object):
    def __init__(self,x,y,radius,color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.vel = 3

    def draw(self,win):
        pygame.draw.circle(win, self.color, (self.x,self.y), self.radius)


def redrawGameWindow():
    win.blit(bg, (0,0))
    text=font.render('Score: ' + str(score), 1, (255,255,255))
    win.blit(text, (1350, 10))
    text=font.render('Lives: ' + str(lives), 1, (255,255,255))
    win.blit(text, (1200, 10))
    pygame.draw.line(win, (255,0,0), (660,0), (660,800), 1)
    ship.draw(win)
    asteroid_1.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    pygame.display.update()



#MAIN LOOP ------------------------------------------------------------------------------
font = pygame.font.SysFont('timesnewroman', 30, True)
ship = player(200, 400, 60, 60)
asteroid_1 = enemy(1400, 600, 60, 60)
score=0
bullets = []
run = True
lives = 2
shootLoop=0
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False



    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and ship.y > ship.vel:
        ship.y -= ship.vel
    if keys[pygame.K_DOWN] and ship.y < 800 - ship.height - ship.vel:
        ship.y += ship.vel
    if keys[pygame.K_LEFT] and ship.x > ship.vel:
        ship.x -= ship.vel
    if keys[pygame.K_RIGHT] and ship.x < 600:
        ship.x += ship.vel


    if asteroid_1.visible == True:
        if ship.hitbox[1] < asteroid_1.hitbox[1] + asteroid_1.hitbox[3] and ship.hitbox[1] + ship.hitbox[3] > asteroid_1.hitbox[1]:
            if ship.hitbox[0] + ship.hitbox[2] > asteroid_1.hitbox[0] and ship.hitbox[0] < asteroid_1.hitbox[0] + asteroid_1.hitbox[2]:
                ship.hit()
                lives-=1
                if lives == 0:
                    pygame.quit()

    if asteroid_1.x<-60:
        asteroid_1.x =1600
        asteroid_1.y = random.randint(50,750)
        ship.hit()
        lives-=1
        if lives == 0:
            pygame.quit()

    if shootLoop > 0:
        shootLoop+=1
    if shootLoop>75:
        shootLoop=0

    if keys[pygame.K_SPACE] and shootLoop==0:
        bulletSound.play()
        if len(bullets) < 25:
            bullets.append(projectile(round(ship.x + ship.width //2), round(ship.y + ship.height//2), 6, (255,255,0)))
            shootLoop=1

    for bullet in bullets:
        if bullet.x < 1500 and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

        if bullet.y - bullet.radius < asteroid_1.hitbox[1] + asteroid_1.hitbox[3] and bullet.y + bullet.radius > asteroid_1.hitbox[1]:
            if bullet.x + bullet.radius > asteroid_1.hitbox[0] and bullet.x - bullet.radius <  asteroid_1.hitbox[0] + asteroid_1.hitbox[2]:
                asteroid_1.hit()
                score = score + 1
                bullets.pop(bullets.index(bullet))
    redrawGameWindow()

pygame.quit()
