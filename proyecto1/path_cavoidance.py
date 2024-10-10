import pygame
import random
import math

# Definir colores
PATH_COLOR = (0, 0, 255)  
AVOID_COLOR = (255, 0, 255)  
LINE_COLOR = (0, 255, 0)

class PathFollowingCharacter:
    def __init__(self, x, y, path, radius=10, color=PATH_COLOR):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.path = path  # Ruta a seguir
        self.velocity = pygame.Vector2(0, 0)
        self.max_speed = 3
        self.target_index = 0  # Índice del punto objetivo en la ruta 

    def follow_path(self):
        if self.target_index >= len(self.path):
            return
        
        # Obtener el punto objetivo
        target = pygame.Vector2(self.path[self.target_index])
        direction = target - pygame.Vector2(self.x, self.y)
        
        if direction.length() < 5:  # Si está cerca del objetivo, pasar al siguiente punto
            self.target_index += 1
            if self.target_index >= len(self.path):
                self.target_index = 0  # Volver al primer punto
        
        if direction.length() > 0:
            self.velocity = direction.normalize() * self.max_speed
        
        self.update_position()

    def update_position(self):
        self.x += self.velocity.x
        self.y += self.velocity.y

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        # Dibujar el camino
        for i in range(len(self.path) - 1):
            pygame.draw.line(screen, LINE_COLOR, self.path[i], self.path[i + 1], 2)
        pygame.draw.line(screen, LINE_COLOR, self.path[-1], self.path[0], 2)  # Cerrar el cuadrado

# Clase para personajes que evitan colisiones
class CollisionAvoidanceCharacter:
    def __init__(self, x, y, radius=10, color=AVOID_COLOR):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.velocity = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize() * 3
        self.max_speed = 1
        self.avoid_radius = 30  # Radio de evitación
        self.wander_angle = 0  # Inicializar el ángulo de deambulación

    def dynamic_wander(self):
        wander_radius = 50
        wander_offset = 60
        wander_change = 20  # Reducir el cambio aleatorio para más estabilidad

        # Aplicar un cambio aleatorio al ángulo de deambulación
        self.wander_angle += random.uniform(-wander_change, wander_change)

        # Calcular el círculo en frente del personaje
        circle_center = self.velocity.normalize() * wander_offset
        
        # Desplazamiento aleatorio en el borde del círculo
        displacement = pygame.Vector2(wander_radius * math.cos(self.wander_angle),
                                      wander_radius * math.sin(self.wander_angle))

        # Calcular la nueva dirección combinando el centro del círculo y el desplazamiento
        wander_force = circle_center + displacement

        # Normalizar la nueva fuerza de wander y aplicar la velocidad resultante
        self.velocity += wander_force.normalize() * 1 # Reducir la influencia de wander_force
        
        if self.velocity.length() > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)
        
        self.update_position()

    def avoid_collisions(self, characters):
        for character in characters:
            if character != self:
                distance = pygame.Vector2(self.x - character.x, self.y - character.y).length()
                if distance < self.avoid_radius + character.radius:
                    # Evadir
                    direction = pygame.Vector2(self.x - character.x, self.y - character.y).normalize()
                    self.velocity += direction * 0.5
                    if self.velocity.length() > self.max_speed:
                        self.velocity.scale_to_length(self.max_speed)
        self.update_position()

    def update_position(self):
        self.x += self.velocity.x
        self.y += self.velocity.y

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)