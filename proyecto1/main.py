import random
import pygame
from interfaz_grafica import init_screen, clear_screen, set_fps, update_screen, handle_events
from kinematic_algorithms import KinematicCharacter
from dynamic_algorithms import DynamicCharacter
from alignment_algorithms import AlignCharacter, VelocityMatchingCharacter, FaceCharacter 
from pursue_evade_wander import PursueCharacter, EvadeCharacter, WanderCharacter
from path_cavoidance import PathFollowingCharacter, CollisionAvoidanceCharacter

import math

# Dimensiones de la ventana
WIDTH, HEIGHT = 800, 600
FPS = 60

# Clase para representar al jugador
class Player:
    def __init__(self, x, y, radius=15, color=(0, 255, 0)):  # Verde para el jugador
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.speed = 5
        self.velocity = pygame.Vector2(0, 0)
    
    def flee(self, pursuer_position, pursuer_velocity):
        """
        Algoritmo Flee para el jugador: alejarse del personaje que lo persigue.
        """
        direction = pygame.Vector2(self.x, self.y) - pursuer_position
        distance = direction.length()

        if distance < 100:
            if direction.length() > 0:
                self.velocity = direction.normalize() * self.speed

        self.x += self.velocity.x
        self.y += self.velocity.y

        # Limitar al jugador dentro de los bordes de la pantalla
        self.x = max(self.radius, min(self.x, WIDTH - self.radius))
        self.y = max(self.radius, min(self.y, HEIGHT - self.radius))

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    def move(self, keys, width, height):
        previous_position = pygame.Vector2(self.x, self.y)

        if keys[pygame.K_LEFT] and self.x - self.radius > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x + self.radius < width:
            self.x += self.speed
        if keys[pygame.K_UP] and self.y - self.radius > 0:
            self.y -= self.speed
        if keys[pygame.K_DOWN] and self.y + self.radius < height:
            self.y += self.speed

        # Calcular la velocidad en función del movimiento actual
        current_position = pygame.Vector2(self.x, self.y)
        self.velocity = current_position - previous_position  # Calcular el vector de velocidad

# Función para mostrar el menú
def mostrar_menu():
    print("Seleccione el algoritmo que desea ejecutar:")
    print("0. Solo movimiento del jugador sin algoritmos activos")
    print("1. Kinematic Arriving: Los personajes se acercan al jugador.")
    print("2. Kinematic Flee: Los personajes huyen del jugador hasta una distancia determinada.")
    print("3. Kinematic Wandering: Los personajes deambulan aleatoriamente.")
    print("4. Dynamic Seek: Los personajes persiguen dinámicamente al jugador.")
    print("5. Dynamic Flee: Los personajes huyen dinámicamente del jugador hasta una distancia.")
    print("6. Dynamic Arrive: Los personajes se desaceleran dinámicamente al acercarse al jugador.")
    print("7. Align: Los personajes ajustan su orientación para mirar al jugador.")
    print("8. Velocity Matching: Los personajes ajustan su velocidad a la del jugador.")
    print("9. Face: 5 personajes miran al jugador desde diferentes lugares.")
    print("10. Pursue and Evade - Look Where You're Going: Persigue y evade.")
    print("11. Dynamic Wander: 5 personajes deambulan aleatoriamente.")
    print("12. Path Following: Sigue un ruta determinada.")
    print("13. Collision Avoidance: Personajes aplicando dynamic wander mientras se evitan entre ellos.")
    opcion = input("Ingrese el número del algoritmo que desea ejecutar: ")
    return int(opcion)

def mostrar_menu_pursue_evade():
    """
    Menú gráfico para seleccionar entre las opciones A y B en el algoritmo Pursue and Evade.
    """
    print("Seleccione la opción:")
    print("a. Un personaje persigue al jugador mientras otro lo evade.")
    print("b. El jugador evade a un personaje que lo persigue.")
    
    opcion = input("Ingrese a o b: ").lower()
    return opcion

# Función para ejecutar el algoritmo seleccionado
def ejecutar_algoritmo(opcion, player, characters):
    if opcion == 0:
        return lambda: None
    elif opcion == 1:
        return lambda: [character.kinematic_arrive(player.x, player.y) for character in characters]
    elif opcion == 2:
        return lambda: [character.kinematic_flee(player.x, player.y) for character in characters]
    elif opcion == 3:
        return lambda: [character.kinematic_wander() for character in characters]
    elif opcion == 4:
        return lambda: [character.dynamic_seek(player.x, player.y) for character in characters]
    elif opcion == 5:
        return lambda: [character.dynamic_flee(player.x, player.y) for character in characters]
    elif opcion == 6:
        return lambda: [character.dynamic_arrive(player.x, player.y) for character in characters]
    elif opcion == 7:
        return lambda: [character.align(player.velocity) for character in characters]
    elif opcion == 8:
        return lambda: [character.velocity_matching(player.velocity) for character in characters]
    elif opcion == 9:
        return lambda: [character.face(player.x, player.y) for character in characters]


# Función para limitar el movimiento de los personajes dentro de los límites de la pantalla
def limitar_movimiento_personajes(characters):
    for character in characters:
        if character.x - character.radius < 0:
            character.x = character.radius
        if character.x + character.radius > WIDTH:
            character.x = WIDTH - character.radius
        if character.y - character.radius < 0:
            character.y = character.radius
        if character.y + character.radius > HEIGHT:
            character.y = HEIGHT - character.radius

