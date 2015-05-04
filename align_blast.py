#!/usr/bin/python

from Bio.Align import AlignInfo
from Bio import AlignIO
from Bio import SeqIO
from Bio.Blast import NCBIWWW
from Bio.Blast import NCBIXML
from Bio.Blast.Applications import NcbiblastxCommandline
from Bio.Align.Applications import ClustalwCommandline


#reads in a txt file of the gene names to be analyzed and strips off the newline character, result is a list of gene names

list_gene_names =[line.strip() for line in open("l_iners_sums_trim.txt",'r')]


accessory_out = open('accessory_blast_id.tsv','w')
accessory_out.write("ORF\tID1\tPercent\tID2\tPercent\tID3\tPercent\tID4\tPercent\tID5\tPercent ")



for i in list_gene_names:
    print i
    
    clustal_cline = ClustalwCommandline("clustalw",infile ="%s.fasta" %(i), type="protein")
    stdout, stderr = clustal_cline()
    print i
    alignment = AlignIO.read("%s.aln" %(i), "clustal")
    summary_align = AlignInfo.SummaryInfo(alignment)
    consensus = summary_align.dumb_consensus()
    
    print i
    
    seq_out = open('%s_cons.fasta' %(i),'w')
    seq_out.write('>%s\n' %(i) + str(consensus))
    seq_out.close()

    blastOUT = open('fragment.xml','w')
    # Set the counter to zero
    fail_count = 0
    # Define the max we'll allow
    max_failures = 4
    # Track exceptions as we go
    exception_caught = False
 
    while fail_count < max_failures:
        try:
            blastx_cline = NcbiblastxCommandline(query="%i_cons.fasta" %(i), db="nr", outfmt=5, out="fragment.xml")
            stdout, stderr = blastx_cline()

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
    accessory_out.write("\n" + str(i) + "\t")
    
    for blast_record in blast_records:
        for alignment in blast_record.alignments:
	    counter +=1
	    if counter == 10:
	        break
            for hsp in alignment.hsps:
                #lacto_out.write(str(hsp.expect))
                species_id = alignment.title
                #print species_id
                print hsp.identities
                per_ident = 100*int(hsp.identities)/length
                species_id = species_id.split("|")[4]
                accessory_out.write(str(species_id) + "\t" + str(per_ident) + "\t")
    

singles_out.close()





