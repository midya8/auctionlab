"""Independent disjoint-bundle exhaustive replay. Never imports mechanism generator."""
from itertools import product
from .model import parse,keys

def verify(r):
 try:
  keys(r,['version','kind','input','allocations','coalitions','welfare','optimal','outcomes','utilities','revenue','core','deviation_audit','menus']);m,n=parse(r['input']);p=r['input'];agents=range(n);allgoods=(1<<m)-1
  def eq(a,b):
   if type(a)is not type(b):raise ValueError('wrong evidence type')
   if type(b)is dict:
    keys(a,b)
    for k in b:eq(a[k],b[k])
   elif type(b)is list:
    if len(a)!=len(b):raise ValueError('evidence length')
    for x,y in zip(a,b):eq(x,y)
   elif a!=b:raise ValueError('evidence mismatch')
  # Native replay enumerates bundle products, rejects intersections and derives ownership IDs.
  rr=[]
  for masks in product(range(allgoods+1),repeat=n):
   seen=0;valid=True
   for mask in masks:
    if seen&mask:valid=False;break
    seen|=mask
   if not valid:continue
   owners=[next((i+1 for i in agents if masks[i]>>j&1),0)for j in range(m)];idx=sum(v*(n+1)**(m-j-1)for j,v in enumerate(owners));values=[p['values'][i][masks[i]]for i in agents];rr.append(dict(id=idx,owners=owners,bundles=list(masks),values=values,welfare=sum(values)))
  rr.sort(key=lambda z:z['id']);eq(r['allocations'],rr);eq(r['version'],1);eq(r['kind'],'auctionlab-vcg');coal=[]
  for k in range(1<<n):
   bidders=[i for i in agents if k>>i&1];feasible=[z for z in rr if all(z['bundles'][i]==0 for i in agents if i not in bidders)];best=max(sum(z['values'][i]for i in bidders)for z in feasible);coal.append(dict(coalition=k,bidders=bidders,welfare=best,allocations=[z['id']for z in feasible if sum(z['values'][i]for i in bidders)==best]))
  eq(r['coalitions'],coal);w=coal[-1]['welfare'];opts=coal[-1]['allocations'];eq(r['welfare'],w);eq(r['optimal'],opts);without=[coal[((1<<n)-1)^(1<<i)]for i in agents];outcomes=[];base=[];rev=None
  for k in opts:
   z=rr[k];payments=[];utilities=[];witnesses=[]
   for i in agents:
    other=sum(v for j,v in enumerate(z['values'])if i!=j);price=without[i]['welfare']-other;u=p['values'][i][z['bundles'][i]]-price;payments.append(price);utilities.append(u);assert 0<=price<=z['values'][i];assert u==w-without[i]['welfare'];witnesses.append(dict(bidder=i,bundle=z['bundles'][i],declared_value=z['values'][i],without_welfare=without[i]['welfare'],without_allocations=without[i]['allocations'],others_welfare=other,payment=price,utility=u))
   if base:assert base==utilities
   base=utilities;rev=sum(payments);assert rev+sum(utilities)==w;outcomes.append(dict(allocation=k,payments=payments,utilities=utilities,revenue=rev,witnesses=witnesses))
  eq(r['outcomes'],outcomes);eq(r['utilities'],base);eq(r['revenue'],rev);cores=[]
  for z in coal:
   paid=rev+sum(base[i]for i in z['bidders']);slack=paid-z['welfare'];cores.append(dict(coalition=z['coalition'],bidders=z['bidders'],value=z['welfare'],witnesses=z['allocations'],payoff=paid,slack=slack,deficit=-slack if slack<0 else 0))
  bad=[z['coalition']for z in cores if z['slack']<0];eq(r['core'],dict(seller_included=True,rows=cores,violations=bad,max_deficit=max(z['deficit']for z in cores),in_core=not bad));audit=[]
  for i in agents:
   cases=[]
   for idx,report in enumerate(p['deviations'][i]):
    scored=[]
    for z in rr:scored.append(report[z['bundles'][i]]+sum(z['values'][j]for j in agents if j!=i))
    best=max(scored);options=[k for k,v in enumerate(scored)if v==best];outs=[]
    for k in options:
     z=rr[k];ov=sum(p['values'][j][z['bundles'][j]]for j in agents if j!=i);price=without[i]['welfare']-ov;true=p['values'][i][z['bundles'][i]];gain=true-price-base[i];assert gain<=0;outs.append(dict(allocation=k,bundle=z['bundles'][i],reported_value=report[z['bundles'][i]],true_value=true,others_welfare=ov,payment=price,true_utility=true-price,utility_gain=gain))
    gains=[z['utility_gain']for z in outs];cases.append(dict(report_id=idx,report=report,reported_welfare=best,allocations=options,outcomes=outs,min_gain=min(gains),max_gain=max(gains)))
   audit.append(dict(bidder=i,truthful_utility=base[i],reports=cases,max_tested_gain=max([0]+[z['max_gain']for z in cases])))
  menus=[]
  for i in agents:
   entries=[]
   for bundle in range(allgoods+1):
    valid=[z for z in rr if z['bundles'][i]==0 and not(any(z['bundles'][j]&bundle for j in agents))];ow=max(sum(z['values'][j]for j in agents if j!=i)for z in valid);witnesses=[z['id']for z in valid if z['welfare']==ow];price=without[i]['welfare']-ow;u=p['values'][i][bundle]-price;entries.append(dict(bundle=bundle,others_welfare=ow,others_allocations=witnesses,price=price,true_value=p['values'][i][bundle],true_utility=u,optimal=u==base[i]))
   best=max(z['true_utility']for z in entries);assert best==base[i];menus.append(dict(bidder=i,entries=entries,best_utility=best,best_bundles=[z['bundle']for z in entries if z['true_utility']==best]))
  eq(r['menus'],menus)
  eq(r['deviation_audit'],audit);return True
 except(KeyError,TypeError,IndexError,OverflowError,AssertionError)as e:raise ValueError('malformed report')from e
