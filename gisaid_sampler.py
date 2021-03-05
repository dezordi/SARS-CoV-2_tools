#!/usr/bin/python3
# -*- coding: utf-8 -*-
#Written by: Filipe Dezordi (https://dezordi.github.io/)
#At FioCruz/IAM - 2020/07/06

import argparse, subprocess, shlex, csv, re, os
import pandas as pd
from sklearn.utils import shuffle 

parser = argparse.ArgumentParser(description = 'This script creates sample files of hCoV-19 Genomes considering redundancy between country and day or week of collection, genomes without complete date of collection are discarted',formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument("-in", "--input", help="Fasta file.",  required=True)
#A reference file should be parsed, in the same model of 'reference_gisaid.csv' file, but with all current countries present on GISAID up to June 03 2020.
parser.add_argument("-rf","--reference",help="Reference file with annotation (reference_gisaid.csv).", required=True)
parser.add_argument("-gp","--groupby",help="Group by Day or Week? default=Day",default='Day',choices=['Day','Week'])
args = parser.parse_args()
sequence_name_file = args.input
reference_file = args.reference
group_opt = args.groupby

input_names = open(sequence_name_file+'.names.txt','w')

#store all sequence names from fasta file.
with open(sequence_name_file,'r') as input_read:
    for line in input_read:
        if '>' in line:
            input_names.write(line)
input_names.close()

with open(sequence_name_file+'.names.txt','r') as input_seqs,open(sequence_name_file+'.tmp','w') as tmp_out_csv:
    tmp_out_csv_writer = csv.writer(tmp_out_csv,delimiter=',')
    tmp_out_csv_writer.writerow(['Genome','Country','Year','Month','Day'])
    read_input_seqs = input_seqs.readlines()
    list_csv = []
    #create a csv file with genome name and country,year,month and day
    for line in read_input_seqs:
        if '2021' in line:
            genome_name = re.sub(r'>','',line).rstrip('\n')
            date_year = re.sub(r'.*2021','2021',line)
            date_year = re.sub(r'-.*','',date_year).rstrip('\n')
            date_month = re.sub(r'.*2021-','',line)
            date_month = re.sub(r'-.*','',date_month).rstrip('\n')
            if 'hCoV' in date_month:
                date_month = ''
            date_day = re.sub(r'.*2020-[0-9]*-','',line).rstrip('\n')
            if 'hCoV' in date_day:
                date_day = ''
        elif '2020' in line:
            genome_name = re.sub(r'>','',line).rstrip('\n')
            date_year = re.sub(r'.*2020','2020',line)
            date_year = re.sub(r'-.*','',date_year).rstrip('\n')
            date_month = re.sub(r'.*2020-','',line)
            date_month = re.sub(r'-.*','',date_month).rstrip('\n')
            if 'hCoV' in date_month:
                date_month = ''
            date_day = re.sub(r'.*2020-[0-9]*-','',line).rstrip('\n')
            if 'hCoV' in date_day:
                date_day = ''
        elif '2019' in line:
            genome_name = re.sub(r'>','',line).rstrip('\n')
            date_year = re.sub(r'.*2019','2019',line)
            date_year = re.sub(r'-.*','',date_year).rstrip('\n')
            date_month = re.sub(r'.*2019-','',line)
            date_month = re.sub(r'-.*','',date_month).rstrip('\n')
            if 'hCoV' in date_month:
                date_month = ''
            date_day = re.sub(r'.*2019-[0-9]*-','',line).rstrip('\n')
            if 'hCoV' in date_day:
                date_day = ''
        with open(reference_file,'r') as input_ref:
            read_input_ref = csv.reader(input_ref,delimiter=',')
            for line_ref in read_input_ref:
                if line_ref[0] in line:
                    list_csv.append([genome_name,line_ref[1],date_year,date_month,date_day])
    tmp_out_csv_writer.writerows(list_csv)

with open(sequence_name_file+'.tmp','r') as tmp_input:
    df =  pd.read_csv(tmp_input, sep=',')
    if group_opt == 'Week': #If Week as parsed with -gb, the days will be grouped in 5 different weeks
        df['Day'].loc[(df['Day'] <= 6)] = 1
        df['Day'].loc[(df['Day'] >6) & (df['Day'] <= 13)] = 2
        df['Day'].loc[(df['Day'] >13) & (df['Day'] <= 20)] = 3
        df['Day'].loc[(df['Day'] >20) & (df['Day'] <= 26)] = 4
        df['Day'].loc[(df['Day'] >26) & (df['Day'] <= 31)] = 5
        df.columns = ['Genome','Country','Year','Month','Week']
        df = shuffle(df)
        df2 = df.drop_duplicates(subset=['Country','Year','Month','Week']).sort_values(by=['Year','Month','Week'],ascending=True)
    else:
        df2 = df.drop_duplicates(subset=['Country','Year','Month','Day']).sort_values(by=['Year','Month','Day'],ascending=True)
    df2 = df2.dropna()
    
with open(sequence_name_file+'.'+group_opt+'.filtred','w') as df_output:
    df2.to_csv(df_output, sep=',', index = False)

os.remove(sequence_name_file+'.tmp')
os.remove(sequence_name_file+'.names.txt')