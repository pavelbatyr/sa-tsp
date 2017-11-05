import random
import copy
import math
import sys
import matplotlib.pyplot as plt

n = 100         # number of cities
t_start = 50    # start temperature
t_end = 0.5     # end temperature
steps = 1000    # steps at given temperature
alpha = 0.98    # temperature reduction coefficient


class Solution:
    def __init__(self):
        self.plan = list(range(n))
        self.plan.append(0)
        self.mutate()
        self.fitness = sys.maxsize

    def mutate(self):
        # inverting randomly selected subpath of random length
        subpath_start = random.randrange(1, n-1)
        subpath_end = random.randrange(subpath_start+2, n+1)
        plan_copy = self.plan[subpath_start:subpath_end]
        plan_copy = plan_copy[::-1]
        self.plan[subpath_start:subpath_end] = plan_copy

    def calc_fitness(self):
        self.fitness = sum([distances[self.plan[i]][self.plan[i + 1]] for i in range(n)])


def make_coord():
    return random.uniform(0, 1000)


def init_plot():
    plt.xlim(1000)
    plt.ylim(1000)
    plt.ion()


def draw_plot():
    x_values = [coords[best.plan[i]][0] for i in range(n + 1)]
    y_values = [coords[best.plan[i]][1] for i in range(n + 1)]
    plt.clf()
    plt.plot(x_values, y_values, 'o-')
    # show start/end city in red color
    plt.plot(x_values[0], y_values[0], 'ro')
    plt.pause(0.001)


coords = [tuple(make_coord() for _ in range(2)) for _ in range(n)]  # cities coordinates

distances = [[_ for _ in range(n)] for _ in range(n)]  # distances matrix between cities

for row in range(n):  # Euclidean distances
    for col in range(n):
        distances[row][col] = math.sqrt(sum((coords[row][i] - coords[col][i]) ** 2 for i in range(2)))

current = Solution()
current.calc_fitness()
working = copy.deepcopy(current)
best = copy.deepcopy(current)
t = t_start

init_plot()

while t > t_end:
    for _ in range(steps):
        f_new = False
        working.mutate()
        working.calc_fitness()
        if working.fitness <= current.fitness:
            f_new = True
        else:
            delta = working.fitness - current.fitness
            p = math.exp(-delta / t)
            if p > random.random():
                f_new = True
        if f_new:
            current = copy.deepcopy(working)
            if current.fitness < best.fitness:
                best = copy.deepcopy(current)
        else:
            working = copy.deepcopy(current)
    print('temperature {:5.2f}, fitness {:10.4f}'.format(t, best.fitness))
    draw_plot()
    t *= alpha
print("route: ", best.plan)

input("Press <Enter> to exit")
