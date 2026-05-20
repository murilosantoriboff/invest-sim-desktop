# Funcionalidades — Regra de Negócio

## Visão geral

A regra de negócio fica em `src/core/` com dois módulos:

- `calculator.py` — cálculos financeiros e preparação de dados pro gráfico
- `constants.py` — cores, dimensões, mapeamento de investimentos

Nenhum depende de Tkinter ou Supabase.

---

## Funções do calculator.py

### `projetar_valor(valor, taxas_por_ano, ano_inicio, anos)`

Calcula o valor futuro aplicando juros compostos ano a ano com taxas variáveis. Usada para investimentos de renda fixa (SELIC, CDI, IPCA, POUPANCA, IGPM). As taxas vêm da view do Supabase separadas por ano de referência (2025, 2026, 2027...). Quando o prazo ultrapassa os anos disponíveis, repete a última taxa.

Exemplo: R$ 10.000 com taxas {2026: 14.75%, 2027: 12.50%, 2028: 10.00%} por 5 anos → R$ 17.182,38 (2029 e 2030 usam 10%).

### `projetar_cotacao(valor, cotacoes_por_ano, ano_inicio, anos)`

Usada exclusivamente para o investimento CAMBIO (Dólar). Diferente dos outros indicadores, a `vlr_mediana` do Câmbio no Focus do BCB representa uma **cotação em R$/USD** (ex.: 5,30), não uma taxa percentual. Por isso, o cálculo segue a fórmula `valor × (cotação_final / cotação_inicial)`. Se o prazo ultrapassa os anos disponíveis, usa a última cotação conhecida; se a cotação inicial for inválida, devolve o valor original.

Exemplo: R$ 10.000 com cotações {2026: 5,10; 2027: 5,17} por 1 ano → R$ 10.137,25 (10.000 × 5,17/5,10).

### `preparar_dados_grafico(itens_carteira, taxas_indicadores, anos, ano_inicio)`

Combina a carteira do usuário com as taxas e gera os dados prontos pro gráfico. Cada item retornado tem: valor investido, valor futuro, ganho, percentual, taxa de exibição e cor. Internamente escolhe entre `projetar_valor` (renda fixa) ou `projetar_cotacao` (CAMBIO) conforme o código do investimento. Se `ano_inicio` não for informado, usa o ano corrente do sistema.

A `taxa_exibicao` é calculada como a **taxa anualizada equivalente** (média geométrica) — ou seja, a taxa fixa que produziria o mesmo `valor_futuro` no prazo solicitado. Isso vale tanto pra renda fixa quanto pra CAMBIO, mantendo a unidade "% a.a." consistente em todos os cards.

### `calcular_totais(dados_grafico)`

Soma os totais da carteira inteira (investido, futuro, ganho, percentual geral). Usado pra mostrar os valores no centro do gráfico.

---

## Constantes

O dicionário `INVESTIMENTOS` mapeia cada código pra nome de exibição e cor. Os códigos são os mesmos da `vw_indicadores_investimento`:

| Código | Nome | Cor |
|---|---|---|
| SELIC | Tesouro Selic | #3B6FE0 |
| CDI | CDB 100% CDI | #DC4437 |
| IPCA | Tesouro IPCA+ | #16A34A |
| POUPANCA | Poupança | #9333EA |
| IGPM | IGP-M | #EAB308 |
| CAMBIO | Dólar | #14B8A6 |

---

## Requisitos atendidos

| Requisito | Função | Status |
|---|---|---|
| Calcular rendimento com juros compostos | `projetar_valor()` | OK |
| Usar taxas reais do BCB por ano | `projetar_valor()` | OK |
| Projetar Dólar pela razão entre cotações | `projetar_cotacao()` | OK |
| Combinar carteira com taxas pro gráfico | `preparar_dados_grafico()` | OK |
| Exibir taxa anualizada equivalente no card | `preparar_dados_grafico()` | OK |
| Totais agregados da carteira | `calcular_totais()` | OK |

---

## Validação

`src/tests/testar_calculator.py` — 30 cenários cobrindo projeção com taxa fixa e variável, projeção cambial por cotação, taxa anualizada equivalente, auxiliares, organização de taxas e integração com dados do Supabase.

Rodar a partir de `src/`: `python tests/testar_calculator.py`

---

*Última atualização: Semana 7 — 19/05/2026*
