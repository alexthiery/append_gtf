#!/usr/bin/env python

import argparse
import pandas as pd
import re
import sys

def parse_args(args=None):
    parser = argparse.ArgumentParser(
        description="Rename SRA fastq files to 10x format",
        epilog="Example usage: python rename_fastq_10x.py --suffix_1 R1 --suffix_2 R2 --suffix_3 I1",
    )
    parser.add_argument('--chroms', type=str, help="space separated list of chromsosomes for which to tag genes names with", metavar='', nargs='+', default=None)
    parser.add_argument('--gtf', type=str, help="path to gtf file", metavar='')
    parser.add_argument('--output', type=str, help="path for output gtf file", metavar='')
    return parser.parse_args(args)

def check_args(args):
    if args.chroms is None:
        sys.exit('--chroms not specified! No genes are tagged with chrom ids.')

def tag_genes(args):
    # create output file to write to
    outfile = open(args.output, 'a')

    with open(args.gtf, 'rt') as gtf:
        for gene in gtf:
            # only search genes with gene_id in order to skip header genes
            if 'gene_id' in gene:

                # change names for genes from chroms of interest
                chrom_name = gene.split()[0]

                if chrom_name in args.chroms:
                    gene = re.sub('gene_id "', 'gene_id "'+''.join(chrom_name)+'-', gene)

                    if 'gene_name' in gene:
                        gene = re.sub('gene_name "', 'gene_name "'+''.join(chrom_name)+'-', gene)

            outfile.write(gene)

def main(args=None):
    args = parse_args(args)
    check_args(args = args)
    tag_genes(args = args)

if __name__ == "__main__":
    sys.exit(main())
