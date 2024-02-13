import pandas as pd
import os
import sys
import numpy as np
from fractions import Fraction

#e_bound = int(sys.argv[1])

#compile solns

homepath = "/scratch/bbxw/alee7/embedding/teste10"

compiled_solns = pd.DataFrame()

for e in range(2,41):
  filepath = str(r"/scratch/bbxw/alee7/embedding/teste10/e"+str(e)+"/")
  os.chdir(filepath)
  filename = str("block_solns(e"+str(e)+").parquet")
  file_read = pd.read_parquet(filename)
  compiled_solns = pd.concat([compiled_solns, file_read])

#output

os.chdir(homepath)
compiled_solns.to_parquet("compiled_solns_8.parquet")
