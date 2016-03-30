#!/usr/bin/python
from Bio.Seq import Seq
from Bio import SeqIO
import sys
import os

#creating output file

combined_fasta = open("16s_mock_combined.ffn","w")

#loops through all files in the directory
for fasta_file in os.listdir("."):
    #executes commands on any fasta files found
    if fasta_file.split(".")[1] == "fasta":
        #extracting the file name to use as the header for the multi_fasta file
        seq_name = str(fasta_file.split(".")[0])
        #reading in the sequence
        for input_sequence in  SeqIO.parse(fasta_file,"fasta"):
            #writing out data
            combined_fasta.write(">" + str(seq_name) + "\n" + str(input_sequence.seq) + "\n") 
        
combined_fasta.close()


