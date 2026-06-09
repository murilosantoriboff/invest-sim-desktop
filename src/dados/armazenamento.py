"""Persistência local em arquivos JSON (carteira do usuário e cache de taxas)."""

import json
import os
from datetime import datetime

_DIR = os.path.dirname(os.path.abspath(__file__))
_DATA_DIR = os.path.join(_DIR, "..", "..", "data")

CARTEIRA_PATH = os.path.join(_DATA_DIR, "carteira.json")
CACHE_TAXAS_PATH = os.path.join(_DATA_DIR, "cache_taxas.json")


def _garantir_diretorio():
    os.makedirs(os.path.dirname(CARTEIRA_PATH), exist_ok=True)


def _ler_json(path):
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, ValueError):
        return None


# Carteira

def salvar_carteira(itens):
    _garantir_diretorio()
    dados = {
        "atualizado_em": datetime.now().isoformat(),
        "itens": itens,
    }
    with open(CARTEIRA_PATH, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)


def carregar_carteira():
    dados = _ler_json(CARTEIRA_PATH)
    if not dados:
        return []
    return dados.get("itens", [])


# Cache de taxas

def salvar_cache_taxas(indicadores):
    _garantir_diretorio()
    dados = {
        "atualizado_em": datetime.now().isoformat(),
        "indicadores": indicadores,
    }
    with open(CACHE_TAXAS_PATH, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)


def carregar_cache_taxas():
    dados = _ler_json(CACHE_TAXAS_PATH)
    if not dados:
        return []
    return dados.get("indicadores", [])


def data_cache_taxas():
    dados = _ler_json(CACHE_TAXAS_PATH)
    if not dados:
        return None
    return dados.get("atualizado_em")
