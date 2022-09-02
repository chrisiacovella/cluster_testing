""" analyze.py :: Initialize the signac dataspace.
    ------
    This is a simple example to demonstrate how to read in
    a Signac project.
    It doesn't actually really do any analysis, but shows how
    to use the job.doc to make sure you are only loading completed
    simulations and shows how to locate your data for analysis.
    -------
"""
import itertools
import os

import numpy as np
import signac
import unyt as u

gpu_results = []
cpu_results = []

project_local = signac.get_project('LJ_cluster_testing')

for job in project_local:
    job_path = job.workspace()
    log_file = open(f'{job_path}/log.txt', 'r')
    lines = log_file.readlines()
    
    if job.sp.n_molecules == 27000:
        print(job_path)
    if "** run complete **" in lines[-1]:
        if job.sp.hoomd_version == 'hoomd2.9.7':
            for line in lines:
                if 'Average TPS:' in line:
                    temp_val = line.split(': ')
                    TPS = float(temp_val[1].strip())
                    gpu_type_temp = job.sp.gres_prefix
                    gpu_type = gpu_type_temp.split(':')
                    print(gpu_type[1])
                    result = {'device': gpu_type[1], 'n_devices': job.sp.srun_n, 'n_particles': job.sp.n_molecules, 'TPS': TPS}
                    if job.sp.run_mode == 'gpu':
                        gpu_results.append(result)
                    else:
                        cpu_results.append(result)
#print(gpu_results)
#print(cpu_results)
gpu_results_sorted = sorted(gpu_results, key=lambda d: d['n_devices'])
cpu_results_sorted = sorted(cpu_results, key=lambda d: d['n_devices'])

print('| n particles | device | n devices | TPS |' )
print('| ------ | ------ | ------ | ------ |' )
for result in gpu_results_sorted:
    print("| ", result['n_particles'], " | ", result['device'], " | ",  result['n_devices'], " | ", result['TPS'], " |")
    
for result in cpu_results_sorted:
    print("| ", result['n_particles'], " | ", "CPU", " | ",  result['n_devices'], " | ", result['TPS'], " |")

                        
