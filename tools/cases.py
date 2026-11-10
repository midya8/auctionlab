import random
from auctionlab.controls import controls

def cases():
 out=[c['input']for c in controls()];rng=random.Random(203081)
 for m in range(1,5):
  for n in range(1,4):
   for _ in range(3):
    vals=[];ds=[]
    for i in range(n):
     row=[0]+[rng.randrange(31)for j in range((1<<m)-1)]
     for mask in range(1<<m):
      for bit in range(m):
       if mask>>bit&1:row[mask]=max(row[mask],row[mask^(1<<bit)])
     vals.append(row);ds.append([[v//2 for v in row],[min(100,2*v)for v in row]])
    out.append(dict(version=1,items=m,values=vals,deviations=ds))
 return out
