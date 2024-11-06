# Castillo de Estrategia - Juego en Pygame

Este proyecto es un juego de estrategia desarrollado en Python utilizando Pygame. El jugador explora un castillo, tratando de capturar a un personaje evasivo mientras evade ataques y enfrenta otros personajes que siguen comportamientos específicos. Cada personaje tiene una máquina de estados que añade profundidad al juego y lo hace dinámico.

## Características del Proyecto

## Estructura de Archivos

- **main.py**: Archivo principal que inicializa el juego y contiene el bucle principal.
- **settings.py**: Configuración de la pantalla, colores y constantes globales.
- **map_elements.py**: Define las paredes y nodos en el mapa.
- **characters.py**: Contiene las clases `PlayerCharacter`, `PathFindingCharacter`, `StaticAlignCharacter`, `EvasiveExplorerCharacter` y `Projectile`.
- **pathfinding.py**: Implementa el algoritmo A* para calcular rutas en el mapa.

### Mapa del Juego

- **Paredes y Límites**: El mapa está rodeado de paredes sólidas que impiden la salida de los personajes, simulando un entorno cerrado como el interior de un castillo.
- **Obstáculos Internos**: Existen barreras y obstáculos adicionales dentro del mapa que los personajes deben evadir, lo que aumenta la complejidad y promueve el uso de pathfinding.
- **Representación del Mundo y Nodos**: El mapa está dividido en regiones con nodos representativos que facilitan la navegación de los personajes con pathfinding. Esta estructura de nodos permite un sistema de movimiento más eficiente y proporciona una representación clara de los puntos clave en el castillo.

### Personajes y Comportamientos

El juego incluye varios personajes, cada uno con un árbol de decisiones que define sus comportamientos en distintas situaciones:

1. **Jugador** (`PlayerCharacter`):
   - Controlado por el usuario usando las teclas de flechas.
   - Su objetivo es capturar al `EvasiveExplorerCharacter` tres veces para ganar el juego.

2. **Personaje con Pathfinding** (`PathFindingCharacter`):
   - **Pathfinding (A*)**: Utiliza el algoritmo A* para calcular rutas hacia puntos específicos en el mapa, evitando obstáculos en el camino.
   - **Seek**: Cambia su estado a "seek" y persigue al jugador cuando este se encuentra a una cierta distancia.
   - **Aumento de Velocidad**: Si es tocado por el `EvasiveExplorerCharacter`, aumenta temporalmente su velocidad.

3. **Personaje Evasivo** (`EvasiveExplorerCharacter`):
   - **Wandering**: En estado natural, este personaje se mueve aleatoriamente dentro del castillo.
   - **Evasión**: Si el jugador se acerca, el `EvasiveExplorerCharacter` prioriza alejarse del jugador.
   - **Persecución de Pathfinding**: Cuando el jugador se aproxima demasiado, intenta dirigirse hacia el `PathFindingCharacter` mientras mantiene la evasión del jugador.

4. **Personaje Estático** (`StaticAlignCharacter`):
   - **Estático**: Estado inicial en reposo.
   - **Align y Disparo de Proyectiles**: Detecta al jugador en su campo de visión, apunta y dispara proyectiles hacia él.
   - **Movimiento Aleatorio**: Después de cierto tiempo sin atacar, se desplaza hacia un punto aleatorio del mapa y retoma su comportamiento defensivo.
   - **Estado de Alerta**: Al detectar al jugador en su rango de visión por un tiempo prolongado, incrementa la frecuencia de sus disparos.

### Objetivos y Mecánicas del Juego

- **Capturar al Explorador**: El jugador debe capturar al `EvasiveExplorerCharacter` tres veces para ganar el juego.
- **Evitar Proyectiles y el Ataque del Seek**: Si el jugador es golpeado por un proyectil o el `PathFindingCharacter` en modo seek, su posición se reinicia y el contador de capturas se restablece a cero.
- **Victoria**: Después de tres capturas exitosas del `EvasiveExplorerCharacter`, el jugador gana.

## Requisitos Cumplidos

1. **Mapa Complejo**: El mapa cuenta con paredes y obstáculos internos, lo que lo hace adecuado para los diferentes tipos de movimiento y pathfinding.
2. **Representación del Mundo**: Los nodos en el mapa representan puntos estratégicos y facilitan el cálculo de rutas, proporcionando una representación clara del entorno.
3. **Máquinas de Estados**: Cada personaje tiene al menos tres estados que definen sus comportamientos:
   - `PathFindingCharacter`: Pathfinding, Seek, Aumento de Velocidad.
   - `EvasiveExplorerCharacter`: Wandering, Evasión, Persecución de Pathfinding.
   - `StaticAlignCharacter`: Estático, Align y Disparo de Proyectiles, Movimiento Aleatorio, Estado de alerta
4. **Pathfinding Visible**: La ruta de los personajes que utilizan pathfinding puede ser visible, permitiendo al jugador observar cómo se calcula y sigue la ruta.
5. **Comportamiento de Alarma**: El `StaticAlignCharacter` entra en estado de alerta cuando el jugador permanece en su rango, aumentando la frecuencia de sus ataques.
                                 El `PathFindingCharacter` aumenta su tamaño al entrar en rango de seek.
