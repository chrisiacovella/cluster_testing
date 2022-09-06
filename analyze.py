""" analyze.py :: Initialize the signac dataspace.
    ------
    This reads in the signac project and will parse the log file that
    reports performance and create a summary table.
    
    python analyze.py
    -------
"""
import itertools
import os
from os.path import exists

import numpy as np
import signac
import unyt as u

gpu_results = []
cpu_results = []

project_local = signac.get_project('LJ_cluster_testing')

for job in project_local:
    job_path = job.workspace()
    log_file_path = f'{job_path}/log.txt'
    file_exists = exists(log_file_path)
    if file_exists:
        log_file = open(log_file_path, 'r')
        lines = log_file.readlines()
        if len(lines) > 0:
            if "run complete" in lines[-1]:
                if job.sp.hoomd_version == 'hoomd2.9.7':
                    for line in lines:
                        if 'Average TPS:' in line:
                            temp_val = line.split(': ')
                            TPS = float(temp_val[1].strip())
                            gpu_type_temp = job.sp.gres_prefix
                            gpu_type = gpu_type_temp.split(':')
                            result = {'device': gpu_type[1], 'n_devices': job.sp.srun_n, 'n_particles': job.sp.n_molecules, 'TPS': TPS}
                            if job.sp.run_mode == 'gpu':
                                gpu_results.append(result)
                            else:
                                cpu_results.append(result)
                
                elif job.sp.hoomd_version == 'hoomd3.4.0':
                    tps_temp = []
                    for line in lines:
                            temp_val = line.split()
                            if temp_val[0].isdigit():
                                TPS = float(temp_val[1].strip())
                                tps_temp.append(TPS)
                            
                    tps_np = np.array(tps_temp)
                    gpu_type_temp = job.sp.gres_prefix
                    gpu_type = gpu_type_temp.split(':')
                    result = {'device': gpu_type[1], 'n_devices': job.sp.srun_n, 'n_particles': job.sp.n_molecules, 'TPS': np.mean(tps_np)}
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

                        
