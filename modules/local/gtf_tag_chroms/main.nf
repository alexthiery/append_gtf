process GTF_TAG_CHROMS {
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
    prefix = task.ext.prefix ?: "tag_chroms"

    """
    gtf_tag_chroms.py \\
        --gtf ${gtf} \\
        --output ${prefix}.gtf \\
        ${args}

    cat <<-END_VERSIONS > versions.yml
    "${task.process}":
        python: \$(python --version | sed 's/Python //g')
    END_VERSIONS   
    """
}


