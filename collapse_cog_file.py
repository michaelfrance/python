#!/usr/bin/python

#this script expects an ncbi conserved domain cog file as input in arg1

import fileinput
import sys
import os
import re
from collections import Counter


def best_choice (cogs, cog_score_orgs):
    
    top_hit = None
    top_hit_result = None
    cog_score_orgs = map(float, cog_score_orgs)

    for current_location, score in enumerate(cog_score_orgs):

        if top_hit is None:
           top_hit = score
           top_hit_result = cogs[current_location]

        if score > top_hit:

           if cogs[current_location] == "#N/A": 
              continue

           else:
               top_hit = score
           
               top_hit_result = cogs[current_location]
               continue

        elif score <= top_hit:
           if top_hit_result == "#N/A":
               top_hit = score
           
               top_hit_result = cogs[current_location]
               continue
    return top_hit_result





filename = str(sys.argv[1]).split(".")[0]


collapsed_out = open('%s_collapsed.tsv' %(filename),'w')

counter = 0


for line in fileinput.input(sys.argv[1]):

    cluster_functions = list()

    if line[0] != "Q":
        continue
    elif line[0:2] == "Q#":

        counter += 1

        clus_org_name = line.split()[2][1:]

        print clus_org_name

        cluster_name = clus_org_name.split('_')[0][1:]

        org_name = clus_org_name.split('_')[1]
        
        cog_code = line.split('\t')[8]
        
        cog_score = line.split('\t')[6]

        if counter == 1:
            cluster_name2 = cluster_name
            collapsed_out.write(cluster_name)
            org_name2 = org_name
            cog_score2 = cog_score

            cogs = list() 
            cogs.append(cog_code)
            cog_score_orgs = list()
            cog_score_orgs.append(cog_score)
            continue


        elif cluster_name != cluster_name2:
            
            cog_of_best = best_choice(cogs, cog_score_orgs)

            collapsed_out.write('\t' + cog_of_best + '\n' + cluster_name)

            cluster_name2 = cluster_name
            org_name2 = org_name
            
            cogs = list() 
            cogs.append(cog_code)
            cog_score_orgs = list()
            cog_score_orgs.append(cog_score)

            continue

        elif cluster_name == cluster_name2:
            
            if org_name == org_name2:

                cogs.append(cog_code)
                cog_score_orgs.append(cog_score)                
                continue

            if org_name != org_name2:
                cog_of_best = best_choice(cogs, cog_score_orgs)
                
                collapsed_out.write('\t' + cog_of_best)

                cogs = list() 
                cogs.append(cog_code)
                cog_score_orgs = list()
                cog_score_orgs.append(cog_score)

                org_name2 = org_name
                continue

cog_of_best = best_choice(cogs, cog_score_orgs)
collapsed_out.write('\t' + cog_of_best)

collapsed_out.close()

summarized_out = open('%s_summarized.tsv' %(filename),'w')
summarized_out.write("Category\tCount\n")


cogs_final = list()

dissent = 0

for line in fileinput.input('%s_collapsed.tsv' %(filename)):
    line = line.replace("\n","")
    cluster_cogs = line.split('\t')
    cluster_cogs.pop(0)
    if len(set(cluster_cogs)) <= 1:
        cogs_final.append(cluster_cogs[0])
    elif len(set(cluster_cogs)) > 1:
        dissent += 1

summarized = dict()
for i in cogs_final:
  summarized[i] = summarized.get(i, 0) + 1

summarized['dissent'] = dissent

for key in summarized.keys():
    summarized_out.write(str(key) + "\t" + str(summarized[key]) + "\n")

summarized_out.close()

print summarized

print dissent

print cogs_final

print len(cogs_final)



