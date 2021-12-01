import random
import pygame
import numpy as np

from sklearn.svm import SVC

def generate_points(clusters_count, count_points_in_cluster):
    data = []
    radius = 30
    for classNum in range(clusters_count):
        center_x, center_y = random.randint(radius, width - radius), random.randint(radius, height - radius)
        for rowNum in range(count_points_in_cluster):
            data.append([[random.gauss(center_x, radius / 2), random.gauss(center_y, radius / 2)], classNum])
    return data

def get_line_coordinates(svc):
    weights = svc.coef_[0]
    rotation_coef = -weights[0] / weights[1]
    x_first = 0
    x_last = width
    y_first = 0

    x_positions = np.array([x_first, x_last])
    y_positions = rotation_coef * x_positions - (svc.intercept_[y_first]) / weights[1]

    return [x_positions[0], y_positions[0]], [x_positions[-1], y_positions[-1]]

def draw_pygame():
    screen = pygame.display.set_mode((width, height))
    screen.fill('white')

    play = True
    while play:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                position = list(event.pos)
                cls = svc.predict([position])[0]
                points.append([position, cls])

            if event.type == pygame.QUIT:
                play = False

        for point in points:
            pygame.draw.circle(screen, colors[point[1]], point[0], 3)

        pygame.draw.line(screen, 'red', p1, p2, 1)

        pygame.display.update()


if __name__ == '__main__':
    width, height = 800, 800
    points = generate_points(2, 50)
    colors = {0: 'black', 1: 'purple'}

    points_coordinates = np.array(list(map(lambda x: x[0], points)))
    points_belong_to_cluster = np.array(list(map(lambda x: x[1], points)))

    svc = SVC(kernel='linear')
    svc.fit(points_coordinates, points_belong_to_cluster)

    p1, p2 = get_line_coordinates(svc)

    draw_pygame()