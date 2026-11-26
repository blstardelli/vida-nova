import json,shutil,subprocess,collections,sys
J=['refeicoes','diario','ff_prato','alimentos_dia']
for f in J: shutil.copy(f'out/{f}.json',f'bak/{f}.json')
base={f:json.load(open(f'out/{f}.json')) for f in J}
od=json.load(open('open_day.json'));E=od['entries'];dia=od['dia'];lab=od['label']
R=[x for x in base['refeicoes'] if x['dia']!=dia];D=[x for x in base['diario'] if x['dia']!=dia]
F=dict(base['ff_prato']);A=dict(base['alimentos_dia'])
hh=collections.OrderedDict()
for e in E: hh[e['h']]=hh.get(e['h'],0)+e['k']
R+=[{"dia":dia,"hora":h,"kcal":round(k)} for h,k in hh.items()]
s=lambda k:int(sum(e[k] for e in E)+.5)
D.append({"dia":dia,"kcal":s('k'),"proteina":s('p'),"carbo":s('c'),"gordura":s('g'),"fibra":s('f')})
F[lab]=od['ff']
ag=collections.OrderedDict()
for e in E:
    a=ag.setdefault(e['n'],[0,0]);a[0]+=e['k'];a[1]+=1
A[lab]=[{"n":n,"k":round(k),"c":c} for n,(k,c) in sorted(ag.items(),key=lambda x:-x[1][0])]
for f,v in zip(J,[R,D,F,A]): json.dump(v,open(f'out/{f}.json','w'),ensure_ascii=False)
import os;subprocess.run(['python3','build_site.py'],check=True,env={**os.environ,'DIA_ABERTO':lab},stdout=subprocess.DEVNULL)
for f in J: shutil.copy(f'bak/{f}.json',f'out/{f}.json')
print('ok',D[-1])
