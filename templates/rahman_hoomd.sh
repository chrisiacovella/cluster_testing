{% extends "slurm.sh" %}
{% block header %}
#!/bin/bash
#SBATCH --job-name="{{ id }}"
#SBATCH --partition={{ partition }}
#SBATCH --gres={{ gres }}
{% block tasks %}
#SBATCH --ntasks={{ ntasks }}
{% endblock %}
{% endblock %}
