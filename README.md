# Item Recovery Problem - ALNS
This repository contains the source code for an ALNS-based optimization technique for the "Item Recovery Problem", which is an optimization problem where an autonomous underwater vehicle (AUV) with some given maximum carrying capacity must visit multiple sites and recover items (i.e. bring them to the "base site") with different "weights".

Report: [Item Recovery Problem
An ALNS-based Approach](https://github.com/rereee3/Item-Recovery-Problem-ALNS/blob/master/report/report.pdf)

Dependencies: ``numpy`` and the ``alns`` package (see https://pypi.org/project/alns/)

# Problem Statement

The following image illustrates a possible scenario of this problem, where an AUV is used to recover items from an underwater cave.

![Example of the item recovery problem.](https://github.com/rereee3/Item-Recovery-Problem-ALNS/blob/master/report/src/Figures/cave.png)

The corresponding weighted graph for this scenario is shown in the following image. The items and their weights are shown to the right of each site.

![Weighted graph of the example scenario.](https://github.com/rereee3/Item-Recovery-Problem-ALNS/blob/master/report/src/Figures/weighted_graph_example.svg)

# Optimization Technique

- ALNS Heuristic
- Destruction Method
  - Random Position Removal
  
  ![Random Position Removal.](https://github.com/rereee3/Item-Recovery-Problem-ALNS/blob/master/report/src/Figures/destruction/remove_rand_pos.svg)
  - Random Position Swap
  
  ![Random Position Swap.](https://github.com/rereee3/Item-Recovery-Problem-ALNS/blob/master/report/src/Figures/destruction/swap_rand_pos.svg)
  - Random Subpath Removal
  
  ![Random Subpath Removal.](https://github.com/rereee3/Item-Recovery-Problem-ALNS/blob/master/report/src/Figures/destruction/remove_rand_sps.svg)
  - Remove Worst Subpaths
  
  ![Remove Worst Subpaths.](https://github.com/rereee3/Item-Recovery-Problem-ALNS/blob/master/report/src/Figures/destruction/remove_worst_sps.svg)
- 6 Repair Method

# Results

Dataset used:

| Instance      | Sites | Sites With Items | Cargo Size | Graph Edges |
| ------------- | ------------- | ------------- | ------------- | ------------- |
| 1   | 40    | 36  | 2 | 101 |
| 2   | 45    | 39  | 9 | 112 |
| 3   | 50    | 44  | 4 | 66 |
| 4   | 55    | 47  | 7 | 111 |
| 5   | 60    | 49  | 3 | 140 |
| 6   | 65    | 61  | 6 | 98 |
| 7   | 70    | 63  | 3 | 169 |
| 8   | 75    | 62  | 5 | 193 |
| 9   | 80    | 68  | 4 | 185 |
| 10  | 85    | 72  | 9 | 170 |
| 11  | 90    | 72  | 9 | 228 |
| 12  | 95    | 86  | 9 | 236 |
| 13  | 100   | 91  | 10 | 156 |

Optimization Results:

![Optimization Results.](https://github.com/rereee3/Item-Recovery-Problem-ALNS/blob/master/report/src/Figures/instance_1_methods.svg)

Optimization Results:

| Instance      | Time Taken | Initial Cost | Best Cost |
| ------------- | ------------- | ------------- | ------------- |
| 1   | 28 min    | 5258  | 3421 |
| 2   | 1 h    | 5724  | 2856 | 
| 3   | 1.3 h    | 9254  | 6046 | 
| 4   | 2.1 h    | 13280  | 8072 | 
| 5   | 1.6 h    | 8098  | 3797 | 
| 6   | 9.7 h    | 11614  | 7354 | 
| 7   | 6.7 h    | 6028  | 2818 | 
| 8   | 5.5 h    | 11614  | 7354 | 
| 9   | 5.5 h    | 8474  | 4040 |
| 10  | 9.4 h    | 7966  | 5018 | 
| 11  | 2.2 h    | 7560  | 3125 | 
| 12  | 10.5 h    | 20932  | 6192 | 
| 13  | 51.6 h   | 35946  | 23444 | 

Note: Apologies to dark mode users.
