#!/usr/bin/python
from Bio import SeqIO                                                               
import sys                                                                          
import fileinput

core = 0
eleven = 0
ten  = 0
nine = 0
eight = 0
seven = 0
six = 0
five = 0
four = 0
three = 0
two = 0
single = 0
paralog = 0






for line in fileinput.input(sys.argv[1]):
    line = line.strip()
    orf = line.split(" ")[0]
    orf = orf.replace(':','')
    #print orf
    #orf_seq = open('%s.fasta' % (orf),'w')
    protein_ids = line.split(" ")
    protein_ids.pop(0)
    #seqiter = SeqIO.parse(open(sys.argv[2]), 'fasta')                                    
    #SeqIO.write((seq for seq in seqiter if seq.id in protein_ids), orf_seq, "fasta")
    count=0
    protein_org_set = list()
    for i in protein_ids:
       protein_org = i.split("|")[1]       
       protein_org = protein_org.split("_")[0]
       protein_org_set.append(protein_org)
       #print protein_org_set 
       count +=1
    size1=len(protein_org_set)
    protein_org_set = list(set(protein_org_set))
    print protein_org_set
    size2=len(protein_org_set)
    if size1 > size2:
        paralog += 0    
    elif size2 == 12:
        core += 1
    elif size2 == 11:
        eleven += 1
    elif size2 == 10:
        ten += 1
    elif size2 == 9:
        nine += 1
    elif size2 == 8:
        eight += 1
    elif size2 == 7:
        seven += 1
    elif size2 == 6:
        six += 1
    elif size2 == 5:
        five += 1
    elif size2 == 4:
        four += 1
    elif size2 == 3:
        three += 1
    elif size2 == 2:
        two += 1
    elif size2 == 1:
        single += 1

print("paralog\t" + str(paralog))
print("core\t" + str(core))
print("11\t" + str(eleven))
print("ten\t" + str(ten))
print("nine\t" + str(nine))
print("eight\t" + str(eight))
print("seven\t" + str(seven))
print("six\t" + str(six))
print("five\t" + str(five))
print("four\t" + str(four))
print("three\t" + str(three))
print("two\t" + str(two))
print("one\t" + str(single))



