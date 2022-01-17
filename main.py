from turtle import left, right
import pygame
from pygame import image
from pygame.surface import Surface

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 960

BLACK = (0, 0, 0)

FPS = 30


pygame.init()
button_sound = pygame.mixer.Sound('btn_sound.wav')

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, img='mouse.png'):
        super().__init__()
        self.image = pygame.image.load(img).convert_alpha()
        self.image = pygame.transform.scale(self.image, (110, 75))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.direction = 'left'
        self.player_left = pygame.image.load('mouse.png').convert_alpha()
        self.player_left = pygame.transform.scale(self.player_left, (110, 75))

        self.player_right = pygame.transform.flip(self.player_left, True, False)
        self.player_right = pygame.transform.scale(self.player_right, (110, 75))

        self.player_up = pygame.transform.rotate(self.player_right, 270)
        self.player_up = pygame.transform.scale(self.player_up, (75, 110))

        self.player_down = pygame.transform.rotate(self.player_right, 90)
        self.player_down = pygame.transform.scale(self.player_down, (75, 110))

        self.change_x = 0
        self.change_y = 0
        self.walls = None

        self.cheese = None
        self.collected_cheese = 0

    def update(self):
        self.rect.x += self.change_x
        block_list = pygame.sprite.spritecollide(self, self.walls, False)
        for block in block_list:
            if self.change_x > 0:
                self.rect.right = block.rect.left
            else:
                self.rect.left = block.rect.right

        self.rect.y += self.change_y
        block_list = pygame.sprite.spritecollide(self, self.walls, False)    
        for block in block_list:
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            else:
                self.rect.top = block.rect.bottom

        cheese_list = pygame.sprite.spritecollide(self, self.cheese, False)
        for cheese in cheese_list:
            self.collected_cheese += 1
            cheese.kill()

        if self.direction == 'right':
            self.image = self.player_right
        if self.direction == 'left':
            self.image = self.player_left
        if self.direction == 'up':
            self.image = self.player_up
        if self.direction == 'down':
            self.image = self.player_down

    def rotate(self):
        self.image = pygame.transform.rotate(self.image, 90)


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)

        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x


class Cheese(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.image.load('cheese.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.image = pygame.transform.scale(self.image, (1280, 960))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

def print_text(message, x, y, font_color=(0, 0, 0), font_type='bip.ttf', font_size=30):
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    screen.blit(text, (x, y))


class Button:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.inactive_color = (13, 162, 58)
        self.active_color = (23, 204, 58)
    
    def draw(self, x, y, message, action=None, font_size=30):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x < mouse[0] < x + self.width and y < mouse[1] < y + self.height:
            pygame.draw.rect(screen, self.active_color, (x, y, self.width, self.height))

            if click[0] == 1:
                pygame.mixer.Sound.play(button_sound)
                pygame.time.delay(300)
                if action == quit:
                    pygame.quit()
                    quit()
                else:
                    action()
                if action is not None:
                    action()

        else:
            pygame.draw.rect(screen, self.inactive_color, (x, y, self.width, self.height))

        print_text(message=message, x = x + 10, y = y + 10, font_size=font_size)


def show_menu(): 
    menu_background = pygame.image.load('menu.jpg')
    menu_background = pygame.transform.scale(menu_background, (1280, 960))

    start_button = Button(288, 70)
    quit_button = Button(122, 70)

    show = True
    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        screen.blit(menu_background, (0, 0))
        start_button.draw(496, 650, 'Start game', start_game, 50)
        quit_button.draw(580, 750, 'Quit', quit, 50)

        pygame.display.update()
        clock.tick(60)


def start_game():

    global player, screen

    start = True
    while start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    player.change_x = -5
                    player.direction = 'right'
                elif event.key == pygame.K_d:
                    player.change_x = 5
                    player.direction = 'left'
                elif event.key == pygame.K_w:
                    player.change_y = -5
                    player.direction = 'up'
                elif event.key == pygame.K_s:
                    player.change_y = 5
                    player.direction = 'down'
                elif event.key == pygame.K_ESCAPE:
                    show_menu()

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    player.change_x = 0
                elif event.key == pygame.K_d:
                    player.change_x = 0
                elif event.key == pygame.K_w:
                    player.change_y = 0
                elif event.key == pygame.K_s:
                    player.change_y = 0

        player.update()
        screen.fill(BLACK)
        screen.blit(background.image, background.rect)
        all_sprites_list.draw(screen)
        pygame.display.flip()

        clock.tick(60)

pygame.init()
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption('Game')
      
background = Background('background.jpg', [0, 0])
all_sprites_list = pygame.sprite.Group()
wall_list = pygame.sprite.Group()

wall_coords = [
    [0, 0, 1280, 10],
    [1270, 0, 10, 960],
    [0, 950, 1140, 10],
    [0, 0, 10, 1280],
    [0, 140, 100, 10],
    [250, 140, 100, 10],
    [350, 140, 10, 500],
    [490, 0, 10, 490],
    [350, 640, 450, 10],
    [490, 490, 150, 10],
    [800, 300, 10, 350],
    [640, 150, 10, 350],
    [640, 150, 245, 10],
    [1035, 150, 245, 10],
    [800, 300, 340, 10],
    [1140, 300, 10, 1000]
]

for coord in wall_coords:
    wall = Wall(coord[0], coord[1], coord[2], coord[3])
    wall_list.add(wall)
    all_sprites_list.add(wall)

cheese = Cheese(50, 50)

cheese_list = pygame.sprite.Group()
cheese_coords = [
    [1200, 50],
    [545, 410],
    [950, 320]
]

for coord in cheese_coords:
    cheese = Cheese(coord[0], coord[1])
    cheese_list.add(cheese)
    all_sprites_list.add(cheese)

player = Player(10, 50)
player.walls = wall_list
all_sprites_list.add(player)

player.cheese = cheese_list

clock = pygame.time.Clock()

show_menu()
pygame.quit()
quit()
