"""
Process 1 scanpy file
"""
#!/usr/bin/env python3

import sys
from os.path import basename, isfile, splitext
import scanpy as sc


def main():
    if len(sys.argv) < 2:
        raise ValueError("Please specify input file")
    if not isfile(sys.argv[1]):
        raise ValueError("Please specify existing input file")
    if splitext(sys.argv[1])[1] != ".h5":
        raise ValueError("Please specify .h5 input file")
    sc.settings.verbosity = 3  # verbosity: errors (0), warnings (1), info (2), hints (3)
    path_input = sys.argv[1]
    input_base = basename(splitext(path_input)[0])
    path_output = f"count_matrix_{input_base}.h5"
    adata = sc.read_10x_h5(path_input)
    adata.var_names_make_unique()
    pcnt_cells: int = int((adata.n_obs * 0.05) // 100)

    # Quality control: For cells, keep those with $ 500 \leq$ number of genes expressed $< 6000$,
    sc.pp.filter_cells(adata, min_genes=500)
    # and with percent of mitochondrial genes (name prefix MT- ) $< 10\%$.
    # For genes, keep those expressed in at least $0.05\%$ of cells.
    sc.pp.filter_genes(adata, min_cells=pcnt_cells)

    adata.var['mt'] = adata.var_names.str.startswith('MT-')  # annotate the group of mitochondrial genes as 'mt'
    sc.pp.calculate_qc_metrics(adata, qc_vars=['mt'], percent_top=None, log1p=False, inplace=True)

    adata = adata[adata.obs.n_genes_by_counts < 6000, :]
    adata = adata[adata.obs.pct_counts_mt < 10, :]

    # Log-normalize data with $100,000$ reads per cell.
    sc.pp.normalize_total(adata, target_sum=1e5)
    sc.pp.log1p(adata)
    # Select top 2000 highly variable genes.
    sc.pp.highly_variable_genes(adata, n_top_genes=2000)
    adata.raw = adata
    adata = adata[:, adata.var.highly_variable]

    sc.pp.regress_out(adata, ['total_counts', 'pct_counts_mt'])
    sc.pp.scale(adata, max_value=10)

    # PCA
    # Get Principal Component Analysis (PCA) embedding with 50 PCs.
    sc.tl.pca(adata, svd_solver='arpack', n_comps=50)

    # Get Nearest Neighborhood graph of 100 neighbors from the 50 PCs.
    sc.pp.neighbors(adata, n_neighbors=100, n_pcs=50)

    # Leiden clustering on PCA embedding with resolution 1.3.
    sc.tl.leiden(adata, resolution=1.3)

    # Calculate UMAP embedding from PCA embedding, and generate UMAP plot with cells colored by their leiden labels.
    sc.tl.paga(adata)
    sc.pl.paga(adata, plot=False)  # remove `plot=False` if you want to see the coarse-grained graph
    sc.tl.umap(adata, init_pos='paga')
    sc.pl.umap(adata, color=['leiden'], save=f"_{input_base}.png")

    # Find marker genes for each leiden cluster using Mann-Whitney-U test, and generate the gene rank plot.
    sc.settings.verbosity = 2
    sc.tl.rank_genes_groups(adata, 'leiden', method='wilcoxon')
    sc.pl.rank_genes_groups(adata, n_genes=25, sharey=False, save=f"_{input_base}.png")
    adata.write(path_output, compression='gzip')
    print("Done!")


if __name__ == "__main__":
    main()
