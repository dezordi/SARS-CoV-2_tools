#!/usr/bin/python3
# -*- coding: utf-8 -*-

import argparse,csv,re
import pandas as pd

parser = argparse.ArgumentParser(description = 'This script creates itol annotation files',formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument("-in", "--input", help="File with sequence names",  required=True)
parser.add_argument("-rf","--reference",help="Reference file with annotation (colors, shapes, etc)", required=True)
parser.add_argument("-fc","--function",help="Function of annotation (color, shapes, domainss)", default='color')
parser.add_argument("-it","--itool",help="iTol template file",required=True,)
args = parser.parse_args()

sequence_name_file = args.input
reference_file = args.reference
function_type = args.function
itool_file = args.itool

annotation_info = open(itool_file+'.info','w',newline='')
writer_out_file = csv.writer(annotation_info)

def func_colors(seq_name,reference_file,itool_file):
    with open(reference_file,'r') as ref_file, open(itool_file,'r') as itool_mod:
        data_csv = csv.reader(ref_file)
        for row in data_csv:
            if row[0] in seq_name:
                if row[0] in 'IAM':
                    writer_out_file.writerow([i.rstrip('\n'),'branch',row[3],'dashed',row[1]])
                else:
                    writer_out_file.writerow([i.rstrip('\n'),'branch',row[3],'normal',row[1]])
    #annotation_info.close()

with open(sequence_name_file,'r') as input_file:
    for i in input_file:
        i = re.sub(r'>','',i)
        i = re.sub(r'/','_',i)
        i = re.sub(r'\|','_',i)
        func_colors(i,reference_file,itool_file)

with open(itool_file) as fp:
    data = fp.read()
with open(itool_file+'.info','r') as fp:
    data2 = fp.read()
data += data2

with open(itool_file+'.branch.txt','w') as output:
    output.write(data)
