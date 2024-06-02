# from networkx.generators.small import tutte_graph
from ktcut.isolation_branching import isolation_branching, isolation_branching_extended_results
import matplotlib.pyplot as plt
import networkx as nx


# this file was modified from the original test file with prints and parameter changes

def test_graph_tutte():
    graph = nx.generators.small.tutte_graph()

    neighbors  = [n for n in graph.neighbors(0)]
    print('Neighbors of 0: ', neighbors)

    for e in graph.edges():
        (a,b) = e
        graph[a][b]['color'] = 'blue'


    pos = nx.spectral_layout(graph)

    edges = graph.edges()
    # colors = [graph[u][v]['color'] for u,v in edges]

    print ('The graph is ')
    print (graph)
    terminals = [1, 17, 34]
    print ('The terminals are: ', terminals)
    source_sets, cut_value, report = isolation_branching(graph, terminals)

    print ('the cut value = ', cut_value)

    for r in report:
        print (r ,':', report[r])


    mapping_node_to_source = {}
    for s in source_sets:
        print ('\t source set: ', s)
        print ('\t', source_sets[s])
        for t in source_sets[s]:
            mapping_node_to_source[t] = s

    removed_edges = set()

    for e in graph.edges():
        (a, b) = e
        if mapping_node_to_source[a] != mapping_node_to_source[b]:
            removed_edges.add(e)

    print ('Removed edges are: ')
    for e in removed_edges:
        print ('\t', e)



def test_graph_tutte_new():
    print('now the new test:')
    graph = nx.generators.small.tutte_graph()
    terminals = [1, 17, 34]
    source_sets, cut_value, report, removed_edges, partition_edges = isolation_branching_extended_results(graph, terminals, return_removed_edges = False, return_partitions = False)
    print ('Removed edges are: ')
    for e in removed_edges:
        print ('\t', e)
    print ('Partition edges are: ')
    for p in partition_edges:
        print ('For partition ', p, ':')
        for e in partition_edges[p]:
            print ('\t', e)

test_graph_tutte()
test_graph_tutte_new()
