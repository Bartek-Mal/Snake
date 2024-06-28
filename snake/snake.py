import pygame
import random
import threading
import time

pygame.init()

screen_width = 700
screen_height = 600
score_display = 100
speed = 50
body_size = 50
body_parts = 3
move_delay = 100
food_size = 50

screen = pygame.display.set_mode((screen_width, screen_height + score_display))
clock = pygame.time.Clock()
running = True
game_over = False
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
        text_rect = text_surface.get_rect(center=(screen_width / 2, 45))
        surface.blit(text_surface, text_rect)
    def timer_display(self, text, font, color, surface):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(screen_width - 100, 45))
        surface.blit(text_surface, text_rect)

class Snake:
    def __init__(self, speed=50, body_parts=3):
        self.speed = speed
        self.body_parts = body_parts
        self.body_part_table = []
        self.direction = 'Down'
        self.create_snake()
    
    def create_snake(self):
        x, y = 0, score_display
        for _ in range(self.body_parts):
            body_rect = pygame.Rect(x, y, body_size, body_size)
            self.body_part_table.append(body_rect)
            y += self.speed
    
    def draw_snake(self):
        for body in self.body_part_table:
            pygame.draw.rect(screen, "Green", body)
    
    def move(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_UP] and self.direction != 'Down':
            self.direction = 'Up'
        elif key[pygame.K_DOWN] and self.direction != 'Up':
            self.direction = 'Down'
        elif key[pygame.K_LEFT] and self.direction != 'Right':
            self.direction = 'Left'
        elif key[pygame.K_RIGHT] and self.direction != 'Left':
            self.direction = 'Right'

        head = self.body_part_table[-1].copy()
        
        if self.direction == 'Down':
            head.y += self.speed
        elif self.direction == 'Up':
            head.y -= self.speed
        elif self.direction == 'Left':
            head.x -= self.speed
        elif self.direction == 'Right':
            head.x += self.speed
        self.body_part_table.append(head)
        self.temp = self.body_part_table.pop(0)
        
        if head.x >= screen_width or head.x < 0 or head.y >= screen_height + score_display or head.y < score_display:
            global game_over
            game_over = True
            
        self.check_collision()
        
    def check_collision(self):
        head = self.body_part_table[-1]
        for part in self.body_part_table[:-1]:
            if head.colliderect(part):
                global game_over
                game_over = True

class Food:
    def __init__(self, food_size=50):
        self.food_size = food_size
        self.new_food()
        self.score_board = 0

    def new_food(self):
        while True:
            x, y = random.randint(0, (screen_width // food_size) - 1) * food_size, random.randint(0, (screen_height // food_size) - 1) * food_size + score_display
            if y >= score_display:
                self.food_rect = pygame.Rect(x, y, food_size, food_size)
                break

    def draw_food(self):
        pygame.draw.circle(screen, "Blue", (self.food_rect.x + self.food_size / 2, self.food_rect.y + self.food_size / 2), self.food_size / 2)

    def collision(self, snake):
        if self.food_rect.colliderect(snake.body_part_table[-1]):
            snake.body_part_table.insert(0, snake.temp)
            self.new_food()
            self.score_board += 50

def draw_grid():
    for x in range(0, screen_width, body_size):
        for y in range(score_display, screen_height + score_display, body_size):
            rect = pygame.Rect(x, y, body_size, body_size)
            pygame.draw.rect(screen, "Grey", rect, 1)

def reset_game():
    global snake, food, game_over, last_move_time, start_time
    snake = Snake()
    food = Food()
    game_over = False
    last_move_time = pygame.time.get_ticks()
    start_time = time.time()

class Timer:
    def __init__(self):
        self.start_time = time.time()
        self.elapsed_time = 0
        self.timer_thread = threading.Thread(target=self.update_timer)
        self.timer_thread.start()

    def update_timer(self):
        while running:
            if not game_over:
                self.elapsed_time = int(time.time() - self.start_time)
            time.sleep(1)

    def get_elapsed_time(self):
        return self.elapsed_time

timer = Timer()
snake = Snake()
food = Food()
score = Score()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game_over:
                reset_game()
            elif event.key == pygame.K_e and game_over:
                running = False
    
    screen.fill((0, 0, 0))
    score.draw_score_space()
    score.score_display('Score: ' + str(food.score_board), font, 'white', screen)
    score.timer_display('Time: ' + str(timer.get_elapsed_time()), font, 'white', screen)
    draw_grid()
    current_time = pygame.time.get_ticks()
    
    if not game_over:
        if current_time - last_move_time > move_delay:
            snake.move()
            food.collision(snake)
            last_move_time = current_time
        
        snake.draw_snake()
        food.draw_food()
    else:
        game_over_text = font.render("Game Over", True, "Red")
        restart_text = font.render("Press R to restart or E to exit", True, "White")
        screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 2 - game_over_text.get_height() // 2))
        screen.blit(restart_text, (screen_width // 2 - restart_text.get_width() // 2, screen_height // 2 + game_over_text.get_height()))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
