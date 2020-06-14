#!/usr/bin/python3
# -*- coding: utf-8 -*-
#Write by: Filipe Dezordi (zimmer.filipe@gmail.com)
#At FioCruz/IAM - 2020/05/25

import argparse,csv,re,os
import pandas as pd

parser = argparse.ArgumentParser(description = 'This script creates itol annotation files',formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("-in", "--input", help="File with sequence names",  required=True)
#A reference file should be parsed, in the same model of 'reference_gisaid.txt' file, but with all current countries present on GISAID.
parser.add_argument("-rf","--reference",help="Reference file with annotation (gisaid regions, country, continent and color, 'reference_gisaid.txt')", required=True)
parser.add_argument("-it","--itol",help="iTol template file, 'iTOL_template.txt' can be used",required=True,)
args = parser.parse_args()
sequence_name_file = args.input
reference_file = args.reference
itol_file = args.itol

#open temp file
annotation_info = open(itol_file+'.info','w',newline='')
writer_out_file = csv.writer(annotation_info)

#create a file with 5 fields, sequence name, branch, color, normal and country
def func_colors(seq_name,reference_file,itol_file):
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
            if row[0] in seq_name:
                if row[0] in 'IAM':
                    writer_out_file.writerow([i.rstrip('\n'),'branch',row[3],'dashed',2,row[1]])
                else:
                    writer_out_file.writerow([i.rstrip('\n'),'branch',row[3],'normal',1,row[1]])
    ref_file.close()

#format sequence name to tree output format sequence names
with open(sequence_name_file,'r') as input_file:
    for i in input_file:
        i = re.sub(r'>','',i)
        i = re.sub(r'/','_',i)
        i = re.sub(r'\|','_',i)
        func_colors(i,reference_file,itol_file)
    annotation_info.close()

#concatenate itol template and annotation file temp output
with open(itol_file) as fp:
    data = fp.read()
with open(itol_file+'.info','r') as fp:
    data2 = fp.read()
data += data2
with open(itol_file+'.branch.txt','w') as output:
    output.write(data)

os.remove(itol_file+'.info')
