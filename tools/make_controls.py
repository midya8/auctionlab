"""Developed finite teaching profiles. Classical bundle-versus-singletons pattern credited."""
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from auctionlab.model import valuation
from auctionlab import analyze,verify
controls=[]
def add(name,m,values):
 ds=[]
 for row in values:
  ds.append([[0]*(1<<m),row[:],[min(100,2*v)for v in row],[v//2 for v in row],[0]+[100]*((1<<m)-1)])
 p=dict(version=1,items=m,values=values,deviations=ds);assert verify(analyze(p));controls.append(dict(id=name,input=p))
add('truthful_not_in_core',2,[[0,0,0,10],[0,6,0,6],[0,0,6,6]])
add('substitutes_restore_core',2,[[0,5,5,10],[0,6,0,6],[0,0,6,6]])
add('one_good_second_price',1,[[0,9],[0,7],[0,3]])
add('tied_winners',1,[[0,7],[0,7]])
add('one_bidder_zero_externality',2,[[0,2,3,9]])
add('all_zero',3,[[0]*8]*3)
add('complements_win',2,[[0,0,0,15],[0,6,0,6],[0,0,6,6]])
add('before_extra_competition',2,[[0,0,0,10],[0,6,0,6]])
add('asymmetric_split',2,[[0,0,0,12],[0,9,0,9],[0,0,5,5]])
add('tied_complement_split',2,[[0,0,0,12],[0,6,0,6],[0,0,6,6]])
add('unit_demand',2,[[0,8,8,8],[0,7,7,7],[0,6,6,6]])
add('additive',2,[[0,4,3,7],[0,2,5,7],[0,3,3,6]])
add('three_way_complement',3,[[0,0,0,0,0,0,0,16],[0,5,6,11,0,5,6,11],[0,0,0,0,8,8,8,8]])
add('four_goods',4,[[5*mask.bit_count()for mask in range(16)],[9 if mask&3==3 else 0 for mask in range(16)],[15 if mask&12==12 else 0 for mask in range(16)]])
add('zero_marginal_extra_item',2,[[0,4,0,4],[0,3,0,3]])
add('single_good_zero',1,[[0,0]])
root=Path(__file__).resolve().parents[1]
for c in controls:(root/'examples'/f"{c['id']}.json").write_text(json.dumps(c['input'],separators=(',',':'))+'\n')
(root/'docs/controls.json').write_text(json.dumps(controls,separators=(',',':'))+'\n');(root/'auctionlab/controls.py').write_text('"""Developed synthetic controls. Not held-out tests."""\nimport copy\n_CONTROLS='+repr(controls)+'\ndef controls():return copy.deepcopy(_CONTROLS)\n')
print('DEVELOPED_CONTROLS',len(controls))
