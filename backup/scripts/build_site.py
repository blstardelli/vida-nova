import json
ref=json.load(open('out/refeicoes.json')); dia=json.load(open('out/diario.json'))
bands=[(5,7),(8,10),(11,13),(14,16),(17,19),(20,22),(23,25),(26,28)]
ffm=json.load(open('out/ff_prato.json'))
AL=json.load(open('out/alimentos_dia.json'))
data=[]
for r in dia:
    rs=[x for x in ref if x['dia']==r['dia']]
    o={"dia":r['dia'],"label":r['dia'][8:10]+'/'+r['dia'][5:7],"kcal":r['kcal'],"p":r['proteina'],"c":r['carbo'],"g":r['gordura'],"f":r.get('fibra',0),"ff":ffm.get(r['dia'][8:10]+'/'+r['dia'][5:7])}
    o["a"]=[[x["n"],x["k"],x.get("c",1)] for x in AL.get(o["label"],[])]
    o["b"]=[sum(x['kcal'] for x in rs if a<=x['hora']<=b) for a,b in bands]
    data.append(o)
import os
if os.environ.get('DIA_ABERTO')==data[-1]['label']: data[-1]['aberto']=True
html=open('site_template.html').read().replace('/*DATA*/[]',json.dumps(data,ensure_ascii=False)).replace('__ULTIMO__',data[-1]['label']+'/2026'+(' (dia em andamento: valores parciais, o déficit do dia ainda vai mudar)' if __import__('os').environ.get('DIA_ABERTO')==data[-1]['label'] else ''))
open('site/index.html','w').write(html)
print(len(html),data[-1])
