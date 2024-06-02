# Updated Introduction

This repository is a fork of the original repository for the following paper. Given a
set of nodes (terminals), this is a tool for obtaining a set of subgraphs such that
each subgraph (partition/component) contains exactly one terminal. The removed edges
are called a cut.

_A Branch and Bound Algorithm based using Isolating Cuts for the k-terminal cut problem._

The preprint of the paper is available [here](https://hochbaum.ieor.berkeley.edu/html/pub/k-cut-isolation-JOCO2020.pdf).

The original repository is outdated but can be found [here](https://github.com/marvel2010/k-terminal-cut).



The original code is outdated. Thus, the following Python packages have been updated:
- networkx has been updated from 2.2 to 2.6.3.
- numpy has been updated from 1.15.4 to 1.22.4
- pytest has been updated from 4.0.2 to 7.4.0
- scikit-learn has been updated from 0.20.1 to 1.2.0

The original code is outdated. Thus, by using updated packages, the following files have been updated:

- ktcut/contract_vertices.py
- ktcut/isolation_branching_tree.py

# Introduction from the original repository
It is a tool for studying properties of the branch-and-bound approach to the k-terminal cut problem. Its performance has not been optimized for large-scale projects (greater than 1,000,000 vertices).

If you use our algorithm in further research, please cite our paper: [Isolation Branching: A Branch and Bound Algorithm for the k-Terminal Cut Problem
](https://doi.org/10.1007/978-3-030-04651-4_42).

## Install

```
pip install .
```

## Example Usage

See /tests/test_minimal_example_graphs.py

```
def test_graph_tutte():
    from networkx.generators.small import tutte_graph
    from ktcut.isolation_branching import isolation_branching
    graph = tutte_graph()
    terminals = [1, 17, 34]
    partition, cut_value = isolation_branching(graph, terminals)
```

## Running the tests

```
pytest
```
This test runs the three scripts in the folder /tests.

## Example Python scripts

For a step-by-step tutorial, we add new tests in the folder /new_tests
- small_test_tutte_graph.py is a file that prints the partition and cut (edges) of the Tutte graph given three nodes as terminals in each cluster. The Tutte graph is a 3-regular graph with 46 vertices and 69 edges named after W. T. Tutte.

# Major functions

from ktcut.isolation_branching import isolation_branching

The function _isolation_branching_ has the following arguments/parameters:
- Arguments:
      graph: the networkx graph in which to find the multi-terminal cut
      terminals: the terminals of the networkx graph
      persistence: if persistence is assumed [strong, weak, None]
      reporting: if the branching solver should print results as it goes
      time_limit: the time after which to terminate,
          even if the optimal solution has not yet been reached.
- Returns:
      source_sets: the partition of the nodes of the graph which defines the minimum cut
      cut_value: the weight of the optimal multi-terminal cut
      report: the final values in the Isolation Branching tree

## Original Author

* **Mark Velednitsky**

## Author of This Version
This version is provided by Shuai Wang (shuai.wang@vu.nl) with minor changes and updates.
All credits go to the original author.

## License

Apache 2.0
