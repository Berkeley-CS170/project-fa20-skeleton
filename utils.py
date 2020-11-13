import networkx as nx

def is_valid_solution(D, G, s, rooms):
    """
    Checks whether D is a valid mapping of G, by checking every room adheres to the stress budget.
    Args:
        D: Dictionary mapping student to room
        G: networkx.Graph
        s: Stress budget
        rooms: Number of breakout rooms


    Returns:
        bool: whether D is a valid solution
    """
    room_budget = s/rooms
    room_to_student = {}
    for k, v in D.items():
        room_to_student.setdefault(v, []).append(k)

    for k, v in room_to_student.items():
        H = G.subgraph(v)
        if len(H.edges) > 0:
            room_stress = H.size("stress")
            if room_stress > room_budget:
                return False
    return True


def calculate_happiness(D, G):
    """
    Calculates the total happiness in mapping D by summing the happiness of each room.
    Args:
        D: Dictionary mapping student to room
        G: networkx.Graph
        s: Stress budget
        k: Number of breakout rooms


    Returns:
        float: total happiness
    """
    room_to_s = {}
    for k, v in D.items():
        room_to_s.setdefault(v, []).append(k)

    happiness_total = 0
    for k, v in room_to_s.items():
        H = G.subgraph(v)
        if len(H.edges) > 0:
            room_happiness = H.size("happiness")
            happiness_total += room_happiness
    return happiness_total
