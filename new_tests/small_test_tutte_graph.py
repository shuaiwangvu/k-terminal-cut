from networkx.generators.small import tutte_graph
from ktcut.isolation_branching import isolation_branching

# this file was modified from the original test file with prints and parameter changes

def test_graph_tutte():
    graph = tutte_graph()
    print ('The graph is ')
    print (graph)
    terminals = [1, 17, 34]
    print ('The terminals are: ', terminals)
    source_sets, cut_value, report = isolation_branching(graph, terminals)

    print ('the cut value = ', cut_value)

    for s in source_sets:
        print ('\t source set: ', s)

    for r in report:
        print (r ,':', report[r])




test_graph_tutte()
