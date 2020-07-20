#!/usr/bin/python3
# -*- coding: utf-8 -*-
#Written by: Filipe Dezordi (https://dezordi.github.io/)
#At FioCruz/IAM - 2020/07/06

import argparse,csv,re,os
import pandas as pd

parser = argparse.ArgumentParser(description = 'This script creates itol annotation files from pangolin csv output',formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("-in", "--input", help="Pangolin output csv file",  required=True)
#A reference file should be parsed, in the same model of 'reference_pangolin.csv' file, but with all current lineages present on pangolin.
parser.add_argument("-rf","--reference",help="Pangolin reference csv file, with lineage and color (reference_pangolin.csv)", required=True)
parser.add_argument("-it","--itol",help="iTOL template file (iTOL_template.txt)",required=True,)
args = parser.parse_args()
pangolin_file = args.input
reference_file = args.reference
itol_file = args.itol

#create temp output file
annotation_info = open(itol_file+'.info','w',newline='')
writer_out_file = csv.writer(annotation_info)

#create a file with 4 fields, sequence name, range, color, lineage
def func_colors(seq_name,seq_lineage,reference_file,itol_file):
    """
    This function execute the match between contries in name sequences and contries in reference file.

    Keyword arguments:
    seq_name - txt file with sequence names, parsed with -in argument.
    reference_file - gisaid reference csv file, parsed with -rf argument.
    itol_file - iTOL template file, parsed with -it argument.
    """
    with open(reference_file,'r') as ref_file, open(itol_file,'r') as itol_mod:
        data_csv = csv.reader(ref_file)
        for row in data_csv:
            if row[0] == seq_lineage:
                writer_out_file.writerow([i.rstrip('\n'),'range',row[1],seq_lineage])

with open(pangolin_file,'r') as input_file:
    pangolin_csv = csv.reader(input_file)
    for x in pangolin_csv:
        i = x[0]
        i_l = x[1]
        i = re.sub(r'>','',i)
        i = re.sub(r'/','_',i)
        i = re.sub(r'\|','_',i)
        func_colors(i,i_l,reference_file,itol_file)
    annotation_info.close()

#concatenate itol template and annotation file temp output
with open(itol_file) as fp:
    data = fp.read()
with open(itol_file+'.info','r') as fp:
    data2 = fp.read()
data += data2

with open(itol_file+'.range.txt','w') as output:
    output.write(data)

os.remove(itol_file+'.info')