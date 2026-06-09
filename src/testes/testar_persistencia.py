"""Testes do armazenamento.py. Rodar a partir de src/: python testes/testar_persistencia.py"""

import sys
import os
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from _runner import teste, resumo
import dados.armazenamento as repo
from dados.armazenamento import (
    salvar_carteira, carregar_carteira,
    salvar_cache_taxas, carregar_cache_taxas,
    data_cache_taxas,
)

def main():
    print("=" * 60)
    print("TESTE - armazenamento.py")
    print("=" * 60)

    # pasta temporária pra não mexer nos dados reais
    with tempfile.TemporaryDirectory() as tmpdir:
        repo.CARTEIRA_PATH = os.path.join(tmpdir, "carteira.json")
        repo.CACHE_TAXAS_PATH = os.path.join(tmpdir, "cache_taxas.json")

        print("\n--- Carteira ---\n")

        teste("Carteira vazia retorna lista vazia",
              carregar_carteira() == [])

        carteira_exemplo = [
            {"cod_investimento": "SELIC",    "valor": 10000.0},
            {"cod_investimento": "CDI",      "valor": 5000.0},
            {"cod_investimento": "POUPANCA", "valor": 3000.0},
        ]
        salvar_carteira(carteira_exemplo)
        teste("Arquivo criado", os.path.exists(repo.CARTEIRA_PATH))

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

        with open(repo.CARTEIRA_PATH, "w") as f:
            f.write("{json invalido!!!")
        teste("Arquivo corrompido retorna lista vazia", carregar_carteira() == [])

        os.remove(repo.CARTEIRA_PATH)
        teste("Após remover arquivo, vazia", carregar_carteira() == [])

        print("\n--- Cache de taxas ---\n")

        teste("Cache não existe", not os.path.exists(repo.CACHE_TAXAS_PATH))
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
        teste("Cache criado", os.path.exists(repo.CACHE_TAXAS_PATH))
        teste("Data não é None", data_cache_taxas() is not None)

        cache = carregar_cache_taxas()
        teste("5 registros carregados", len(cache) == 5)
        teste("Primeiro é SELIC 14.75%",
              cache[0]["cod_investimento"] == "SELIC" and cache[0]["vlr_mediana"] == 14.75)

    return resumo()


if __name__ == "__main__":
    sys.exit(main())
