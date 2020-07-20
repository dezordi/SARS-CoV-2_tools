#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#Base code from https://biopython.org/wiki/Sequence_Cleaner
#Modified by Filipe Dezordi (https://dezordi.github.io/)
#At FioCruz/IAM - 2020/07/06

import argparse
from Bio import SeqIO

parser = argparse.ArgumentParser(description = 'This script removes sequences by length and N% tresholds.')
parser.add_argument("-in", "--input", help="Fasta file",  required=True)
parser.add_argument("-lg","--min_length",help="Length threshold", required=True)
parser.add_argument("-np","--n_per",help="N percentage", default=5)

args = parser.parse_args()
fasta_file = args.input
min_length = args.min_length
n_per = args.n_per

#check if sequences have the min length and are bellow the percentage of N parsed.
def fasta_clean(file, length, n_per):
    """
    This function execute the cleanning steps..

    Keyword arguments:
    file - fasta file, parsed with -in argument
    length - treshold length value, parsed with -ln argument
    n_per - treshold N percentage value, parsed with -np argument.
    """
    sequences={}
    for seq_record in SeqIO.parse(fasta_file, "fasta"):
        sequence = str(seq_record.seq)
        if (len(sequence) >= float(min_length) and (float(sequence.count("n")+sequence.count("N"))/float(len(sequence)))*100 <= float(n_per)):
            if sequence not in sequences:
                sequences[sequence] = seq_record.id
    with open(fasta_file+'.clean', "w+") as output_file:
        for sequence in sequences:
            output_file.write(">" + sequences[sequence] + "\n" + sequence + "\n")
            
try:
    fasta_clean(fasta_file,min_length,n_per)
    print('DONE.')
except:
    print('Some error occurred')