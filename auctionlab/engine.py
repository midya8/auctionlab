"""Exact finite VCG allocation, pivot prices and seller-coalition audit."""
from itertools import product
from copy import deepcopy
from .model import parse

def analyze(p):
 m,n=parse(p);ids=list(range(n));rows=[]
 for idx,owners in enumerate(product(range(n+1),repeat=m)):
  bundles=[sum(1<<j for j,v in enumerate(owners)if v==i+1)for i in ids];vals=[p['values'][i][bundles[i]]for i in ids];rows.append(dict(id=idx,owners=list(owners),bundles=bundles,values=vals,welfare=sum(vals)))
 def restricted(coal):
  eligible=[z for z in rows if all(v==0 or coal>>(v-1)&1 for v in z['owners'])];best=max(z['welfare']for z in eligible);return dict(coalition=coal,bidders=[i for i in ids if coal>>i&1],welfare=best,allocations=[z['id']for z in eligible if z['welfare']==best])
 coalitions=[restricted(k)for k in range(1<<n)];full=(1<<n)-1;w=coalitions[full]['welfare'];optimal=coalitions[full]['allocations'];without=[coalitions[full^(1<<i)]for i in ids];utilities=[w-z['welfare']for z in without];revenue=w-sum(utilities);outcomes=[]
 for k in optimal:
  z=rows[k];payments=[without[i]['welfare']-(w-z['values'][i])for i in ids];witnesses=[dict(bidder=i,bundle=z['bundles'][i],declared_value=z['values'][i],without_welfare=without[i]['welfare'],without_allocations=without[i]['allocations'],others_welfare=w-z['values'][i],payment=payments[i],utility=utilities[i])for i in ids];outcomes.append(dict(allocation=k,payments=payments,utilities=utilities[:],revenue=revenue,witnesses=witnesses))
 core=[]
 for z in coalitions:
  paid=revenue+sum(utilities[i]for i in z['bidders']);core.append(dict(coalition=z['coalition'],bidders=z['bidders'],value=z['welfare'],witnesses=z['allocations'],payoff=paid,slack=paid-z['welfare'],deficit=max(0,z['welfare']-paid)))
 # Seller-free coalitions own no goods and have value zero; all utilities are nonnegative.
 violations=[z['coalition']for z in core if z['deficit']>0];audit=[]
 for i in ids:
  cases=[]
  for idx,report in enumerate(p['deviations'][i]):
   scored=[sum(report[z['bundles'][j]]if j==i else z['values'][j]for j in ids)for z in rows];best=max(scored);opts=[z['id']for z in rows if scored[z['id']]==best];deviants=[]
   for k in opts:
    z=rows[k];other=sum(z['values'][j]for j in ids if j!=i);payment=without[i]['welfare']-other;truevalue=p['values'][i][z['bundles'][i]];deviants.append(dict(allocation=k,bundle=z['bundles'][i],reported_value=report[z['bundles'][i]],true_value=truevalue,others_welfare=other,payment=payment,true_utility=truevalue-payment,utility_gain=truevalue-payment-utilities[i]))
   cases.append(dict(report_id=idx,report=report[:],reported_welfare=best,allocations=opts,outcomes=deviants,min_gain=min(z['utility_gain']for z in deviants),max_gain=max(z['utility_gain']for z in deviants)))
  audit.append(dict(bidder=i,truthful_utility=utilities[i],reports=cases,max_tested_gain=max([0]+[z['max_gain']for z in cases])))
 menus=[]
 for i in ids:
  entries=[]
  for bundle in range(1<<m):
   eligible=[z for z in rows if z['bundles'][i]==0 and all(not(z['bundles'][j]&bundle)for j in ids)];v=max(z['welfare']for z in eligible);price=without[i]['welfare']-v;entries.append(dict(bundle=bundle,others_welfare=v,others_allocations=[z['id']for z in eligible if z['welfare']==v],price=price,true_value=p['values'][i][bundle],true_utility=p['values'][i][bundle]-price,optimal=p['values'][i][bundle]-price==utilities[i]))
  menus.append(dict(bidder=i,entries=entries,best_utility=utilities[i],best_bundles=[z['bundle']for z in entries if z['optimal']]))
 return dict(version=1,kind='auctionlab-vcg',input=deepcopy(p),allocations=rows,coalitions=coalitions,welfare=w,optimal=optimal,outcomes=outcomes,utilities=utilities,revenue=revenue,core=dict(seller_included=True,rows=core,violations=violations,max_deficit=max(z['deficit']for z in core),in_core=not violations),deviation_audit=audit,menus=menus)
