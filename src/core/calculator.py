"""
calculator.py — Cálculos financeiros e preparação de dados para o gráfico.
"""

try:
    from src.core.constants import INVESTIMENTOS, R_HOLE, R_PRINC
except ModuleNotFoundError:
    from core.constants import INVESTIMENTOS, R_HOLE, R_PRINC


def projetar_valor(valor, taxas_por_ano, ano_inicio, anos):
    if not taxas_por_ano:
        return valor

    acumulado = valor
    anos_disponiveis = sorted(taxas_por_ano.keys())
    ultima_taxa = taxas_por_ano[anos_disponiveis[-1]]

    for i in range(anos):
        ano = ano_inicio + i
        taxa = taxas_por_ano.get(ano, ultima_taxa)
        acumulado *= (1 + taxa / 100)

    return acumulado


def calcular_ganho(valor, valor_futuro):
    return valor_futuro - valor


def calcular_percentual_ganho(valor, ganho):
    if valor <= 0:
        return 0.0
    return (ganho / valor) * 100


def preparar_dados_grafico(itens_carteira, taxas_indicadores, anos, ano_inicio=None):
    taxas_mapa = _organizar_taxas(taxas_indicadores)

    if ano_inicio is None:
        todos_anos = [ano for taxas in taxas_mapa.values() for ano in taxas]
        ano_inicio = min(todos_anos) if todos_anos else 2026

    resultados = []
    for item in itens_carteira:
        cod = item["cod_investimento"]
        valor = item["valor"]

        config = INVESTIMENTOS.get(cod)
        if config is None:
            continue

        taxas_por_ano = taxas_mapa.get(cod, {})
        valor_futuro = projetar_valor(valor, taxas_por_ano, ano_inicio, anos)

        if taxas_por_ano:
            primeiro_ano = min(taxas_por_ano.keys())
            taxa_exibicao = taxas_por_ano[primeiro_ano]
        else:
            taxa_exibicao = 0.0

        ganho = calcular_ganho(valor, valor_futuro)
        pct = calcular_percentual_ganho(valor, ganho)

        resultados.append({
            "cod_investimento": cod,
            "nome_exibicao":    config["nome_exibicao"],
            "valor":            valor,
            "valor_futuro":     round(valor_futuro, 2),
            "ganho":            round(ganho, 2),
            "percentual_ganho": round(pct, 1),
            "taxa_exibicao":    taxa_exibicao,
            "cor_rgb":          config["cor_rgb"],
            "cor_hex":          config["cor_hex"],
        })

    return resultados


def calcular_totais(dados_grafico):
    total_inv = sum(d["valor"] for d in dados_grafico)
    total_fut = sum(d["valor_futuro"] for d in dados_grafico)
    total_ganho = total_fut - total_inv
    pct = calcular_percentual_ganho(total_inv, total_ganho)

    return {
        "total_investido":        round(total_inv, 2),
        "total_futuro":           round(total_fut, 2),
        "total_ganho":            round(total_ganho, 2),
        "percentual_ganho_total": round(pct, 1),
    }


def calcular_raio_ganho(ganho, valor_base):
    espessura = R_PRINC - R_HOLE
    ratio = ganho / valor_base if valor_base > 0 else 0
    return R_PRINC + ratio * espessura


def _organizar_taxas(taxas_indicadores):
    mapa = {}
    for ind in taxas_indicadores:
        cod = ind.get("cod_investimento", "")
        ano = ind.get("ano_referencia")
        taxa = ind.get("vlr_mediana")

        if not cod or ano is None or taxa is None:
            continue

        if cod not in mapa:
            mapa[cod] = {}
        mapa[cod][int(ano)] = float(taxa)

    return mapa
