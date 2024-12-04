import pygame
import math
from settings import WIDTH, HEIGHT, WHITE, GRID_SIZE, RED
from map_elements import walls, draw_map, nodos
from characters import PlayerCharacter, PathFindingCharacter, StaticAlignCharacter, EvasiveExplorerCharacter
from map_elements import tactical_points_advantageous, tactical_points_disadvantageous

# Inicialización de Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Castillo")

# Fuentes para el texto de contador y victoria
font = pygame.font.Font(None, 36)  # Fuente para el contador
victory_font = pygame.font.Font(None, 74)  # Fuente para el texto de victoria
victory_text = victory_font.render("Victoria", True, (0, 0, 0))

# Cargar sprites después de inicializar la pantalla
PISO_SPRITE = pygame.image.load("assets/textures/sprite_piso.png").convert()
PARED_SPRITE = pygame.image.load("assets/textures/sprite_pared.jpg").convert()

# Cargar sprites de personajes
PLAYER_SPRITE = pygame.image.load("assets/textures/player_sprite.png").convert_alpha()
PATHFINDER_SPRITE = pygame.image.load("assets/textures/pathfinder_sprite.png").convert_alpha()
STATIC_SPRITE = pygame.image.load("assets/textures/static_sprite.png").convert_alpha()
EXPLORER_SPRITE = pygame.image.load("assets/textures/explorer_sprite.png").convert_alpha()

# Ajustar tamaño de los sprites
PISO_SPRITE = pygame.transform.scale(PISO_SPRITE, (GRID_SIZE, GRID_SIZE))
PARED_SPRITE = pygame.transform.scale(PARED_SPRITE, (GRID_SIZE, GRID_SIZE))

PLAYER_SPRITE = pygame.transform.scale(PLAYER_SPRITE, (40, 40))
PATHFINDER_SPRITE = pygame.transform.scale(PATHFINDER_SPRITE, (60, 60))
STATIC_SPRITE = pygame.transform.scale(STATIC_SPRITE, (50, 40))
EXPLORER_SPRITE = pygame.transform.scale(EXPLORER_SPRITE, (40, 40))

# Instancia de personajes
initial_player_position = (WIDTH - 50, HEIGHT - 50)
player = PlayerCharacter(*initial_player_position, PLAYER_SPRITE)
path_finder = PathFindingCharacter(50, 50, nodos, PATHFINDER_SPRITE, seek_distance=200)
explorer = EvasiveExplorerCharacter(300, 300, path_finder, EXPLORER_SPRITE)
static_characters = [
    StaticAlignCharacter(750, 50, STATIC_SPRITE),
    StaticAlignCharacter(150, 50, STATIC_SPRITE),
    StaticAlignCharacter(400, 300, STATIC_SPRITE),
    StaticAlignCharacter(50, 500, STATIC_SPRITE)
]

# Contador de capturas y estado de victoria
captures = 0
victory = False

def check_collision(player, explorer):
    distancia = math.hypot(player.x - explorer.x, player.y - explorer.y)
    return distancia < (player.radio + explorer.radio)

def check_projectile_collision(player, static_characters):
    player_rect = pygame.Rect(player.x - player.radio, player.y - player.radio, player.radio * 2, player.radio * 2)
    for character in static_characters:
        for proyectil in character.proyectiles:
            proyectil_rect = pygame.Rect(proyectil.x - proyectil.radio, proyectil.y - proyectil.radio, proyectil.radio * 2, proyectil.radio * 2)
            if player_rect.colliderect(proyectil_rect):
                return True
    return False

def check_seek_collision(player, seeker):
    distancia = math.hypot(player.x - seeker.x, player.y - seeker.y)
    return distancia < (player.radio + seeker.radio)

def mostrar_contador(captures):
    # Renderizar el texto del contador en pantalla
    contador_text = font.render(f"Capturas: {captures}/3", True, (255, 255, 255))
    screen.blit(contador_text, (10, 10))  

# Bucle principal
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not victory:
        teclas = pygame.key.get_pressed()
        player.mover(teclas, walls)
        path_finder.mover(walls, player)
        explorer.mover(player, walls)

        # Verificar si el jugador atrapa al explorador
        if check_collision(player, explorer):
            explorer.x = path_finder.x + 20
            explorer.y = path_finder.y + 20
            captures += 1

            # Verificar si el jugador ha capturado al explorador 3 veces
            if captures >= 3:
                victory = True

        # Verificar si el jugador es golpeado por un proyectil o por el personaje con seek
        if check_projectile_collision(player, static_characters) or check_seek_collision(player, path_finder):
            player.x, player.y = initial_player_position  # Reiniciar posición del jugador
            captures = 0  # Reiniciar contador de capturas
        
         # Verificar si el explorer toca al pathfinding
        if explorer.tocar_pathfinding():
            path_finder.velocidad =  3.5

        # Calcular ruta táctica antes de dibujar
        path_finder.calcular_ruta_tactica(walls, tactical_points_advantageous, tactical_points_disadvantageous)

        # Dibujar todo
        draw_map(screen, PISO_SPRITE, PARED_SPRITE)
        player.dibujar(screen)
        path_finder.dibujar(screen)
        explorer.dibujar(screen)
        path_finder.dibujar_ruta(screen)
        path_finder.dibujar_ruta_tactica(screen)
        for character in static_characters:
            character.apuntar_y_disparar(player, walls)
            character.actualizar_proyectiles(walls)
            character.comportamiento_temporal() 
            character.mover()
            character.dibujar(screen)
        
        for nodo in nodos:
            pygame.draw.circle(screen, RED, nodo, 5)
        
        # Mostrar el contador de capturas
        mostrar_contador(captures)
    else:
        # Mostrar el mensaje de victoria
        screen.fill(WHITE)
        screen.blit(victory_text, (WIDTH // 2 - victory_text.get_width() // 2, HEIGHT // 2 - victory_text.get_height() // 2))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
