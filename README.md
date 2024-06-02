# Updated Introduction

This repository is a fork of the original repository for the following paper. This is
a tool for obtaining a partition that isolates k nodes in a graph.

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

## Example Useage

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

## Built With

* [Python](https://www.python.org/)
* [NetworkX](https://networkx.github.io/)



## Authors

* **Mark Velednitsky**

## License

Apache 2.0
