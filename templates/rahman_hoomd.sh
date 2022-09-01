{% extends "base_script.sh" %}
{% block header %}
#!/bin/bash
#SBATCH --job-name="{{ id }}"
#SBATCH --partition={{ partition }}
#SBATCH -t {{ walltime|format_timedelta }}
{% block tasks %}
#SBATCH --ntasks={{ np_global }}
{% endblock %}
{% endblock %}
