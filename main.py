import pygame
import battle

from tilemap import tilemap


pygame.init()

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Dragon Game")

clock = pygame.time.Clock()
FPS = 60

TILE_SIZE = 20


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
GREEN = (0, 180, 0)
RED = (200, 0, 0)
BLUE = (0, 100, 255)
YELLOW = (255, 255, 0)


# controls which screen is showing
game_state = "DRAGON_SELECT"


# stores the dragon the player chooses
selected_dragon = None


player_row = 0
player_column = 0


# keeps track of what happened during battle
battle_message = "Choose a move using 1, 2, 3, or 4"


# stops the player from adding another move while Round Robin is running
waiting_for_round = False


# finds where the player starts on the map
for row_index, row in enumerate(tilemap):

    for column_index, tile in enumerate(row):

        if tile == "5":

            player_row = row_index
            player_column = column_index


# draws the choose your dragon screen
def draw_dragon_select_screen():

    window.fill(BLACK)

    title_font = pygame.font.Font(None, 64)
    text_font = pygame.font.Font(None, 34)
    small_font = pygame.font.Font(None, 26)

    title = title_font.render(
        "CHOOSE YOUR DRAGON",
        True,
        YELLOW
    )

    window.blit(
        title,
        (
            WINDOW_WIDTH // 2 - title.get_width() // 2,
            70
        )
    )

    wyvern_title = text_font.render(
        "1 - WYVERN",
        True,
        WHITE
    )

    window.blit(
        wyvern_title,
        (
            WINDOW_WIDTH // 2 - wyvern_title.get_width() // 2,
            210
        )
    )

    wyvern_stats = [
        "Attack: 10",
        "Defense: 10",
        "Speed: 10",
        "HP: 50"
    ]

    stat_y = 270

    for stat in wyvern_stats:

        stat_text = small_font.render(
            stat,
            True,
            WHITE
        )

        window.blit(
            stat_text,
            (
                WINDOW_WIDTH // 2 - stat_text.get_width() // 2,
                stat_y
            )
        )

        stat_y += 40

    choose_text = text_font.render(
        "Press 1 to choose Wyvern",
        True,
        YELLOW
    )

    window.blit(
        choose_text,
        (
            WINDOW_WIDTH // 2 - choose_text.get_width() // 2,
            520
        )
    )


# draws the map
def draw_tilemap(camera_x, camera_y):

    for row_index, row in enumerate(tilemap):

        for column_index, tile in enumerate(row):

            x = (column_index * TILE_SIZE) - camera_x
            y = (row_index * TILE_SIZE) - camera_y

            if tile == "0":
                color = GREEN

            elif tile == "1":
                color = GRAY

            elif tile == "3":
                color = RED

            elif tile == "5":
                color = GREEN

            else:
                color = WHITE

            pygame.draw.rect(
                window,
                color,
                (x, y, TILE_SIZE, TILE_SIZE)
            )


# draws the player
def draw_player(camera_x, camera_y):

    x = (player_column * TILE_SIZE) - camera_x
    y = (player_row * TILE_SIZE) - camera_y

    pygame.draw.rect(
        window,
        BLUE,
        (x, y, TILE_SIZE, TILE_SIZE)
    )


# checks if the player can move onto a tile
def can_move_to(row, column):

    if row < 0 or row >= len(tilemap):
        return False

    if column < 0 or column >= len(tilemap[row]):
        return False

    tile = tilemap[row][column]

    # tile 1 is blocked
    if tile == "1":
        return False

    return True


# adds the player's move and CPU move to the queue
def start_battle_round(player_move):

    global battle_message
    global waiting_for_round

    if player_move == 1:

        battle.choose_tail_slash()

        battle_message = (
            "Tail Slash and CPU Claw added to the queue"
        )

    elif player_move == 2:

        battle.choose_wyverns_wrath(4)

        battle_message = (
            "Wyvern's Wrath and CPU Claw added to the queue"
        )

    elif player_move == 3:

        battle.choose_wing_rush(4)

        battle_message = (
            "Wing Rush and CPU Claw added to the queue"
        )

    elif player_move == 4:

        battle.choose_venomous_bite(5)

        battle_message = (
            "Venomous Bite and CPU Claw added to the queue"
        )

    # CPU automatically chooses Claw Attack
    battle.choose_enemy_claw(4)

    waiting_for_round = True


# runs one step of Round Robin
def run_round_robin_step():

    global battle_message
    global waiting_for_round

    if len(battle.action_queue) == 0:

        waiting_for_round = False

        battle_message = (
            "Round finished. Choose another move."
        )

        return

    current_action = battle.action_queue[0]

    owner = current_action["owner"]
    action = current_action["action"]
    old_time = current_action["remaining_time"]

    battle.round_robin_scheduler()

    owner_name = owner

    if owner_name == "dragon":
        owner_name = "Dragon"

    elif owner_name == "enemy":
        owner_name = "CPU"

    if old_time <= battle.time_quantum:

        battle_message = (
            owner_name
            + " - "
            + action
            + " finished!"
        )

    else:

        new_time = old_time - battle.time_quantum

        battle_message = (
            owner_name
            + " - "
            + action
            + " used quantum "
            + str(battle.time_quantum)
            + ". "
            + str(new_time)
            + " remaining."
        )

    if len(battle.action_queue) == 0:

        waiting_for_round = False


