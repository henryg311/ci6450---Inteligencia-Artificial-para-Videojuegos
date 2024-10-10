import pygame

# Definir colores
DYNAMIC_COLOR = (255, 0, 0)  # Rojo para los personajes dinámicos

# Clase base para personajes dinámicos
class DynamicCharacter:

    #Inicialización de un personaje dinámico con su posición, radio, color y atributos de movimiento.
    def __init__(self, x, y, radius=10, color=DYNAMIC_COLOR):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.velocity = pygame.Vector2(0, 0)
        self.acceleration = pygame.Vector2(0, 0)
        self.max_speed = 4
        self.max_acceleration = 0.5

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    def update_position(self):
        # Sumar aceleración a la velocidad
        self.velocity += self.acceleration
        # Limitar la velocidad a la máxima permitida
        if self.velocity.length() > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)
        # Actualizar la posición del personaje
        self.x += self.velocity.x
        self.y += self.velocity.y

    def dynamic_seek(self, target_x, target_y):
        """
        Algoritmo Dynamic Seek: El personaje se mueve dinámicamente hacia un objetivo.
        """
        direction = pygame.Vector2(target_x - self.x, target_y - self.y)
        if direction.length() == 0:
            # Si el objetivo está en la misma posición, detener la aceleración
            self.acceleration = pygame.Vector2(0, 0)
            return
        # Normalizar la dirección y multiplicar por la aceleración máxima
        direction = direction.normalize() * self.max_acceleration
        self.acceleration = direction
        self.update_position()

    def dynamic_flee(self, target_x, target_y, flee_distance=150):
        """
        Algoritmo Dynamic Flee: El personaje huye de un objetivo si está dentro de una distancia determinada.
        """
        direction = pygame.Vector2(self.x - target_x, self.y - target_y)
        if direction.length() > flee_distance:
            # Si el objetivo está fuera del radio de huida, no acelerar
            self.acceleration = pygame.Vector2(0, 0)
            return
        # Normalizar la dirección y multiplicar por la aceleración máxima
        direction = direction.normalize() * self.max_acceleration
        self.acceleration = direction
        self.update_position()

    def dynamic_arrive(self, target_x, target_y, slow_radius=100):
        """
        Algoritmo Dynamic Arrive: El personaje desacelera gradualmente al acercarse al objetivo.
        """
        direction = pygame.Vector2(target_x - self.x, target_y - self.y)
        distance = direction.length()
        if distance < 1:
            # Si el personaje está muy cerca del objetivo, detener la aceleración
            self.acceleration = pygame.Vector2(0, 0)
            return
         # Ajustar la velocidad en función de la distancia al objetivo
        if distance < slow_radius:
            desired_speed = self.max_speed * (distance / slow_radius)
        else:
            desired_speed = self.max_speed
        # Calcular la aceleración basada en la velocidad deseada
        direction = direction.normalize() * (desired_speed - self.velocity.length())
        self.acceleration = direction
        self.update_position()
