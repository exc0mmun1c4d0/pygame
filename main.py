import random
import pygame

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 960

BLACK = (0, 0, 0)

FPS = 30

level = 1

current_coords = [[0, 0]]

endlevel = []
for i in range(1100, 1281):
    some_coords = []
    some_coords.append(i)
    some_coords.append(960)
    endlevel.append(some_coords)

pygame.init()
button_sound = pygame.mixer.Sound('btn_sound.wav')


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, img='mouse.png'): 
        global alive
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

        self.enemies = pygame.sprite.Group()
        self.alive = True

    def update(self):
        self.new_level()
        self.rect.x += self.change_x
        current_coords[0][0] = self.rect.x
        block_list = pygame.sprite.spritecollide(self, self.walls, False)
        for block in block_list:
            if self.change_x > 0:
                self.rect.right = block.rect.left
            else:
                self.rect.left = block.rect.right

        self.rect.y += self.change_y
        current_coords[0][1] = self.rect.y
        block_list = pygame.sprite.spritecollide(self, self.walls, False)    
        for block in block_list:
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            else:
                self.rect.top = block.rect.bottom

        cheese_list = pygame.sprite.spritecollide(self, self.cheese, False)
        for cheese in cheese_list:
            cheese.kill()

        if pygame.sprite.spritecollide(self, self.enemies, False):
            self.alive = False

        if not self.alive:
            if level == 1:
                dead_screen_after_first()
            elif level == 2:
                dead_screen_after_second()
            else:
                dead_screen_after_third()

        if self.direction == 'right':
            self.image = self.player_right
        if self.direction == 'left':
            self.image = self.player_left
        if self.direction == 'up':
            self.image = self.player_up
        if self.direction == 'down':
            self.image = self.player_down

    def new_level(self):
        global level

        if level == 1:
            if current_coords[0] in endlevel:
                wall_coords.clear()
                current_coords[0][0] = 10
                current_coords[0][1] = 50
                player.kill()
                self.rect.x = 10
                self.rect.y = 50
                level += 1
                pause_after_first()
                return start_game, self.new_level
        elif level == 2:
            if current_coords[0] in endlevel:
                wall_coords.clear()
                current_coords[0][0] = 10
                current_coords[0][1] = 50
                player.kill()
                self.rect.x = 10
                self.rect.y = 50
                level += 1
                pause_after_second()
                return start_game, self.new_level
        elif level == 3:
            if current_coords[0] in endlevel:
                end_screen()
                return start_game, self.new_level

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


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, img='cat.png'):
        super().__init__()
        self.image = pygame.image.load(img).convert_alpha()
        self.image = pygame.transform.scale(self.image, (70, 70))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.start = x
        self.stop = x + 250
        self.direct = 1

    def update(self):
        if self.rect.x >= self.stop:
            self.rect.x = self.stop
            self.direct = -1

        if self.rect.x <= self.start:
            self.rect.x = self.start
            self.direct = 1

        self.rect.x += self.direct * 2

class Enemy1(pygame.sprite.Sprite):
    def __init__(self, x, y, img='cat.png'):
        super().__init__()
        self.image = pygame.image.load(img).convert_alpha()
        self.image = pygame.transform.scale(self.image, (70, 70))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.start = y
        self.stop = y + 220
        self.direct = 1

    def update(self):
        if self.rect.y >= self.stop:
            self.rect.y = self.stop
            self.direct = -1

        if self.rect.y <= self.start:
            self.rect.y = self.start
            self.direct = 1

        self.rect.y += self.direct * 2


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


def pause_after_first():
    menu_background = pygame.image.load('complete.JPEG')
    menu_background = pygame.transform.scale(menu_background, (1280, 960))

    continue_button = Button(510, 70)

    show = True
    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        screen.blit(menu_background, (0, 0))
        continue_button.draw(385, 650, 'Следующий уровень', start_level2, 50)
        pygame.display.update()
        clock.tick(60)

def pause_after_second():
    menu_background = pygame.image.load('complete.JPEG')
    menu_background = pygame.transform.scale(menu_background, (1280, 960))

    continue_button = Button(510, 70)

    show = True
    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        screen.blit(menu_background, (0, 0))
        continue_button.draw(385, 650, 'Следующий уровень', start_level3, 50)
        pygame.display.update()
        clock.tick(60)

def start_level2():
    global all_sprites_list, wall_list, cheese, cheese_list, cheese_coords, wall_coords, screen, clock, player, enemy

    for i in all_sprites_list:
        i.kill()
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    all_sprites_list = pygame.sprite.Group()
    wall_list = pygame.sprite.Group()

    wall_coords = [
        [0, 0, 1280, 10],
        [1270, 0, 10, 960],
        [0, 950, 1140, 10],
        [0, 0, 10, 1280],
        [0, 130, 1000, 10],
        [1000, 130, 10, 100],
        [200, 230, 810, 10],
        [200, 230, 10, 400],
        [400, 430, 880, 10],
        [200, 630, 100, 10],
        [450, 630, 680, 10],
        [1130, 630, 10, 330]
    ]

    for coord in wall_coords:
        wall = Wall(coord[0], coord[1], coord[2], coord[3])
        wall_list.add(wall)
        all_sprites_list.add(wall)

    cheese = Cheese(50, 50)

    cheese_list = pygame.sprite.Group()
    cheese_coords = [
        [900, 160],
        [1150, 360],
        [1050, 770]
    ]

    for coord in cheese_coords:
        cheese = Cheese(coord[0], coord[1])
        cheese_list.add(cheese)
        all_sprites_list.add(cheese)

    enemies_list = pygame.sprite.Group()
    enemies_coords = [[950, 650]]
    for coord in enemies_coords:
        enemy = Enemy1(coord[0], coord[1])
        enemies_list.add(enemy)
        all_sprites_list.add(enemy)

    player = Player(10, 50)
    player.walls = wall_list
    all_sprites_list.add(player)

    player.cheese = cheese_list
    player.enemies = enemies_list

    pygame.init()
    clock = pygame.time.Clock()
    start_game()

