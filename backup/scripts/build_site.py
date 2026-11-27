import json
ref=json.load(open('out/refeicoes.json')); dia=json.load(open('out/diario.json'))
bands=[(5,7),(8,10),(11,13),(14,16),(17,19),(20,22),(23,25),(26,28)]
ffm=json.load(open('out/ff_prato.json'))
AL=json.load(open('out/alimentos_dia.json'))
import os
AH=json.load(open('out/alimentos_hora.json')) if os.path.exists('out/alimentos_hora.json') else {}
def bi(h):
    h=h+24 if h<5 else h
    for i,(a,b) in enumerate(bands):
        if a<=h<=b:return i
    return None
data=[]
for r in dia:
    rs=[x for x in ref if x['dia']==r['dia']]
    o={"dia":r['dia'],"label":r['dia'][8:10]+'/'+r['dia'][5:7],"kcal":r['kcal'],"p":r['proteina'],"c":r['carbo'],"g":r['gordura'],"f":r.get('fibra',0),"ff":ffm.get(r['dia'][8:10]+'/'+r['dia'][5:7])}
    o["b"]=[sum(x['kcal'] for x in rs if a<=x['hora']<=b) for a,b in bands]
    if o["label"] in AH:
        g={}
        for e in AH[o["label"]]:
            i=bi(e['h']);d=g.setdefault(e['n'],[0,0,[0]*8,[0]*8])
            d[0]+=e['k'];d[1]+=1
            if i is not None:d[2][i]+=e['k'];d[3][i]+=1
        o["a"]=[[n,round(d[0]),d[1],[round(v) for v in d[2]],1,d[3]] for n,d in sorted(g.items(),key=lambda x:-x[1][0])]
    else:
        tb=sum(o["b"]) or 1;o["a"]=[]
        for x in AL.get(o["label"],[]):
            o["a"].append([x["n"],x["k"],x.get("c",1),[round(x["k"]*v/tb) for v in o["b"]],0,None])
    data.append(o)
if os.environ.get('DIA_ABERTO')==data[-1]['label']: data[-1]['aberto']=True
html=open('site_template.html').read().replace('/*DATA*/[]',json.dumps(data,ensure_ascii=False)).replace('__ULTIMO__',data[-1]['label']+'/2026'+(' (dia em andamento: valores parciais, o déficit do dia ainda vai mudar)' if __import__('os').environ.get('DIA_ABERTO')==data[-1]['label'] else ''))
open('site/index.html','w').write(html)
print(len(html),data[-1])
