# get acces to pygame library
import pygame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SCREEN_TITLE = 'My CrossGame'
WHITE_COLOR = (255,255,255)
BLACK_COLOR = (0,0,0)
RED_COLOR = (255,0,0)
GREEN_COLOR = (0,255,0)
BLUE_COLOR = (0,0,255)
# clock used to update the gamne screen
clock = pygame.time.Clock()
pygame.font.init()
font = pygame.font.SysFont('comicsans', 75)

class Game:
    TICK_RATE = 60

    # Initializer for the game class to set up width, height and the title
    def __init__(self, image_path, title, width, height):
        self.title = title
        self.width = width
        self.height = height
        self.game_screen = pygame.display.set_mode((width,height))
        self.game_screen.fill(WHITE_COLOR)
        pygame.display.set_caption(title)
        background_image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(background_image, (width, height))

    def run_game_loop(self, level):
        is_game_over = False
        did_win = True
        direction = 0

        player_character = PlayerCharacter('player.png',375,700,50,50)
        enemy0 = NonPlayerCharacter('enemy.png',75,600,50,50)
        enemy0.SPEED *= level

        enemy1 = NonPlayerCharacter('enemy.png',self.width - 755 ,400,50,50)
        enemy1.SPEED *= level

        enemy2 = NonPlayerCharacter('enemy.png',75,200,50,50)
        enemy2.SPEED *= level

        treasure = GameObject('treasure.png', 375, 50, 50, 50)

        while not is_game_over:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_game_over = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        direction = 1
                    elif event.key == pygame.K_DOWN:
                        direction = -1
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        direction = 0
                print(event)

            # fill background again
            self.game_screen.fill(WHITE_COLOR)

            self.game_screen.blit(self.image, (0,0))

            # draw treasure
            treasure.draw(self.game_screen)

            #pygame.draw.rect(game_screen,BLUE_COLOR,[150,150,100,100])
            #pygame.draw.circle(game_screen,RED_COLOR,[600,600], 50)
            #game_screen.blit(player_image, (375,375))

            # update the player position
            player_character.move(direction, SCREEN_HEIGHT)
            # draw player at the new position
            player_character.draw(self.game_screen)
            

            # move enemy
            enemy0.move(self.width)
            enemy0.draw(self.game_screen)

            if level > 2:
                enemy1.move(self.width)
                enemy1.draw(self.game_screen)
                if player_character.detect_collision(enemy1):
                    is_game_over=True
                    did_win = False
                    text = font.render('You lose!',True, BLACK_COLOR)
                    self.game_screen.blit(text, (300,350))
                    pygame.display.update()
                    clock.tick(1)
                    break
           
            if level > 4:
                enemy2.move(self.width)
                enemy2.draw(self.game_screen)
                if player_character.detect_collision(enemy2):
                    is_game_over=True
                    did_win = False
                    text = font.render('You lose!',True, BLACK_COLOR)
                    self.game_screen.blit(text, (300,350))
                    pygame.display.update()
                    clock.tick(1)
                    break

            # start collision detection
            if player_character.detect_collision(enemy0):
                is_game_over=True
                did_win = False
                text = font.render('You lose!',True, BLACK_COLOR)
                self.game_screen.blit(text, (300,350))
                pygame.display.update()
                clock.tick(1)
                break
            elif player_character.detect_collision(treasure):
                did_win = True
                is_game_over=True
                text = font.render('You win! :-)',True, GREEN_COLOR)
                self.game_screen.blit(text, (300,350))
                pygame.display.update()
                clock.tick(1)
                break


            # redraw the whole screen
            pygame.display.update()
            # tick to do the update
            clock.tick(self.TICK_RATE)

        if did_win:
            self.run_game_loop(level + 0.5)
        else:
            return

# Genereoc game object class as superclass for later sub-classes
class GameObject:

    def __init__(self, image_path, x, y, width, height):

        object_image = pygame.image.load(image_path)
        # scale up the image
        self.image = pygame.transform.scale(object_image,(width,height))

        self.x_pos = x
        self.y_pos = y
        self.width = width
        self.height = height


    #draw the object by blitting it onto the game screen
    def draw(self,background):
        background.blit(self.image, (self.x_pos, self.y_pos))

# Class to represent the player char
class PlayerCharacter(GameObject):

    # number of tiles character moves per second
    SPEED = 10

    def __init__(self, image_path, x, y, width, height):
        super().__init__(image_path, x, y, width, height)

    #Move function will move char up or down depending on positive or negative direction
    def move(self, direction, max_height):
         
        if direction > 0:
            self.y_pos -= self.SPEED
        elif direction < 0:
            self.y_pos += self.SPEED

        # avoid leaving the screen
        if self.y_pos >= max_height -70:
            self.y_pos = max_height -70
        if self.y_pos <= 70:
            self.y_pos = 70

    def detect_collision(self, other_body):
        if self.y_pos > other_body.y_pos + other_body.height:
            return False
        elif self.y_pos + self.height < other_body.y_pos:
            return False
        if self.x_pos > other_body.x_pos+ other_body.width:
            return False
        elif self.x_pos + self.width < other_body.x_pos:
            return False

        return True


# Class to represent the player char
class NonPlayerCharacter(GameObject):

    # number of tiles character moves per second
    SPEED = 10

    def __init__(self, image_path, x, y, width, height):
        super().__init__(image_path, x, y, width, height)

    #Move function will move char up or down depending on positive or negative direction
    def move(self, max_width):
        if self.x_pos <= 20:
            self.SPEED= abs(self.SPEED)
        elif self.x_pos >= max_width - 70:
            self.SPEED = -abs(self.SPEED)
        self.x_pos += self.SPEED


pygame.init()

new_game=Game('background.png', SCREEN_TITLE, SCREEN_WIDTH, SCREEN_HEIGHT)
new_game.run_game_loop(1)

# Quit Pygame and the programm
pygame.quit()
quit()
