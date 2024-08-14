#!/bin/bash
#
#SBATCH --job-name=myJobarray
#SBATCH --nodes=1 --ntasks-per-node=1
#SBATCH --time=20:00
#SBATCH --mem=32GB
#SBATCH --output=single_%A_%a.out
#SBATCH --error=single_%A_%a.err
cd /mnt/hgfs/SLURM/RUN

python process_scanpy.py MantonBM${SLURM_ARRAY_TASK_ID}_HiSeq_1.h5
