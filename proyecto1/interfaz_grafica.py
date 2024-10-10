import pygame

# Definir colores
WHITE = (255, 255, 255)

# Dimensiones de la ventana
WIDTH, HEIGHT = 800, 600

# Inicializar la pantalla y otras configuraciones de pygame
def init_screen():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Simulación de Personajes")
    return screen

# Limpiar la pantalla
def clear_screen(screen):
    screen.fill(WHITE)

# Controlar el framerate
def set_fps(clock, fps=60):
    clock.tick(fps)

# Actualizar la pantalla
def update_screen():
    pygame.display.flip()

# Finalizar pygame
def quit_game():
    pygame.quit()

# Manejar los eventos de salida
def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_game()
            exit()
