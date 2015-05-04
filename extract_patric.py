#!/usr/bin/python

import sys
import os

for org_name in open(sys.argv[1],"r"):
    org_name = org_name.replace("\n","")
    genus_species = ''.join(org_name.split("_")[0:2]).replace("\n","")

    if genus_species == "Pseudomonasaeruginosa":
        #print('/data/patric/genomes/%s/%s.PATRIC.faa ~/pseudomonas/05-External_genomes/.' %(org_name,org_name))
        os.system('cp /data/patric/genomes/%s/%s.PATRIC.faa ~/pseudomonas/05-External_genomes/.' %(org_name,org_name))