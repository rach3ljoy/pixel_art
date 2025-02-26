import pygame
import sys
import os

pygame.init()
INITIAL_WIDTH, INITIAL_HEIGHT = 1000, 600
CELL_SIZE = 20

# colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
INDIGO = (75, 0, 130)
VIOLET = (238, 130, 238)
PASTEL_PINK = (255, 182, 193)
PASTEL_YELLOW = (255, 255, 204)
PASTEL_GREEN = (152, 251, 152)
PASTEL_BLUE = (173, 216, 230)
PASTEL_PURPLE = (230, 230, 250)
BROWN = (165, 42, 42)
GRAY = (128, 128, 128)

# colour palette
COLOR_PALETTE = [
    RED, ORANGE, YELLOW, GREEN, BLUE, INDIGO, VIOLET,
    BROWN, BLACK, PASTEL_PINK, PASTEL_YELLOW, PASTEL_GREEN, PASTEL_BLUE, PASTEL_PURPLE
]

screen = pygame.display.set_mode((INITIAL_WIDTH, INITIAL_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Pixel Art Editor")
grid = [[WHITE for _ in range(INITIAL_WIDTH // CELL_SIZE)] for _ in range(INITIAL_HEIGHT // CELL_SIZE)]

current_color = BLACK
brush_size = 1  # 1x1 default brush size
undo_stack = []
redo_stack = []



def draw_with_brush(x, y):
    for i in range(-brush_size + 1, brush_size):
        for j in range(-brush_size + 1, brush_size):
            col, row = x + i, y + j
            if 0 <= col < COLS and 0 <= row < ROWS:
                grid[row][col] = current_color


running = True
drawing = False  # track when mouse is held down
while running:
    WIDTH, HEIGHT = screen.get_size()
    COLS, ROWS = (WIDTH - 200) // CELL_SIZE, HEIGHT // CELL_SIZE

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            new_width, new_height = event.size
            screen = pygame.display.set_mode((new_width, new_height), pygame.RESIZABLE)
            COLS, ROWS = (new_width - 200) // CELL_SIZE, new_height // CELL_SIZE
            new_grid = [[WHITE for _ in range(COLS)] for _ in range(ROWS)]
            for row in range(min(ROWS, len(grid))):
                for col in range(min(COLS, len(grid[row]))):
                    new_grid[row][col] = grid[row][col]
            grid = new_grid
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if x < WIDTH - 200:  
                drawing = True
                col, row = x // CELL_SIZE, y // CELL_SIZE
                if 0 <= col < COLS and 0 <= row < ROWS:
                    undo_stack.append([row.copy() for row in grid])
                    redo_stack.clear()  
                    draw_with_brush(col, row)
            else:  
                if WIDTH - 180 <= x <= WIDTH - 130:
                    if 20 <= y <= 50:  # "+" button
                        brush_size = min(brush_size + 1, 5)  
                    elif 60 <= y <= 90:  # "-" button
                        brush_size = max(brush_size - 1, 1)  
                index = (y - 120) // 50
                if 0 <= index < len(COLOR_PALETTE):
                    current_color = COLOR_PALETTE[index]
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1: 
                drawing = False
        elif event.type == pygame.MOUSEMOTION:
            if drawing:  # 
                x, y = pygame.mouse.get_pos()
                if x < WIDTH - 200: 
                    col, row = x // CELL_SIZE, y // CELL_SIZE
                    if 0 <= col < COLS and 0 <= row < ROWS:
                        draw_with_brush(col, row)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z and pygame.key.get_mods() & pygame.KMOD_CTRL:  #undo
                if undo_stack:
                    redo_stack.append([row.copy() for row in grid])
                    grid = undo_stack.pop()
            elif event.key == pygame.K_y and pygame.key.get_mods() & pygame.KMOD_CTRL:  #redo
                if redo_stack:
                    undo_stack.append([row.copy() for row in grid])
                    grid = redo_stack.pop()
            elif event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:  #save
                pygame.image.save(screen, "pixel_art.png")
                print("Artwork saved as pixel_art.png")
            elif event.key == pygame.K_l and pygame.key.get_mods() & pygame.KMOD_CTRL:  #load
                if os.path.exists("pixel_art.png"):
                    loaded_image = pygame.image.load("pixel_art.png")
                    for row in range(ROWS):
                        for col in range(COLS):
                            grid[row][col] = loaded_image.get_at((col * CELL_SIZE, row * CELL_SIZE))
                    print("Artwork loaded from pixel_art.png")

    screen.fill(WHITE)
    for row in range(ROWS):
        for col in range(COLS):
            pygame.draw.rect(screen, grid[row][col], (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    for i, color in enumerate(COLOR_PALETTE):
        pygame.draw.rect(screen, color, (WIDTH - 180, 120 + i * 50, 50, 50))

    pygame.draw.rect(screen, GRAY, (WIDTH - 180, 20, 50, 30))  # "+" button
    pygame.draw.rect(screen, GRAY, (WIDTH - 180, 60, 50, 30))  # "-" button
    font = pygame.font.SysFont(None, 30)
    plus_text = font.render("+", True, BLACK)
    minus_text = font.render("-", True, BLACK)
    screen.blit(plus_text, (WIDTH - 165, 25))
    screen.blit(minus_text, (WIDTH - 165, 65))

    brush_text = font.render(f"Brush: {brush_size}x{brush_size}", True, BLACK)
    screen.blit(brush_text, (WIDTH - 180, 100))
    pygame.display.flip()

#quit
pygame.quit()
sys.exit()
