import re
import os

import networkx as nx

import utils


def validate_file(path):
    """File must not exceed 100KB and must contain only numbers and spaces"""
    if os.path.getsize(path) > 100000:
        print(f"{path} exceeds 100KB, make sure you're not repeating edges!")
        return False
    with open(path, "r") as f:
        if not re.match(r"^[\d\.\s]+$", f.read()):
            print(f"{path} contains characters that are not numbers and spaces")
            return False
    return True


def read_input_file(path, max_size=None):
    """
    Parses and validates an input file

    :param path: str, a path
    :param max_size: int, number of max add_nodes_from
    :return: networkx Graph is the input is well formed, AssertionError thrown otherwise
    """
    with open(path, "r") as fo:
        n = fo.readline().strip()
        assert n.isdigit()
        n = int(n)

        stress_budget = fo.readline().strip()
        assert bool(re.match(r"(^\d+\.\d{1,3}$|^\d+$)", stress_budget))
        stress_budget = float(stress_budget)
        assert 0 < stress_budget < 100

        lines = fo.read().splitlines()
        fo.close()

        # validate lines
        for line in lines:
            tokens = line.split(" ")

            assert len(tokens) == 4
            assert tokens[0].isdigit() and int(tokens[0]) < n
            assert tokens[1].isdigit() and int(tokens[1]) < n
            assert bool(re.match(r"(^\d+\.\d{1,3}$|^\d+$)", tokens[2]))
            assert bool(re.match(r"(^\d+\.\d{1,3}$|^\d+$)", tokens[3]))
            assert 0 <= float(tokens[2]) < 100
            assert 0 <= float(tokens[3]) < 100

        G = nx.parse_edgelist(lines, nodetype=int, data=(("happiness", float),("stress", float),))
        G.add_nodes_from(range(n))

        #check completeness and connectivity
        assert nx.is_connected(G)
        assert len(G.edges()) == n*(n-1)//2

        if max_size is not None:
            assert len(G) <= max_size

        return G, stress_budget


def write_input_file(G, stress_budget, path):
    with open(path, "w") as fo:
        n = len(G)
        s_total = stress_budget
        lines = nx.generate_edgelist(G, data=["happiness","stress"])
        fo.write(str(n) + "\n")
        fo.write(str(s_total) + "\n")
        fo.writelines("\n".join(lines))
        fo.close()


def read_output_file(path, G, s):
    """
    Parses and validates an output file

    :param path: str, a path
    :param G: the input graph corresponding to this output
    :return: networkx Graph is the output is well formed, AssertionError thrown otherwise
    """
    with open(path, "r") as fo:
        nodes = set()
        rooms = set()
        D = {}
        lines = fo.read().splitlines()
        fo.close()

        for line in lines:
            tokens = line.split()
            assert len(tokens) == 2
            #validate node
            node = int(tokens[0])
            assert tokens[0].isdigit() and 0 <= node < len(G)
            nodes.add(node)
            #validate rooms
            room = int(tokens[1])
            assert tokens[0].isdigit() and 0 <= room < len(G)
            rooms.add(room)

            D[node] = room

        assert len(nodes) == len(G)
        assert utils.is_valid_solution(D, G, s, len(rooms))

    return D


def write_output_file(D, path):
    """
    Writes a mapping to an output file

    :param path: str, a path
    :param D: dict, a mapping
    :return: None -- creates a text file
    """
    with open(path, "w") as fo:
        for key, value in D.items():
            fo.write(str(key) + " " + str(value) + "\n")
        fo.close()
