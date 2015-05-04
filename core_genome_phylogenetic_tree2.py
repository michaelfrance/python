#!/usr/bin/python
import os
import sys

for name in open(sys.argv[1],"r"):
    filename = 'Gene' + name[:-1] + '-DNA.fasta'
    print '1'
    nexus_name = filename[:-6] + '.nexus'
    os.system("mbsum  -n 1000 -o %s.in %s.t" %(nexus_name,nexus_name))

os.system('bucky *.in')

