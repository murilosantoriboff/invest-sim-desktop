"""
testar_integracao.py — Fluxo completo: persistência + regra de negócio.

Rodar a partir da raiz: python src/tests/testar_integracao.py

Testa dois cenários:
  1. Com dados reais do Supabase (se a lib estiver instalada e online)
  2. Com cache local simulado (sempre funciona)
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from infrastructure.storage.json_repository import (
    salvar_carteira,
    carregar_carteira,
    limpar_carteira,
    salvar_cache_taxas,
    carregar_cache_taxas,
    CARTEIRA_PATH,
    CACHE_TAXAS_PATH,
)
from core.calculator import preparar_dados_grafico, calcular_totais

passed = 0
failed = 0


def teste(nome, condicao):
    global passed, failed
    if condicao:
        print(f"  OK  {nome}")
        passed += 1
    else:
        print(f"  FALHOU  {nome}")
        failed += 1


def aprox(a, b, tol=0.01):
    return abs(a - b) < tol


def fluxo_com_supabase():
    """Tenta o fluxo real: busca do Supabase → salva cache → calcula."""
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
    teste("Cache salvo e carregado com mesma quantidade", len(cache) == len(taxas))

    carteira = [
        {"cod_investimento": "SELIC", "valor": 10000.0},
        {"cod_investimento": "CDI",   "valor": 5000.0},
    ]

    dados = preparar_dados_grafico(carteira, taxas, anos=5)
    teste("Gerou dados pro gráfico", len(dados) > 0)

    for d in dados:
        teste(f"{d['nome_exibicao']}: futuro > investido",
              d["valor_futuro"] > d["valor"])

    totais = calcular_totais(dados)
    teste("Total futuro > total investido",
          totais["total_futuro"] > totais["total_investido"])

    print(f"\n  Resultado real:")
    for d in dados:
        print(f"    {d['nome_exibicao']}: R$ {d['valor']:,.0f} → R$ {d['valor_futuro']:,.2f} (+{d['percentual_ganho']:.1f}%)")
    print(f"    TOTAL: R$ {totais['total_investido']:,.0f} → R$ {totais['total_futuro']:,.2f}\n")


def fluxo_com_cache():
    """Fluxo offline: usa cache local simulado."""
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
    teste("Cache gravado e lido corretamente", len(taxas) == len(taxas_simuladas))

    carteira_original = [
        {"cod_investimento": "SELIC",    "valor": 10000.0},
        {"cod_investimento": "CDI",      "valor": 5000.0},
        {"cod_investimento": "POUPANCA", "valor": 3000.0},
    ]
    salvar_carteira(carteira_original)
    carteira = carregar_carteira()
    teste("Carteira salva e carregada com 3 itens", len(carteira) == 3)

    dados = preparar_dados_grafico(carteira, taxas, anos=5, ano_inicio=2025)
    teste("Gerou dados pra 3 investimentos", len(dados) == 3)

    for d in dados:
        teste(f"{d['nome_exibicao']}: rendeu",
              d["valor_futuro"] > d["valor"])
        teste(f"{d['nome_exibicao']}: tem cor hex",
              d["cor_hex"].startswith("#"))

    totais = calcular_totais(dados)
    teste("Total investido = R$ 18.000",
          aprox(totais["total_investido"], 18000.0))
    teste("Total futuro > investido",
          totais["total_futuro"] > totais["total_investido"])
    teste("Ganho > 0", totais["total_ganho"] > 0)


    carteira.pop(2)
    salvar_carteira(carteira)
    carteira = carregar_carteira()
    teste("Após remover, carteira tem 2 itens", len(carteira) == 2)

    dados2 = preparar_dados_grafico(carteira, taxas, anos=5, ano_inicio=2025)
    teste("Gráfico atualizado com 2 itens", len(dados2) == 2)

    # simula o usuário adicionando mais um
    carteira.append({"cod_investimento": "IPCA", "valor": 7000.0})
    salvar_carteira(carteira)
    carteira = carregar_carteira()

    dados3 = preparar_dados_grafico(carteira, taxas, anos=10, ano_inicio=2025)
    teste("Com IPCA adicionado e prazo 10 anos", len(dados3) == 3)

    totais3 = calcular_totais(dados3)
    teste("Prazo maior = ganho maior",
          totais3["total_ganho"] > totais["total_ganho"])

    print(f"\n  Resultado simulado (5 anos):")
    for d in dados:
        print(f"    {d['nome_exibicao']}: R$ {d['valor']:,.0f} → R$ {d['valor_futuro']:,.2f} (+{d['percentual_ganho']:.1f}%)")
    print(f"    TOTAL: R$ {totais['total_investido']:,.0f} → R$ {totais['total_futuro']:,.2f}")


def limpar():
    limpar_carteira()
    if os.path.exists(CACHE_TAXAS_PATH):
        os.remove(CACHE_TAXAS_PATH)
    data_dir = os.path.dirname(CARTEIRA_PATH)
    if os.path.exists(data_dir) and not os.listdir(data_dir):
        os.rmdir(data_dir)


def main():
    global passed, failed

    print("=" * 60)
    print("TESTE DE INTEGRAÇÃO — persistência + regra de negócio")
    print("=" * 60)

    fluxo_com_supabase()
    fluxo_com_cache()

    limpar()

    print("\n" + "=" * 60)
    print(f"RESULTADO: {passed} passaram, {failed} falharam")
    print("=" * 60)

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
