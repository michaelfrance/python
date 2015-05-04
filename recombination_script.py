#!/usr/bin/python
from Bio.Blast import NCBIWWW
from Bio.Blast import NCBIXML
from Bio.Blast.Applications import NcbiblastxCommandline
from Bio import SeqIO

#asks the user for the genome file name
Filename = raw_input("Input genome file name 5' to 3': ")

Genome = ''

#opens the give file
for rec in SeqIO.parse(open(Filename,"r"), "fasta") :
    Genome += rec + ("N" * 50) 

Genome.id = "mergedseq"
Genome.description = "merged seq"
SeqIO.write(Genome, "Genome.fasta", "fasta")

Genome = ""

Genome = open('Genome.fasta').read()

#removes the top line that contains the fasta  	header
Genome = "\n".join(Genome.split('\n')[1:])


#removes all of the newline expressions from the file
Genome = Genome.replace('\n', '')

#determines genome size
Length = len(Genome)

#windows size and slide setting
Slide = 100
Window_size = 500

#number of blast searchs required
Num_Blasts = Length/250

#creating the output file and labeling the column headings
recomb_out = open('blast_results.tsv','w')
recomb_out.write("Start\tEnd\tGC_content\tr1\tr2\tr3\tr4\tr5\tr6\tr7\tr8\tr9\tr10")

#creating an output file for the candidate genes
candidate_out = open('candidate_foreign_DNA.tsv','w')
candidate_out.write('Start\tEnd\tGC_content\tnumhits\tsequence')

#creating the sliding window
for window in range(0,int(Num_Blasts)):
    #moveing the output to a new line
    recomb_out.write("\n")

    #defining the window start and end
    start_window = Slide*window
    end_window = Slide*(window+Window_size)

    #extracting the sequence from the genome
    sequence = Genome[start_window:end_window]

    #forces the string into uppercase just in case it isn't
    sequence = sequence.upper()
    
    if sequence.count('N') > 25:
        print "SEQUENCE BREAK"
        continue

    #determining the GC content of the window
    #GC_window = sequence.count("G") + sequence.count("C")/len(sequence)    , this is the old way it is slower
    check = ['G', 'C']
 
    result = {}
    for char in check:
        result[char] = 0
 
        result["total"] = 0
 
    for char in sequence:
        if char in check:
            result[char] = result[char] + 1
            result["total"] = result["total"] + 1    

    GC_percent = 100*int(result['total'])/len(sequence)
    #print GC_percent

    completion =100*float("%.2f" %(window/float(Num_Blasts)))
    print(str(completion) + " Percent Complete\r")

    #writing the start and end location as well as the GC content of the window to the file
    recomb_out.write(str(start_window) + "\t" + str(end_window) + "\t" + str(GC_percent) + "\t" )    


    #output the file into a fasta format so that it can be used in the standalone blast
    fragSeq = open('fragment.fasta','w')
    fragSeq.write('>fragment' + '\n' + str(sequence))
    fragSeq.close()
    
    #blasts input fragment across genomic reference sequences and returns top 10 results 
    
    #line of code for server request
    #Blast_r = NCBIWWW.qblast("blastn", "refseq_genomic", sequence, hitlist_size=10)
    
    #line of code for local request
    Blast_r = NcbiblastxCommandline(cmd="blastn", query = "fragment.fasta",db="~/dev/pos_sel_lacto/l_crispatus/l_crisp",outfmt=5,out="fragment.xml")
    Blast_r()
    result_handle = open("fragment.xml")
    blast_records = NCBIXML.parse(result_handle)
    counter=0
    for blast_record in blast_records:
	for alignment in blast_record.alignments:
            for hsp in alignment.hsps:
               counter += 1
               species_id = alignment.title
               species_id = species_id.split("|")[6]
               recomb_out.write(str(species_id) + "\t") #[0:20]
               break

    # creating a file of the 
    if counter < 3:
        candidate_out.write("\n" + str(start_window) + "\t" + str(end_window) + "\t" + str(GC_percent) + "\t" + str(counter) + "\t" + str(sequence))
        
        continue

recomb_out.close()
    






