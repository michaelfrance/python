#!/usr/bin/python

#loading in required python modules
from Bio import SeqIO
from Bio.Blast import NCBIWWW
from Bio.Blast import NCBIXML
import sys
import matplotlib.pyplot as pyplot


#setting the start as 0
position = 0

#extracting the window size and the movement length from the command line entry
window_size= int(sys.argv[2])
move_length= int(sys.argv[3])

#reading in the genome from fasta file
fasta_input = SeqIO.read(open(sys.argv[1],"r"), "fasta")

#extracting the raw sequence from the sequence object
sequence=str(fasta_input.seq)

#determining the length of the genome
seq_length=len(fasta_input)

#calculating the number of iterations neccessary to cover entire genome
iterations = int(seq_length/window_size)*(window_size/move_length)

#printing useful information
print seq_length
print window_size
print iterations

#setting a counter variable to keep track of loop
count=1

#creating two blank lists for the plot
x=list()
y=list()


#creating a tab separated file for writing, will store results in here
gc_content = open('gc_content_%s_%s.tsv' %(window_size,move_length),'w')
gc_content.write("Start\tEnd\tGC_content")

#looping through the sequence, look window each time and then moving by the movement length
for i in range(0,iterations):

    #calculating the end of the window

    end = position+window_size
    
    #incrimenting the count
    count += 1
    #pulling out the window sequence for analysis

    window_sequence = sequence[int(position):int(end)]
    
    #moving the position along for the next iteration

    position = position + move_length
    
    #writing a new line to our output tab sep file
    gc_content.write("\n")
    
    #creating a variable that contains G and C to match against
    check = ['G', 'C']
 
    #creating a blank dictionary to store results in
    result = {}
    
    #looping through chech variable to create entries in dictionary
    for char in check:
        result[char] = 0
 
        result["total"] = 0

    #looping through window sequence and incrimenting if G or C
    for char in window_sequence:
        if char in check:
            result[char] = result[char] + 1
            result["total"] = result["total"] + 1    

    #calculating the percent GC using the dictionary data
    GC_percent = 100*int(result['total'])/len(window_sequence)
    
    #writing results to file
    gc_content.write(str(position) + "\t" + str(end) + "\t" + str(GC_percent))	    
    
    #appending the start and gc percent to x and y lists for plotting
    x.append(position)
    y.append(GC_percent)


#making a very basic plot of the data
pyplot.plot(x,y)
pyplot.savefig('gc_content%s_%s' %(window_size,move_length)) 
