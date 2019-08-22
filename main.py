from math import sqrt


def cartesian_distance_point_to_point(x, y, sx, sy):
    return sqrt((sx - x) ** 2 + (sy - y) ** 2)


# TODO
def grasp_build_greedy_rand_solution(a, random_seed, p, js):
    js = []
    for i in range(p):
        # RCL = make_rcl(a,j,js,gamma)
        # s = select_facility(rcl, random_seed, js)
        # js.append(s) # js = js union {s}
        # adapt_greedy_function(s, j, js, gM, gM-1, gamma)
        pass


def max_gamma(ys):
    m = 0.0
    for gs in ys:
        if gs > m:
            m = gs


def yet_to_be_selected(locations_selected, candidate_locations):
    unselected_locations = []
    for location in candidate_locations:
        if location not in locations_selected:
            unselected_locations.append(location)
    return unselected_locations


# TODO restriction mechanism function ( restricted candidate list )
def make_rcl(a, j, js, gamma):
    rcl = []
    yjjs = yet_to_be_selected(j,js)
    gamma_st = max_gamma(sum_weights(yjjs))
    for s in yjjs:
        if sum_weights(s) >= a * gamma_st:
            rcl.append(s)
    return rcl


# TODO
def local_search(js):
    pass

# TODO
def sum_weight_location(location):
    pass

# TODO
def sum_weights(js):
    pass


# TODO
def grasp(a, max_iter, random_seed):
    best_solution_found = None
    p = None
    js = []
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
