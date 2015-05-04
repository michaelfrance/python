#!/usr/bin/python
from Bio.Seq import Seq
from Bio import SeqIO
import sys

#asks the user for the genome file name

filepath = sys.argv[1]

#splits the ending off the name so that it can be used to name the output file
name = filepath.split('.')[-2]

#creating an empty string variable
Genome = ''

#looping through the input file

for rec in SeqIO.parse(open(filepath,"r"), "fasta") :
    #pasting the contigs together with 50Ns between each
    Genome += rec + ("N" * 50) 

#giving it an id and description, could probably make this more informative
Genome.id = "mergedseq"
Genome.description = "merged seq"
#writing the Genome string variable to a fasta file
SeqIO.write(Genome, "%s_combined.fasta" %(name), "fasta")




