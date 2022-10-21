import pygame, random



pygame.init()

WINDOW_WIDTH = 339
WINDOW_HEIGHT = 339
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Puzzle Game')

FPS = 10
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
CRIMSON = (220, 20, 60)
ORANGE = (255, 127, 0)

bg = pygame.image.load('brandy.png')
bg_rect = bg.get_rect()
bg_rect.topleft = (0, 0)

font_title = pygame.font.Font('freesansbold.ttf', 64)
font_content = pygame.font.Font('freesansbold.ttf', 40)





selected_img = None
is_game_over = False
show_start_screen = True

rows = None
cols = None

cell_width = None
cell_height = None

cells = []

def start_game():
    global cells, cell_width, cell_height, show_start_screen

    rows = 4
    cols = 4
    num_cells = rows * cols

    cell_width = WINDOW_WIDTH // rows
    cell_height = WINDOW_HEIGHT // cols

    cell = []
    rand_indexes = list(range(0, num_cells))

    for i in range(num_cells):
        x = (i % rows) * cell_width
        y = (i // cols) * cell_height
        rect = pygame.Rect(x, y, cell_width, cell_height)
        rand_pos = random.choice(rand_indexes)
        rand_indexes.remove(rand_pos)
        cells.append({'rect': rect, 'border': WHITE, 'order': i, 'pos':rand_pos})

    show_start_screen = False

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            if is_game_over:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_SPACE]:
                    is_game_over = False
                    show_start_screen = True
            



        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not is_game_over:
            mouse_pos = pygame.mouse.get_pos()

            for cell in cells:
                rect = cell['rect']
                order = cell['order']

                if rect.collidepoint(mouse_pos):
                    if not selected_img:
                        selected_img = cell
                        cell['border'] = RED
                    else:
                        current_img = cell
                        if current_img['order'] != selected_img['order']:
                            #swap images
                            temp = selected_img['pos']
                            cells[selected_img['order']]['pos'] = cells[current_img['order']]['pos']
                            cells[current_img['order']]['pos'] = temp

                            cells[selected_img['order']]['border'] = WHITE
                            selected_img = None

                            # check if puzzle is solved
                            is_game_over = True
                            for cell in cells:
                                if cell['order'] != cell['pos']:
                                    is_game_over = False


    if show_start_screen:
        start_game()
    else:

        screen.fill(WHITE)

        if not is_game_over:
            for i, val in enumerate(cells):
                pos = cells[i]['pos']
                img_area = pygame.Rect(cells[pos]['rect'].x, cells[pos]['rect'].y, cell_width, cell_height)
                screen.blit(bg, cells[i]['rect'], img_area)
                pygame.draw.rect(screen, cells[i]['border'], cells[i]['rect'], 1)
        else:
            screen.blit(bg, bg_rect)
            screen.blit(play_again_text, play_again_rect)
            screen.blit(continue_text, continue_rect)

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
