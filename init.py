""" init.py :: Initialize the signac dataspace.
    ------
    This is a simple example to demonstrate the use of
    MoSDeF and Signac to perform a simulation using GROMACS.
    This file defines the dataspace that will be considered.
    Note, each job in the dataspace will have the same
    thermodynamic inputs, but will be initialized
    with different length alkanes.
    -------
"""
import itertools
import os

import numpy as np
import signac
import unyt as u

# Define a new project and give it a name.
pr = signac.init_project('LJ_cluster_testing')


# system sizes 22**3, 30**3, 40**3
system_sizes = [10648] #, 27000, 64000]

system_density = 1.0
temperature = 1.0
velocity_seed = 8675309
run_time = 50000


node_param = {
    "node_type": 'std',
    "module": 'hoomd/single/2.9.7std',
    "hoomd_version": 'hoomd2.9.7',
    "gres_prefix": 'gpu:GTX980:2',
    "srun_n": [1, 2, 1, 2, 4, 8, 16],
    "run_modes": ['gpu', 'gpu', 'cpu', 'cpu', 'cpu', 'cpu', 'cpu'],
}



# Loop over the design space to create an array of statepoints
total_statepoints = []
for i, run_mode in enumerate(node_param['run_modes']):
    
    for system_size in system_sizes:
        statepoint = {
            "temperature": temperature,
            "velocity_seed": velocity_seed,
            "run_time": run_time,
            "n_molecules": system_size,
            "system_density": system_density,
            "node_type": node_param['node_type'],
            "module": node_param['module'],
            "hoomd_version": node_param['hoomd_version'],
            "gres_prefix": node_param['gres_prefix'],
            "srun_n": node_param['srun_n'][i],
            "run_mode": run_mode,
        }
        total_statepoints.append(statepoint)

# Initialize the statepoints.
# Since we only are defining small handful,
# we will also print them to the screen.
print('statepoints initialized:')
for sp in total_statepoints:
    print(sp)
    pr.open_job(
            statepoint=sp,
            ).init()
