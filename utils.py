import math

def get_closest_expansion_location(available_locations, own_base):
    best = None
    distance = math.inf
    for expansion in available_locations:
        temp = expansion.distance2_to(own_base)
        if temp < distance and temp > 0:
            distance = temp
            best = expansion
    return best