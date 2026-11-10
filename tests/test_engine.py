import copy,itertools,json,random,subprocess,sys,tempfile,unittest
from pathlib import Path
from auctionlab import analyze,verify
from auctionlab.controls import controls
from auctionlab.model import parse,loads
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from cases import cases
class Tests(unittest.TestCase):
 def test_full_reports(self):
  rs=[analyze(p)for p in cases()]
  for r in rs:self.assertTrue(verify(r))
  print('REPORTS',len(rs),'ALLOCATIONS',sum(len(r['allocations'])for r in rs),'OPTIMAL',sum(len(r['optimal'])for r in rs),'COALITIONS',sum(len(r['coalitions'])for r in rs),'MENUS',sum(len(z['entries'])for r in rs for z in r['menus']),'REPORT_DEVIATIONS',sum(len(z['reports'])for r in rs for z in r['deviation_audit']),'DEVIATION_OUTCOMES',sum(len(z['outcomes'])for r in rs for a in r['deviation_audit']for z in a['reports']))
 def test_default_core_deficit(self):
  r=analyze(controls()[0]['input']);self.assertEqual(r['welfare'],12);self.assertEqual(r['optimal'],[11]);self.assertEqual(r['outcomes'][0]['payments'],[0,4,4]);self.assertEqual(r['utilities'],[0,2,2]);self.assertEqual(r['revenue'],8);self.assertEqual(r['core']['violations'],[1]);self.assertEqual(r['core']['max_deficit'],2);self.assertFalse(r['core']['in_core'])
 def test_substitutes_control(self):
  r=analyze(controls()[1]['input']);self.assertEqual(r['welfare'],12);self.assertEqual(r['revenue'],10);self.assertTrue(r['core']['in_core'])
 def test_single_good_second_price(self):
  r=analyze(controls()[2]['input']);self.assertEqual(r['outcomes'][0]['payments'],[7,0,0]);self.assertEqual(r['utilities'],[2,0,0]);self.assertTrue(r['core']['in_core'])
 def test_ties_keep_all(self):
  r=analyze(controls()[3]['input']);self.assertEqual(len(r['optimal']),2);self.assertEqual([z['payments']for z in r['outcomes']],[[7,0],[0,7]]);self.assertEqual(r['utilities'],[0,0]);self.assertEqual(r['revenue'],7)
 def test_one_bidder(self):
  r=analyze(controls()[4]['input']);self.assertEqual(r['utilities'],[9]);self.assertEqual(r['revenue'],0);self.assertTrue(r['core']['in_core']);self.assertTrue(all(z['price']==0 for z in r['menus'][0]['entries']))
 def test_all_zero(self):
  r=analyze(controls()[5]['input']);self.assertEqual(len(r['optimal']),64);self.assertEqual(r['revenue'],0);self.assertEqual(r['core']['max_deficit'],0);self.assertTrue(verify(r))
 def test_complements_win(self):
  r=analyze(controls()[6]['input']);self.assertEqual(r['outcomes'][0]['payments'],[12,0,0]);self.assertEqual(r['utilities'],[3,0,0]);self.assertTrue(r['core']['in_core'])
 def test_revenue_nonmonotonic(self):
  a,b=analyze(controls()[7]['input']),analyze(controls()[0]['input']);self.assertEqual(a['welfare'],10);self.assertEqual(a['revenue'],6);self.assertEqual(b['revenue'],8)
  # Stronger developed equal-value split: entry raises welfare yet removes all revenue.
  p=dict(version=1,items=2,values=[[0,0,0,10],[0,10,0,10]],deviations=[[],[]]);x=analyze(p);p['values'].append([0,0,10,10]);p['deviations'].append([]);y=analyze(p);self.assertEqual((x['welfare'],x['revenue']),(10,10));self.assertEqual((y['welfare'],y['revenue']),(20,0));self.assertTrue(verify(y))
 def test_menu_matches_all_truthful_allocations(self):
  for c in controls():
   r=analyze(c['input'])
   for menu in r['menus']:
    i=menu['bidder'];actual=sorted({r['allocations'][k]['bundles'][i]for k in r['optimal']});self.assertEqual(actual,menu['best_bundles']);self.assertEqual(menu['best_utility'],max(z['true_utility']for z in menu['entries']))
    for z in r['outcomes']:self.assertEqual(z['payments'][i],menu['entries'][r['allocations'][z['allocation']]['bundles'][i]]['price'])
 def test_menu_report_independence(self):
  for c in controls():
   p=copy.deepcopy(c['input']);a=analyze(p)
   for i in range(len(p['values'])):
    q=copy.deepcopy(p);q['values'][i]=[0]*len(p['values'][i]);b=analyze(q);self.assertEqual([z['price']for z in a['menus'][i]['entries']],[z['price']for z in b['menus'][i]['entries']])
 def test_every_tested_deviation_nonprofitable(self):
  for c in controls():
   r=analyze(c['input'])
   for a in r['deviation_audit']:
    for z in a['reports']:self.assertLessEqual(z['max_gain'],0)
 def test_report_ties_not_prefiltered_by_truth(self):
  r=analyze(controls()[4]['input']);z=r['deviation_audit'][0]['reports'][0];self.assertEqual(len(z['outcomes']),4);self.assertEqual((z['min_gain'],z['max_gain']),(-9,0))
 def test_payoff_conservation_and_ir(self):
  for c in controls():
   r=analyze(c['input']);self.assertEqual(r['revenue']+sum(r['utilities']),r['welfare']);self.assertGreaterEqual(min(r['utilities']),0);self.assertEqual(r['core']['rows'][-1]['slack'],0)
   for z in r['outcomes']:
    self.assertGreaterEqual(min(z['payments']),0)
    for i,v in enumerate(z['witnesses']):self.assertLessEqual(v['payment'],v['declared_value'])
 def test_affine_scale(self):
  p=copy.deepcopy(controls()[0]['input']);a=analyze(p);p['values']=[[v*2 for v in row]for row in p['values']];p['deviations']=[[[min(100,v*2)for v in row]for row in reports]for reports in p['deviations']];b=analyze(p);self.assertEqual(a['optimal'],b['optimal']);self.assertEqual(b['welfare'],2*a['welfare']);self.assertEqual(b['revenue'],2*a['revenue']);self.assertEqual(b['core']['max_deficit'],2*a['core']['max_deficit']);self.assertTrue(verify(b))
 def test_bidder_relabeling(self):
  for c in controls():
   p=copy.deepcopy(c['input']);a=analyze(p);p['values'].reverse();p['deviations'].reverse();b=analyze(p);self.assertEqual(b['welfare'],a['welfare']);self.assertEqual(b['revenue'],a['revenue']);self.assertEqual(b['utilities'],a['utilities'][::-1]);self.assertEqual(b['core']['max_deficit'],a['core']['max_deficit']);self.assertTrue(verify(b))
 def test_all_tiny_valuations(self):
  count=0
  for a,b,c in itertools.product(range(4),repeat=3):
   p=dict(version=1,items=1,values=[[0,a],[0,b],[0,c]],deviations=[[[0,k]for k in range(4)]]*3);self.assertTrue(verify(analyze(p)));count+=1
  self.assertEqual(count,64)
 def test_exhaustive_two_good_small_types(self):
  types=[[0,a,b,c]for a,b,c in itertools.product(range(3),repeat=3)if c>=max(a,b)];self.assertEqual(len(types),14);profiles=reports=outcomes=0
  for a,b in itertools.product(types,repeat=2):
   p=dict(version=1,items=2,values=[a,b],deviations=[types,types])
   # Public schema caps supplied reports at six. Split the complete finite type universe into valid batches.
   for start in range(0,len(types),6):
    p['deviations']=[types[start:start+6],types[start:start+6]];r=analyze(p);self.assertTrue(verify(r));reports+=sum(len(z['reports'])for z in r['deviation_audit']);outcomes+=sum(len(z['outcomes'])for d in r['deviation_audit']for z in d['reports'])
   profiles+=1
  self.assertEqual((profiles,reports),(196,5488));print('TWO_GOOD_SMALL_TYPE_EXHAUSTION',profiles,'REPORTS',reports,'ALL_TIE_OUTCOMES',outcomes)
 def test_item_relabeling(self):
  for c in controls():
   p=copy.deepcopy(c['input']);m=p['items'];perm=lambda k:sum(((k>>j)&1)<<(m-j-1)for j in range(m));a=analyze(p);p['values']=[[row[perm(k)]for k in range(1<<m)]for row in p['values']];p['deviations']=[[[row[perm(k)]for k in range(1<<m)]for row in reports]for reports in p['deviations']];b=analyze(p);self.assertEqual((a['welfare'],a['revenue'],a['utilities'],a['core']['max_deficit']),(b['welfare'],b['revenue'],b['utilities'],b['core']['max_deficit']));self.assertTrue(verify(b))
 def test_structural_rejection_and_detachment(self):
  p=controls()[0]['input'];r=analyze(p);r['deviation_audit'][0]['reports'][0]['report'][3]=1;self.assertEqual(p['deviations'][0][0][3],0)
  for field in ['allocations','coalitions','outcomes','utilities','deviation_audit','menus']:
   for mode in ['missing','duplicate','reordered']:
    r=analyze(p)
    if mode=='missing':r[field].pop()
    elif mode=='duplicate':r[field].append(copy.deepcopy(r[field][0]))
    else:r[field].reverse()
    if mode=='reordered'and len(r[field])<2:continue
    with self.assertRaises(ValueError):verify(r)
  r=analyze(p);r['extra']=None
  with self.assertRaises(ValueError):verify(r)
 def test_forgery_rejection(self):
  total=0
  for c in [controls()[0],controls()[3],controls()[15]]:
   r=analyze(c['input']);paths=[]
   def walk(v,path):
    if type(v)is dict:
     for k,z in v.items():
      if path or k!='input':walk(z,path+[k])
    elif type(v)is list:
     for k,z in enumerate(v):walk(z,path+[k])
    else:paths.append(path)
   walk(r,[])
   for path in paths:
    z=copy.deepcopy(r);q=z
    for k in path[:-1]:q=q[k]
    v=q[path[-1]];q[path[-1]]=v+1 if type(v)is int else not v if type(v)is bool else'forged'
    with self.assertRaises(ValueError,msg=str(path)):verify(z)
   total+=len(paths)
  print('PRIMITIVE_FORGERIES',total)
 def test_import_independence(self):subprocess.run([sys.executable,'-c','from auctionlab import verify;import sys;assert "auctionlab.engine"not in sys.modules'],check=True)
 def test_schema_and_parser(self):
  p=controls()[0]['input']
  for k,v in [('version',True),('items',True),('items',0),('items',5),('values',[]),('values',[[0,3,0,2]]),('values',[[0,0,0,101]]),('values',[[False,0,0,0]]),('deviations',[]),('deviations',[[[0,0,0,0]]*7]*3)]:
   q=copy.deepcopy(p);q[k]=v
   with self.assertRaises(ValueError):parse(q)
  for t in ['{"x":1,"x":2}','{"x":1.0}','{"x":1e0}','{"x":NaN}']:
   with self.assertRaises(ValueError):loads(t)
 def test_cli_and_limits(self):
  z=subprocess.run([sys.executable,'-m','auctionlab','demo'],capture_output=True,text=True,check=True);self.assertTrue(verify(json.loads(z.stdout)))
  with tempfile.TemporaryDirectory()as d:
   f=Path(d)/'input.json'
   for t in ['x'*65537,'['*2000+']'*2000,'{}']:
    f.write_text(t);z=subprocess.run([sys.executable,'-m','auctionlab','run',str(f)],capture_output=True,text=True);self.assertEqual(z.returncode,2);self.assertFalse(z.stdout);self.assertNotIn('Traceback',z.stderr)
if __name__=='__main__':unittest.main()
