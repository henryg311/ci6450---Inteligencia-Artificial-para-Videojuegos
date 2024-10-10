import pygame
import random
import math

# Definir colores
KINEMATIC_COLOR = (0, 0, 255)  # Azul para los personajes cinemáticos

# Clase para representar a los personajes cinemáticos
class KinematicCharacter:
    def __init__(self, x, y, radius=10, color=KINEMATIC_COLOR):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.velocity = pygame.Vector2(0, 0)
        self.max_speed = 2
        self.wander_angle = 0

    # Dibuja el personaje en la pantalla
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    # Actualiza la posición del personaje en función de su velocidad
    def update_position(self):
        self.x += self.velocity.x
        self.y += self.velocity.y

    def kinematic_arrive(self, target_x, target_y):
        """
        Kinematic Arriving: Los personajes se acercan al jugador.
        """
        direction = pygame.Vector2(target_x - self.x, target_y - self.y)
        if direction.length() < 30:
            # Si el personaje está muy cerca del objetivo, se detiene
            self.velocity = pygame.Vector2(0, 0)
            return
        # Normalizar la dirección para moverse hacia el objetivo
        direction = direction.normalize()
        # Actualizar la velocidad para moverse hacia el objetivo
        self.velocity = direction * self.max_speed
        self.update_position()

    def kinematic_flee(self, target_x, target_y, flee_distance=100):
        """
        Kinematic Flee: Los personajes huyen del jugador hasta una distancia determinada.
        """
        direction = pygame.Vector2(self.x - target_x, self.y - target_y)
        if direction.length() > flee_distance:
            # Si el objetivo está fuera de la distancia de huida, detener el personaje
            self.velocity = pygame.Vector2(0, 0)
            return
        # Normalizar la dirección para moverse en la dirección opuesta al objetivo
        direction = direction.normalize()
        # Establecer la velocidad para huir del objetivo
        self.velocity = direction * self.max_speed
        self.update_position()

    def kinematic_wander(self):
        """
        Algoritmo Kinematic Wandering: Deambular de forma aleatoria.
        """
        # Parámetros para deambular
        wander_radius = 50  # Radio del círculo de deambular
        wander_distance = 60  # Distancia desde el personaje hacia el círculo de deambular
        wander_jitter = 0.2  # Variación aleatoria

        # Generar un cambio aleatorio en el ángulo de deambulación
        self.wander_angle += random.uniform(-1, 1) * wander_jitter

        # Calcular el círculo en frente del personaje
        circle_center = self.velocity.normalize() * wander_distance if self.velocity.length() > 0 else pygame.Vector2(1, 0) * wander_distance

        # Desplazamiento aleatorio en el borde del círculo
        displacement = pygame.Vector2(wander_radius * math.cos(self.wander_angle), wander_radius * math.sin(self.wander_angle))

        # Calcular la nueva fuerza de wander (desplazamiento sobre el círculo)
        wander_force = circle_center + displacement

        # Normalizar la fuerza y aplicarla como nueva velocidad
        self.velocity = wander_force.normalize() * self.max_speed
        self.update_position()

