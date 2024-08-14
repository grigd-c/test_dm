### Way to use:
#### Make sure that cromwell.jar is copied into the directory where this source code is located.
***bash ./run_me.sh***

Observe 8 pythons running in the background.
In few minutes there will be output which lists all of output arrays:

* "ScatterSingleCell.umap_png",
* "ScatterSingleCell.count_matrix_h5ad",
* "ScatterSingleCell.gene_rank_png".

#### Note: 
This code makes sure that same-type files are "bunched up" in the same directory before end of execution.

If this is not required, a simpler, previous version of single_cell.wdl can be used which does not have
"GatherH5" task so output arrays at the end of the run represent files located in per-shard directories, 
which may be acceptable for the next stages.

#### Slurm: 
sbatch --array=1-8 straight_scanpy.s