# draws the battle screen
def draw_battle_screen():

    window.fill(BLACK)

    title_font = pygame.font.Font(None, 60)
    text_font = pygame.font.Font(None, 32)
    small_font = pygame.font.Font(None, 26)

    title = title_font.render(
        "WYVERN VS CPU",
        True,
        WHITE
    )

    dragon_hp_text = text_font.render(
        f"Wyvern HP: {battle.dragon_state['hp']}",
        True,
        WHITE
    )

    enemy_hp_text = text_font.render(
        f"CPU HP: {battle.enemy_state['hp']}",
        True,
        WHITE
    )

    window.blit(
        title,
        (
            WINDOW_WIDTH // 2 - title.get_width() // 2,
            50
        )
    )

    window.blit(
        dragon_hp_text,
        (100, 150)
    )

    window.blit(
        enemy_hp_text,
        (700, 150)
    )

    # shows move choices when there is not a round running
    if waiting_for_round == False:

        choose_text = text_font.render(
            "Choose a move:",
            True,
            YELLOW
        )

        window.blit(
            choose_text,
            (100, 240)
        )

        move1 = text_font.render(
            "1 - Tail Slash",
            True,
            WHITE
        )

        move2 = text_font.render(
            "2 - Wyvern's Wrath",
            True,
            WHITE
        )

        move3 = text_font.render(
            "3 - Wing Rush",
            True,
            WHITE
        )

        move4 = text_font.render(
            "4 - Venomous Bite",
            True,
            WHITE
        )

        window.blit(move1, (100, 300))
        window.blit(move2, (100, 350))
        window.blit(move3, (100, 400))
        window.blit(move4, (100, 450))

    # shows Round Robin information after the player picks a move
    else:

        space_text = text_font.render(
            "Press SPACE to run the next Round Robin step",
            True,
            YELLOW
        )

        window.blit(
            space_text,
            (100, 240)
        )

        queue_title = text_font.render(
            "ROUND ROBIN QUEUE",
            True,
            YELLOW
        )

        window.blit(
            queue_title,
            (100, 300)
        )

        quantum_text = small_font.render(
            "Time Quantum: " + str(battle.time_quantum),
            True,
            WHITE
        )

        window.blit(
            quantum_text,
            (100, 340)
        )

        queue_y = 390

        for action in battle.action_queue:

            owner_name = action["owner"]

            if owner_name == "dragon":
                owner_name = "Dragon"

            elif owner_name == "enemy":
                owner_name = "CPU"

            queue_text = small_font.render(
                owner_name
                + " - "
                + action["action"]
                + " - "
                + str(action["remaining_time"])
                + " remaining",
                True,
                WHITE
            )

            window.blit(
                queue_text,
                (120, queue_y)
            )

            queue_y += 40

    # shows the latest thing that happened
    message_text = small_font.render(
        battle_message,
        True,
        WHITE
    )

    window.blit(
        message_text,
        (100, 570)
    )


running = True


while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False

        if event.type == pygame.KEYDOWN:

            # dragon selection controls
            if game_state == "DRAGON_SELECT":

                if event.key == pygame.K_1:

                    selected_dragon = "Wyvern"

                    game_state = "MAP"

            # map controls
            elif game_state == "MAP":

                new_row = player_row
                new_column = player_column

                if event.key == pygame.K_UP:

                    new_row -= 1

                elif event.key == pygame.K_DOWN:

                    new_row += 1

                elif event.key == pygame.K_LEFT:

                    new_column -= 1

                elif event.key == pygame.K_RIGHT:

                    new_column += 1

                if can_move_to(
                    new_row,
                    new_column
                ):

                    player_row = new_row
                    player_column = new_column

                    current_tile = (
                        tilemap[player_row][player_column]
                    )

                    # tile 3 starts the battle
                    if current_tile == "3":

                        game_state = "BATTLE"

                        battle_message = (
                            "Choose a move using 1, 2, 3, or 4"
                        )

            # battle controls
            elif game_state == "BATTLE":

                # player chooses a move
                if waiting_for_round == False:

                    if event.key == pygame.K_1:

                        start_battle_round(1)

                    elif event.key == pygame.K_2:

                        start_battle_round(2)

                    elif event.key == pygame.K_3:

                        start_battle_round(3)

                    elif event.key == pygame.K_4:

                        start_battle_round(4)

                # SPACE runs one Round Robin step
                else:

                    if event.key == pygame.K_SPACE:

                        run_round_robin_step()


    # dragon selection screen
    if game_state == "DRAGON_SELECT":

        draw_dragon_select_screen()

    # map screen
    elif game_state == "MAP":

        camera_x = (
            player_column * TILE_SIZE
            - WINDOW_WIDTH // 2
        )

        camera_y = (
            player_row * TILE_SIZE
            - WINDOW_HEIGHT // 2
        )

        window.fill(BLACK)

        draw_tilemap(
            camera_x,
            camera_y
        )

        draw_player(
            camera_x,
            camera_y
        )

    # battle screen
    elif game_state == "BATTLE":

        draw_battle_screen()


    pygame.display.flip()

    clock.tick(FPS)


pygame.quit()