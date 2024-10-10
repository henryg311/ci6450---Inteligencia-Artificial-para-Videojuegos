import pygame
import math
import random

# Definir colores
PURSUE_COLOR = (255, 0, 0) 
EVADE_COLOR = (0, 0, 255)  
WANDER_COLOR = (0, 255, 0) 

# Clase base para comportamiento dinámico
class DynamicCharacter:
    def __init__(self, x, y, radius=10, color=WANDER_COLOR):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.velocity = pygame.Vector2(0, 0)
        self.max_speed = 4
        self.orientation = 0  # Inicializar la orientación

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        # Dibujar la dirección de la orientación
        line_length = self.radius * 2
        end_x = self.x + math.cos(self.orientation) * line_length
        end_y = self.y + math.sin(self.orientation) * line_length
        pygame.draw.line(screen, (0, 0, 0), (self.x, self.y), (end_x, end_y), 2)  # Línea negra

    def update_position(self):
        self.x += self.velocity.x
        self.y += self.velocity.y
        self.look_where_you_are_going()  # Ajustar la orientación después de moverse

    def look_where_you_are_going(self):
        """
        Actualiza la orientación del personaje para que mire en la dirección en la que se mueve.
        """
        if self.velocity.length() > 0:
            self.orientation = math.atan2(self.velocity.y, self.velocity.x)

# Clase para persiguir al jugador
class PursueCharacter(DynamicCharacter):

    def __init__(self, x, y, radius=10, color=PURSUE_COLOR):
        super().__init__(x, y, radius, color)

    def pursue(self, target, target_velocity, max_prediction=1):
        """
        Algoritmo pursue: Anticipar el movimiento del objetivo (jugador) y seguirlo.
        """
        direction = target - pygame.Vector2(self.x, self.y)
        distance = direction.length()

        # Si el perseguidor está demasiado cerca, deja de predecir
        if distance < 30:
            self.velocity = pygame.Vector2(0, 0)
            return

        speed = self.velocity.length()
        prediction = max_prediction
        if speed > distance / max_prediction:
            prediction = distance / speed

        future_position = target + target_velocity * prediction

        # Aplicar Seek hacia la posición futura
        self.seek(future_position)

    def seek(self, target_position):
        """
        Algoritmo Seek: Movimiento hacia el objetivo.
        """
        direction = target_position - pygame.Vector2(self.x, self.y)
        if direction.length() > 0:
            self.velocity = direction.normalize() * self.max_speed

        self.update_position()

# Clase para evadir al perseguidor
class EvadeCharacter(DynamicCharacter):
    def __init__(self, x, y, radius=10, color=EVADE_COLOR):
        super().__init__(x, y, radius, color)

    def evade(self, pursuer, pursuer_velocity, max_prediction=1):
        """
        Algoritmo Evade: Anticipar el movimiento del perseguidor y escapar.
        """
        direction = pygame.Vector2(self.x, self.y) - pursuer
        distance = direction.length()

        # Si el personaje que evade está demasiado lejos, deja de evadir
        if distance > 150: 
            self.velocity = pygame.Vector2(0, 0)
            return

        speed = self.velocity.length()
        prediction = max_prediction
        if speed > distance / max_prediction:
            prediction = distance / speed

        future_position = pursuer + pursuer_velocity * prediction

        # Aplicar Flee desde la posición futura del perseguidor
        self.flee(future_position)

    def flee(self, target_position):
        """
        Algoritmo Flee: Movimiento para alejarse del objetivo.
        """
        direction = pygame.Vector2(self.x, self.y) - target_position
        if direction.length() > 0:
            self.velocity = direction.normalize() * self.max_speed

        self.update_position()

# Clase para el comportamiento Dynamic Wander
class WanderCharacter(DynamicCharacter):
    def __init__(self, x, y, radius=10, color=WANDER_COLOR):
        super().__init__(x, y, radius, color)
        self.wander_angle = 0

    def dynamic_wander(self):
        """
        Algoritmo Dynamic Wander: Deambular aleatoriamente.
        """
        wander_radius = 50  # Radio del círculo de deambulación
        wander_offset = 60  # Distancia desde el personaje hacia el círculo de deambulación
        wander_change = 0.8  # Variación del ángulo

        # Aplicar un cambio aleatorio al ángulo de deambulación
        self.wander_angle += random.uniform(-wander_change, wander_change)

        if self.velocity.length() == 0:
            self.velocity = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize() * self.max_speed

        # Calcular el círculo en frente del personaje
        circle_center = self.velocity.normalize() * wander_offset
        displacement = pygame.Vector2(wander_radius * math.cos(self.wander_angle), wander_radius * math.sin(self.wander_angle))

        # Calcular la nueva velocidad como una combinación de las dos
        self.velocity = circle_center + displacement
        if self.velocity.length() > self.max_speed:
            self.velocity = self.velocity.normalize() * self.max_speed

        self.update_position()
