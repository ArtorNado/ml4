import pygame
import random
import numpy as np

# /Users/artemartemev/Downloads/dbscan.py

# выдаём 1-ым те, у которых рядом 3 точки есть
# жёлтые, кто хотя бы касаются с одной зелёной точкой
# красные - кто с зелёными не касается
# закидываем жёлтые ко ближайщему зелёному

def random_color():
    return [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]

def color_for_cluster(index):
    if index >= len(cache_colors):
        # добавляем сколько нужно еще, если нужны новые цвета
        for i in range(len(cache_colors) - index + 1):
            cache_colors.append(random_color())
    return cache_colors[index]

def dist(p1, p2):
    return np.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

def give_flags():
    # находим зелёные
    for i in range(len(points)):
        neighbour = 0
        for j in range(len(points)):
            if dist(points[i], points[j]) <= distance_between_points and i != j:
                neighbour += 1
        if neighbour >= min_amount_of_points:
            flagged_points[i] = 'green'
    
    # создаём словарь ближайших жёлтых точек к зелёной точке
    # чтобы затем их добавить в кластер к зелёным
    closest_greens = {}
    # находим жёлтые
    for i in range(len(points)):
        closest_green = None
        if flagged_points[i] != 'green':
            for j in range(len(points)):
                if flagged_points[j] == 'green': 
                    if dist(points[i], points[j]) <= distance_between_points and i != j:
                        flagged_points[i] = 'yellow'
                        closest_green = points[j]
        if closest_green is not None:
            closest_greens.setdefault(closest_green, []).append(points[i])
                
    # комбинируем цвет и точку в новый массив
    full_points = [] 
    for i in range(len(points)):
        if flagged_points[i] != 'red' and flagged_points[i] != 'yellow':
            full_points.append([points[i][0], points[i][1], flagged_points[i]])

    # распределяем на кластеры
    clusters = []
    while len(full_points) > 0:
        cluster = [full_points.pop(0)]

        # добавляем точку в кластер
        for point1 in cluster:
            for point2 in full_points:
                if point1 is point2:
                    continue
                if dist(point1, point2) <= distance_between_points:
                    if point2 not in cluster:
                        full_points.remove(point2)
                        cluster.append(point2)

        # добавляем жёлтые точки в кластер
        yellows_in_cluster = []
        for point_green in cluster:
            [x, y, color] = point_green
            if (x, y) in closest_greens:
                yellows_array = closest_greens[(x,y)]
                for i in range(len(yellows_array)):
                    yellows_in_cluster.append([yellows_array[i][0], yellows_array[i][1], color])
        cluster.extend(yellows_in_cluster)
        clusters.append(cluster)

    for cluster_index, cluster in enumerate(clusters):
        color = color_for_cluster(cluster_index)
        for i in range(len(cluster)):
            cluster[i][2] = color
    return clusters

def draw_near(xCord, yCord):
    points.append((xCord,yCord))
    flagged_points.append('red')
    k = random.randint(1,4)
    d = list(range(-5*radius, -2*radius)) + list(range(2*radius, 5*radius))
    for i in range(k):
        x_new = xCord + random.choice(d) # случайный выбор из списка
        y_new = yCord + random.choice(d)
        points.append((x_new, y_new))
        flagged_points.append('red')

def draw_game():
    global flagged_points
    global cache_colors
    clusters = []
    screen = pygame.display.set_mode((1024, 840), pygame.RESIZABLE)
    screen.fill('WHITE')
    play = True
    while play:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    draw_near(event.pos[0], event.pos[1])
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                   clusters = give_flags()
            screen.fill('WHITE')
            for i in range(len(points)):
                pygame.draw.circle(screen, flagged_points[i],
                            ((points[i][0], points[i][1])), radius)
            if len(clusters) > 0:
                for cluster in clusters:
                    for i in range(len(cluster)):
                        pygame.draw.circle(screen, cluster[i][2], (cluster[i][0], cluster[i][1]), radius)
        pygame.display.update()

if __name__ == '__main__':
    points = [] # точки
    flagged_points = [] # массив цветов для точек
    radius = 10
    cache_colors = [] # массив кешированных цветов для кластеров
    # 1 - параметр, по которому можно сказать рядом человек или нет (например, расстояние между 2 точками)
    # 2 - с человеком рядом хотя бы n-человека
    distance_between_points, min_amount_of_points = 60, 3
    draw_game()