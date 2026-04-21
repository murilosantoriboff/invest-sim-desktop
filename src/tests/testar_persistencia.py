"""
testar_persistencia.py — Testa o json_repository.py de forma isolada.

Rode pelo terminal:  python testar_persistencia.py

"""

import sys
import os

# Ajusta o path para importar o modulo corretamente
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from infrastructure.storage.json_repository import (
    salvar_carteira,
    carregar_carteira,
    limpar_carteira,
    salvar_cache_taxas,
    carregar_cache_taxas,
    cache_taxas_existe,
    data_cache_taxas,
    CARTEIRA_PATH,
    CACHE_TAXAS_PATH,
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
    print("TESTE DE PERSISTÊNCIA — json_repository.py")
    print("=" * 60)

    print("\n--- Carteira do Usuário ---\n")

    limpar_carteira()
    teste("Carteira vazia retorna lista vazia",
          carregar_carteira() == [])

    carteira_exemplo = [
        {"cod_investimento": "SELIC",    "valor": 10000.0},
        {"cod_investimento": "CDI",      "valor": 5000.0},
        {"cod_investimento": "POUPANCA", "valor": 3000.0},
    ]
    salvar_carteira(carteira_exemplo)
    teste("Arquivo carteira.json foi criado",
          os.path.exists(CARTEIRA_PATH))

    carregada = carregar_carteira()
    teste("Carteira carregada tem 3 itens",
          len(carregada) == 3)
    teste("Primeiro item é SELIC com R$ 10000",
          carregada[0]["cod_investimento"] == "SELIC" and carregada[0]["valor"] == 10000.0)
    teste("Segundo item é CDI com R$ 5000",
          carregada[1]["cod_investimento"] == "CDI" and carregada[1]["valor"] == 5000.0)

    # Atualizar carteira (adicionar investimento)
    carteira_exemplo.append({"cod_investimento": "IPCA", "valor": 7000.0})
    salvar_carteira(carteira_exemplo)
    carregada = carregar_carteira()
    teste("Carteira atualizada tem 4 itens",
          len(carregada) == 4)

    # Remover investimento
    carteira_exemplo.pop(1)  # remove CDI
    salvar_carteira(carteira_exemplo)
    carregada = carregar_carteira()
    teste("Após remover CDI, carteira tem 3 itens",
          len(carregada) == 3)
    teste("CDI não está mais na carteira",
          all(it["cod_investimento"] != "CDI" for it in carregada))

    with open(CARTEIRA_PATH, "w") as f:
        f.write("{json invalido aqui!!!")
    teste("Arquivo corrompido retorna lista vazia",
          carregar_carteira() == [])

    limpar_carteira()
    teste("Após limpar, carteira está vazia",
          carregar_carteira() == [])

    print("\n--- Cache de Taxas ---\n")

    if os.path.exists(CACHE_TAXAS_PATH):
        os.remove(CACHE_TAXAS_PATH)

    teste("Cache não existe inicialmente",
          not cache_taxas_existe())
    teste("Data do cache é None quando não existe",
          data_cache_taxas() is None)
    teste("Carregar cache inexistente retorna lista vazia",
          carregar_cache_taxas() == [])

    taxas_exemplo = [
        {
            "cod_investimento": "SELIC",
            "des_investimento": "Tesouro Selic",
            "ano_referencia": 2025,
            "vlr_mediana": 14.75,
            "dat_indicador": "2026-04-14",
        },
        {
            "cod_investimento": "SELIC",
            "des_investimento": "Tesouro Selic",
            "ano_referencia": 2026,
            "vlr_mediana": 12.50,
            "dat_indicador": "2026-04-14",
        },
        {
            "cod_investimento": "CDI",
            "des_investimento": "CDB 100% CDI",
            "ano_referencia": 2025,
            "vlr_mediana": 14.65,
            "dat_indicador": "2026-04-14",
        },
        {
            "cod_investimento": "POUPANCA",
            "des_investimento": "Poupança",
            "ano_referencia": 2025,
            "vlr_mediana": 6.17,
            "dat_indicador": "2026-04-14",
        },
        {
            "cod_investimento": "IPCA",
            "des_investimento": "Tesouro IPCA+",
            "ano_referencia": 2025,
            "vlr_mediana": 5.50,
            "dat_indicador": "2026-04-14",
        },
    ]

    salvar_cache_taxas(taxas_exemplo)
    teste("Arquivo cache_taxas.json foi criado",
          cache_taxas_existe())
    teste("Data do cache não é None",
          data_cache_taxas() is not None)

    cache = carregar_cache_taxas()
    teste("Cache carregado tem 5 registros",
          len(cache) == 5)
    teste("Primeiro registro é SELIC 2025 com 14.75%",
          cache[0]["cod_investimento"] == "SELIC" and cache[0]["vlr_mediana"] == 14.75)

    print("\n" + "=" * 60)
    print(f"RESULTADO: {passed} passaram, {failed} falharam")
    print("=" * 60)

    limpar_carteira()
    if os.path.exists(CACHE_TAXAS_PATH):
        os.remove(CACHE_TAXAS_PATH)

    data_dir = os.path.dirname(CARTEIRA_PATH)
    if os.path.exists(data_dir) and not os.listdir(data_dir):
        os.rmdir(data_dir)

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
