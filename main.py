from pygame import *
from random import randint

_SCREEN_WIDTH = 800
_SCREEN_HEIGHT = 640
window = display.set_mode(( _SCREEN_WIDTH, _SCREEN_HEIGHT))
clock = time.Clock()
font.init()

class GameSprite(sprite.Sprite):
    def __init__(self, imagefile, x, y, width, height, speed = 0):
        sprite.Sprite.__init__(self)
        self.image = image.load(imagefile)
        self.image = transform.scale(self.image, (width, height))
        self.rect = Rect(x, y, width, height)
        self.speed = speed
    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, imagefile, x, y, width, height, key_up, key_down, speed=0):
        super().__init__(imagefile, x, y, width, height, speed)
        self.key_up = key_up
        self.key_down = key_down
    def update(self):
        keys = key.get_pressed()
        if keys[self.key_up]:
            self.rect.y -= self.speed
        if keys[self.key_down]:
            self.rect.y += self.speed
        
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > _SCREEN_HEIGHT:
            self.rect.bottom = _SCREEN_HEIGHT

class Ball(GameSprite):
    def update(self):
        if self.rect.bottom >= _SCREEN_HEIGHT or self.rect.top < 0:
            self.speed.y *= -1
        self.rect.topleft += self.speed
ball = Ball("ball.png", 400, 300, 50, 50, speed=Vector2(4,4))

paddle_left = Player(imagefile="Paddle1.png", x=20, y=280, width=20, height=120, 
                    key_up=K_q, key_down=K_a, speed=10)
paddle_right = Player(imagefile="Paddle1.png", x=_SCREEN_WIDTH-40, y=280, width=20, height=120, 
                    key_up=K_UP, key_down=K_DOWN, speed=10)

r_win_text = font.Font(None, 100).render("Right player wins!", True, '#DC143C')
l_win_text = font.Font(None, 100).render("Left player wins!", True, '#DC143C')

while not event.peek(QUIT):
    if ball.rect.left <0:
        window.blit(r_win_text, (120, 320))
    elif ball.rect.right > _SCREEN_WIDTH:
        window.blit(l_win_text, (120, 320))
    else:
        window.fill('lightblue')

        if sprite.collide_rect(ball, paddle_left) or sprite.collide_rect(ball, paddle_right):
            ball.speed.x *= -1.1

        ball.update()
        ball.draw(window)
        paddle_right.update()
        paddle_right.draw(window)
        paddle_left.update()
        paddle_left.draw(window)



    display.update()
    clock.tick(60)