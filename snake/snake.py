import pygame
import random

pygame.init()

screen_width = 700
screen_height = 700
score_display = 100
speed = 50
body_size = 50
body_parts = 3
move_delay = 100
food_size = 50

screen = pygame.display.set_mode((screen_width, screen_height+score_display))
clock = pygame.time.Clock()
running = True
last_move_time = pygame.time.get_ticks()

pygame.font.init()
font = pygame.font.SysFont('Silkscreen.ttf', 36)

class Score:
    def __init__(self):
        self.score = pygame.Rect(0, 90, screen_width, 10)
    def draw_score_space(self):
        pygame.draw.rect(screen, "Dark Grey", self.score)
    def score_display(self, text, font, color, surface):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(screen_width/2, 45))
        surface.blit(text_surface, text_rect)

class Snake:
    def __init__(self, speed=50, body_parts=3):
        self.speed = speed
        self.body_parts = body_parts
        self.body_part_table = []
        self.direction = 'Down'
        self.create_snake()
    
    def create_snake(self):
        x, y = 0, 100
        for _ in range(self.body_parts):
            body_rect = pygame.Rect(x, y, body_size, body_size)
            self.body_part_table.append(body_rect)
            y += self.speed
    
    def draw_snake(self):
        for body in self.body_part_table:
            pygame.draw.rect(screen, "Green", body)
    
    def move(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_UP] and self.direction != 'Down' :
            self.direction = 'Up'
        elif key[pygame.K_DOWN] and self.direction != 'Up':
            self.direction = 'Down'
        elif key[pygame.K_LEFT] and self.direction != 'Right':
            self.direction = 'Left'
        elif key[pygame.K_RIGHT] and self.direction != 'Left':
            self.direction = 'Right'

        head = self.body_part_table[-1].copy()
        
        if self.direction == 'Down':
            head.y += snake.speed
        elif self.direction == 'Up':
            head.y -= snake.speed
        elif self.direction == 'Left':
            head.x -= snake.speed
        elif self.direction == 'Right':
            head.x += snake.speed
        self.body_part_table.append(head)
        self.temp = self.body_part_table.pop(0)
        
        if head.x > screen_width or head.x < 0 or head.y <= score_display or head.y > screen_height:
            global running
            running = False
            
        self.check_collision()
        
    def check_collision(self):
        head = self.body_part_table[-1]
        for part in self.body_part_table[:-1]:
            if head.colliderect(part):
                global running
                running = False
        
        
class Food:
    def __init__(self,food_size = 50):
        self.food_size = food_size
        self.new_food()
        self.score_board = 0

    def new_food(self):
        x,y = random.randint(0, int(screen_width/50 - 1)) *50, random.randint(0,int(screen_width/50 - 1)) * 50
        if y <=100:
            self.new_food()
        else:
            self.food_rect = pygame.Rect(x, y, food_size, food_size)
    def draw_food(self):
        pygame.draw.circle(screen, "Blue", (self.food_rect.x + self.food_size / 2, self.food_rect.y + self.food_size / 2), self.food_size / 2)

    def collision(self, snake):
        if self.food_rect.colliderect(snake.body_part_table[-1]):
            snake.body_part_table.insert(0, snake.temp)
            self.new_food()
            self.score_board +=50
            

def draw_grid():
    for x in range(0, screen_width, body_size):
        for y in range(score_display, screen_height + score_display, body_size):
            rect = pygame.Rect(x, y, body_size, body_size)
            pygame.draw.rect(screen, "Grey", rect, 1)
        
snake = Snake()
food = Food()
score = Score()


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill((0, 0, 0)) 
    score.draw_score_space()    
    score.score_display('Score: ' + str(food.score_board) , font,'white', screen)
    draw_grid()
    current_time = pygame.time.get_ticks()
    
    if current_time - last_move_time > move_delay:
        snake.move()
        food.collision(snake)
        last_move_time = current_time
        
    snake.draw_snake()
    food.draw_food()
    
    
    pygame.display.flip()
    clock.tick(60) 

pygame.quit()
