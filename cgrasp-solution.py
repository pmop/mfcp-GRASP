from random import randint, sample
from math import sqrt
import math
from copy import deepcopy
import pygame

"""
TODO: Linear Search
TODO: Adapting to the problem
"""
Ternary = [[0, 1], [0, -1], [1, 0], [1, 1], [1, -1], [-1, 0], [-1, 1], [-1, -1]]


def cartesian_distance_point_to_point(A, B):
    x, y = A[0], A[1]
    sx, sy = B[0], B[1]
    return sqrt((sx - x) ** 2 + (sy - y) ** 2)


# Input: vector min [x,y], vector max [maxX,maxY]
# Output: sorted list with respect to X of random points from min to max
def generate_random_points(min, max, p):
    points = []
    minX, minY = min[0], min[1]
    maxX, maxY = max[0], max[1]
    for _ in range(p):
        x = randint(minX, maxX)
        y = randint(minY, maxY)
        points.append([x, y])
    points.sort(key=lambda k: k[0] + k[1])
    return points


def solution_fully_covers(demand_points, facility_points, radius):
    covered = 0
    for point in demand_points:
        for facility in facility_points:
            if cartesian_distance_point_to_point(point, facility) <= radius:
                covered = covered + 1
                break
    return covered == len(demand_points)


# Input: the set of tuples of demand points and one tuple facility
# Output: the set of indexes of demand points covered by facility
def points_facility_covers(demand_points, facility, radius):
    output = []
    for i in range(len(demand_points)):
        point = demand_points[i]
        if cartesian_distance_point_to_point(point, facility) <= radius:
            output.append(i)
    return output


# Input: the set of demand points
# Output: Vectors lower bound (minX,minY) upper bound (maxX,maxY)
def min_max_demands(demand_points):
    first = demand_points[0]
    minX, minY, maxX, maxY = first[0], first[1], 0, 0
    for demand in demand_points:
        x, y = demand[0], demand[1]
        if x > maxX:
            maxX = x
        if x < minX:
            minX = x
        if y > maxY:
            maxY = y
        if y < minY:
            minY = y
    return [minX, maxX], [minY, maxY]


# i represents the ith coordinate of x
def line_search(x, f, h, i, n, l, u, demand_points):
    xstar = deepcopy(x)
    z = xstar[i]
    o = f([x], demand_points)
    d = 0
    while vleq(u,xstar) and vgeq(l,xstar):
        xstar[i] = xstar[i] + d


def randomly_select_element(rcl):
    return sample(rcl, 1)


def min(*args):
    m = args[0]
    for arg in args:
        if arg < m:
            m = arg
    return m


# vector b >= a
def vgeq(a, b):
    x0, y0 = a[0], a[1]
    x1, y1 = b[0], b[1]
    if x1 >= x0 and y1 >= y0:
        return True
    else:
        return False


# vector b <= a
def vleq(a, b):
    x0, y0 = a[0], a[1]
    x1, y1 = b[0], b[1]
    if x1 <= x0 and y1 <= y0:
        return True
    else:
        return False


# l is lower bound, u is upper bound
def local_improvement(x, f, n, h, l, u, max_dir_to_try):
    improved = True
    # c = 3**n - 1
    xstar = deepcopy(x)
    fstar = f(x)
    D = []
    c = len(Ternary)
    # num_dir_to_try = min(c, max_dir_to_try)
    num_dir_to_try = c
    while improved:
        improved = False
        while len(D) <= num_dir_to_try and not improved:
            r = randint(1, c)
            while r in D:
                r = randint(1, c)
            D.append(r)
            d = Ternary[r]
            x[0], x[1] = xstar[0] + h * d[0], xstar[1] + h * d[1]
            if vgeq(l, x) and vleq(u, x):
                if f(x) < fstar:
                    xstar = x
                    fstar = f(x)
                    D.clear()
                    improved = True
    return xstar


# n is always 2 because we're dealing with plane
# x is a solution
# f is the objective function
# h is the search parameter
# l and u are the max and min vectors
# alpha is the selection parameter
def construct_greedy_randomized(x, f, n, h, l, u, alpha, demand_points):
    S = [i for i in range(n)]
    z_set = dict(int)
    g_set = dict(int)
    while len(S) > 0:
        mn = math.inf
        mx = -math.inf
        for i in range(n):
            if i in S:
                z_set[i] = line_search(x, h, i, n, l, u, demand_points)
                g_set[i] = f(z_set[i], demand_points)
                if mn > g_set[i]:
                    mn = g_set[i]
                if mx < g_set[i]:
                    mx = g_set[i]

        RCL = []
        for i in range(n):
            if i in S and g_set[i] <= (1 - alpha) * mn + alpha * mx:
                RCL.append(i)
        j = randomly_select_element(RCL)
        x[j] = z_set[j]
        S.remove(j)

    return x


# returns an uniformly randomized integer vector
def unif_rand(u, l):
    minX, minY = u[0], u[1]
    maxX, maxY = l[0], l[1]
    x = randint(minX, maxX)
    y = randint(minY, maxY)
    return [x, y]


# Objective function
def objective_function(x, demand_points):
    score = len(x)
    uncovered = deepcopy(demand_points)
    for t in x:
        index_covered = points_facility_covers(uncovered, t, 30)
        for i in index_covered:
            uncovered.remove(demand_points[i])
        score = score - len(index_covered)
    return score


def cgrasp(demand_points, radius, max_iters, max_num_iter_no_improv, num_times_to_run, max_dir_to_try, alpha=1):
    fstar = math.inf
    l, u = min_max_demands(demand_points)
    xstar = None
    for _ in range(num_times_to_run):
        x = unif_rand(l, u)
        h = 1
        num_iter_no_improv = 0
        for _ in range(max_iters):
            x = construct_greedy_randomized(x, objective_function,2, h, l, u, alpha)
            x = local_improvement(x, objective_function, 2, h, l, u, max_dir_to_try)
            # there are some adaptations to do here. we have to acknowledge for uncovered points and
            # also, the solution is a set
            if objective_function(x, demand_points) < fstar:
                xstar = x
                fstar = objective_function(x, demand_points)
                num_iter_no_improv = 0
            else:
                num_iter_no_improv = num_iter_no_improv + 1
            if num_iter_no_improv >= max_num_iter_no_improv:
                h = h / 2
                num_iter_no_improv = 0
    return xstar


def solution(width, height, demand_points, radius):
    p = len(demand_points)
    solution_found = False
    sol = None
    while not solution_found:
        sol = generate_random_points(width, height, randint(p, p + 5))
        solution_found = solution_fully_covers(demand_points, sol, radius)
    return sol


def show_sol(dpoints, floc, fradius):
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    surface = pygame.Surface(screen.get_size())
    running = True

    while running:
        surface.fill((0, 0, 0))
        screen.blit(surface, (0, 0))
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            running = False
        for point in dpoints:
            pygame.draw.circle(screen, (255, 255, 255), (point[0], point[1]), 2, 0)
        for facility in floc:
            pygame.draw.circle(screen, (0, 0, 255), (facility[0], facility[1]), fradius, 1)
        pygame.time.wait(500)
        pygame.display.flip()
    pygame.quit()


def simul():
    radius = 30
    demand_points = generate_random_points(620, 460, 50)
    print("Waiting for solution.")
    sol = grasp(demand_points, radius, 50)
    show_sol(demand_points, sol, radius)


simul()
