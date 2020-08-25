#!/usr/bin/python3
# -*- coding: utf-8 -*-
#Written by: Filipe Dezordi (https://dezordi.github.io/)
#At FioCruz/IAM - 2020/07/06

import argparse, csv
from Bio import AlignIO
parser = argparse.ArgumentParser(description = 'This script inform the nucleotide or aminoacid present on specific sites (-st)')

parser.add_argument("-in", "--input", help="Alignment file", required=True)
parser.add_argument("-st","--sites",help="Pass specific sites positions in a crescent order (e.g. 5 14 94 121)", type=int, nargs='+')
args = parser.parse_args()
alignment_file = args.input
sites = args.sites
sites_header = ['Genomes']
for i in sites:
    sites_header.append(i)

alignment = AlignIO.read(open(alignment_file), "fasta")
output = open(alignment_file+".info.tsv",'w')
output_writer = csv.writer(output, delimiter='\t')
output_writer.writerow(sites_header)

for record in alignment:
    list_teste = [] 
    base_number = 1
    list_teste.append(record.id)
    for base in record.seq:
        if base_number in sites:
            list_teste.append(base)
        base_number += 1
    output_writer.writerow(list_teste)
