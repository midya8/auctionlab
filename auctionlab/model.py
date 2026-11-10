"""Strict finite monotone valuation inputs. No mechanism construction."""
import json

def keys(x,ks):
 if type(x)is not dict or set(x)!=set(ks):raise ValueError('unexpected fields')
def integer(x):
 if type(x)is not int:raise ValueError('expected non-boolean integer')
 return x
def valuation(row,m):
 if type(row)is not list or len(row)!=1<<m:raise ValueError('one value per bitmask bundle required')
 for v in row:
  if not 0<=integer(v)<=100:raise ValueError('value must be integer 0..100')
 if row[0]!=0:raise ValueError('empty bundle value must be zero')
 for mask in range(1<<m):
  for j in range(m):
   if not(mask>>j&1)and row[mask]>row[mask|1<<j]:raise ValueError('values must be monotone under inclusion')
def parse(p):
 keys(p,['version','items','values','deviations'])
 if integer(p['version'])!=1:raise ValueError('version must be 1')
 m=integer(p['items'])
 if not 1<=m<=4:raise ValueError('items must be 1..4')
 if type(p['values'])is not list or not 1<=len(p['values'])<=3:raise ValueError('bidders must be 1..3')
 n=len(p['values'])
 for row in p['values']:valuation(row,m)
 if type(p['deviations'])is not list or len(p['deviations'])!=n:raise ValueError('deviation list per bidder required')
 for reports in p['deviations']:
  if type(reports)is not list or len(reports)>6:raise ValueError('at most six explicit reports per bidder')
  for row in reports:valuation(row,m)
 return m,n
def loads(text):
 def pairs(ps):
  out={}
  for k,v in ps:
   if k in out:raise ValueError('duplicate key')
   out[k]=v
  return out
 def no(_):raise ValueError('JSON decimals/constants forbidden')
 return json.loads(text,object_pairs_hook=pairs,parse_float=no,parse_constant=no)
