#!/usr/local/bin/python

import sys
import argparse
import re

def parse_args(args=None):
    Description = "Reformat nf-core/viralrecon samplesheet file and check its contents."
    Epilog = "Example usage: python check_samplesheet.py <FILE_IN> <FILE_OUT>"

    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--input', type=str, help="Input gtf path.", metavar='')
    parser.add_argument('-o', '--output', type=str, help="Prefix for output gtf file.", metavar='')
    parser.add_argument('--gene_ids', type=str, help="space separated list of gene_ids to be renamed", metavar='', nargs='+', default=None)
    parser.add_argument('--gene_names', type=str, help="space separated list of gene_names to be rename gene_ids with", metavar='', nargs='+', default=None)
    return parser.parse_args(args)

def lists_to_dict(gene_ids, gene_names):
    if len(gene_ids) != len(gene_names):
        sys.exit("Different number of --gene_ids and --gene_names specified!")

    res = {gene_ids[i]: gene_names[i] for i in range(len(gene_ids))}
    return(res)

def rename_genes(gtf, outfile, goi):
        
    gtf =  open(gtf, 'rt')

    # create output file to write to
    outfile = open(outfile, 'a')

    for line in gtf:
        if 'gene_id' in line:
    #       Check if any gene_ids in line
            if any(gene_id in line for gene_id in goi.keys()):
    #           Get matching gene name from dict
                gene_name = [gene_name for gene_id, gene_name in goi.items() if gene_id in line]
    #           If gene_name is already in line - remove and replace
                if 'gene_name' in line:
                    line = re.sub('gene_name.*?;', '', line, flags=re.DOTALL)
                line = line.rstrip() + ' gene_name "' + gene_name[0] + '";\n'
        outfile.write(line)


def main(args=None):
    args = parse_args(args)
    goi = lists_to_dict(gene_ids=args.gene_ids, gene_names=args.gene_names)
    rename_genes(gtf = args.input, outfile = args.output, goi = goi)

if __name__ == '__main__':
    sys.exit(main())
    