import pygame
from settings import GREEN, BLUE, GRID_SIZE
from map_elements import walls
from pathfinding import astar
import math
import time
from settings import BLACK, HEIGHT, WIDTH
import random


class PlayerCharacter:
    def __init__(self, x, y, sprite):
        self.x = x
        self.y = y
        self.sprite = sprite
        self.radio = 15
        self.color = GREEN
        self.velocidad = 5

    def mover(self, teclas, paredes):
        if teclas[pygame.K_LEFT]:
            self.x -= self.velocidad
            if self.colisiona_con_paredes(paredes):
                self.x += self.velocidad
        if teclas[pygame.K_RIGHT]:
            self.x += self.velocidad
            if self.colisiona_con_paredes(paredes):
                self.x -= self.velocidad
        if teclas[pygame.K_UP]:
            self.y -= self.velocidad
            if self.colisiona_con_paredes(paredes):
                self.y += self.velocidad
        if teclas[pygame.K_DOWN]:
            self.y += self.velocidad
            if self.colisiona_con_paredes(paredes):
                self.y -= self.velocidad

    def colisiona_con_paredes(self, paredes):
        rect = pygame.Rect(self.x - self.radio, self.y - self.radio, self.radio * 2, self.radio * 2)
        for pared in paredes:
            if rect.colliderect(pared):
                return True
        return False

    def dibujar(self, screen):
        screen.blit(self.sprite, (self.x - self.sprite.get_width() // 2, self.y - self.sprite.get_height() // 2))

class PathFindingCharacter:
    def __init__(self, x, y, path, sprite, seek_distance=180):
        self.x = x
        self.y = y
        self.original_sprite = sprite
        self.enlarged_sprite = pygame.transform.scale(sprite, (int(sprite.get_width() * 1.5), int(sprite.get_height() * 1.5))) 
        self.radio = 10
        self.color = BLUE
        self.velocidad = 2
        self.aceleracion = 0.1  # Aceleración para suavizar el cambio
        self.velocidad_actual = pygame.Vector2(0, 0)  # Velocidad inicial
        self.path = path
        self.target_index = 0
        self.ruta = []
        self.current_target = None
        self.calcular_ruta(walls)
        self.seek_distance = seek_distance
        self.evasion_timer = 0
        self.seeking = False
        self.failed_attempts = 0

    def calcular_ruta(self, paredes):
        if self.target_index >= len(self.path):
            self.target_index = 0

        start = (self.x // GRID_SIZE * GRID_SIZE, self.y // GRID_SIZE * GRID_SIZE)
        end = (self.path[self.target_index][0] // GRID_SIZE * GRID_SIZE, self.path[self.target_index][1] // GRID_SIZE * GRID_SIZE)
        self.ruta = astar(start, end, paredes)
        if self.ruta:
            self.current_target = self.ruta.pop(0)
        else:
            self.current_target = None

    def mover(self, paredes, jugador):
        # Calcular la distancia al jugador
        distancia_al_jugador = math.hypot(jugador.x - self.x, jugador.y - self.y)

        if distancia_al_jugador < self.seek_distance:
            # Si el jugador está cerca, hacer `dynamic seek` y agrandar el sprite
            self.seeking = True
            self.sprite = self.enlarged_sprite  # Cambia al sprite agrandado
            self.dynamic_seek(jugador, paredes)
        else:
            # Si el jugador está lejos, seguir el pathfinding y restaurar el tamaño original
            self.seeking = False
            self.sprite = self.original_sprite  # Restaura el sprite original
            self.seguir_ruta(paredes)

    def seguir_ruta(self, paredes):
        if not self.ruta and not self.current_target:
            self.target_index += 1
            self.calcular_ruta(paredes)

        if self.current_target:
            target_x, target_y = self.current_target
            objetivo = pygame.Vector2(target_x, target_y)
            posicion_actual = pygame.Vector2(self.x, self.y)

            # Calcular dirección deseada hacia el objetivo
            direccion_deseada = objetivo - posicion_actual
            distancia = direccion_deseada.length()

            if distancia < self.velocidad:
                # Si llega al punto actual de la ruta, toma el siguiente
                self.x, self.y = target_x, target_y
                if self.ruta:
                    self.current_target = self.ruta.pop(0)
                else:
                    self.current_target = None
                    self.target_index += 1
                    self.calcular_ruta(paredes)
                self.failed_attempts = 0  # Reinicia el contador si avanza
            else:
                # Normalizar dirección deseada y escalarla por la aceleración
                direccion_deseada = direccion_deseada.normalize() * self.velocidad
                # Ajustar la velocidad actual hacia la dirección deseada
                self.velocidad_actual += (direccion_deseada - self.velocidad_actual) * self.aceleracion

                # Calcular nueva posición
                nueva_x = self.x + self.velocidad_actual.x
                nueva_y = self.y + self.velocidad_actual.y

                # Verificar colisiones antes de actualizar la posición
                if not self.colisiona_con_paredes(nueva_x, nueva_y, paredes):
                    self.x = nueva_x
                    self.y = nueva_y
                    self.failed_attempts = 0
                else:
                    # Si no puede moverse, incrementa los intentos fallidos
                    self.failed_attempts += 1
                    if self.failed_attempts > 3:  # Si se queda atascado
                        self.aplicar_evasion_temporal(paredes)
                    elif self.failed_attempts > 100:  # Recalcular ruta tras múltiples fallos
                        self.calcular_ruta(paredes)
                        self.failed_attempts = 0
    
    def aplicar_evasion_temporal(self, paredes):
        # Generar una dirección aleatoria para salir del atasco
        angulo_aleatorio = random.uniform(0, 360)
        direccion_evasion = pygame.Vector2(
            math.cos(math.radians(angulo_aleatorio)),
            math.sin(math.radians(angulo_aleatorio))
        ).normalize()

        # Intentar moverse en la dirección de evasión
        nueva_x = self.x + direccion_evasion.x * self.velocidad
        nueva_y = self.y + direccion_evasion.y * self.velocidad

        if not self.colisiona_con_paredes(nueva_x, nueva_y, paredes):
            self.x = nueva_x
            self.y = nueva_y
            self.failed_attempts = 0  # Restablecer intentos fallidos
        else:
            # Si no puede moverse en esta dirección, vuelve a intentarlo en otro frame
            self.failed_attempts += 1

    def dynamic_seek(self, jugador, paredes):
        # Calcular la dirección hacia el jugador
        base_direction = pygame.Vector2(jugador.x - self.x, jugador.y - self.y).normalize()

        # Si el temporizador de evasión está activo, moverse perpendicularmente
        if self.evasion_timer > 0:
            perpendicular_direction = base_direction.rotate(90)  # Rotación de 90 grados
            if self.intentar_mover(perpendicular_direction, paredes):
                self.evasion_timer -= 1  # Reducir el temporizador de evasión
            else:
                # Si no puede moverse perpendicularmente, reiniciar el temporizador
                self.evasion_timer = 0
        else:
            # Intentar moverse en dirección hacia el jugador
            if not self.intentar_mover(base_direction, paredes):
                # Si no puede avanzar, activar temporizador de evasión
                self.evasion_timer = 10

    def intentar_mover(self, direction, paredes):
        nueva_x = self.x + direction.x * self.velocidad
        nueva_y = self.y + direction.y * self.velocidad
        if not self.colisiona_con_paredes(nueva_x, nueva_y, paredes):
            self.x = nueva_x
            self.y = nueva_y
            return True
        return False

    def colisiona_con_paredes(self, x, y, paredes):
        rect = pygame.Rect(x - self.radio, y - self.radio, self.radio * 2, self.radio * 2)
        for pared in paredes:
            if rect.colliderect(pared):
                return True
        return False
    
    def calcular_ruta_tactica(self, paredes, tactical_points, disadvantageous_points):
        if self.target_index >= len(self.path):
            self.target_index = 0

        start = (self.x // GRID_SIZE * GRID_SIZE, self.y // GRID_SIZE * GRID_SIZE)
        end = (self.path[self.target_index][0] // GRID_SIZE * GRID_SIZE, self.path[self.target_index][1] // GRID_SIZE * GRID_SIZE)

        ruta_completa = []
        current_position = start

        for tactical_point in sorted(
            tactical_points,
            key=lambda point: math.hypot(point[0] - current_position[0], point[1] - current_position[1])
        ):
            if math.hypot(current_position[0] - tactical_point[0], current_position[1] - tactical_point[1]) <= GRID_SIZE * 3:
                sub_ruta = astar(current_position, tactical_point, paredes, tactical_points, disadvantageous_points)
                if sub_ruta:
                    ruta_completa += sub_ruta
                    current_position = tactical_point

        final_ruta = astar(current_position, end, paredes, tactical_points, disadvantageous_points)
        ruta_completa += final_ruta
        self.ruta_tactica = ruta_completa

    def dibujar(self, screen):
        screen.blit(self.sprite, (self.x - self.sprite.get_width() // 2, self.y - self.sprite.get_height() // 2))

    def dibujar_ruta(self, screen):
        if self.ruta:
            puntos = [(self.x, self.y)] + self.ruta  # Inicia con la posición actual y sigue la ruta
            pygame.draw.lines(screen, (0, 0, 255), False, puntos, 2)  # Azul, sin cerrar la línea, grosor 2
    
    def dibujar_ruta_tactica(self, screen):
        if hasattr(self, 'ruta_tactica') and self.ruta_tactica:
            puntos = [(self.x, self.y)] + self.ruta_tactica  # Inicia con la posición actual y sigue la ruta táctica
            pygame.draw.lines(screen, (0, 255, 0), False, puntos, 2)  # Verde, sin cerrar la línea, grosor 2

class StaticAlignCharacter:
    def __init__(self, x, y, sprite):
        self.x = x
        self.y = y
        self.sprite = sprite
        self.radio = 10
        self.color = BLACK
        self.last_shot_time = time.time()
        self.proyectiles = []
        self.move_timer = time.time()  # Temporizador para movimiento
        self.is_moving = False
        self.move_target = None 
        self.alert_time = 0 
        self.alert_threshold = 3  
        self.normal_shot_interval = 3  
        self.alert_shot_interval = 1.5 

    def apuntar_y_disparar(self, jugador, paredes):
        dx = jugador.x - self.x
        dy = jugador.y - self.y
        distancia = math.hypot(dx, dy)

        # Comprobar si el jugador está en rango
        if distancia < 300:
            self.alert_time += time.time() - self.last_shot_time
            interval = self.alert_shot_interval if self.alert_time >= self.alert_threshold else self.normal_shot_interval
            if time.time() - self.last_shot_time >= interval:
                angulo = math.atan2(dy, dx)
                self.disparar_proyectil(angulo)
                self.last_shot_time = time.time()
            self.move_timer = time.time()
        else:

            self.alert_time = 0

    def disparar_proyectil(self, angulo):
        proyectil = Projectile(self.x, self.y, angulo)
        self.proyectiles.append(proyectil)

    def actualizar_proyectiles(self, paredes):
        for proyectil in self.proyectiles[:]:
            proyectil.mover(paredes)
            if proyectil.colisiona_con_paredes(paredes):
                self.proyectiles.remove(proyectil)

    def mover_a_punto_aleatorio(self):
        target_x = random.randint(50, WIDTH - 50)
        target_y = random.randint(50, HEIGHT - 50)
        self.move_target = (target_x, target_y)
        self.is_moving = True

    def mover(self):
        # Movimiento sin colisiones
        if self.is_moving and self.move_target:
            target_x, target_y = self.move_target
            direction = pygame.Vector2(target_x - self.x, target_y - self.y).normalize()
            self.x += direction.x * 2  # Ajusta la velocidad si es necesario
            self.y += direction.y * 2

            # Si alcanza el punto objetivo, detiene el movimiento
            if math.hypot(target_x - self.x, target_y - self.y) < 5:
                self.is_moving = False
                self.move_timer = time.time()  # Reinicia el temporizador

    def comportamiento_temporal(self):
        if not self.is_moving and time.time() - self.move_timer >= 6:
            self.mover_a_punto_aleatorio()

    def dibujar(self, screen):
        screen.blit(self.sprite, (self.x - self.sprite.get_width() // 2, self.y - self.sprite.get_height() // 2))
        for proyectil in self.proyectiles:
            proyectil.dibujar(screen)


class Projectile:
    def __init__(self, x, y, angulo):
        self.x = x
        self.y = y
        self.velocidad = 5
        self.angulo = angulo
        self.radio = 5
        self.color = BLACK

    def mover(self, paredes):
        dx = math.cos(self.angulo) * self.velocidad
        dy = math.sin(self.angulo) * self.velocidad
        nueva_x = self.x + dx
        nueva_y = self.y + dy
        # Mueve el proyectil si no colisiona
        if not self.colisiona_con_paredes(paredes):
            self.x = nueva_x
            self.y = nueva_y

    def colisiona_con_paredes(self, paredes):
        rect = pygame.Rect(self.x - self.radio, self.y - self.radio, self.radio * 2, self.radio * 2)
        for pared in paredes:
            if rect.colliderect(pared):
                return True
        return False

    def dibujar(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radio)


class EvasiveExplorerCharacter:
    def __init__(self, x, y, target_character, sprite):
        self.x = x
        self.y = y
        self.sprite = sprite
        self.radio = 10
        self.color = GREEN
        self.velocidad = 2
        self.target_character = target_character  # Personaje de pathfinding
        self.escape_distance = 190  # Distancia a la que se activa la evasión
        self.wandering_direction = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize()
        self.wandering_timer = 0

    def mover(self, jugador, paredes):
        # Calcular la distancia al jugador
        dx = jugador.x - self.x
        dy = jugador.y - self.y
        distancia = math.hypot(dx, dy)

        if distancia < self.escape_distance:
            # Si el jugador está cerca, intentar moverse hacia el personaje de pathfinding mientras evade
            self.evadir_jugador_hacia_target(jugador, paredes)
        else:
            # Si el jugador no está cerca, hacer wandering
            self.wandering(paredes)
    
    def tocar_pathfinding(self):
        dx = self.target_character.x - self.x
        dy = self.target_character.y - self.y
        distancia = math.hypot(dx, dy)
        return distancia < (self.radio + self.target_character.radio)

    def evadir_jugador_hacia_target(self, jugador, paredes):
        # Dirección hacia el personaje de pathfinding
        target_dx = self.target_character.x - self.x
        target_dy = self.target_character.y - self.y
        direction_to_target = pygame.Vector2(target_dx, target_dy).normalize()

        # Intentar varias rotaciones alrededor de la dirección hacia el personaje de pathfinding
        for angle_offset in range(0, 360, 15):
            adjusted_direction = direction_to_target.rotate(angle_offset)
            if self.intentar_mover(adjusted_direction, paredes):
                return

    def seguir_ruta(self, paredes):
        if not self.ruta and not self.current_target:
            self.target_index += 1
            self.calcular_ruta(paredes)

        if self.current_target:
            target_x, target_y = self.current_target
            direction = pygame.Vector2(target_x - self.x, target_y - self.y)
            if direction.length() < self.velocidad:
                # Si llega al punto actual de la ruta, toma el siguiente
                self.x, self.y = target_x, target_y
                if self.ruta:
                    self.current_target = self.ruta.pop(0)
                else:
                    self.current_target = None
                    self.target_index += 1
                    self.calcular_ruta(paredes)
            else:
                # Intenta moverse en la dirección del objetivo
                if not self.intentar_mover(direction.normalize(), paredes):
                    # Si no puede moverse, recalcula la ruta
                    self.calcular_ruta(paredes)

    def intentar_mover(self, direction, paredes):
        nueva_x = self.x + direction.x * self.velocidad
        nueva_y = self.y + direction.y * self.velocidad
        if not self.colisiona_con_paredes(nueva_x, nueva_y, paredes):
            self.x = nueva_x
            self.y = nueva_y
            return True
        return False

    def wandering(self, paredes):
        # Cambiar la dirección de wandering aleatoriamente cada cierto tiempo
        if self.wandering_timer <= 0:
            self.wandering_direction = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize()
            self.wandering_timer = 50  # Cambia la dirección de wandering cada 50 frames

        # Mover en la dirección de wandering
        if not self.intentar_mover(self.wandering_direction, paredes):
            # Si hay colisión, ajustar la dirección y reiniciar el temporizador de wandering
            self.wandering_direction = self.wandering_direction.rotate(90).normalize()
            self.wandering_timer = 100

        # Reducir el temporizador de wandering
        self.wandering_timer -= 1

    def colisiona_con_paredes(self, x, y, paredes):
        rect = pygame.Rect(x - self.radio, y - self.radio, self.radio * 2, self.radio * 2)
        for pared in paredes:
            if rect.colliderect(pared):
                return True
        return False

    def dibujar(self, screen):
        screen.blit(self.sprite, (self.x - self.sprite.get_width() // 2, self.y - self.sprite.get_height() // 2))