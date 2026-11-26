# Vida Nova – regras para retomar a sessão (backup)

Usuário: Bruno (português, app mobile do Claude, fuso America/Sao_Paulo). Registra alimentos como "+quantidade de alimento".

## Resposta a cada "+alimento"
1. kcal e macros (P/C/G/fibra) de cada item e do total da entrada.
2. Tabela de ritmo: Hora, Janela de hoje, Tempo decorrido, Consumido, Esperado no ritmo, Diferença (acima/abaixo), Falta para a meta, FF do dia, Fibra do dia, Proteína do dia, Carboidrato do dia, Gordura do dia.
3. Atualizar `backup/open_day.json`, rodar `publish_open_day.py` e enviar o site (index.html) para a `main` do repositório (sem PR). Backup vai junto no mesmo commit.

## Ritmo
- Meta 2.450 kcal. Janela de 15 h a partir do primeiro registro do dia; esperado = 450 kcal no primeiro registro + 133,33 kcal/h.
- Se a janela for encurtada (ex.: 25/11 termina às 03:00), o ritmo é redistribuído: (2450 − 450) / horas da janela (25/11: 11h26 → 175 kcal/h).
- O dia só fecha quando o usuário disser. Registros após a meia-noite pertencem ao dia aberto. Um "Bom dia" no dia seguinte foi tratado como aviso de fechamento.
- Gasto 2.800 kcal/dia nos gráficos de saldo; 7.700 kcal ≈ 1 kg de gordura.

## FF (Fullness Factor)
FF = 0,6167 + 41,67·kcal^−0,7 + 0,05·proteína + fibra³/1620 − gordura³/138000 (por 100 g; kcal ≥ 30, proteína ≤ 30, fibra ≤ 12, gordura ≤ 50; limitar a 0,5–5).
FF do dia = todos os sólidos do dia somados como "um prato" (mais whey), por 100 g, fórmula aplicada uma vez. Líquidos (sucos, leite, água de coco, açaí, azeite, Baly, expresso, óleo) ficam FORA do FF do dia e não têm FF no site.
Patinho moído: 219 kcal/100 g nos registros, 171 kcal/100 g (P29, G6) para o FF.

## Convenções nutricionais
- Arroz com lentilha 50/50: 119,3 kcal/100 g (P5,86, C22,4, G0,69, fibra 4,75). Antes de 23/11: 118 kcal/100 g.
- Patinho moído cozido: 219 kcal/100 g (P31, G10,5). Strogonoff de frango 135 kcal/100 g (P15,5, C3,5, G6,5).
- Pepino 15 kcal/100 g. Goiaba 68 kcal/100 g (fibra 5,4). Suco de laranja 45 kcal/100 ml.
- Combo Whey = 150 ml leite + 30 g whey = 212 kcal (P29 C10 G7).
- Pão francês 150 kcal; pão de forma integral 65 kcal/fatia; Sonho de Valsa 105 kcal; Ouro Branco 90 kcal/20 g.
- Baly energético ≈ 44 kcal/100 ml (200 ml = 88 kcal, ~22 g carboidrato).
- Batata-baroa cozida: 80 kcal/100 g, FF 2,60, IG 55.
- IG (glicose=100): tabela `IGA` em `site_template.html` (valores aproximados; bombons estimados em 65).

## Site (index.html, Raio-X de Bruno)
- `site_template.html` + `build_site.py` leem `dados/*.json` (copiados de `out/`) e geram o index. Placeholders `/*DATA*/[]` e `__ULTIMO__`.
- Projeção (seção "Simulação de Monte Carlo: déficit calórico"): sempre do mês vigente (data do navegador); déficit acumulado só dos dias do mês; consumo estimado com os últimos 30 dias fechados; degraus de 100 g de gordura (7.700 kcal = 1 kg; ajustam sozinhos se q95 passar de 1 kg).
- Simulação tem 2 modos (botões "Pelo menos X" e "Entre X e Y").
- Dia aberto: `DIA_ABERTO=<dd/mm>` marca a última linha como `aberto` (botão "Hoje: sim/não" e aviso de parcial).
- Gráfico "O que consumi": ordenação por kcal, FF, Registros e IG (botão Combinar = ordenação múltipla), colunas Reg., FF e IG.
- Cartões: Balanço energético; Macronutrientes e fibra; Saciedade e horário.
- Preferência: gráficos/análises em JPG/PNG. Não alterar `peso.html`.
- Ao fechar um dia: gravar o dia definitivo em refeicoes/diario/ff_prato/alimentos_dia (com contagem de registros por alimento).

## Estado
Dados fechados: 11/11 a 25/11. Dia aberto: ver `open_day.json` (26/11, sem registros ainda). Para fechar um dia: `python3 publish_open_day.py --fechar` e depois `./push_repo.sh`, e zerar `open_day.json` para o próximo dia.
