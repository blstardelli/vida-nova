import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt, numpy as np, json
def FF(cal,pr,df,tf):
    cal=max(cal,30);pr=min(pr,30);df=min(df,12);tf=min(tf,50)
    return min(5.0,max(0.5,37/60+(2500/60)*cal**-0.7+(3/60)*pr+df**3/1620-tf**3/138000))
# kcal/100g, prot, fibra, gord
C={"goiaba":(68,2.55,5.4,.95),"arroz_lent":(118,6.9,5.8,.6),"strog":(135,17,.5,5.5),"patinho":(171,27.4,0,6.4),
"ovo":(155,12.6,0,10.6),"pao_int":(252,12.4,6.0,3.5),"mussarela":(300,22.2,0,22.4),"whey":(400,80,0,6.7),
"pao_fr":(289,9.4,2.4,3.5),"tilapia":(128,26.2,0,2.7),"fradinho":(116,7.7,6.5,.5),"folhas":(15,1.4,1.3,.15),
"bife":(180,28,0,7),"contra":(220,29,0,11),"mand_frita":(300,2,2.5,14),"cenoura":(41,.9,2.8,.2),
"pepino":(15,.65,.5,.11),"tomate":(18,.9,1.2,.2),"banana":(89,1.1,2.6,.3),"iogurte":(120,4,0,5),
"broa":(330,4.5,2.0,12.5),"bat_frita":(300,3,3.5,15),"arroz_int":(123,2.74,1.6,.97),"manteiga":(717,.85,0,81),
"ketchup":(101,1,.3,.1),"sonho":(525,7.5,1,30),"ouro":(530,6,1,29),"pao_br":(253,8.7,2.3,3.1)}
D={
"11/11":[("goiaba",200),("arroz_lent",150),("tilapia",150),("whey",30),("pao_fr",100),("manteiga",10),("arroz_lent",200),("ovo",200),("pao_fr",50),("manteiga",5),("pao_int",25),("banana",73),("iogurte",100),("pepino",250)],
"12/11":[("pao_int",50),("ovo",150),("bife",120),("fradinho",50),("folhas",100),("mand_frita",50),("broa",88),("pao_fr",50),("mussarela",40),("whey",60),("goiaba",120),("pepino",250)],
"13/11":[("arroz_lent",560),("cenoura",30),("tilapia",80),("patinho",410),("goiaba",120),("whey",30),("pepino",250)],
"14/11":[("pao_br",50),("ovo",150),("arroz_lent",170),("patinho",340),("pepino",250),("goiaba",420),("whey",30),("pao_fr",150),("mussarela",100),("tomate",120),("ketchup",80)],
"15/11":[("ovo",150),("pao_fr",100),("arroz_lent",370),("patinho",575),("pepino",250),("goiaba",230),("mussarela",40),("ketchup",33)],
"16/11":[("patinho",310),("arroz_lent",100+100+195+130),("pepino",250),("whey",30),("strog",350),("pao_fr",50),("mussarela",40)],
"17/11":[("arroz_lent",390),("strog",545),("goiaba",500),("pao_fr",100),("mussarela",80),("ketchup",55),("tomate",120),("pepino",250)],
"18/11":[("arroz_int",180),("strog",250),("pao_fr",25),("whey",30),("arroz_lent",270),("patinho",330),("sonho",80),("ouro",17),("pao_int",125),("ketchup",33),("pepino",250)],
"19/11":[("arroz_lent",280),("patinho",320),("whey",30),("pao_int",25),("bat_frita",200),("contra",50),("sonho",20),("ouro",17),("pepino",250)],
"20/11":[("pao_int",75),("ovo",150),("goiaba",347),("patinho",480),("arroz_lent",420),("ouro",20),("sonho",20),("pepino",250)],
"21/11":[("patinho",150),("arroz_lent",330),("ouro",60),("whey",30),("pao_int",200),("strog",380),("sonho",20),("ketchup",136),("pepino",250)],
"22/11":[("goiaba",280),("arroz_lent",100),("strog",200),("ouro",40),("pepino",250)],
}
res=[]
for d,items in D.items():
    pts=0;k=0
    for n,g in items:
        c,p,df,f=C[n]; ff=FF(c,p,df,f)
        pts+=ff/c*g; k+=c*g/100
    res.append((d,pts,k,pts/k*100))
    print(f"{d} pontos={pts:5.1f} kcal_solidos={k:5.0f} pts/100kcal={pts/k*100:.2f}")
json.dump(res,open("out/saciedade_dia.json","w"))
SURFACE="#fcfcfb"; INK="#0b0b0b"; INK2="#52514e"; GRID="#e6e5e1"; BLUE="#2a78d6"; ORANGE="#eb6834"
days=[r[0] for r in res]; pts=np.array([r[1] for r in res]); den=np.array([r[3] for r in res])
x=np.arange(len(days))
fig,(a1,a2)=plt.subplots(2,1,figsize=(11.69,8.27),facecolor=SURFACE,sharex=True,gridspec_kw={"hspace":0.28})
for ax in (a1,a2):
    ax.set_facecolor(SURFACE); ax.grid(axis="y",color=GRID,lw=1); ax.set_axisbelow(True)
    for s in ("top","right","left"): ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(GRID); ax.tick_params(axis="y",labelsize=11,labelcolor=INK2,length=0); ax.tick_params(axis="x",length=0)
cols=[BLUE]*(len(days)-1)+["#8fb8ea"]
a1.bar(x,pts,width=0.62,color=cols,zorder=3)
for xi,v in zip(x,pts): a1.annotate(f"{v:.1f}".replace(".",","),(xi,v),textcoords="offset points",xytext=(0,6),ha="center",fontsize=11.5,fontweight="bold",color=INK)
a1.set_ylim(0,max(pts)*1.2); a1.set_ylabel("pontos de saciedade/dia",fontsize=11,color=INK2)
a2.plot(x,den,color=ORANGE,lw=2.4,marker="o",ms=8,mec=SURFACE,mew=2,zorder=3)
for xi,v in zip(x,den): a2.annotate(f"{v:.2f}".replace(".",","),(xi,v),textcoords="offset points",xytext=(0,10),ha="center",fontsize=11,fontweight="bold",color=INK)
a2.set_ylim(min(den)*0.8,max(den)*1.15); a2.set_ylabel("pontos por 100 kcal",fontsize=11,color=INK2)
a2.set_xticks(x); a2.set_xticklabels([d if d!="22/11" else "22/11\n(parcial)" for d in days],fontsize=12,color=INK2)
fig.suptitle("Saciedade por dia (11 a 22/11/2026)",x=0.075,y=0.975,ha="left",fontsize=18,fontweight="bold",color=INK)
fig.text(0.075,0.918,"Pontos = Σ FF ÷ kcal por 100 g × peso (g) de cada alimento sólido · em cima: total do dia · embaixo: pontos por 100 kcal",fontsize=10.5,color=INK2,ha="left")
fig.subplots_adjust(left=0.075,right=0.97,top=0.87,bottom=0.1)
fig.text(0.075,0.025,"Sem líquidos (sucos, leite, água de coco, açaí, azeite). Pesos e composições reconstruídos do histórico; 21/11 a partir dos lançamentos resumidos. Valores aproximados.",fontsize=9,color=INK2,ha="left")
fig.savefig("out/saciedade_por_dia.jpg",dpi=200,facecolor=SURFACE,pil_kwargs={"quality":95})
fig.savefig("out/prev_saciedade.png",dpi=70,facecolor=SURFACE)
