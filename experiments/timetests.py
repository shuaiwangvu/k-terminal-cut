"""Timing/profiling tests of the branch and bound algorithm."""

import random
import cProfile
import time

import matplotlib.pyplot as plt

import numpy as np
import networkx as nx

from ktcut.ip_algorithm import ip_algorithm
from ktcut.spectral_clustering import suggested_terminals
from ktcut.isolation_branching import isolation_branching
from ktcut.read_data import read_dimacs_graph
from ktcut.read_data import read_konect_graph

from pulp import GUROBI

DIMACS_DATASETS = [
    # 'data/dimacs/adjnoun.graph',  # bad with 10
    'data/dimacs/polbooks.graph',
    # 'data/dimacs/football.graph',  # unclear with 10
    # 'data/dimacs/netscience.graph',  # old
    # 'data/dimacs/celegans_metabolic.graph',  # old
    'data/dimacs/jazz.graph',  # unclear with 10
    # 'data/dimacs/email.graph',
    # 'data/dimacs/power.graph',  # old
    # 'data/dimacs/hep-th.graph',  # old
    # 'data/dimacs/polblogs.graph',
    # 'data/dimacs/PGPGiantcompo.graph',  # old
    # 'data/dimacs/as-22july06.graph',  # old
    # 'data/dimacs/astro-ph.graph'  # old
]

KONECT_DATASETS = [
    'data/konect/out.arenas-email',  # 41 kb
    'data/konect/out.arenas-jazz',  # 19 kb
    'data/konect/out.arenas-pgp',  # 229 kb
    'data/konect/out.as20000102',  # 114 kb
    # 'data/konect/out.as-caida20071105',  # 500 kb
    # 'data/konect/out.ca-AstroPh',  # 1944 kb
    # 'data/konect/out.com-amazon',  # 11783 kb
    # 'data/konect/out.com-dblp',  # 13096 kb
    # 'data/konect/out.douban',  # 3945 kb
    'data/konect/out.ego-facebook',  # 26 kb
    # 'data/konect/out.livemocha',  # 26580 kb
    # 'data/konect/out.loc-brightkite_edges', # 2225 kb
    # 'data/konect/out.log-gowalla_edges',  # 10810 kb
    'data/konect/out.maayan-pdzbase',  # 2 kb
    'data/konect/out.maayan-vidal',  # 57 kb
    'data/konect/out.moreno_propro_propro',  # 19 kb
    'data/konect/out.opsahl-powergrid',  # 62 kb
    'data/konect/out.petster-friendships-hamster-uniq',  # 99 kb
    'data/konect/out.petster-hamster',  # 134 kb
    # 'data/konect/out.reactome',  # 1456 kb
    'data/konect/out.subelj_euroroad_euroroad',  # 12 kb
    'data/konect/out.tntp-ChicagoRegional',  # 12 kb
    # 'data/konect/out.wordnet-words'  # 7773 kb
]


def main():

    # model = 'powerlaw_cluster'
    # for size in range(1000, 2000, 1000):
    #     time_test_synthetic_repeated(model, size, 5, repeat=5)

    # graph_reader = read_dimacs_graph
    graph_reader = read_konect_graph

    for dataset in KONECT_DATASETS:
        graph = graph_reader(dataset)
        # Restrict to Largest Connected Component
        largest_cc = max(nx.connected_components(graph), key=len)
        graph_prime = graph.subgraph(largest_cc).copy()
        # Suggest Terminals
        terminals, total_degree = suggested_terminals(graph_prime, 5)
        information = {
            "Graph Name": dataset,
            "Vertex Count": len(graph_prime.nodes),
            "Edge Count": len(graph_prime.nodes),
            "Terminals": terminals,
            "Total Terminal Degree": total_degree
        }
        print(information)

        # nx.draw_networkx(graph_prime)
        # plt.show()

        bb_time, _, _, _, ip_time_gurobi = time_test_simple(graph_prime,
                                                            terminals,
                                                            True,
                                                            False,
                                                            False,
                                                            False,
                                                            True)

        print("bb time", bb_time)
        print("ip time gurobi", ip_time_gurobi)
        print()


