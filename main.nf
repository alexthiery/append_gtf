#!/usr/bin/env nextflow
/*

nextflow.enable.dsl = 2

/*
========================================================================================
    IMPORT LOCAL MODULES/SUBWORKFLOWS
========================================================================================
*/

include {GTF_TAG_CHROMS} from './modules/local/gtf_tag_chroms/main'

include {GTF_RENAME_GENES} from './modules/local/gtf_rename_genes/main'

/*
========================================================================================
    IMPORT NF-CORE MODULES/SUBWORKFLOWS
========================================================================================
*/

include { CUSTOM_DUMPSOFTWAREVERSIONS } from './modules/nf-core/modules/custom/dumpsoftwareversions/main'

/*
========================================================================================
    VALIDATE & PRINT PARAMETER SUMMARY
========================================================================================
*/

// Check if --input file is empty
ch_input = file(params.gtf, checkIfExists: true)
if (ch_input.isEmpty()) {exit 1, "File provided with --input is empty: ${ch_input.getName()}!"}

workflow {

    ch_versions = Channel.empty()

    // MODULE: Add prefix to chromosomes of interest
    GTF_TAG_CHROMS( ch_input )
    ch_versions = ch_versions.mix(GTF_TAG_CHROMS.out.versions)

    // MODULE: Modify gene names of interest in GTF
    if (params.rename_genes){
        GTF_RENAME_GENES(GTF_TAG_CHROMS.out.gtf)
        ch_versions = ch_versions.mix(GTF_RENAME_GENES.out.versions)
    }

    //
    // MODULE: Dump software versions for all tools used in the workflow
    //
    CUSTOM_DUMPSOFTWAREVERSIONS (
        ch_versions.unique().collectFile(name: 'collated_versions.yml')
    )
}