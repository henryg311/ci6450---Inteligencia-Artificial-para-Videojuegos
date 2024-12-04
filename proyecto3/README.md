# Actualización del Proyecto: Inteligencia Artificial para Videojuegos

## Cambios Introducidos

### 1. Pathfinding Mejorado
- **Aceleración Dinámica**: Implementada en el movimiento del `PathFindingCharacter` para evitar cambios bruscos de dirección.
- **Evasión Temporal**: Añadida lógica para gestionar atascos en paredes o rutas bloqueadas.

### 2. Rutas Tácticas
- **Tactical Points**:
  - **Ventajosos (Verdes)**: Añadidos puntos estratégicos que favorecen el movimiento del personaje.
  - **Desventajosos (Morados)**: Añadidos puntos que penalizan el movimiento del personaje.
- **Ruta Táctica (Línea Verde)**: Calculada para priorizar el paso por puntos ventajosos y evitar puntos desventajosos.

### 3. Visualización de Rutas
- **Línea Azul**: Representa la ruta estándar calculada con A*.
- **Línea Verde**: Representa la ruta táctica optimizada por puntos estratégicos.

### 4. Ajustes de Mapa
- **Dibujo de Tactical Points**: Los puntos ventajosos y desventajosos ahora se visualizan en el mapa.

### 5. Ajustes de Personajes
- **`PathFindingCharacter`**: Añadidas funciones para calcular y dibujar rutas estándar y tácticas:
  - `calcular_ruta_tactica()`
  - `dibujar_ruta()`
  - `dibujar_ruta_tactica()`

## Archivos Modificados
- **`characters.py`**: Actualizaciones en lógica de movimiento y nuevas funciones de pathfinding.
- **`pathfinding.py`**: Integración de puntos tácticos en el algoritmo A*.
- **`map_elements.py`**: Añadidos puntos tácticos ventajosos y desventajosos.
- **`main.py`**: Integración de lógica para calcular y visualizar rutas tácticas.
- **`settings.py`**: Sin cambios significativos, pero contiene configuraciones clave de colores y dimensiones.


