#!/usr/bin/python3
# -*- coding: utf-8 -*-
#Written by: Filipe Dezordi (https://dezordi.github.io/)
#At FioCruz/IAM - 2020/07/06

import argparse, subprocess, shlex, csv, re, os
import pandas as pd

parser = argparse.ArgumentParser(description = 'This script returns nucleotide diversy per SNP position and metrics about SNPs by hCoV-19 genome region.')
parser.add_argument("-sn", "--snp_pos", help="SNPs positions in a txt file, onde position per line",  required=True)
parser.add_argument("-bc","--bam_readcount",help="bam-readcount output file", required=True)

args = parser.parse_args()
snp_file = args.snp_pos
bam_rc_file = args.bam_readcount
prefix = snp_file
prefix = re.sub("\..*","",prefix)
prefix = re.sub('.*/','',prefix).rstrip('\n')

"""
Genes position
UTR5 = [1,265]
ORF1AB = [266,21555]
S = [21563,25384]
ORF3A = [25393,26220]
E = [26242,26472]
M = [26523,27191]
ORF6 = [27202,27387]
ORF7A = [27394,27759]
ORF7B = [27756,27887]
ORF8 = [27894,28259]
N = [28274,29533]
ORF10 = [29558,29674]
UTR3 = [29675,29903]
"""

with open(snp_file,'r') as snp_in_file, open(snp_file+'.distr.tsv','w') as snp_file_out:
    reader_snp_in_file = snp_in_file.readlines()
    output_csv_writer = csv.writer(snp_file_out,delimiter='\t')
    output_csv_writer.writerow(['GENOME','POS','REGION','DEPTH','A_DEPTH','A_PLUS','A_MINUS','C_DEPTH','C_PLUS','C_MINUS','G_DEPTH','G_PLUS','G_MINUS','T_DEPTH','T_PLUS','T_MINUS','N'])
    out_list = []
    for snp_line in reader_snp_in_file:
        snp_line = snp_line.rstrip('\n')      
        with open(bam_rc_file,'r') as bam_rc_file_in: #, open(bam_rc_file+'.csv','w') as output_csv:
            bam_rc_file_read = csv.reader(bam_rc_file_in, delimiter='\t')
            for line in bam_rc_file_read:
                if snp_line == line[1]:
                    var_pos = line[1].rstrip('\n')
                    var_depth = line[3].rstrip('\n')
                    A_depth_line = line[5].rstrip('\n')
                    A_depth = ":".join(A_depth_line.split(":", 2)[:2])
                    A_depth = re.sub(r".*:","",A_depth)
                    A_plus = ":".join(A_depth_line.split(":", 6)[:6])
                    A_plus = re.sub(r".*:","",A_plus)
                    A_minus = ":".join(A_depth_line.split(":", 7)[:7])
                    A_minus = re.sub(r".*:","",A_minus)
                    C_depth_line = line[6].rstrip('\n')
                    C_depth = ":".join(C_depth_line.split(":", 2)[:2])
                    C_depth = re.sub(r".*:","",C_depth)
                    C_plus = ":".join(C_depth_line.split(":", 6)[:6])
                    C_plus = re.sub(r".*:","",C_plus)
                    C_minus = ":".join(C_depth_line.split(":", 7)[:7])
                    C_minus = re.sub(r".*:","",C_minus)
                    G_depth_line = line[7].rstrip('\n')
                    G_depth = ":".join(G_depth_line.split(":", 2)[:2])
                    G_depth = re.sub(r".*:","",G_depth)
                    G_plus = ":".join(G_depth_line.split(":", 6)[:6])
                    G_plus = re.sub(r".*:","",G_plus)
                    G_minus = ":".join(G_depth_line.split(":", 7)[:7])
                    G_minus = re.sub(r".*:","",G_minus)
                    T_depth_line = line[8].rstrip('\n')
                    T_depth = ":".join(T_depth_line.split(":", 2)[:2])
                    T_depth = re.sub(r".*:","",T_depth)
                    T_plus = ":".join(T_depth_line.split(":", 6)[:6])
                    T_plus = re.sub(r".*:","",T_plus)
                    T_minus = ":".join(T_depth_line.split(":", 7)[:7])
                    T_minus = re.sub(r".*:","",T_minus)
                    N_depth = line[9].rstrip('\n')
                    N_depth = ":".join(N_depth.split(":", 2)[:2])
                    N_depth = re.sub(r".*:","",N_depth)
                    if int(var_pos) <= 265:
                        region = '5UTR'
                    elif int(var_pos) <= 21555:
                        region = 'ORF1AB'
                    elif int(var_pos) <= 25384:
                        region = 'S'
                    elif int(var_pos) <= 26220:
                        region = 'ORF3A'
                    elif int(var_pos) <= 26472:
                        region = 'E'
                    elif int(var_pos) <= 27191:
                        region = 'M'
                    elif int(var_pos) <= 27387:
                        region = 'ORF6'
                    elif int(var_pos) <= 27759:
                        region = 'ORF7A'
                    elif int(var_pos) <= 27887:
                        region = 'ORF7B'
                    elif int(var_pos) <= 28259:
                        region = 'ORF8'
                    elif int(var_pos) <= 29533:
                        region = 'N'
                    elif int(var_pos) <= 29674:
                        region = 'ORF10'
                    else:
                        region = '3UTR'
                    out_list.append([prefix,var_pos,region,var_depth,A_depth,A_plus,A_minus,C_depth,C_plus,C_minus,G_depth,G_plus,G_minus,T_depth,T_plus,T_minus,N_depth])
    output_csv_writer.writerows(out_list)
df = pd.read_csv(snp_file+'.distr.tsv',sep='\t')
df2 = df[['REGION','DEPTH']]
df2 = pd.DataFrame(group.describe().loc[['count','min','max','mean','std']].rename(columns={'DEPTH':name}).squeeze()for name, group in df2.groupby('REGION'))
df2 = df2.round(2)
df2.insert(loc=0,column='GENOME',value=prefix)
df2.to_csv(snp_file+'.metrics.tsv',sep='\t')