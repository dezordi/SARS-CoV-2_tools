#!/usr/bin/python3
# -*- coding: utf-8 -*-

import argparse,csv,re
import pandas as pd

parser = argparse.ArgumentParser(description = 'This script creates itol annotation files',formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument("-in", "--input", help="Pangolin output csv file",  required=True)
#parser.add_argument("-lc", "--lineage_color", help="CSV file with SARS-CoV-2 lineages and rbg color code",  required=True)
parser.add_argument("-it","--itool",help="iTol template file",required=True,)

args = parser.parse_args()

sequence_name_file = args.input
#color_code = args.lineage_color
itool_file = args.itool
color_code = [['NA','#800000'],['A','#8B0000'],['A.1','#A52A2A'],['A.1.1','#B22222'],['A.1.3','#DC143C'],['A.2','#FF0000'],['A.3','#FF6347'],['A.4','#FF7F50'],['A.5','#CD5C5C'],['A.6','#F08080'],['A.p7','#0000FF'],['B','#0000EE'],['B.1','#0000CD'],['B.1.1','#00008B'],['B.1.1.1','#000080'],['B.1.1.2','#191970'],['B.1.1.3','#3D59AB'],['B.1.1.4','#4169E1'],['B.1.1.5','#4876FF'],['B.1.1.6','#436EEE'],['B.1.1.7','#3A5FCD'],['B.1.1.8','#27408B'],['B.1.1.9','#6495ED'],['B.1.1.10','#B0C4DE'],['B.1.1.13','#CAE1FF'],['B.1.1.14','#BCD2EE'],['B.1.1.17','#A2B5CD'],['B.1.1.18','#6E7B8B'],['B.1.1.p11','#778899'],['B.1.1.p12','#708090'],['B.1.1.p15','#C6E2FF'],['B.1.1.p16','#B9D3EE'],['B.1.1.p19','#9FB6CD'],['B.1.3','#6C7B8B'],['B.1.5','#1E90FF'],['B.1.5.1','#1C86EE'],['B.1.5.2','#1874CD'],['B.1.5.3','#104E8B'],['B.1.5.4','#F0F8FF'],['B.1.5.5','#4682B4'],['B.1.5.6','#63B8FF'],['B.1.6','#5CACEE'],['B.1.8','#4F94CD'],['B.1.12','#36648B'],['B.1.13','#87CEFA'],['B.1.19','#B0E2FF'],['B.1.22','#A4D3EE'],['B.1.23','#8DB6CD'],['B.1.26','#607B8B'],['B.1.29','#87CEFF'],['B.1.30','#7EC0EE'],['B.1.31','#6CA6CD'],['B.1.32','#4A708B'],['B.1.33','#87CEEB'],['B.1.34','#00BFFF'],['B.1.35','#00B2EE'],['B.1.36','#009ACD'],['B.1.37','#00688B'],['B.1.38','#33A1C9'],['B.1.39','#ADD8E6'],['B.1.40','#BFEFFF'],['B.1.41','#B2DFEE'],['B.1.43','#9AC0CD'],['B.1.44','#68838B'],['B.1.66','#B0E0E6'],['B.1.67','#98F5FF'],['B.1.69','#8EE5EE'],['B.1.70','#7AC5CD'],['B.1.71','#53868B'],['B.1.72','#00F5FF'],['B.1.p11','#00E5EE'],['B.1.p16','#00C5CD'],['B.1.p2','#00868B'],['B.1.p21','#5F9EA0'],['B.1.p25','#00CED1'],['B.1.p42','#F0FFFF'],['B.1.p68','#E0EEEE'],['B.1.p73','#C1CDCD'],['B.1.p9','#838B8B'],['B.2','#E0FFFF'],['B.2.1','#D1EEEE'],['B.2.2','#B4CDCD'],['B.2.4','#7A8B8B'],['B.2.5','#BBFFFF'],['B.2.6','#AEEEEE'],['B.2.7','#96CDCD'],['B.3','#668B8B'],['B.4','#2F4F4F'],['B.5','#97FFFF'],['B.6','#8DEEEE'],['B.7','#79CDCD'],['B.9','#528B8B'],['B.10','#00FFFF'],['B.13','#00EEEE'],['B.14','#00CDCD'],['B.15','#008B8B'],['B.16','#008080'],['B.p11','#48D1CC'],['B.p12','#20B2AA']]
color = ''

annotation_info = open(itool_file+'.pan.info','w',newline='')
writer_out_file = csv.writer(annotation_info)

def func_colors(pangolin_file, itool_file):
    with open(pangolin_file,'r') as pan_file, open(itool_file,'r') as itool_mod:
        data_csv = csv.reader(pan_file)
        for row in data_csv:
            seq_name = row[0]
            seq_name = seq_name.rstrip('\n')
            group = row[1]
            group = group.rstrip('\n')
            seq_name = re.sub(r'>','',seq_name)
            seq_name = re.sub(r'/','_',seq_name)
            seq_name = re.sub(r'\|','_',seq_name)
            for i in color_code:
                
                pan_lin = i[0]
                if group == pan_lin:
                    break
                color = i[1]
            writer_out_file.writerow([seq_name,'range',color,group])
            #print(seq_name,group,color)

func_colors(sequence_name_file,itool_file)

with open(itool_file) as fp:
    data = fp.read()
with open(itool_file+'.pan.info','r') as fp:
    data2 = fp.read()
data += data2

with open(itool_file+'.range.txt','w') as output:
    output.write(data)