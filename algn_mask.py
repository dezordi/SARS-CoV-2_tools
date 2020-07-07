#!/usr/bin/python3
# -*- coding: utf-8 -*-
#Write by: Filipe Dezordi (zimmer.filipe@gmail.com)
#At FioCruz/IAM - 2020/07/06

from Bio import AlignIO
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq
from Bio import SeqIO
import argparse


parser = argparse.ArgumentParser(description = 'This script masks hCoV-19 alignment.',formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("-in", "--input", help="Fasta file.",  required=True)
parser.add_argument("-mk","--mask",help="Mask alignment file? Mask positions according 'Issues with hCoV-19 sequencing data' Maio et al, 2020.\nCAUTION: your alignment should be referenced to MN908947.3.\nDefault = True.\nSet false if only gaps should be masked",choices=['False','True'],default='True')
args = parser.parse_args()
input_file = args.input
mask = args.mask

#Format output name
if mask == 'True':
    ext = '.mk.fasta'
else:
    ext = '.nogap.fasta'

#Open aligment and output file
alignment = AlignIO.read(open(input_file),'fasta')
output_handle = open(input_file+ext, "w")

#Regions and sites to mask according Maio et al, 2020.
mask_ranges = [[0,54],[29803,29902]]
mask_sites = [186,240,334,1058,2093,3036,3129,3144,4049,6254,6989,8021,8781,9222,10322,10740,11073,11082,11703,13401,13407,14407,14723,14785,14804,15323,16886,17246,19683,20147,21136,21574,23402,24033,24377,25562,26143,26460,26680,27383,28076,28825,28853,29352,29699,29735]

#For each sequence in alignment, mask regions and sites with putative sequencing errors, gaps and non-specific nucleotides [^ATCG] (if -mk True), or just gaps and non-specific nucleotides (if -mk False).
for record in alignment:
    new_seq_lst = list(record.seq)
    new_seq = ''
    record_lst = []
    if mask == 'True':
        for i in mask_ranges:
            for n in range(i[0],i[1]+1):
                new_seq_lst[n] = 'N'
        for i in mask_sites:
            new_seq_lst[i] = 'N'
    for letter in new_seq_lst:
        if letter not in 'ATCGatcg':
            letter = 'N'
        new_seq += letter
    record = SeqRecord(Seq(new_seq), id=record.id, description = '')
    record_lst.append(record)
    SeqIO.write(record_lst,output_handle,'fasta')