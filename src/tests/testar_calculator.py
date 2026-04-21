"""
testar_calculator.py — Testa o calculator.py.

Rodar a partir da raiz: python src/tests/testar_calculator.py
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from core.calculator import (
    projetar_valor,
    calcular_ganho,
    calcular_percentual_ganho,
    preparar_dados_grafico,
    calcular_totais,
    calcular_raio_ganho,
    _organizar_taxas,
)
from core.constants import R_PRINC, R_HOLE

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


def main():
    global passed, failed

    print("=" * 60)
    print("TESTE — calculator.py")
    print("=" * 60)

    # ── Projeção ──────────────────────────────────────────────────────────────
    print("\n--- Projeção de valor ---\n")

    # taxa fixa repetida por ano (como vem do Supabase)
    taxas_selic = {2026: 14.75, 2027: 14.75, 2028: 14.75, 2029: 14.75, 2030: 14.75}
    resultado = projetar_valor(10000, taxas_selic, 2026, 5)
    teste("R$ 10.000 a 14.75% fixo por 5 anos ≈ R$ 19.895",
          aprox(resultado, 19895.89, 1.0))

    teste("Taxa 0% não altera o valor",
          projetar_valor(1000, {2026: 0}, 2026, 1) == 1000.0)

    teste("R$ 5.000 a 10% por 1 ano = R$ 5.500",
          aprox(projetar_valor(5000, {2026: 10}, 2026, 1), 5500.0))

    teste("Sem taxas retorna valor original",
          projetar_valor(10000, {}, 2026, 5) == 10000.0)

    # taxas variáveis de verdade
    taxas_var = {2026: 14.75, 2027: 12.50, 2028: 10.00}

    resultado_1 = projetar_valor(10000, taxas_var, 2026, 1)
    teste("1 ano (14.75%) ≈ R$ 11.475",
          aprox(resultado_1, 11475.0))

    resultado_2 = projetar_valor(10000, taxas_var, 2026, 2)
    teste("2 anos (14.75% + 12.50%) ≈ R$ 12.909",
          aprox(resultado_2, 12909.37, 1.0))

    resultado_3 = projetar_valor(10000, taxas_var, 2026, 3)
    teste("3 anos (14.75% + 12.50% + 10.00%) ≈ R$ 14.200",
          aprox(resultado_3, 14200.31, 1.0))

    # anos além dos disponíveis usam a última taxa (10%)
    resultado_5 = projetar_valor(10000, taxas_var, 2026, 5)
    teste("5 anos (3 taxas + 2 flat a 10%) ≈ R$ 17.182",
          aprox(resultado_5, 17182.38, 2.0))

    # ── Auxiliares ────────────────────────────────────────────────────────────
    print("\n--- Auxiliares ---\n")

    teste("Ganho = futuro - investido",
          calcular_ganho(10000, 15000) == 5000.0)

    teste("Percentual 50%",
          aprox(calcular_percentual_ganho(10000, 5000), 50.0))

    teste("Valor zero retorna 0%",
          calcular_percentual_ganho(0, 5000) == 0.0)

    # ── Geometria ─────────────────────────────────────────────────────────────
    print("\n--- Raio do anel de ganho ---\n")

    espessura = R_PRINC - R_HOLE

    teste("Ganho 100% → raio = R_PRINC + espessura",
          aprox(calcular_raio_ganho(10000, 10000), R_PRINC + espessura))

    teste("Ganho 0 → raio = R_PRINC",
          calcular_raio_ganho(0, 10000) == R_PRINC)

    teste("Ganho 50% → raio proporcional",
          aprox(calcular_raio_ganho(5000, 10000), R_PRINC + espessura * 0.5))

    # ── Organizar taxas ──────────────────────────────────────────────────────
    print("\n--- Organizar taxas ---\n")

    taxas_flat = [
        {"cod_investimento": "SELIC", "ano_referencia": 2025, "vlr_mediana": 14.75},
        {"cod_investimento": "SELIC", "ano_referencia": 2026, "vlr_mediana": 12.50},
        {"cod_investimento": "CDI",   "ano_referencia": 2025, "vlr_mediana": 14.65},
    ]
    mapa = _organizar_taxas(taxas_flat)
    teste("SELIC tem 2 anos", len(mapa["SELIC"]) == 2)
    teste("CDI tem 1 ano", len(mapa["CDI"]) == 1)
    teste("SELIC 2025 = 14.75", mapa["SELIC"][2025] == 14.75)

    mapa_vazio = _organizar_taxas([{"cod_investimento": "", "ano_referencia": None}])
    teste("Dados inválidos são ignorados", len(mapa_vazio) == 0)

    # ── Dados para o gráfico ─────────────────────────────────────────────────
    print("\n--- Preparar dados para o gráfico ---\n")

    carteira = [
        {"cod_investimento": "SELIC",    "valor": 10000.0},
        {"cod_investimento": "POUPANCA", "valor": 5000.0},
    ]
    taxas_supabase = [
        {"cod_investimento": "SELIC",    "ano_referencia": 2026, "vlr_mediana": 14.75},
        {"cod_investimento": "SELIC",    "ano_referencia": 2027, "vlr_mediana": 12.50},
        {"cod_investimento": "POUPANCA", "ano_referencia": 2026, "vlr_mediana": 6.17},
        {"cod_investimento": "POUPANCA", "ano_referencia": 2027, "vlr_mediana": 6.17},
    ]

    dados = preparar_dados_grafico(carteira, taxas_supabase, anos=2, ano_inicio=2026)
    teste("2 investimentos preparados", len(dados) == 2)
    teste("Primeiro é SELIC", dados[0]["cod_investimento"] == "SELIC")
    teste("Cor hex correta", dados[0]["cor_hex"] == "#3B6FE0")
    teste("SELIC rendeu", dados[0]["valor_futuro"] > dados[0]["valor"])
    teste("Poupança rendeu", dados[1]["valor_futuro"] > dados[1]["valor"])

    dados_inv = preparar_dados_grafico(
        [{"cod_investimento": "BITCOIN", "valor": 1000.0}], taxas_supabase, anos=1)
    teste("Investimento desconhecido é ignorado", len(dados_inv) == 0)

    dados_sem = preparar_dados_grafico(
        [{"cod_investimento": "SELIC", "valor": 10000.0}], [], anos=5)
    teste("Sem taxas → valor futuro = valor", dados_sem[0]["valor_futuro"] == 10000.0)

    # ── Totais ────────────────────────────────────────────────────────────────
    print("\n--- Totais ---\n")

    totais = calcular_totais(dados)
    teste("Total investido = R$ 15.000", aprox(totais["total_investido"], 15000.0))
    teste("Total futuro > investido", totais["total_futuro"] > totais["total_investido"])
    teste("Ganho > 0", totais["total_ganho"] > 0)

    # ── Resumo ────────────────────────────────────────────────────────────────
    print("\n" + "=" * 60)
    print(f"RESULTADO: {passed} passaram, {failed} falharam")
    print("=" * 60)

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
