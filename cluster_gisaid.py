#!/usr/bin/python3
# -*- coding: utf-8 -*-
#Written by: Filipe Dezordi (https://dezordi.github.io/)
#At FioCruz/IAM - 2020/07/06

import argparse, subprocess, shlex, csv, re, os
parser = argparse.ArgumentParser(description = 'This script automatize cd-hit-est hCoV-19 genomes from GISAID by country',formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument("-in", "--input", help="Fasta file.",  required=True)
#A reference file should be parsed, in the same model of 'reference_gisaid.csv' file, but with all current countries present on GISAID up to June 03 2020.
parser.add_argument("-rf","--reference",help="Reference file with annotation (reference_gisaid.csv)", required=True)
parser.add_argument("-p","--threads",help="Threads for cd-hit-est analyze.", default = 1, type=int)
parser.add_argument("-m","--memory",help="Memory in MB for cd-hit-est analyze",default = 2000, type=int)
args = parser.parse_args()
sequence_name_file = args.input
reference_file = args.reference
var_threads = args.threads
var_memory = args.memory

input_names = open(sequence_name_file+'.names.txt','w')

#store all sequence names from fasta file.
with open(sequence_name_file,'r') as input_read:
    for line in input_read:
        if '>' in line:
            input_names.write(line)
input_names.close()
list_to_cd_hit = []
#Create files with extesion '.names' containing all fasta names per country
with open(reference_file,'r') as input_reference, open(sequence_name_file+'.names.txt') as name_reader:
    list_of_lines_reference = input_reference.readlines()
    csv_reader = csv.reader(list_of_lines_reference)
    list_of_lines_name = name_reader.readlines()
    for line_ref in csv_reader:
        with open(line_ref[1]+'.names','a') as country_list_file:
            for line_name in list_of_lines_name:
                if line_ref[0] in line_name:
                    line_name = re.sub(r'>','',line_name)
                    country_list_file.write(line_name)
        if os.stat(line_ref[1]+'.names').st_size == 0:
            os.remove(line_ref[1]+'.names')
        else:
            if line_ref[1]+'.names' not in list_to_cd_hit:
                list_to_cd_hit.append(line_ref[1]+'.names')
            else:
                pass

#list with all files with sequence names by country.
seqtk_output_list = []

#Generates fasta files for each country, using the previous list 'list_to_cd_hit'
for file_name in list_to_cd_hit:
    with open(file_name+'.fasta','w') as seqtk_out:
        seqtk_cmd = 'seqtk subseq '+sequence_name_file+' '+file_name
        seqtk_cmd = shlex.split(seqtk_cmd)
        seqtk_cmd_process = subprocess.Popen(seqtk_cmd,stdout = seqtk_out)
        seqtk_cmd_process.wait()
        seqtk_output_list.append(file_name+'.fasta')

#Run cd-hit-est for each file, considering only identical sequences to perform clusterizations
for output_name in seqtk_output_list:
    with open(output_name+'.cd-hit.log','w') as cd_hit_log:
        cd_hit_out = output_name+'.cd'
        cd_hit_est_cmd = 'cd-hit-est -i '+output_name+' -o '+cd_hit_out+' -c 1 -s 1 -M '+str(var_memory)+' -T '+str(var_threads)+' -d 200'
        cd_hit_est_cmd = shlex.split(cd_hit_est_cmd)
        cd_hit_est_cmd_process = subprocess.Popen(cd_hit_est_cmd,stdout = cd_hit_log)
        cd_hit_est_cmd_process.wait()