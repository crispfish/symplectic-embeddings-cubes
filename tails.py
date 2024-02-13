#!/usr/bin/python

# import libraries
import sys
import re
import ast
#import csv
#from tqdm import tqdm
import pandas as pd
import numpy as np
import math
from cachetools import cached
from cachetools.keys import hashkey
from cachetools import LRUCache

#Define auxiliary functions

def selfint(d,e):
  return 2*d*e+1

def chern(d,e):
  return 2*(d+e)-1

def length_bound(m,z):
  """ Tests whether a candidate tail is too long
  :type m: tuple; tail to be considered
  :param r: Optional; length of first block
  :param z: Optional; max length of tail
  """
  if len(m)<=z:
    return True
  else:
    return False

#Define ClassDataGenerator
def ClassDataGenerator(d,e,limit=0):
    """
    Given head (d,e), find all tails which solve Diophantine equations. Also incorporates length bound.
    :param d: Larger term in head
    :param e: Second term in head
    :param z: Optional, length bound
    """
    # Set up parameters
    square_sum = selfint(d,e)
    linear_sum = chern(d,e)
    previous_term=int(np.floor(np.sqrt(square_sum)))

    #Define Extend, customized for these parameters
    @cached(cache=LRUCache(maxsize=640*1024), key=lambda square_sum, linear_sum, previous_term, index=0, z=limit: hashkey(square_sum, linear_sum, previous_term))
    def Extend(square_sum,linear_sum,previous_term, index=0, z=limit):
        """ Function to recursively generate solutions to Diophantine system
        :param square_sum Target L2 norm of vector
        :param linear_sum Target L1 norm of vector
        :param previous_term If nonzero, last term in vector
        :param index: Current position in vector counting from the largest entry on the left
        :param z: Length cutoff
        """
        ret=()

        if square_sum < 0 or linear_sum <0:
            #print("One of the sums is negative")
            return ret
        if square_sum < linear_sum:
            #print("Squaresum less than linearsum")
            return ret
        if square_sum==linear_sum and square_sum <= z-index:
            #print("Completed with 1's")
            return ((),((1,)*square_sum))
        if square_sum==linear_sum and square_sum > z-index:
            #print("Too many 1's")
            return ret
        if limit!=0 and index>z:
            #print("Failed length bound at the top")
            return ret

        initial_m=int(np.floor(np.sqrt(square_sum)))

        if previous_term!=0:
            start=min(previous_term,initial_m)
        elif previous_term==0:
            start=initial_m

        for i in range(start, 1, -1):
            ret = ret + tuple([tuple((i,)+sub) for sub in Extend(square_sum-i*i,linear_sum-i,i, index+1,z)])
            if limit!=0:
                ret = tuple([x for x in ret if length_bound(x,z)])
        return ret

    #Run Extend
    classes_list=pd.DataFrame(Extend(square_sum,linear_sum,previous_term))

    #print("Finished with",str(d),"and",str(e),"found",classes_list)

    #Create filename with metadata
    label="Tails"+"(e"+str(e)+"d"+str(d)+"z"+str(limit)+").parquet"

    classes_list.columns = classes_list.columns.astype(str)
    classes_list.to_parquet(label)

    #with open(label, "wb") as binary_file:
    #    binary_file.write(bytes_classes_list)

#Scheduler will input e, we calculate d range
e = int(sys.argv[1])

coordinates_list=[]

d_min=max(e-2,1)

d_max=2*e+2

for d in range(d_min, d_max,1):
    coordinates_list=coordinates_list+[[d,e]]

for pair in coordinates_list:
  ClassDataGenerator(pair[0],pair[1],limit=19)

# print task number
#print('Hello! I am task number : ', sys.argv[1])
