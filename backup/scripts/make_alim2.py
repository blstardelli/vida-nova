import json
src=open("make_saciedade.py").read()
exec(src[:src.index("res=[]")].split("SURFACE=")[0])
exec(open("make_alim.py").read().split("dia=json")[0].split("exec(src")[0]) if False else None
dens={"patinho":219,"pao_fr":300,"pao_br":300,"ketchup":106,"strog":135,"arroz_lent":118,"sonho":525,"ouro":530}
names={"goiaba":"Goiaba","arroz_lent":"Arroz com lentilha","strog":"Strogonoff de frango","patinho":"Patinho moído","ovo":"Ovos","pao_int":"Pão de forma integral","mussarela":"Mussarela","whey":"Whey + leite","pao_fr":"Pão francês","tilapia":"Tilápia","fradinho":"Feijão fradinho","folhas":"Folhas","bife":"Bife","contra":"Contrafilé","mand_frita":"Mandioca frita","cenoura":"Cenoura","pepino":"Pepino","tomate":"Tomate","banana":"Banana","iogurte":"Iogurte grego","broa":"Broa de canjica","bat_frita":"Batata frita","arroz_int":"Arroz integral","manteiga":"Manteiga","ketchup":"Ketchup","sonho":"Sonho de Valsa","ouro":"Ouro Branco","pao_br":"Pão francês"}
dia={x["dia"][8:10]+"/"+x["dia"][5:7]:x["kcal"] for x in json.load(open("out/diario.json"))}
liq={"11/11":{"Azeite":205,"Óleo da air fryer":90},
"12/11":{"Suco de laranja":315},
"14/11":{"Suco de laranja":202,"Água de coco":70,"Expresso com chantilly":55,"Azeite":27},
"16/11":{"Suco de laranja":194},"17/11":{"Suco de laranja":238},
"18/11":{"Açaí":590,"Suco de laranja":180},"19/11":{"Água de coco":70},
"20/11":{"Suco de laranja":68,"Baly (energético)":110}}
fix={"12/11":{"Whey + leite":243},"14/11":{"Whey + leite":243}}
final={}
for d,items in D.items():
    if d in("13/11","21/11","22/11"): continue
    agg={}
    for n,g in items:
        k=g/30*212 if n=="whey" else g*dens.get(n,C[n][0])/100
        agg[names[n]]=agg.get(names[n],0)+k
    agg.update(fix.get(d,{}))
    L=liq.get(d,{}); target=dia[d]-sum(L.values()); f=target/sum(agg.values())
    print(d,"escala dos sólidos",round(f,3))
    out=[{"n":k,"k":round(v*f)} for k,v in agg.items()]+[{"n":k,"k":v} for k,v in L.items()]
    final[d]=out
E=lambda l:[{"n":a,"k":b} for a,b in l]
final["13/11"]=E([("Patinho moído",899),("Arroz com lentilha",706),("Whey + leite",212),("Suco de laranja",180),("Tilápia",104),("Goiaba",82),("Azeite",45),("Pepino",38),("Cenoura",12)])
final["21/11"]=E([("Patinho moído",329),("Arroz com lentilha",389),("Ouro Branco",270),("Whey + leite",212),("Pão de forma integral",520),("Strogonoff de frango",514),("Sonho de Valsa",105),("Ketchup",104)])
final["22/11"]=E([("Arroz com lentilha",271),("Strogonoff de frango",506),("Goiaba",190),("Ouro Branco",180),("Pão de forma integral",455),("Ricota",33),("Ketchup",90),("Sonho de Valsa",315),("Azeite",45),("Pepino",38)])
final["23/11"]=E([("Strogonoff de frango",804),("Goiaba",252),("Arroz com lentilha",250),("Ovos",215),("Whey + leite",212),("Arroz com brócolis",179),("Pão francês",150),("Pão de forma integral",130),("Sonho de Valsa",105),("Presunto",96),("Ouro Branco",90),("Pepino",63),("Azeite",35)])
for d in final:
    final[d].sort(key=lambda x:-x["k"])
    t=sum(x["k"] for x in final[d]); print(d,t,dia[d],t-dia[d])
json.dump(final,open("out/alimentos_dia.json","w"),ensure_ascii=False)
