import pygame
import math

# Definir colores
ALIGN_COLOR = (255, 165, 0)  # Naranja para personajes que usan Align
VELOCITY_MATCH_COLOR = (0, 128, 128)  # Verde azulado para Velocity Matching
FACE_COLOR = (128, 0, 128)  # Morado para Face

# Clase base para personajes con alineación
class AlignCharacter:
    def __init__(self, x, y, radius=10, color=ALIGN_COLOR):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.orientation = 0  # Ángulo de orientación inicial (radianes)
        self.rotation_speed = 0.1  # Velocidad de rotación
        self.velocity = pygame.Vector2(0, 0)
        self.max_speed = 2

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        # Dibujar una línea indicando la dirección de la orientación
        line_length = self.radius * 2
        end_x = self.x + math.cos(self.orientation) * line_length
        end_y = self.y + math.sin(self.orientation) * line_length
        pygame.draw.line(screen, (0, 0, 0), (self.x, self.y), (end_x, end_y), 2)

    def update_position(self):
        self.x += self.velocity.x
        self.y += self.velocity.y

    def align(self, player_velocity):
        """
        Algoritmo Align: Ajustar la orientación del personaje para que coincida con la dirección de movimiento del jugador.
        """
        if player_velocity.length() > 0:  # Solo si el jugador tiene una velocidad no nula
            # Calcular la orientación objetivo en función de la dirección del movimiento del jugador
            target_orientation = math.atan2(player_velocity.y, player_velocity.x)

            # Calcular la diferencia de orientación
            rotation = target_orientation - self.orientation

            # Ajustar la rotación en función de la velocidad de rotación
            if abs(rotation) > self.rotation_speed:
                rotation = self.rotation_speed if rotation > 0 else -self.rotation_speed

            # Aplicar la rotación calculada
            self.orientation += rotation

    def update_position(self):
        self.x += self.velocity.x
        self.y += self.velocity.y


# Clase para personajes con Velocity Matching
class VelocityMatchingCharacter(AlignCharacter):
    def __init__(self, x, y, radius=10, color=VELOCITY_MATCH_COLOR):
        super().__init__(x, y, radius, color)
        self.max_speed = 4

    def velocity_matching(self, target_velocity):
        """
        Algoritmo Velocity Matching: Ajustar la velocidad del personaje para igualar la del objetivo.
        """
        # Verificar que la velocidad del objetivo no sea cero
        if target_velocity.length() == 0:
            return  # Si la velocidad del jugador es cero, no hacemos nada.

        # Calcular la diferencia de velocidad
        velocity_difference = target_velocity - self.velocity
        
        # Aplicar la diferencia con una tasa de ajuste más rápida
        self.velocity += velocity_difference * 0.05  # Aumentar la tasa de ajuste

        # Limitar la velocidad para que no exceda la velocidad máxima del personaje
        if self.velocity.length() > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)

        # Actualizar la posición en función de la nueva velocidad
        self.update_position()

# Clase para personajes que siempre miran al jugador
class FaceCharacter(AlignCharacter):
    def __init__(self, x, y, radius=10, color=FACE_COLOR):
        super().__init__(x, y, radius, color)

    def face(self, target_x, target_y):
        """
        Algoritmo Face: Hacer que el personaje mire hacia un objetivo.
        """
        # Calcular el ángulo hacia el objetivo
        direction = pygame.Vector2(target_x - self.x, target_y - self.y)
        if direction.length() > 0:
            self.orientation = math.atan2(direction.y, direction.x)

        self.update_position()
