from math import sqrt


def cartesian_distance_point_to_point(x, y, sx, sy):
    return sqrt((sx - x) ** 2 + (sy - y) ** 2)


# TODO
def grasp_build_greedy_rand_solution(a, random_seed, p, js):
    pass


# TODO
def local_search(js):
    pass


# TODO
def sum_weights(js):
    pass


# TODO
def grasp(a, max_iter, random_seed):
    best_solution_found = None
    p = None
    js = None
    for _ in range(max_iter):
        grasp_build_greedy_rand_solution(a, random_seed, p, js)
        local_search(js)
        if best_solution_found is not None:
            if sum_weights(js) > sum_weights(best_solution_found):
                best_solution_found = js
    return best_solution_found


# TODO
def get_solution():
    # p > 0 facilities to be placed
    p = 10
    # J is the set of n potential facility locations
    J = []
    # Define n finite sets, each corresponding to a potential facility location
    sP = []
    # The set of m demand points that can be covered by the n potential facilities
    I = []
    # We associate  a weight to each demand point
    W = []
