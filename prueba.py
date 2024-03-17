import random
import numpy as np
from PIL import Image
import pygame
import time
# Inicializamos Pygame
pygame.init()

# Definimos algunas constantes
WIDTH, HEIGHT = 800, 600   #TIENE QUE SER LAS DIMENSIONES DE LA IMAGEN
FPS = 60
RADIO = 3
MAX_BRUSHES = 100000
# Cargamos la imagen de referencia
reference_img = Image.open("george-mono.webp")
reference_array = np.array(reference_img)  # Convertimos la imagen de referencia a un array numpy
IMG_HEIGHT = reference_array.shape[0]  # Obtiene el alto de la imagen
IMG_WIDTH = reference_array.shape[1]  # Obtiene el ancho de la imagen

# Función para calcular la distancia euclidiana entre dos colores
def color_distance(color1, color2):
    return np.sqrt(np.sum((np.array(color1) - np.array(color2))**2))

# Clase para representar un agente
class Agent:
    def __init__(self):
        self.brushes = []

 # Método para generar una pincelada aleatoria en blanco y negro
    def generate_brush(self):
        current_time = int(time.time())

# Establecer la semilla para la generación de números aleatorios
        random.seed(current_time)
        x = random.randint(0, IMG_WIDTH - 1)
        y = random.randint(0, IMG_HEIGHT - 1)
        red = random.randint(0, 255)  # Escala de grises
        green = random.randint(0, 255) 
        blue = random.randint(0, 255) 
        color = (red, green, blue)
        #print(x,y)
        return (x, y), color

    # Método para generar el agente inicial
    def generate_initial(self, num_brushes=10):
        self.brushes = [self.generate_brush() for _ in range(num_brushes)]

    # Método para evaluar el agente
    def evaluate(self):
        total_distance = 0
        for brush in self.brushes:
            pos, color = brush
            if pos[1] >= IMG_HEIGHT or pos[0] >= IMG_WIDTH:
                # Si la brocha está fuera de los límites, asignamos una puntuación máxima
                total_distance += 255
            else:
                reference_color = reference_array[pos[1], pos[0]]
                total_distance += color_distance(color, reference_color)
        return total_distance

   
    # Método para generar descendencia
    def generate_offspring(self, mutation_rate=1):
        offspring = Agent()
        for brush in self.brushes:
            new_pos = (brush[0][0] + random.randint(-10*mutation_rate,10*mutation_rate), brush[0][1] + random.randint(-10*mutation_rate, 10*mutation_rate))
            new_pos = (max(0, min(IMG_WIDTH - 1, new_pos[0])), max(0, min(IMG_HEIGHT - 1, new_pos[1])))
            new_color = tuple(max(0, min(255, c + random.randint(-30, 30))) for c in brush[1])

        offspring.brushes.append((new_pos, new_color))
        return offspring 


# Creamos la ventana de visualización
screen = pygame.display.set_mode((IMG_WIDTH, IMG_HEIGHT))
pygame.display.set_caption("Pinceladas ")

# Reloj para controlar la velocidad de fotogramas
clock = pygame.time.Clock()

# Creamos varios agentes iniciales
num_agents = 200
numGenPorCiclo = 0
numCiclos = 0

# Lista para almacenar todas las pinceladas dibujadas
all_brushes = []

running = True
while running:
    # Manejo de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    if numGenPorCiclo ==0:
        numGenPorCiclo =400
        agents = [Agent() for _ in range(num_agents)]
        for agent in agents:
            agent.generate_initial()

    while numGenPorCiclo > 0:

        # Vaciamos la lista de pinceladas en cada iteración para comenzar de nuevo
        all_brushes = []

        # Dibujamos en la pantalla
        #screen.fill((255, 255, 255))
        for agent in agents:
            all_brushes.extend(agent.brushes)

        if len(all_brushes) > MAX_BRUSHES:
            #print(len(all_brushes))
            all_brushes = all_brushes[-MAX_BRUSHES:]

        for brush in all_brushes:
            pos, color = brush
            pygame.draw.circle(screen, color, pos, RADIO)  # Dibujamos un círculo en la posición con el color dado

        best_agents = sorted(agents, key=lambda x: x.evaluate())[:100]


        # Generamos descendencia para cada uno de los 4 mejores agentes
        offspring = []
        for agent in best_agents:
            offspring.extend([agent.generate_offspring() for _ in range(2)])

        # new_agents = [Agent() for _ in range(1)]
        # for agent in new_agents:
        #     agent.generate_initial()

        # offspring.extend(new_agents)
        # Reemplazamos los agentes anteriores con la nueva descendencia
        agents = offspring
        # Actualizamos la pantalla
        pygame.display.flip()

        # Controlamos la velocidad de fotogramas
        clock.tick(FPS)
        numGenPorCiclo -= 1

# Salimos de Pygame
pygame.quit()