def time_test_synthetic_repeated(model_name,
                                 node_count,
                                 terminal_count,
                                 repeat=3,
                                 test_bb=True,
                                 test_bb_weak=False,
                                 test_bb_strong=False,
                                 test_ip_cbc=False,
                                 test_ip_gurobi=True):
    """Runs several time tests and reports average and median for each of the algorithms."""

    times_bb, times_bb_weak, times_bb_strong, times_ip_cbc, times_ip_gurobi = [], [], [], [], []

    for _ in range(repeat):

        graph, _ = create_random_graph(model_name=model_name,
                                       node_count=node_count,
                                       terminal_count=terminal_count)
        terminals, _ = suggested_terminals(graph=graph,
                                           terminal_count=terminal_count)
        print(len(graph.nodes), len(graph.edges))

        time_bb, time_bb_weak, time_bb_strong, time_ip_cbc, time_ip_gurobi = time_test_simple(graph,
                                                                                              terminals,
                                                                                              test_bb,
                                                                                              test_bb_weak,
                                                                                              test_bb_strong,
                                                                                              test_ip_cbc,
                                                                                              test_ip_gurobi)

        times_bb.append(time_bb)
        times_bb_weak.append(time_bb_weak)
        times_bb_strong.append(time_bb_strong)
        times_ip_cbc.append(time_ip_cbc)
        times_ip_gurobi.append(time_ip_gurobi)

    if test_bb:
        print("Raw Times for B&B:", times_bb)
        print("Average Time for B&B:", np.average(times_bb))
        print("Median Time for B&B:", np.median(times_bb))
        print()

    if test_bb_weak:
        print("Raw Times for B&B Weak:", times_bb_weak)
        print("Average Time for B&B Weak:", np.average(times_bb_weak))
        print("Median Time for B&B Weak:", np.median(times_bb_weak))
        print()

    if test_bb_strong:
        print("Raw Times for B&B Strong:", times_bb_strong)
        print("Avg Time for B&B Strong:", np.average(times_bb_strong))
        print("Med Time for B&B Strong:", np.median(times_bb_strong))
        print()

    if test_ip_cbc:
        print("Raw Times for Integer Program CBC:", times_ip_cbc)
        print("Average Time for Integer Program CBC:", np.average(times_ip_cbc))
        print("Median Time for Integer Program CBC:", np.median(times_ip_cbc))
        print()

    if test_ip_gurobi:
        print("Raw Times for Integer Program Gurobi:", times_ip_gurobi)
        print("Average Time for Integer Program Gurobi:", np.average(times_ip_gurobi))
        print("Median Time for Integer Program Gurobi:", np.median(times_ip_gurobi))
        print()

    print()

    return (np.average(times_bb),
            np.average(times_bb_weak),
            np.average(times_bb_strong),
            np.average(times_ip_cbc),
            np.average(times_ip_gurobi)
    )


def time_test_simple(graph,
                     terminals,
                     test_bb,
                     test_bb_weak,
                     test_bb_strong,
                     test_ip_cbc,
                     test_ip_gurobi):
    """Runs a single time test of each of the algorithms (B&B, B&B-weak, B&B-strong, IP)."""
    t1 = time.time()

    if test_bb:
        isolation_branching(graph.copy(), terminals)

    t2 = time.time()

    if test_bb_weak:
        isolation_branching(graph.copy(), terminals, persistence='weak')

    t3 = time.time()

    if test_bb_strong:
        isolation_branching(graph.copy(), terminals, persistence='strong')

    t4 = time.time()

    if test_ip_cbc:
        ip_algorithm(graph.copy(), terminals)

    t5 = time.time()

    if test_ip_gurobi:
        ip_algorithm(graph.copy(), terminals, solver=GUROBI(msg=False))

    t6 = time.time()

    return t2-t1, t3-t2, t4-t3, t5-t4, t6-t5


def time_test_breakdown_branch_and_bound(graph,
                                         terminals):
    """Runs cProfile to determine the time spent within each function."""
    variable_specifications = {'branch_and_bound_algorithm': isolation_branching,
                               'graph': graph,
                               'terminals': terminals}

    cProfile.runctx("branch_and_bound_algorithm(graph, terminals)",
                    variable_specifications, {}, sort='cumtime')


def time_test_breakdown_ip(graph,
                           terminals,
                           solver=None):
    """Runs cProfile to determine the time spent within each function."""
    variable_specifications = {'ip_algorithm': ip_algorithm,
                               'graph': graph,
                               'terminals': terminals,
                               'solver': solver}

    cProfile.runctx("ip_algorithm(graph, terminals, solver)",
                    variable_specifications, {}, sort='cumtime')


def create_random_graph(model_name,
                        node_count,
                        terminal_count=4):
    """Creates a random graph according to some model.

    Args:
        model_name: which model to use for the random graph
        node_count: number of nodes in the graph
        terminal_count: number of terminals in the graph

    Returns:
        graph: the graph in networkx format
        terminals: the terminals in a list

    Raises:
        ValueError: if model_name is not a valid model name
    """

    if model_name == 'gnp':
        graph = nx.gnp_random_graph(node_count, 0.01)
    elif model_name == 'lobster':
        graph = nx.random_lobster(node_count, 0.1, 0.1)
    elif model_name == 'powerlaw_tree':
        graph = nx.random_powerlaw_tree(node_count)
    elif model_name == 'powerlaw_cluster':
        # n = the number of nodes
        # m = the number of random edges to add for each new node
        # p = probability of adding a triangle after adding a random edge
        graph = nx.powerlaw_cluster_graph(node_count, 10, 0.1)
    elif model_name == 'barabasi_albert':
        graph = nx.barabasi_albert_graph(node_count, 3)
    elif model_name == 'connected_watts_strogatz':
        graph = nx.connected_watts_strogatz_graph(node_count, 10, 0.1)
    elif model_name == 'newman_watts_strogatz':
        graph = nx.newman_watts_strogatz_graph(node_count, 10, 0.1)
    else:
        raise ValueError("")

    for edge in graph.edges():
        graph[edge[0]][edge[1]]['capacity'] = 0.1 + random.random()

    terminals = range(terminal_count)

    return graph, terminals


if __name__ == '__main__':
    main()