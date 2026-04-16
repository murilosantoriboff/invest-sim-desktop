#json_repository.py — Persistencia local em arquivos JSON.

import json
import os
from datetime import datetime

_DIR = os.path.dirname(os.path.abspath(__file__))
_DATA_DIR = os.path.join(_DIR, "..", "..", "..", "data")

CARTEIRA_PATH = os.path.join(_DATA_DIR, "carteira.json")
CACHE_TAXAS_PATH = os.path.join(_DATA_DIR, "cache_taxas.json")


def _garantir_diretorio():
    """Cria o diretório data/ se não existir."""
    os.makedirs(os.path.dirname(CARTEIRA_PATH), exist_ok=True)


def salvar_carteira(itens: list[dict]) -> None:

    _garantir_diretorio()
    dados = {
        "atualizado_em": datetime.now().isoformat(),
        "itens": itens,
    }
    with open(CARTEIRA_PATH, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)


def carregar_carteira() -> list[dict]:

    if not os.path.exists(CARTEIRA_PATH):
        return []
    try:
        with open(CARTEIRA_PATH, "r", encoding="utf-8") as f:
            dados = json.load(f)
        itens = dados.get("itens", [])

        validados = []
        for item in itens:
            if "cod_investimento" in item and "valor" in item:
                validados.append({
                    "cod_investimento": str(item["cod_investimento"]),
                    "valor": float(item["valor"]),
                })
        return validados
    except (json.JSONDecodeError, KeyError, TypeError, ValueError):
        return []


def limpar_carteira() -> None:
    
    if os.path.exists(CARTEIRA_PATH):
        os.remove(CARTEIRA_PATH)


def salvar_cache_taxas(indicadores: list[dict]) -> None:

    _garantir_diretorio()
    dados = {
        "atualizado_em": datetime.now().isoformat(),
        "indicadores": indicadores,
    }
    with open(CACHE_TAXAS_PATH, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)


def carregar_cache_taxas() -> list[dict]:

    if not os.path.exists(CACHE_TAXAS_PATH):
        return []
    try:
        with open(CACHE_TAXAS_PATH, "r", encoding="utf-8") as f:
            dados = json.load(f)
        return dados.get("indicadores", [])
    except (json.JSONDecodeError, KeyError, TypeError):
        return []


def cache_taxas_existe() -> bool:
    return os.path.exists(CACHE_TAXAS_PATH)


def data_cache_taxas() -> str | None:
    if not os.path.exists(CACHE_TAXAS_PATH):
        return None
    try:
        with open(CACHE_TAXAS_PATH, "r", encoding="utf-8") as f:
            dados = json.load(f)
        return dados.get("atualizado_em")
    except (json.JSONDecodeError, KeyError, TypeError):
        return None
