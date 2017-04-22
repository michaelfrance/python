#!/usr/bin/python
from Bio import SeqIO
from Bio.Blast import NCBIWWW
from Bio.Blast import NCBIXML
import sys
import time

singles_out = open('singletons_blast_id.tsv','w')
singles_out.write("ORF\tID1\tID2\tID3\tID4\tID5 ")


for rec in SeqIO.parse(open(sys.argv[1],"r"), "fasta") :
    
    num_n = 0

    for i in rec:
        if i == 'X':
            num_n += 1
        if num_n > 5:
            continue
    length = len(rec.seq)
    
    print length
    print rec.seq
    time.sleep(5)

    blastOUT = open('fragment.xml','w')

    # Set the counter to zero
    fail_count = 0
    
    # Define the max we'll allow
    max_failures = 10

    # Track exceptions as we go
    exception_caught = False
 
    while fail_count < max_failures:

        try:
            Blast_r = NCBIWWW.qblast("blastp", "nr", rec.seq, hitlist_size=10)
            blastOUT.write(Blast_r.read())
            # If we reach here an exception didn't occur
            exception_caught = False
    
        except Exception as e:
            # Something as gone wrong
            fail_count += 1
            exception_caught = True
            print "ERROR IN BLAST QUERY"
    
        finally:
            # Always close our file 
            blastOUT.close()
        
        # Was this a run that didn't result in an exception?
        if not exception_caught:
            break
    
    result_handle = open("fragment.xml")

    blast_records = NCBIXML.parse(result_handle)
    
    counter = 0

    singles_out.write("\n" + str(rec.id) + "\t")
    
    for blast_record in blast_records:

        for alignment in blast_record.alignments:

	    counter +=1

	    if counter == 10:

	        break

            for hsp in alignment.hsps:
                #lacto_out.write(str(hsp.expect))

                species_id = alignment.title

                print species_id

                print hsp.identities

                per_ident = 100*int(hsp.identities)/length

                species_id = species_id.split("|")[4]

                singles_out.write(str(species_id) + "\t" + str(per_ident) + "\t")
    

singles_out.close()

