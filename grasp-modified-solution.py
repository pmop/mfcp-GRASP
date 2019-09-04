from random import randint
from math import sqrt
from copy import deepcopy
import pygame
import threading
import time

mlock = threading.Condition()
GSOL = []
GBOUNDS = []
GPARTIAL = []
GRUN = True


def cartesian_distance_point_to_point(A, B):
    x, y = A[0], A[1]
    sx, sy = B[0], B[1]
    return sqrt((sx - x) ** 2 + (sy - y) ** 2)


def generate_random_points(lower, upper, p):
    points = []
    for _ in range(p):
        x = randint(lower[0], upper[0])
        y = randint(lower[1], upper[1])
        points.append([x, y])
    points.sort(key=lambda k: k[0] + k[1])
    return points


def solution_fully_covers(demand_points, facility_points, radius):
    covered = 0
    for point in demand_points:
        for facility in facility_points:
            if cartesian_distance_point_to_point(point, facility) <= radius:
                covered = covered + 1
    return len(demand_points) == covered


# Input: the set of tuples of demand points and one tuple facility
# Output: the set of indexes of demand points covered by facility
def points_facility_covers(demand_points, facility, radius):
    output = []
    for i in range(len(demand_points)):
        point = demand_points[i]
        if cartesian_distance_point_to_point(point, facility) <= radius:
            output.append(i)
    return output


def heightmost_demand(demand_points):
    heightmost = 0
    for demand in demand_points:
        if demand[1] > heightmost:
            heightmost = demand[1]
    return heightmost


def get_bounds(demand_points):
    minX = demand_points[0][0]
    maxX = 0
    minY = demand_points[0][1]
    maxY = 0
    for point in demand_points:
        x, y = point[0], point[1]
        if x > maxX:
            maxX = x
        if y > maxY:
            maxY = y
        if x < minX:
            minX = x
        if y < minY:
            minY = y
    lower = [minX, minY]
    upper = [maxX, maxY]
    return lower, upper


def vec_scalar_sum(vec, s):
    for i in range(len(vec)):
        vec[i] += s
    return vec


def greedy_random_solution(demand_points, radius, p):
    global GRUN
    global GSOL
    global GBOUNDS

    sol = []
    uncovered_demand = [i for i in demand_points]
    while GRUN and len(uncovered_demand) > 0:
        sol_candidates = []
        lower, upper = get_bounds(uncovered_demand)

        step_solution_covered_points = []
        sol_ = generate_random_points(lower, upper, p)
        for facility in sol_:
            # points_covered is a list of indexes of uncovered_demand that are now covered
            points_covered = points_facility_covers(uncovered_demand, facility, radius)
            if len(points_covered) > 0:
                sol_candidates.append(facility)
                # remove covered points from uncovered demand
                uncovered = []
                for index in range(len(uncovered_demand)):
                    if index in points_covered:
                        points_covered.remove(index)
                    else:
                        uncovered.append(uncovered_demand[index])
                uncovered_demand = uncovered

        sol = sol + sol_candidates
        p = len(uncovered_demand)  # generate at most p facilities
        mlock.acquire()
        GSOL = deepcopy(sol)
        GBOUNDS = deepcopy([lower, upper])
        mlock.release()
        time.sleep(1)

    return sol


def grasp(demand_points, radius, max_iter):
    global GRUN
    best = greedy_random_solution(demand_points, radius, len(demand_points))
    best_l = len(best)
    solutions_costs = [best_l]
    for _ in range(max_iter - 1):
        if GRUN is False:
            break
        sol = greedy_random_solution(demand_points, radius, best_l)
        j = len(sol)
        solutions_costs.append(j)
        if j < best_l:
            best_l = j
            best = sol
    print(solutions_costs)
    print(f"\n Best is: {best_l}")
    return best


def solution(width, height, demand_points, radius):
    p = len(demand_points)
    solution_found = False
    sol = None
    while not solution_found:
        sol = generate_random_points(width, height, randint(p, p + 5))
        solution_found = solution_fully_covers(demand_points, sol, radius)
    return sol


def show_sol(dpoints, fradius):
    global GBOUNDS
    global GPARTIAL
    global GSOL
    global GRUN

    dbounds = None
    dsol = None

    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    surface = pygame.Surface(screen.get_size())
    running = True
    clock = pygame.time.get_ticks()

    while running:
        surface.fill((0, 0, 0))
        screen.blit(surface, (0, 0))
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            running = False
            GRUN = False

        for point in dpoints:
            pygame.draw.circle(screen, (255, 255, 255), (point[0], point[1]), 3)

        if dbounds is not None and (dsol is not None):
            r = pygame.Rect((dbounds[0][0], dbounds[0][1]), (dbounds[1][0], dbounds[1][1]))
            pygame.draw.rect(screen, (0, 255, 0), r, 1)
            for facility in dsol:
                pygame.draw.circle(screen, (0, 0, 255), (facility[0], facility[1]), fradius, 1)

        # Update our copy of the solution every 500 ms
        if clock == 0:
            mlock.acquire()
            dbounds = deepcopy(GBOUNDS)
            dsol = deepcopy(GSOL)
            mlock.release()
            clock = pygame.time.get_ticks()
        elif clock > 40:
            clock = 0
        else:
            clock = pygame.time.get_ticks()

        pygame.time.wait(500)
        pygame.display.flip()
    pygame.quit()


"""
Melhoria final: faça um dicionario: pra cada ponto de demanda, as torres que o atendem. Se o ponto de demanda é coberto
por mais de uma torre, existem vizinhos que são cobertos por mais de uma torre. Apenas uma torre e necessária para
cobrir esse ponto e seus vizinhos

"""


def brute_force_improving(demand_points, facilities_points, radius):
    removee = []
    for k in range(len(facilities_points)):
        better_set = [facility for facility in facilities_points]
        better_set.pop(k)
        if solution_fully_covers(demand_points, better_set, radius):
            removee.append(k)
    better_set = []
    for k in range(len(facilities_points)):
        if (k in removee):
            removee.remove(k)
        else:
            better_set.append(facilities_points[k])
    return better_set


def simul():
    global GBOUNDS
    global GRUN

    radius = 30
    demand_points = generate_random_points([0, 0], [790, 590], 500)
    GBOUNDS = [[0, 0], [620, 460]]
    # print("Waiting for solution.(GRASP-MODIFIED)")
    # sol = grasp(demand_points, radius, 50)
    solver_proc = threading.Thread(target=grasp, args=[demand_points, radius, 50])
    solver_proc.start()
    show_proc = threading.Thread(target=show_sol, args=[demand_points, radius])
    show_proc.start()
    show_proc.join()
    # show_sol(demand_points, radius)
    if solver_proc.is_alive():
        GRUN = False
    # w = len(sol)
    # print(f"After improving: {w}")


simul()
