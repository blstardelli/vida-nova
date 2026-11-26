import json
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter
src=open('make_saciedade.py').read()
exec(src[:src.index("res=[]")].split("SURFACE=")[0])   # FF, C, D
C["ricota"]=(110,6,0,6)
C["mix5050"]=(119.3,5.86,4.75,0.69)
D["22/11"]=D["22/11"]+[("pao_int",50),("ricota",30),("arroz_lent",130),("strog",175),("pao_int",75),("ketchup",51),("pao_int",50),("ketchup",34),("sonho",20)]
D["23/11"]=[("ovo",150),("pao_int",52),("goiaba",370),("mix5050",150),("strog",205),("pepino",420)]
ref=json.load(open('out/refeicoes.json')); dia=json.load(open('out/diario.json'))
ffp=json.load(open('out/ff_prato.json')); ffw=json.load(open('out/ff_dia.json'))
ref+= [{"dia":"2026-11-23","hora":h,"kcal":k} for h,k in {7:380,8:252,10:519}.items()]
def prato(items):
    g=k=p=fi=fa=0
    for n,gr in items:
        c,pr,df,f=C[n]; g+=gr;k+=c*gr/100;p+=pr*gr/100;fi+=df*gr/100;fa+=f*gr/100
    r=100/g; return round(FF(k*r,p*r,fi*r,fa*r),2)
ffp["23/11"]=prato(D["23/11"])
dia.append({"dia":"2026-11-23","kcal":1151,"proteina":79,"carbo":135,"gordura":39,"fibra":32})
F=Font(name="Arial",size=10); B=Font(name="Arial",size=10,bold=True,color="FFFFFF"); fill=PatternFill("solid",fgColor="305496")
wb=Workbook()
def sheet(title,hdr,rows,widths,first=False):
    ws=wb.active if first else wb.create_sheet()
    ws.title=title; ws.append(hdr)
    for r in rows: ws.append(r)
    for row in ws.iter_rows():
        for c in row: c.font=F; c.alignment=Alignment(vertical="top",wrap_text=True)
    for c in ws[1]: c.font=B; c.fill=fill
    for i,w in enumerate(widths,1): ws.column_dimensions[get_column_letter(i)].width=w
    ws.freeze_panes="A2"; return ws
rows=[]
for r in dia:
    lb=r['dia'][8:10]+'/'+r['dia'][5:7]
    rows.append([lb+(" (parcial, até 10:40)" if lb=="23/11" else ""),r['kcal'],r['proteina'],r['carbo'],r['gordura'],r.get('fibra'),ffp.get(lb),ffw.get(lb)])
sheet("Diário",["Dia (2026)","kcal","Proteína (g)","Carboidrato (g)","Gordura (g)","Fibra (g)","FF do dia (prato único)","FF ponderado pelas kcal (obsoleto)"],rows,[24,10,13,15,13,10,22,26],True)
sheet("kcal por hora",["Dia","Hora do relógio (>=24 = após meia-noite, conta no dia anterior)","kcal"],[[r['dia'],r['hora'],r['kcal']] for r in ref],[14,40,10])
al=[]
for d,items in D.items():
    for n,g in items: al.append([d,n,g])
sheet("Alimentos por dia",["Dia","Alimento (código)","Peso (g)"],al,[10,24,12])
sheet("Composições",["Alimento (código)","kcal/100 g","Proteína (g/100 g)","Fibra (g/100 g)","Gordura (g/100 g)","FF"],
      [[n,c,p,fi,fa,round(FF(c,p,fi,fa),2)] for n,(c,p,fi,fa) in C.items()],[24,12,18,15,17,8])
