#!/usr/bin/python
from Bio import SeqIO
from Bio.Blast import NCBIWWW
from Bio.Blast import NCBIXML
import sys

#open file for writing the results
gc_content = open('gc_content.tsv','w')
gc_content.write("ORF\tLength\tGC_content")

#looping through fasta file
for rec in SeqIO.parse(open(sys.argv[1],"r"), "fasta") :
    #extracting the sequence from the record
    sequence = str(rec.seq)
    #writing a newline to the output file

    gc_content.write("\n")
    #printing the sequence
    print sequence
    #determining if the sequencing contains Ns, if so then it will kick out the sequencing
    if sequence.count('N') > 25:
        print "SEQUENCE BREAK"
        continue
    #sets the variable check equal to the characters G and C
    check = ['G', 'C']
    #creating a dictionary to put the results in

    result = {}
    #looping through the values of the variable check (G and C) to set them equal to 0 in the dictionary
    for char in check:
        #setting the value of each character equal to 0
        result[char] = 0
        #setting the total (G+C) equal to 0
        result["total"] = 0
    #looping through each character in the sequencing

    for char in sequence:
        #checks if the character in the sequencing is a G or C, if so it increments the values in the dictionary by 1
        if char in check:
            result[char] = result[char] + 1
            result["total"] = result["total"] + 1    
    #calculating the GC content from the dictionary values and the length of the sequence, this is really important if it is not done properly python will round the value incorrectly
    GC_percent = 100*int(result['total'])/len(sequence)
    
    #writing the result to the file
    gc_content.write(str(rec.id) + "\t" + str(len(sequence)) + "\t" + str(GC_percent))	    
