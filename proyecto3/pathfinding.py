import pygame
from queue import PriorityQueue
from settings import GRID_SIZE, WIDTH, HEIGHT

def es_valido(x, y, paredes):
    rect = pygame.Rect(x, y, GRID_SIZE, GRID_SIZE)
    if rect.left < 0 or rect.right > WIDTH or rect.top < 0 or rect.bottom > HEIGHT:
        return False
    for pared in paredes:
        if rect.colliderect(pared):
            return False
    return True

def astar(start, end, paredes, tactical_points=None, disadvantageous_points=None):
    open_set = PriorityQueue()
    open_set.put((0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, end)}

    while not open_set.empty():
        _, current = open_set.get()

        if current == end:
            return reconstruir_ruta(came_from, current)

        vecinos = obtener_vecinos(current, paredes)
        for vecino in vecinos:
            tentative_g_score = g_score[current] + 1

            # Favorecer puntos ventajosos
            if tactical_points and vecino in tactical_points:
                tentative_g_score -= 2  # Reduce el costo para pasar por puntos ventajosos

            # Penalizar puntos desventajosos
            if disadvantageous_points and vecino in disadvantageous_points:
                tentative_g_score += 5  # Incrementa el costo para evitar puntos desventajosos

            if vecino not in g_score or tentative_g_score < g_score[vecino]:
                came_from[vecino] = current
                g_score[vecino] = tentative_g_score
                f_score[vecino] = tentative_g_score + heuristic(vecino, end)
                open_set.put((f_score[vecino], vecino))

    return []


def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def reconstruir_ruta(came_from, current):
    ruta = [current]
    while current in came_from:
        current = came_from[current]
        ruta.append(current)
    ruta.reverse()
    return ruta

def obtener_vecinos(celda, paredes):
    x, y = celda
    vecinos = [(x + GRID_SIZE, y), (x - GRID_SIZE, y), (x, y + GRID_SIZE), (x, y - GRID_SIZE)]
    return [vecino for vecino in vecinos if es_valido(vecino[0], vecino[1], paredes)]
