"""Optional input-built binary bundle reference. All coalition and menu subproblems."""
import json,sys
from pathlib import Path
import numpy as np,scipy
from scipy.optimize import milp,Bounds,LinearConstraint
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from auctionlab import analyze
from cases import cases
solves=0;maxerr=0.;constraints=0
for p in cases():
 m=p['items'];n=len(p['values']);b=1<<m;report=analyze(p);objective=np.array([-p['values'][i][mask]for i in range(n)for mask in range(b)],dtype=float);mat=[];lo=[];hi=[]
 for i in range(n):mat.append([float(j==i)for j in range(n)for mask in range(b)]);lo.append(1.);hi.append(1.)
 for item in range(m):mat.append([float(mask>>item&1)for j in range(n)for mask in range(b)]);lo.append(0.);hi.append(1.)
 def solve(active,reserved=0):
  global solves,maxerr,constraints
  upper=np.array([float(mask==0 or(active>>i&1 and mask&reserved==0))for i in range(n)for mask in range(b)]);z=milp(objective,integrality=np.ones(n*b),bounds=Bounds(np.zeros(n*b),upper),constraints=LinearConstraint(np.array(mat),lo,hi),options={'mip_rel_gap':0.});assert z.success,z.message;x=np.rint(z.x).astype(int);assert np.max(np.abs(z.x-x))<=1e-8;assert np.all(x<=upper);bundles=[]
  for i in range(n):
   row=x[i*b:(i+1)*b];assert sum(row)==1;bundles.append(int(row.argmax()))
  seen=reserved
  for i,mask in enumerate(bundles):assert not(seen&mask);seen|=mask;assert(active>>i&1)or mask==0
  value=sum(p['values'][i][mask]for i,mask in enumerate(bundles));assert abs(-z.fun-value)<=1e-8;solves+=1;constraints+=len(mat);return z.fun,value
 for k,z in enumerate(report['coalitions']):
  raw,v=solve(k);error=abs(-raw-z['welfare']);maxerr=max(maxerr,error);assert error<=1e-8;assert v==z['welfare']
 for menu in report['menus']:
  for entry in menu['entries']:
   raw,v=solve(((1<<n)-1)^(1<<menu['bidder']),entry['bundle']);error=abs(-raw-entry['others_welfare']);maxerr=max(maxerr,error);assert error<=1e-8;assert v==entry['others_welfare']
print(json.dumps(dict(scipy=scipy.__version__,profiles=len(cases()),integer_solves=solves,constraint_rows=constraints,max_abs_error=maxerr,tolerance=1e-8)))
