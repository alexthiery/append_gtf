process GTF_RENAME_GENES {
    tag "$gtf"
    label 'process_low'

    container "quay.io/biocontainers/bioframe:0.0.12--pyh3252c3a_0"

    input:
    path gtf

    output:
    path "${prefix}.gtf", emit: gtf
    path "versions.yml"                , emit: versions

    script:
    def args = task.ext.args  ?: ''
    prefix = task.ext.prefix ?: "rename_genes"

    """
    gtf_rename_genes.py \\
        --input ${gtf} \\
        --output ${prefix}.gtf \\
        ${args}

    cat <<-END_VERSIONS > versions.yml
    "${task.process}":
        python: \$(python --version | sed 's/Python //g')
    END_VERSIONS   
    """
}


