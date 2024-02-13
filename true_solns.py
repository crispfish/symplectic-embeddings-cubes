import pandas as pd
import os
import sys
import numpy as np
from fractions import Fraction

e = int(sys.argv[1])

#e_bound = 39

#Functions
def de_pair_generator(e):
    coordinates_list=[]
    d_min=max(e-2,1)
    d_max=2*e+2
    for d in range(d_min, d_max,1):
        coordinates_list=coordinates_list+[[d,e]]
    return coordinates_list

def filenames_generator(e,z=0):
    filenames=[]
    coordinates_list=de_pair_generator(e)
    for pair in coordinates_list:
        info_dictionary={}
        info_dictionary["d"]=pair[0]
        info_dictionary["e"]=pair[1]
        info_dictionary["filename"]="Tails"+"(e"+str(pair[1])+"d"+str(pair[0])+"z"+str(z)+").parquet"
        filenames.append(info_dictionary)
    return filenames

def WeightSeq(floor,p,q):
  initial=int(floor)+Fraction(p,q)
  start=[]
  divisor=1
  remainder=initial
  while remainder>0:
    ordered=sorted([remainder,divisor])
    divisor,remainder=ordered
    start.append(divisor)
    remainder=remainder-divisor
    #print(f"Divisor is {divisor} and remainder is {remainder}")
  return np.array(start)

def block_indices(floor,p,q):
    weight_sequence = WeightSeq(floor,p,q)
    unique_entries = set(weight_sequence)
    return [[i for i, x in enumerate(weight_sequence) if x==entry] for entry in unique_entries]

def block_multiplicity_check(block_multi_indices, tail):
    blocks = [[tail[i] for i in block_multi_index] for block_multi_index in block_multi_indices]
    number_distinct = [len(set(block)) for block in blocks]
    if sum(number_distinct) > len(blocks)+1: #Only one block can have at most two distinct entries
        return False
    for block in blocks: #Never have to loop over more than 3-4 blocks so OK
        if sum(block)/max(block)!=len(block): #If block is not uniform
            if (len(block)*min(block)+1-sum(block))*(len(block)*max(block)-1-sum(block))!=0: #If off entry is more than +-1 different from rest
              return False
    return True

homepath = "/scratch/bbxw/alee7/embedding/teste10"

block_solns = pd.DataFrame()

block_index = block_indices(8,0,2)

total_length = sum(len(index) for index in block_index)+4

filepath = str(r"/scratch/bbxw/alee7/embedding/teste10/"+"e"+str(e)+"/")
os.chdir(filepath)  #Change to correct directory
pairs = filenames_generator(e, z=19) #Generate filenames

for pair in pairs:
  print("Checking pair",pair)
  d = pair["d"]
  #print(os.listdir(path=None))
  candidates = pd.read_parquet(pair['filename'])

  candidates = candidates.fillna(0)

  candidates.insert(loc=0, column='ell2', value=np.linalg.norm(candidates, axis=1)**2)
  candidates.insert(loc=0, column='ell1', value=np.sum(candidates.drop('ell2', axis=1), axis=1))

  candidates.insert(loc=0, column='d', value=d)

  candidates.insert(loc=0, column='e', value=e)
  e_solns = candidates.loc[(candidates['ell2'].astype(int)==2*d*e+1) & (candidates['ell1'].astype(int)==2*(d+e)-1)]

  if e_solns.shape[1]<total_length:
    block_solns = pd.concat([block_solns, e_solns])
    continue

  block_consistent_list= e_solns.drop(['d','e','ell2','ell1'],axis=1).apply(lambda x: block_multiplicity_check(block_index,x), axis=1)
  #block_consistent = e_solns.loc[e_solns.index[block_consistent_list]]
  block_consistent = e_solns[block_consistent_list]

  block_solns = pd.concat([block_solns, block_consistent])

#os.chdir(homepath)
label = str(r"block_solns(e"+str(e)+").parquet")
block_solns.to_parquet(label)
