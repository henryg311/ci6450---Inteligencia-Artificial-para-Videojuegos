import pygame
from settings import WIDTH, HEIGHT, GRID_SIZE, RED, GREEN

# Paredes del mapa
walls = [
    pygame.Rect(0, 0, WIDTH, 30),                   
    pygame.Rect(0, HEIGHT - 30, WIDTH, 30),   
    pygame.Rect(0, 0, 30, HEIGHT),                  
    pygame.Rect(WIDTH - 30, 0, 30, HEIGHT),   
    pygame.Rect(100, 0, 30, 200),                    
    pygame.Rect(100, 200, 200, 30),                  
    pygame.Rect(500, 0, 30, 250),                    
    pygame.Rect(300, 400, 200, 30),                  
    pygame.Rect(200, 300, 30, 200),                  
    pygame.Rect(600, 300, 30, 200),                  
    pygame.Rect(400, 500, 200, 30)                  
]

# Nodos del mapa
nodos = [
    (50, 50), (200, 50), (400, 50), (650, 50),
    (50, 300), (200, 300), (400, 300), (650, 300),
    (50, 550), (200, 550), (400, 550), (650, 550),
    (150, 150), (550, 150),
    (250, 450), (550, 450)
]    

# Puntos tácticos ventajosos
tactical_points_advantageous = [
    (100, 100),
    (700, 100),
    (100, 500),
    (700, 500),
    (400, 350)   
]

def draw_map(screen, piso_sprite, pared_sprite):  # Recibe los sprites como parámetros
    # Dibujar piso
    for x in range(0, WIDTH, GRID_SIZE):
        for y in range(0, HEIGHT, GRID_SIZE):
            screen.blit(piso_sprite, (x, y))

    # Dibujar paredes
    for wall in walls:
        for x in range(wall.left, wall.right, GRID_SIZE):
            for y in range(wall.top, wall.bottom, GRID_SIZE):
                screen.blit(pared_sprite, (x, y))

    # Dibujar nodos
    for nodo in nodos:
        pygame.draw.circle(screen, RED, nodo, 5)
    
     # Dibujar puntos tácticos ventajosos
    for point in tactical_points_advantageous:
        pygame.draw.circle(screen, GREEN, point, 10)