def start_level3():
    global all_sprites_list, wall_list, cheese, cheese_list, cheese_coords, wall_coords, screen, clock, player, enemy

    for i in all_sprites_list:
        i.kill()
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    all_sprites_list = pygame.sprite.Group()
    wall_list = pygame.sprite.Group()

    wall_coords = [ 
        [0, 0, 1280, 10], 
        [1270, 0, 10, 960], 
        [0, 950, 1140, 10], 
        [0, 0, 10, 1280], 
        [0, 160, 210, 10], 
        [210, 160, 10, 320],  
        [210, 650, 10, 100], 
        [390, 0, 10, 550], 
        [210, 750, 600, 10], 
        [390, 550, 220, 10], 
        [600, 400, 10, 150], 
        [600, 0, 10, 200], 
        [800, 200, 10, 550], 
        [800, 200, 350, 10], 
        [1140, 200, 10, 1100] 
    ]

    for coord in wall_coords:
        wall = Wall(coord[0], coord[1], coord[2], coord[3])
        wall_list.add(wall)
        all_sprites_list.add(wall)

    cheese = Cheese(50, 50)

    cheese_list = pygame.sprite.Group()
    cheese_coords = [ 
        [450, 80], 
        [50, 200], 
        [1000, 300] 
    ]

    for coord in cheese_coords:
        cheese = Cheese(coord[0], coord[1])
        cheese_list.add(cheese)
        all_sprites_list.add(cheese)

    enemies_list = pygame.sprite.Group()
    enemies_coords = [[810, 500]]
    for coord in enemies_coords:
        enemy = Enemy(coord[0], coord[1])
        enemies_list.add(enemy)
        all_sprites_list.add(enemy)

    player = Player(10, 50)
    player.walls = wall_list
    all_sprites_list.add(player)

    player.cheese = cheese_list
    player.enemies = enemies_list
    pygame.init()
    clock = pygame.time.Clock()
    start_game()

def restart_first_level():
    global all_sprites_list, wall_list, cheese, cheese_list, cheese_coords, wall_coords, screen, clock, player, enemy

    for i in all_sprites_list:
        i.kill()

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

    enemies_list = pygame.sprite.Group()
    enemies_coords = [[810, 500]]
    for coord in enemies_coords:
        enemy = Enemy(coord[0], coord[1])
        enemies_list.add(enemy)
        all_sprites_list.add(enemy)

    player = Player(10, 50)
    player.walls = wall_list
    all_sprites_list.add(player)

    player.cheese = cheese_list
    player.enemies = enemies_list

    pygame.init()
    clock = pygame.time.Clock()
    start_game()

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

def end_screen():
    menu_background = pygame.image.load('endscreen.jpg')
    menu_background = pygame.transform.scale(menu_background, (1280, 960))

    main_menu = Button(288, 70)
    quit_button = Button(122, 70)

    show = True
    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        screen.blit(menu_background, (0, 0))
        main_menu.draw(396, 850, 'Main menu', show_menu, 50)
        quit_button.draw(762, 850, 'Quit', quit, 50)

        pygame.display.update()
        clock.tick(60)

def dead_screen_after_first():
    menu_background = pygame.image.load('dead_screen.JPEG')
    menu_background = pygame.transform.scale(menu_background, (1280, 960))

    restart = Button(200, 70)

    show = True
    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        screen.blit(menu_background, (0, 0))
        restart.draw(540, 850, 'Restart', restart_first_level, 50)

        pygame.display.update()
        clock.tick(60)

def dead_screen_after_second():
    menu_background = pygame.image.load('dead_screen.JPEG')
    menu_background = pygame.transform.scale(menu_background, (1280, 960))

    restart = Button(200, 70)

    show = True
    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        screen.blit(menu_background, (0, 0))
        restart.draw(540, 850, 'Restart', start_level2, 50)

        pygame.display.update()
        clock.tick(60)

def dead_screen_after_third():
    menu_background = pygame.image.load('dead_screen.JPEG')
    menu_background = pygame.transform.scale(menu_background, (1280, 960))

    restart = Button(200, 70)

    show = True
    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        screen.blit(menu_background, (0, 0))
        restart.draw(540, 850, 'Restart', start_level3, 50)

        pygame.display.update()
        clock.tick(60)

def start_game():
    global player, screen, enemy

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
        enemy.update()
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

enemies_list = pygame.sprite.Group()
enemies_coords = [[810, 500]]
for coord in enemies_coords:
    enemy = Enemy(coord[0], coord[1])
    enemies_list.add(enemy)
    all_sprites_list.add(enemy)

player = Player(10, 50)
player.walls = wall_list
all_sprites_list.add(player)

player.cheese = cheese_list
player.enemies = enemies_list

clock = pygame.time.Clock()

show_menu()
pygame.quit()
quit()
