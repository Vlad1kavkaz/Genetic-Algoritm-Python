import random
import math
import time
from graph import graph

POPULATION_SIZE = 10
NUM_GENERATIONS = 10000
MUTATION_RATE = 0.03
NUM_CITIES = 20

# Чтение точек из текстового файла
def read_points_from_file(filename):
    points = []
    with open(filename, 'r') as file:
        for line in file:
            x, y = line.strip().split()
            points.append((int(x), int(y)))
    return points

# Расчет расстояния между двумя точками
def distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


# Расчет длины пути для данного порядка точек
def path_length(points_order, points):
    total_distance = 0
    for i in range(len(points_order) - 1):
        point1 = points[points_order[i]]
        point2 = points[points_order[i + 1]]
        total_distance += distance(point1, point2)
    # Возвращение к начальной точке
    total_distance += distance(points[points_order[-1]], points[points_order[0]])
    return total_distance


# Создание случайной популяции
def create_population():
    population = []
    for _ in range(POPULATION_SIZE):
        individual = list(range(NUM_CITIES))
        random.shuffle(individual)
        population.append(individual)
    return population


# Выбор лучших особей
def selection(population, points):
    fitness_scores = [1 / path_length(individual, points) for individual in population]
    total_fitness = sum(fitness_scores)
    probabilities = [score / total_fitness for score in fitness_scores]
    selected_indices = random.choices(range(POPULATION_SIZE), probabilities, k=2)
    return [population[index] for index in selected_indices]


# Кроссовер (скрещивание) двух родителей для создания нового потомка
def crossover(parent1, parent2):
    size = len(parent1)
    i, j = sorted(random.sample(range(size), 2))
    child1 = parent1[i:j]
    child2 = [item for item in parent2 if item not in child1]
    return child2[:i] + child1 + child2[i:]


# Мутация - случайная перестановка двух элементов
def mutation(individual):
    i, j = random.sample(range(len(individual)), 2)
    individual[i], individual[j] = individual[j], individual[i]
    return individual


# Генетический алгоритм
def genetic_algorithm(points):
    population = create_population()
    best_path = None
    best_distance = float('inf')

    for _ in range(NUM_GENERATIONS):
        selected_population = [selection(population, points) for _ in range(POPULATION_SIZE)]
        new_population = []
        for parents in selected_population:
            child = crossover(parents[0], parents[1])
            if random.random() < MUTATION_RATE:
                child = mutation(child)
            new_population.append(child)
        population = new_population

        current_best_path = min(population, key=lambda ind: path_length(ind, points))
        current_best_distance = path_length(current_best_path, points)
        if current_best_distance < best_distance:
            best_path = current_best_path
            best_distance = current_best_distance

    # Возвращение к начальной точке
    best_path.append(best_path[0])


    return best_path, best_distance


# Вывод результата в файл и на консоль
def print_result(points, best_path, best_distance):
    best_path_coordinates = [points[i] for i in best_path]

    with open('output.txt', 'w') as file:

        for point in best_path_coordinates:
            file.write(f"{point[0]} {point[1]}\n")

    print("Best path:")
    for i in range(len(best_path_coordinates) - 1):
        print(f"({best_path_coordinates[i][0]}, {best_path_coordinates[i][1]}) -> ", end='')
    print(f"({best_path_coordinates[-1][0]}, {best_path_coordinates[-1][1]})")
    print(f"Best distance: {best_distance}")

    # Применение локального поиска 2-opt для улучшения пути


def local_search_2opt(points, path):
    while True:
        improved = False
        for i in range(1, len(path) - 2):
            for j in range(i + 1, len(path)):
                if j - i == 1:
                    continue
                new_path = path[:]
                new_path[i:j] = reversed(path[i:j])
                new_distance = path_length(new_path, points)
                if new_distance < path_length(path, points):
                    path = new_path
                    improved = True
        if not improved:
            break
    return path

    # Пример использования

def main():
    points = read_points_from_file('points.txt')

    best_path, best_distance = genetic_algorithm(points)

    best_path = local_search_2opt(points, best_path)
    print_result(points, best_path, best_distance)


if __name__ == '__main__':
    start_time = time.time()
    main()
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time} seconds")
    graph()
