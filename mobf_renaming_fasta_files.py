#!/usr/bin/python
import os
from Bio import SeqIO

for filename in sorted(os.listdir(os.getcwd())):
    if filename.endswith(".gb"):
        input_handle = open(filename,'rU')
        revised_filename = filename.split(" ")[0]
        revised_filename = revised_filename.split(".")[0] + '.fasta'

        print revised_filename
        output_handle = open(revised_filename,'w')

        for seq_record in SeqIO.parse(input_handle,"genbank") :
            for seq_feature in seq_record.features :
                if seq_feature.type=='CDS' :
                    name = seq_feature.qualifiers.get('locus_tag','none')
                    if name[0] == 'none':
                        continue
                    else:
                        name = name[0]
                    sequence = seq_feature.qualifiers.get('translation','none')
                    if sequence == 'none':
                        continue
                    else:
                        sequence = sequence[0]

                    output_handle.write(">" + str(name) + '\n' + str(sequence) + '\n')
        output_handle.close()
        input_handle.close()            


file_key = open('mobf_file_key.csv', "w")

count = 101


for filename in sorted(os.listdir(os.getcwd())):
    if filename.endswith(".fasta"):
        print filename
        
        file_key.write(filename + ',mobf' + str(count) + '\n')
        
        renamed_fasta = open('mobf%s.fasta' %(count), "w")

        orf_count = 1000
        
        for rec in SeqIO.parse(open(filename,"r"), "fasta"):
            #if str(rec.seq).count("N") > 5:
             #   continue
            #if len(str(rec.seq)) < 25: 
             #   continue

            renamed_fasta.write('>mobf' + str(count) + '|' + str(count) + "_" + str(orf_count) + '\n'+str(rec.seq)+'\n')
            orf_count += 1


        count += 1

    else:
        continue


file_key.close()
    
