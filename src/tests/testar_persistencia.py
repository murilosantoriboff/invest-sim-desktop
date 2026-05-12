"""
testar_persistencia.py — Testa o json_repository.py.

Rodar a partir de src/: python tests/testar_persistencia.py
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from infrastructure.storage.json_repository import (
    salvar_carteira, carregar_carteira, limpar_carteira,
    salvar_cache_taxas, carregar_cache_taxas,
    cache_taxas_existe, data_cache_taxas,
    CARTEIRA_PATH, CACHE_TAXAS_PATH,
)

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


def main():
    global passed, failed

    print("=" * 60)
    print("TESTE — json_repository.py")
    print("=" * 60)

    print("\n--- Carteira ---\n")

    limpar_carteira()
    teste("Carteira vazia retorna lista vazia",
          carregar_carteira() == [])

    carteira_exemplo = [
        {"cod_investimento": "SELIC",    "valor": 10000.0},
        {"cod_investimento": "CDI",      "valor": 5000.0},
        {"cod_investimento": "POUPANCA", "valor": 3000.0},
    ]
    salvar_carteira(carteira_exemplo)
    teste("Arquivo criado", os.path.exists(CARTEIRA_PATH))

    carregada = carregar_carteira()
    teste("3 itens carregados", len(carregada) == 3)
    teste("Primeiro é SELIC R$ 10.000",
          carregada[0]["cod_investimento"] == "SELIC" and carregada[0]["valor"] == 10000.0)

    carteira_exemplo.append({"cod_investimento": "IPCA", "valor": 7000.0})
    salvar_carteira(carteira_exemplo)
    teste("Atualizada com 4 itens", len(carregar_carteira()) == 4)

    carteira_exemplo.pop(1)
    salvar_carteira(carteira_exemplo)
    carregada = carregar_carteira()
    teste("Após remover CDI, 3 itens", len(carregada) == 3)
    teste("CDI removido", all(it["cod_investimento"] != "CDI" for it in carregada))

    with open(CARTEIRA_PATH, "w") as f:
        f.write("{json invalido!!!")
    teste("Arquivo corrompido retorna lista vazia", carregar_carteira() == [])

    limpar_carteira()
    teste("Após limpar, vazia", carregar_carteira() == [])

    print("\n--- Cache de taxas ---\n")

    if os.path.exists(CACHE_TAXAS_PATH):
        os.remove(CACHE_TAXAS_PATH)

    teste("Cache não existe", not cache_taxas_existe())
    teste("Data é None", data_cache_taxas() is None)
    teste("Carregar retorna lista vazia", carregar_cache_taxas() == [])

    taxas_exemplo = [
        {"cod_investimento": "SELIC", "ano_referencia": 2025, "vlr_mediana": 14.75},
        {"cod_investimento": "SELIC", "ano_referencia": 2026, "vlr_mediana": 12.50},
        {"cod_investimento": "CDI",   "ano_referencia": 2025, "vlr_mediana": 14.65},
        {"cod_investimento": "POUPANCA", "ano_referencia": 2025, "vlr_mediana": 6.17},
        {"cod_investimento": "IPCA",  "ano_referencia": 2025, "vlr_mediana": 5.50},
    ]

    salvar_cache_taxas(taxas_exemplo)
    teste("Cache criado", cache_taxas_existe())
    teste("Data não é None", data_cache_taxas() is not None)

    cache = carregar_cache_taxas()
    teste("5 registros carregados", len(cache) == 5)
    teste("Primeiro é SELIC 14.75%",
          cache[0]["cod_investimento"] == "SELIC" and cache[0]["vlr_mediana"] == 14.75)

    # limpeza
    limpar_carteira()
    if os.path.exists(CACHE_TAXAS_PATH):
        os.remove(CACHE_TAXAS_PATH)
    data_dir = os.path.dirname(CARTEIRA_PATH)
    if os.path.exists(data_dir) and not os.listdir(data_dir):
        os.rmdir(data_dir)

    print("\n" + "=" * 60)
    print(f"RESULTADO: {passed} passaram, {failed} falharam")
    print("=" * 60)

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
