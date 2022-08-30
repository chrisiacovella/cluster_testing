# Cluster Testing

This repository is based off of the [Simple signac workflow](https://github.com/chrisiacovella/simple_signac_workflow), modified to perform testing/benchmarking. This repository could be easily modified to be used for benchmarking a system to find optimal runtime parameters (e.g., MPI vs. openMPI threads, single vs. multi-GPU, etc.). 


------


[init.py](init.py): Defines the signac workspace.  Here we will be considering different chemical systems, system sizes, computing resources, and builds of the software.

[project.py](project.py): A simple signac-flow script encode a workflow for performing the testing/benchmarking over the design space, using mBuild and Foyer to initialize and atomtype the system. 

[analyze.py](analyze.py): A very simple framework to aggregate the data for testing and benchmarking.  While not an exhaustive set of tests, we will compare potential energy of identical statepoints, RDFs, as well as aggregating the performance metrics.  