# Función para manejar la separación entre los personajes y el jugador
def manejar_separacion(player, characters):
    # Verificar colisiones entre el jugador y los personajes
    for character in characters:
        dx = character.x - player.x
        dy = character.y - player.y
        distance = (dx**2 + dy**2) ** 0.5
        min_dist = player.radius + character.radius
        if distance < min_dist and distance > 0:
            # Separar al jugador del personaje
            overlap = min_dist - distance
            direction = pygame.Vector2(dx, dy).normalize()
            player.x -= direction.x * overlap / 2
            player.y -= direction.y * overlap / 2
            character.x += direction.x * overlap / 2
            character.y += direction.y * overlap / 2

    # Verificar colisiones entre personajes
    for i, char_a in enumerate(characters):
        for char_b in characters[i+1:]:
            dx = char_b.x - char_a.x
            dy = char_b.y - char_a.y
            distance = (dx**2 + dy**2) ** 0.5
            min_dist = char_a.radius + char_b.radius
            if distance < min_dist and distance > 0:
                # Separar a los personajes
                overlap = min_dist - distance
                direction = pygame.Vector2(dx, dy).normalize()
                char_a.x -= direction.x * overlap / 2
                char_a.y -= direction.y * overlap / 2
                char_b.x += direction.x * overlap / 2
                char_b.y += direction.y * overlap / 2

# Función principal
def main():
    opcion = mostrar_menu()
    screen = init_screen()
    clock = pygame.time.Clock()

    # Inicializamos al jugador
    player = Player(WIDTH // 2, HEIGHT // 2)

    # Inicializar
    if opcion in [1, 2, 3]:
        characters = [KinematicCharacter(100, 100), KinematicCharacter(700, 100), KinematicCharacter(100, 500)]
        ejecutar = ejecutar_algoritmo(opcion, player, characters)
    elif opcion in [4, 5, 6]:
        characters = [DynamicCharacter(100, 100), DynamicCharacter(700, 100), DynamicCharacter(100, 500)]
        ejecutar = ejecutar_algoritmo(opcion, player, characters)
    elif opcion == 7:
        characters = [AlignCharacter(100, 100), AlignCharacter(700, 100), AlignCharacter(100, 500)]
        ejecutar = ejecutar_algoritmo(opcion, player, characters)
    elif opcion == 8:
        characters = [VelocityMatchingCharacter(100, 100), VelocityMatchingCharacter(700, 100), VelocityMatchingCharacter(100, 500)]
        ejecutar = ejecutar_algoritmo(opcion, player, characters)
    elif opcion == 9:
        characters = [FaceCharacter(100, 100), FaceCharacter(700, 100), FaceCharacter(100, 500), FaceCharacter(100, 200), FaceCharacter(200, 100)]
        ejecutar = ejecutar_algoritmo(opcion, player, characters)
    elif opcion == 10:
        # Inicializar una lista vacía de personajes
        characters = []
        sub_opcion = mostrar_menu_pursue_evade()

        if sub_opcion == 'a':
            # Un personaje persigue al jugador y otro lo evade
            pursuer = PursueCharacter(100, 100)
            evader = EvadeCharacter(300, 300)
            characters.extend([pursuer, evader])  # Agregar los personajes a la lista characters
            ejecutar = lambda: [pursuer.pursue(pygame.Vector2(player.x, player.y), player.velocity),
                                evader.evade(pygame.Vector2(player.x, player.y), player.velocity),]
            
            # El jugador evade a un personaje que lo persigue
        elif sub_opcion == 'b':
            pursuer = PursueCharacter(100, 100)  # Personaje que persigue
            player = Player(WIDTH // 2, HEIGHT // 2)
            characters.append(pursuer)  # Solo agregamos el perseguidor
            ejecutar = lambda: [pursuer.pursue(pygame.Vector2(player.x, player.y), player.velocity),
                                player.flee(pygame.Vector2(pursuer.x, pursuer.y), pursuer.velocity)   ]
        else:
            print("Opción inválida, seleccionando el movimiento del jugador solamente.")
            return lambda: None
    elif opcion == 11:
        characters = [WanderCharacter(100, 100), WanderCharacter(700, 100), WanderCharacter(300, 300),
                      WanderCharacter(500, 200), WanderCharacter(400, 400)]
        ejecutar = lambda: [character.dynamic_wander() for character in characters]

    elif opcion == 12:  # Path Following
        path = [(100, 100), (700, 100), (700, 500), (100, 500)]  # Cuadrado
        characters = [PathFollowingCharacter(200, 150, path)]
        ejecutar = lambda: [character.follow_path() for character in characters]

    elif opcion == 13:
        # Collision Avoidance con 10 personajes
        characters = [CollisionAvoidanceCharacter(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)) for _ in range(10)]
        ejecutar = lambda: [(character.dynamic_wander(), character.avoid_collisions(characters)) for character in characters]
    
    else:
        characters = []
        ejecutar = lambda: None


    while True:
        handle_events()
        keys = pygame.key.get_pressed()

        # Mover al jugador
        player.move(keys, WIDTH, HEIGHT)

        # Limpiar la pantalla
        clear_screen(screen)

        # Dibujar al jugador
        player.draw(screen)

        # Ejecutar el algoritmo seleccionado para los personajes
        ejecutar()

        # Limitar el movimiento de los personajes dentro de la pantalla
        limitar_movimiento_personajes(characters)

        # Manejar la separación entre personajes y el jugador
        manejar_separacion(player, characters)

        # Dibujar a los personajes
        for character in characters:
            character.draw(screen)

        # Actualizar la pantalla
        update_screen()
        set_fps(clock, FPS)

if __name__ == "__main__":
    main()
