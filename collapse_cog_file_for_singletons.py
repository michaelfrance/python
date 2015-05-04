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
        cog_code = line.split('\t')[8]
        cog_score = line.split('\t')[6]
        cogs = list() 
        cogs.append(cog_code)
        cog_score_orgs = list()
        cog_score_orgs.append(cog_score)

        cog_of_best = best_choice(cogs, cog_score_orgs)
        collapsed_out.write(cog_of_best + '\n')

collapsed_out.close()

summarized_out = open('%s_summarized.tsv' %(filename),'w')
summarized_out.write("Category\tCount\n")


cogs_final = list()

dissent = 0

for line in fileinput.input('%s_collapsed.tsv' %(filename)):
    line = line.replace("\n","")
    cogs_final.append(line)
summarized = dict()

for i in cogs_final:
  summarized[i] = summarized.get(i, 0) + 1


for key in summarized.keys():
    summarized_out.write(str(key) + "\t" + str(summarized[key]) + "\n")

summarized_out.close()

print summarized

print dissent

print cogs_final

print len(cogs_final)



