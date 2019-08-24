from random import randint
from math import sqrt
import pygame

"""
TODO: THIS IS A COPY'N'PASTE FROM GRASP
"""
def cartesian_distance_point_to_point(A, B):
    x, y = A[0], A[1]
    sx, sy = B[0], B[1]
    return sqrt((sx - x) ** 2 + (sy - y) ** 2)


def generate_random_points(width, height, p):
    points = []
    for _ in range(p):
        x = randint(0, width)
        y = randint(0, height)
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


def heightmost_demand(demand_points):
    heightmost = 0
    for demand in demand_points:
        if demand[1] > heightmost:
            heightmost = demand[1]
    return heightmost


def greedy_random_solution(demand_points, radius):
    sol = []
    uncovered_demand = [i for i in demand_points]
    while len(uncovered_demand) > 0:
        sol_candidates = []
        leftmost_demand = uncovered_demand[0][0] + radius
        heightmost = heightmost_demand(uncovered_demand) + radius
        step_solution_covered_points = []
        p = len(uncovered_demand) # generate at most p facilities
        sol_ = generate_random_points(leftmost_demand, heightmost, p)
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

    return sol


def grasp(demand_points, radius, max_iter):
    best = greedy_random_solution(demand_points, radius)
    best_l = len(best)
    solutions_costs = [best_l]
    for _ in range(max_iter - 1):
        sol = greedy_random_solution(demand_points, radius)
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
