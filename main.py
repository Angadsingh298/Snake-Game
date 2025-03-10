import pygame, sys, random
from pygame.math import Vector2

# Constants
CELL_SIZE = 30
GRID_WIDTH = 27
GRID_HEIGHT = 20
BG_COLOR_1 = (127, 255, 0)
BG_COLOR_2 = (118, 238, 0)
TEXT_COLOR = (255, 255, 255)
GAME_OVER_COLOR = (255, 255, 255)
SCORE_COLOR = (0, 0, 0)
WELCOME_BG = (50, 150, 200)  # Light Blue
GAME_OVER_BG = (200, 100, 100) # Light Red

class Snake:
    def __init__(self, color, start_pos):
        self.body = [Vector2(start_pos[0] - i, start_pos[1]) for i in range(3)]
        self.direction = Vector2(1, 0)
        self.color = color
        self.grow = False
    
    def draw(self, screen):
        for part in self.body:
            pygame.draw.rect(screen, self.color, pygame.Rect(part.x * CELL_SIZE, part.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    
    def move(self):
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False
        self.body.insert(0, self.body[0] + self.direction)
    
    def check_collision(self, other):
        return self.body[0] in other.body
    
    def check_self_collision(self):
        return self.body[0] in self.body[1:]
    
    def check_wall_collision(self):
        return not (0 <= self.body[0].x < GRID_WIDTH and 0 <= self.body[0].y < GRID_HEIGHT)

class EnemySnake(Snake):
    def __init__(self, player_pos):
        while True:
            start_x = random.randint(3, GRID_WIDTH - 6)
            start_y = random.randint(3, GRID_HEIGHT - 6)
            if abs(start_x - player_pos.x) > GRID_WIDTH / 3 and abs(start_y - player_pos.y) > GRID_HEIGHT / 3:
                break
        super().__init__(pygame.Color("red"), (start_x, start_y))
        self.body = [Vector2(start_x - i, start_y) for i in range(6)]

    def move_towards_player(self, player_pos):
        diff = player_pos - self.body[0]
        if abs(diff.x) > abs(diff.y):
            new_direction = Vector2(1, 0) if diff.x > 0 else Vector2(-1, 0)
        else:
            new_direction = Vector2(0, 1) if diff.y > 0 else Vector2(0, -1)
        
        next_pos = self.body[0] + new_direction
        if 0 <= next_pos.x < GRID_WIDTH and 0 <= next_pos.y < GRID_HEIGHT:
            self.direction = new_direction
        
        if random.randint(0, 99) < 51:
            self.move()

class Fruit:
    def __init__(self):
        self.randomize()

    def randomize(self):
        self.position = Vector2(random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

    def draw(self, screen):
        pygame.draw.rect(screen, pygame.Color("magenta"), pygame.Rect(self.position.x * CELL_SIZE, self.position.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)) # Magenta fruit

# Game Setup
pygame.init()
screen = pygame.display.set_mode((GRID_WIDTH * CELL_SIZE, GRID_HEIGHT * CELL_SIZE))
clock = pygame.time.Clock()
pygame.display.set_caption("Snake Game")
font_large = pygame.font.Font(None, 60)
font_medium = pygame.font.Font(None, 40)
font_small = pygame.font.Font(None, 30)

def draw_grid():
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if (row + col) % 2 == 0:
                pygame.draw.rect(screen, BG_COLOR_1, rect)
            else:
                pygame.draw.rect(screen, BG_COLOR_2, rect)

def show_instructions():
    screen.fill(WELCOME_BG)
    title_text = font_large.render("SNAKE GAME", True, TEXT_COLOR)
    instructions = [
        "Use ARROW KEYS to move.",
        "Avoid the RED snake!",
        "Eat MAGENTA fruits for points.",
        "Press any key to start."
    ]
    screen.blit(title_text, (GRID_WIDTH * CELL_SIZE // 4, 50))
    y_offset = 200
    for line in instructions:
        text = font_medium.render(line, True, TEXT_COLOR)
        screen.blit(text, (GRID_WIDTH * CELL_SIZE // 4, y_offset))
        y_offset += 50
    pygame.display.update()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                waiting = False

def show_game_over(score):
    screen.fill(GAME_OVER_BG)
    game_over_text = font_large.render("GAME OVER", True, GAME_OVER_COLOR)
    score_text = font_medium.render(f"Score: {score}", True, TEXT_COLOR)
    restart_text = font_small.render("Press SPACE to try again", True, TEXT_COLOR)

    # Center the text
    game_over_rect = game_over_text.get_rect(center=(GRID_WIDTH * CELL_SIZE // 2, GRID_HEIGHT * CELL_SIZE // 3))
    score_rect = score_text.get_rect(center=(GRID_WIDTH * CELL_SIZE // 2, GRID_HEIGHT * CELL_SIZE // 2))
    restart_rect = restart_text.get_rect(center=(GRID_WIDTH * CELL_SIZE // 2, GRID_HEIGHT * CELL_SIZE * 2 // 3))

    screen.blit(game_over_text, game_over_rect)
    screen.blit(score_text, score_rect)
    screen.blit(restart_text, restart_rect)

    pygame.display.update()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    main()
                waiting = False

def main():
    snake = Snake(pygame.Color("yellow"), (5, 10))
    enemy = EnemySnake(snake.body[0])
    fruit = Fruit()
    score = 0

    MOVE_EVENT = pygame.USEREVENT
    pygame.time.set_timer(MOVE_EVENT, 150)

    running = True
    while running:
        draw_grid()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOVE_EVENT:
                snake.move()
                enemy.move_towards_player(snake.body[0])
                if snake.body[0] == fruit.position:
                    fruit.randomize()
                    snake.grow = True
                    score += 1
                if snake.check_collision(enemy) or snake.check_self_collision() or snake.check_wall_collision():
                    running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.direction != Vector2(0, 1):
                    snake.direction = Vector2(0, -1)
                if event.key == pygame.K_DOWN and snake.direction != Vector2(0, -1):
                    snake.direction = Vector2(0, 1)
                if event.key == pygame.K_LEFT and snake.direction != Vector2(1, 0):
                    snake.direction = Vector2(-1, 0)
                if event.key == pygame.K_RIGHT and snake.direction != Vector2(-1, 0):
                    snake.direction = Vector2(1, 0)

        fruit.draw(screen)
        snake.draw(screen)
        enemy.draw(screen)
        
        score_text = font_medium.render(f"Score: {score}", True, SCORE_COLOR)
        screen.blit(score_text, (20, 20))
        
        pygame.display.update()
        clock.tick(60)
    show_game_over(score) # Added this line to show the end screen.

show_instructions()
main()
