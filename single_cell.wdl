## Simple workflow to do single cell sequencing

version development-1.1

workflow ScatterSingleCell {
    input {
        String docker_image
        Array[File] input_h5s
    }

    scatter(input_h5 in input_h5s) {
    call ProcessOneH5 {
        input:
            docker_image = docker_image,
            input_h5 = input_h5
        }
    }

    call GatherH5 {
        input:
            count_matrixes_h5s = ProcessOneH5.count_matrix,
            umaps_pngs = ProcessOneH5.umap,
            rank_genes_pngs = ProcessOneH5.rank_genes
    }

    output {
        Array[File] count_matrix_h5ad = GatherH5.count_matrixes
        Array[File] umap_png = GatherH5.umaps
        Array[File] gene_rank_png = GatherH5.rank_genes
    }
}

task ProcessOneH5 {
    input {
        String docker_image
        File input_h5
    }

    String base_filename = basename(input_h5, ".h5")

    command {
        cp ${input_h5} .
        python /reporting/process_scanpy.py ${input_h5}
    }

    output {
        File count_matrix = "count_matrix_~{base_filename}.h5"
        File umap = "figures/umap_~{base_filename}.png"
        File rank_genes = "figures/rank_genes_groups_leiden_~{base_filename}.png"
    }

    runtime {
        docker: docker_image
    }
}

task GatherH5 {
    input {
        Array[File] count_matrixes_h5s
        Array[File] umaps_pngs
        Array[File] rank_genes_pngs
    }

    command {
        mkdir count_matrixes
        cp ${sep=' ' count_matrixes_h5s} count_matrixes
        mkdir umaps
        cp ${sep=' ' umaps_pngs} umaps
        mkdir rank_genes
        cp ${sep=' ' rank_genes_pngs} rank_genes
    }

    output {
        Array[File] count_matrixes = glob("count_matrixes/*.h5")
        Array[File] umaps = glob("umaps/umap_*.png")
        Array[File] rank_genes = glob("rank_genes/rank_genes_groups_leiden_*.png")
    }
}
