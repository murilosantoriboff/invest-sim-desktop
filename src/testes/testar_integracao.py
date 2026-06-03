"""
testar_integracao.py — Fluxo completo: persistência + regra de negócio.

Rodar a partir de src/: python testes/testar_integracao.py
"""

import sys
import os
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from _runner import teste, aprox, resumo
from infrastructure.storage import json_repository as repo
from infrastructure.storage.json_repository import (
    salvar_carteira, carregar_carteira,
    salvar_cache_taxas, carregar_cache_taxas,
)
from core.calculator import preparar_dados_grafico, calcular_totais

def fluxo_com_supabase():
    print("\n--- Fluxo com Supabase (online) ---\n")
    try:
        from infrastructure.database.supabase_client import buscar_indicadores
    except ImportError:
        print("  PULOU  lib supabase não instalada\n")
        return

    try:
        taxas = buscar_indicadores()
    except Exception as e:
        print(f"  PULOU  erro ao conectar: {e}\n")
        return

    teste("Supabase retornou dados", len(taxas) > 0)
    if not taxas:
        return

    salvar_cache_taxas(taxas)
    cache = carregar_cache_taxas()
    teste("Cache salvo e carregado", len(cache) == len(taxas))

    carteira = [
        {"cod_investimento": "SELIC", "valor": 10000.0},
        {"cod_investimento": "CDI",   "valor": 5000.0},
    ]
    dados = preparar_dados_grafico(carteira, taxas, anos=5)
    teste("Gerou dados pro gráfico", len(dados) > 0)

    for d in dados:
        teste(f"{d['nome_exibicao']}: rendeu", d["valor_futuro"] > d["valor"])

    totais = calcular_totais(dados)
    teste("Total futuro > investido", totais["total_futuro"] > totais["total_investido"])


def fluxo_com_cache():
    print("\n--- Fluxo com cache local (offline) ---\n")

    taxas_simuladas = [
        {"cod_investimento": "SELIC",    "ano_referencia": 2025, "vlr_mediana": 14.75},
        {"cod_investimento": "SELIC",    "ano_referencia": 2026, "vlr_mediana": 12.50},
        {"cod_investimento": "SELIC",    "ano_referencia": 2027, "vlr_mediana": 10.50},
        {"cod_investimento": "CDI",      "ano_referencia": 2025, "vlr_mediana": 14.65},
        {"cod_investimento": "CDI",      "ano_referencia": 2026, "vlr_mediana": 12.40},
        {"cod_investimento": "CDI",      "ano_referencia": 2027, "vlr_mediana": 10.40},
        {"cod_investimento": "IPCA",     "ano_referencia": 2025, "vlr_mediana": 5.50},
        {"cod_investimento": "IPCA",     "ano_referencia": 2026, "vlr_mediana": 4.50},
        {"cod_investimento": "POUPANCA", "ano_referencia": 2025, "vlr_mediana": 7.35},
        {"cod_investimento": "POUPANCA", "ano_referencia": 2026, "vlr_mediana": 7.35},
    ]

    salvar_cache_taxas(taxas_simuladas)
    taxas = carregar_cache_taxas()
    teste("Cache gravado e lido", len(taxas) == len(taxas_simuladas))

    carteira_original = [
        {"cod_investimento": "SELIC",    "valor": 10000.0},
        {"cod_investimento": "CDI",      "valor": 5000.0},
        {"cod_investimento": "POUPANCA", "valor": 3000.0},
    ]
    salvar_carteira(carteira_original)
    carteira = carregar_carteira()
    teste("Carteira com 3 itens", len(carteira) == 3)

    dados = preparar_dados_grafico(carteira, taxas, anos=5, ano_inicio=2025)
    teste("3 investimentos no gráfico", len(dados) == 3)

    for d in dados:
        teste(f"{d['nome_exibicao']}: rendeu", d["valor_futuro"] > d["valor"])

    totais = calcular_totais(dados)
    teste("Total investido = R$ 18.000", aprox(totais["total_investido"], 18000.0))
    teste("Total futuro > investido", totais["total_futuro"] > totais["total_investido"])

    carteira.pop(2)
    salvar_carteira(carteira)
    teste("Após remover, 2 itens", len(carregar_carteira()) == 2)

    dados2 = preparar_dados_grafico(carregar_carteira(), taxas, anos=5, ano_inicio=2025)
    teste("Gráfico com 2 itens", len(dados2) == 2)

    carteira = carregar_carteira()
    carteira.append({"cod_investimento": "IPCA", "valor": 7000.0})
    salvar_carteira(carteira)
    dados3 = preparar_dados_grafico(carregar_carteira(), taxas, anos=10, ano_inicio=2025)
    teste("Com IPCA e prazo 10 anos", len(dados3) == 3)

    totais3 = calcular_totais(dados3)
    teste("Prazo maior = ganho maior", totais3["total_ganho"] > totais["total_ganho"])


def main():
    print("=" * 60)
    print("TESTE DE INTEGRAÇÃO — persistência + regra de negócio")
    print("=" * 60)

    # Usa um diretório temporário pra não tocar nos dados reais do app
    with tempfile.TemporaryDirectory() as tmpdir:
        repo.CARTEIRA_PATH = os.path.join(tmpdir, "carteira.json")
        repo.CACHE_TAXAS_PATH = os.path.join(tmpdir, "cache_taxas.json")

        fluxo_com_supabase()
        fluxo_com_cache()

    return resumo()


if __name__ == "__main__":
    sys.exit(main())
