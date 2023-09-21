import matplotlib.pyplot as plt

# Чтение точек из файла
def graph():
    points = []
    with open('output.txt', 'r') as file:
        for line in file:
            x, y = map(int, line.strip().split())
            points.append((x, y))

    # Извлечение координат x и y
    x_coords = [point[0] for point in points]
    y_coords = [point[1] for point in points]

    # Построение графика
    for i in range(len(x_coords) - 1):
        plt.plot([x_coords[i], x_coords[i + 1]], [y_coords[i], y_coords[i + 1]], marker='o', color='blue')

    # Подсветка точки (1, 2) красным цветом
    plt.plot(1, 2, marker='o', color='red')

    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Последовательность точек')
    plt.grid(True)
    plt.show()
