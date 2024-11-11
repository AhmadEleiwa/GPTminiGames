import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Constants
WIDTH = 600
HEIGHT = 600
FONT = pygame.font.SysFont("comicsans", 40)

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
line_color = (28, 170, 156)
circle_color = (242, 85, 96)
rect_color = (28, 100, 220)
circle_radius = 60
rect_width = 90
bg_color = (135, 206, 235)  # Sky blue
slime_color = (0, 255, 0)
platform_color = (139, 69, 19)
slime_squash_color = (50, 255, 50)
line_width = 15
space = 55

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Menu")

# Global grid for Tic-Tac-Toe
grid = [['' for _ in range(3)] for _ in range(3)]

# Menu
def draw_menu():
    screen.fill(black)
    title_text = FONT.render("Game Menu", True, white)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))

    options = ["1. Escape the Maze", "2. Slime Jump", "3. Tic Tac Toe", "4. Quit"]
    for i, option in enumerate(options):
        option_text = FONT.render(option, True, white)
        screen.blit(option_text, (WIDTH // 2 - option_text.get_width() // 2, HEIGHT // 2 + i * 50))

    pygame.display.flip()

# Escape the Maze game
def escape_the_maze():
    cols, rows = WIDTH // 40, HEIGHT // 40
    player_x, player_y = 0, 0
    maze = [[1 if random.random() < 0.3 else 0 for _ in range(cols)] for _ in range(rows)]
    maze[0][0] = 0  # Start position
    maze[rows - 1][cols - 1] = 0  # End position
    collectibles = [(random.randint(0, cols - 1), random.randint(0, rows - 1)) for _ in range(5)]
    collectibles = [pos for pos in collectibles if maze[pos[1]][pos[0]] == 0]
    score = 0

    clock = pygame.time.Clock()
    running = True
    while running:
        screen.fill(black)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and player_y > 0 and maze[player_y - 1][player_x] == 0:
                    player_y -= 1
                elif event.key == pygame.K_DOWN and player_y < rows - 1 and maze[player_y + 1][player_x] == 0:
                    player_y += 1
                elif event.key == pygame.K_LEFT and player_x > 0 and maze[player_y][player_x - 1] == 0:
                    player_x -= 1
                elif event.key == pygame.K_RIGHT and player_x < cols - 1 and maze[player_y][player_x + 1] == 0:
                    player_x += 1
        
        if (player_x, player_y) in collectibles:
            score += 1
            collectibles.remove((player_x, player_y))

        for y in range(rows):
            for x in range(cols):
                color = black if maze[y][x] == 1 else white
                pygame.draw.rect(screen, color, (x * 40, y * 40, 40, 40))
        
        for cx, cy in collectibles:
            pygame.draw.circle(screen, green, (cx * 40 + 20, cy * 40 + 20), 10)

        pygame.draw.rect(screen, blue, (player_x * 40, player_y * 40, 40, 40))

        if player_x == cols - 1 and player_y == rows - 1:
            print(f"You escaped the maze with a score of {score}!")
            running = False

        pygame.display.flip()
        clock.tick(10)

# Slime Jump game
def slime_jump():
    slime_width = 40
    slime_height = 40
    gravity = 1
    move_speed = 5
    cooldown_time = 1000
    slime_x = WIDTH // 2 - slime_width // 2
    slime_y = HEIGHT - slime_height - 10
    slime_velocity_y = 0
    slime_velocity_x = 0
    is_jumping = False
    jump_charge = 0
    last_jump_time = 0
    platforms = [(random.randint(50, WIDTH - 150), random.randint(100, HEIGHT - 50), random.choice([-1, 1])) for _ in range(5)]

    clock = pygame.time.Clock()
    running = True
    while running:
        screen.fill(bg_color)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            slime_velocity_x = -move_speed
        elif keys[pygame.K_RIGHT]:
            slime_velocity_x = move_speed
        else:
            slime_velocity_x = 0

        if keys[pygame.K_SPACE] and not is_jumping:
            if pygame.time.get_ticks() - last_jump_time > cooldown_time:
                jump_charge = max(jump_charge - 1, -20)

        elif not keys[pygame.K_SPACE] and not is_jumping:
            if pygame.time.get_ticks() - last_jump_time > cooldown_time:
                slime_velocity_y = jump_charge
                is_jumping = True
                last_jump_time = pygame.time.get_ticks()
                jump_charge = 0

        slime_x += slime_velocity_x
        slime_y += slime_velocity_y
        slime_velocity_y += gravity

        if slime_y >= HEIGHT - slime_height:
            slime_y = HEIGHT - slime_height
            slime_velocity_y = 0
            is_jumping = False

        for platform_x, platform_y, platform_direction in platforms:
            if platform_y <= slime_y + slime_height <= platform_y + 20:
                if platform_x <= slime_x + slime_width // 2 <= platform_x + 100:
                    slime_y = platform_y - slime_height
                    slime_velocity_y = 0
                    is_jumping = False
                    break

            platform_x += platform_direction
            if platform_x <= 0 or platform_x + 100 >= WIDTH:
                platform_direction *= -1

        if is_jumping:
            pygame.draw.rect(screen, slime_squash_color, (slime_x, slime_y, slime_width, slime_height // 2))
            pygame.draw.rect(screen, slime_color, (slime_x, slime_y + slime_height // 2, slime_width, slime_height // 2))
        else:
            pygame.draw.rect(screen, slime_color, (slime_x, slime_y, slime_width, slime_height))

        for platform_x, platform_y, _ in platforms:
            pygame.draw.rect(screen, platform_color, (platform_x, platform_y, 100, 20))

        pygame.display.flip()
        clock.tick(60)

# Tic-Tac-Toe game
def tic_tac_toe():
    global grid
    player = 'X'
    game_over = False
    winner = None

    clock = pygame.time.Clock()
    while True:
        screen.fill(bg_color)
        draw_lines()
        draw_marks()

        if game_over:
            if winner:
                text = FONT.render(f"Player {winner} wins!", True, (0, 0, 0))
            else:
                text = FONT.render("It's a Draw!", True, (0, 0, 0))
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if not game_over and event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                clicked_row = y // 200
                clicked_col = x // 200
                if grid[clicked_row][clicked_col] == '':
                    grid[clicked_row][clicked_col] = player
                    if check_win(player):
                        game_over = True
                        winner = player
                    elif check_draw():
                        game_over = True
                        winner = None
                    player = 'O' if player == 'X' else 'X'

        pygame.display.update()

# Function to check if a player wins in Tic-Tac-Toe
def check_win(player):
    for row in range(3):
        if grid[row][0] == grid[row][1] == grid[row][2] == player:
            pygame.draw.line(screen, line_color, (0, row * 200 + 100), (WIDTH, row * 200 + 100), line_width)
            return True
    for col in range(3):
        if grid[0][col] == grid[1][col] == grid[2][col] == player:
            pygame.draw.line(screen, line_color, (col * 200 + 100, 0), (col * 200 + 100, HEIGHT), line_width)
            return True
    if grid[0][0] == grid[1][1] == grid[2][2] == player:
        pygame.draw.line(screen, line_color, (0, 0), (WIDTH, HEIGHT), line_width)
        return True
    if grid[0][2] == grid[1][1] == grid[2][0] == player:
        pygame.draw.line(screen, line_color, (WIDTH, 0), (0, HEIGHT), line_width)
        return True
    return False

def check_draw():
    for row in grid:
        for col in row:
            if col == '':
                return False
    return True

def draw_lines():
    pygame.draw.line(screen, line_color, (200, 0), (200, HEIGHT), line_width)
    pygame.draw.line(screen, line_color, (400, 0), (400, HEIGHT), line_width)
    pygame.draw.line(screen, line_color, (0, 200), (WIDTH, 200), line_width)
    pygame.draw.line(screen, line_color, (0, 400), (WIDTH, 400), line_width)

def draw_marks():
    for row in range(3):
        for col in range(3):
            if grid[row][col] != '':
                mark = FONT.render(grid[row][col], True, black)
                screen.blit(mark, (col * 200 + 100 - mark.get_width() // 2, row * 200 + 100 - mark.get_height() // 2))

# Main game loop
def main():
    draw_menu()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    escape_the_maze()
                elif event.key == pygame.K_2:
                    slime_jump()
                elif event.key == pygame.K_3:
                    tic_tac_toe()
                elif event.key == pygame.K_4:
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()

# Run the main menu
main()
