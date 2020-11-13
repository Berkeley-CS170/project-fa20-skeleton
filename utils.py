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
        room_stress = calculate_stress_for_room(v, G)
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
        room_happiness = calculate_happiness_for_room(v, G)
        happiness_total += room_happiness
    return happiness_total

def convert_dictionary(room_to_student):
    """
    Converts the dictionary mapping room_to_student to a valid return of the solver
    Args:
        room_to_student: Dictionary of room to a list of students
    Returns:
        D: Dictionary mapping student to room
    e.g {0: [1,2,3]} ==> {1:0, 2:0, 3:0}
    """
    d = {}
    for room, lst in room_to_student.items():
        for student in lst:
            d[student] = room
    return d

def calculate_stress_for_room(arr, G):
    """
    Given an array of students in to be placed in a room, calculate stress for the room.
    Args:
        arr: Array of students
        G: Original graph
    Returns:
        room_stress: Stress value of the room
    """
    H = G.subgraph(arr)
    return H.size("stress")

def calculate_happiness_for_room(arr, G):
    """
    Given an array of students in to be placed in a room, calculate happiness for the room.
    Args:
        arr: Array of students
        G: Original graph
    Returns:
        room_happiness: Happiness value of the room
    """
    H = G.subgraph(arr)
    return H.size("happiness")