regras=[
["Meta diária","2.200 kcal a partir de 23/11 (antes: 2.450 kcal)"],
["Gasto calórico usado nos gráficos de saldo","2.800 kcal (antes 2.700)"],
["Objetivo de gordura","32 g/dia = −246 kcal/dia vs. gasto de 2.700; 7.700 kcal ≈ 1 kg de gordura"],
["Janela do dia","15 h a partir do primeiro lançamento do dia"],
["Ritmo esperado","Até 22/11: 450 kcal no primeiro lançamento + 133,33 kcal/h (chega a 2.450). Desde 23/11: 450 kcal + 116,67 kcal/h (chega a 2.200 no fim da janela)"],
["Tabela a cada lançamento","Hora, janela, tempo decorrido, consumido, esperado no ritmo, diferença, falta para a meta, FF do dia e fibra do dia"],
["Pepino japonês","Reestimado em 250 g/dia às 12:00 para todos os dias de 11/11 a 22/11 (valor real informado)"],
["Arroz com lentilha","A partir de 23/11: meio a meio (arroz integral + lentilha), 119 kcal/100 g (P 5,9, fibra 4,8, G 0,7)"],
["Lançamentos após a meia-noite","Contam no dia anterior (dentro da janela)"],
["Combo Whey","150 ml de leite integral + 30 g de whey = 212 kcal (P 29, C 10, G 7)"],
["Arroz com lentilha (até 22/11)","2/3 lentilha + 1/3 arroz integral: 118 kcal/100 g (P 7, C 22, G 0,6)"],
["Patinho moído","cozido: 219 kcal/100 g (36 P, 7 G) nos lançamentos; 171 kcal/100 g (USDA) no cálculo do FF"],
["Strogonoff de frango (creme de ricota light)","135 kcal/100 g (~17 P, 4 C, 5,5 G)"],
["Outros","Ouro Branco 90 kcal/20 g; Sonho de Valsa 105 kcal; pão de forma integral 65 kcal/fatia; pão francês 150 kcal/50 g; mussarela 60 kcal/fatia; goiaba USDA 68 kcal/100 g; ketchup ~1,06 kcal/g"],
["Faixas de 3 horas","05–07, 08–10, 11–13, 14–16, 17–19, 20–22, 23–01, 02–04 (horas do relógio)"],
["Fórmula do FF (Fullness Factor)","FF = 0,6167 + 41,67 × kcal^−0,7 + 0,05 × proteína + fibra³/1620 − gordura³/138000 (por 100 g; limites: kcal ≥30, proteína ≤30, fibra ≤12, gordura ≤50; resultado de 0,5 a 5). Aproximação: não foi possível confirmar na patente US 7.620.531."],
["FF do dia (prato único)","Soma peso, kcal, proteína, fibra e gordura dos sólidos (e whey) do dia, converte para 100 g e aplica a fórmula uma vez. Líquidos (sucos, leite, água de coco, açaí, azeite) ficam de fora."],
["Gatilho 'Raio x'","Enviar 3 gráficos: macros por dia, consumo de kcal vs. gasto (barras) e mediana por faixa de 3 h"],
["Gatilho 'dash horarios' / 'Vida Nova de Bruno'","Trazer o painel (artefato do Claude e site)"],
["Site","https://blstardelli.github.io/vida-nova/ (GitHub) e vida-nova-bruno.netlify.app (Netlify); atualização manual ao fechar cada dia"],
["Observação","Valores estimados a partir das porções informadas; 21/11 e 22/11 reconstruídos de resumos e podem ter pequenas diferenças. 23/11 está parcial (até 10:40). Fibra de 11 a 22/11 estimada."]]
sheet("Regras e convenções",["Item","Definição"],regras,[40,110])
wb.save("out/vida_nova_backup.xlsx")
json.dump({"diario":dia,"refeicoes":ref,"alimentos":D,"composicoes":C,"ff_prato":ffp,"ff_ponderado":ffw},open("out/vida_nova_backup.json","w"),ensure_ascii=False,indent=1)
print(len(rows),len(ref),len(al),ffp["22/11"],ffp["23/11"])
