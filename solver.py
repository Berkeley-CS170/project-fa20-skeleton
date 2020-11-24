import networkx as nx
from parse import read_input_file, write_output_file, read_output_file
from utils import is_valid_solution, calculate_happiness, calculate_stress_for_room
import sys


def solve(G, s):
    """
    Args:
        G: networkx.Graph
        s: stress_budget
    Returns:
        D: Dictionary mapping for student to breakout room r e.g. {0:2, 1:0, 2:1, 3:2}
        k: Number of breakout rooms
    """

    # TODO: your code here!
    ratios = []
    for u, v, happiness in G.edges.data("happiness"):
        happy_to_stress_ratio = happiness / G[u][v]["stress"]
        triple = (u, v, happy_to_stress_ratio)
        ratios.append(triple)
    ratios = sorted(ratios, key=lambda x: x[-1])
    D= {}
    total_stress = 0
    for u, v, stress in G.edges.data("stress"):
        total_stress = total_stress + stress
    for i in G.nodes:
        D[i] = 0
    rooms = 1
    while not is_valid_solution(D, G, s, rooms):
        for i in range(rooms):
            people_in_room_i = [person for person in D.keys() if D[person] == i]
            while calculate_stress_for_room(people_in_room_i, G) > s/rooms:
                min_ratio = float("inf")
                for person in people_in_room_i:
                    my_ratio = sum([ratio[2] for ratio in ratios if ratios[0] == person])
                    if my_ratio < min_ratio:
                        person_to_take_out = person
                D[person_to_take_out] = i + 1
                people_in_room_i.remove(person_to_take_out)
        rooms = rooms + 1
    return D, rooms

# sorted(g.edges(data=True),key= lambda x: x[2]['callDuration'],reverse=True)

# Here's an example of how to run your solver.

# Usage: python3 solver.py test.in

if __name__ == '__main__':
    assert len(sys.argv) == 2
    path = sys.argv[1]
    G, s = read_input_file(path)
    D, k = solve(G, s)
    assert is_valid_solution(D, G, s, k)
    cost_t = calculate_happiness(D, G)
    output_path = 'samples/50.out'
    write_output_file(D, output_path)
    D = read_output_file(output_path, G, s)
    print("Total Happiness: {}".format(cost_t))
    # write_output_file(D, 'out/test.out')


# For testing a folder of inputs to create a folder of outputs, you can use glob (need to import it)
# if __name__ == '__main__':
#     inputs = glob.glob('file_path/inputs/*')
#     for input_path in inputs:
#         output_path = 'file_path/outputs/' + basename(normpath(input_path))[:-3] + '.out'
#         G, s = read_input_file(input_path, 100)
#         D, k = solve(G, s)
#         assert is_valid_solution(D, G, s, k)
#         cost_t = calculate_happiness(T)
#         write_output_file(D, output_path)

#pass in 2d array of outputs where each line represents a room,
# returns a list of tuples where each tuple represents a line in the input
