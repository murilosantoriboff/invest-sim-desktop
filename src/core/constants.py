"""
constants.py — Constantes e configurações globais do simulador.
"""

# Cores
BG       = "#F7F5F2"
PANEL    = "#FFFFFF"
BORDER   = "#E8E5DE"
TXT      = "#18181B"
TXT_SEC  = "#71717A"
GREEN    = "#16A34A"
BLUE     = "#3B6FE0"
BLUE_D   = "#2952B8"

# Investimentos disponíveis (códigos alinhados com a vw_indicadores_investimento)
INVESTIMENTOS = {
    "SELIC": {
        "nome_exibicao": "Tesouro Selic",
        "cor": "#3B6FE0",
    },
    "CDI": {
        "nome_exibicao": "CDB 100% CDI",
        "cor": "#DC4437",
    },
    "IPCA": {
        "nome_exibicao": "Tesouro IPCA+",
        "cor": "#16A34A",
    },
    "POUPANCA": {
        "nome_exibicao": "Poupança",
        "cor": "#9333EA",
    },
    "IGPM": {
        "nome_exibicao": "IGP-M",
        "cor": "#EAB308",
    },
    "CAMBIO": {
        "nome_exibicao": "Dólar",
        "cor": "#14B8A6",
    },
}

# Gráfico
CV_W  = 400
CV_H  = 400
CX    = CV_W // 2
CY    = CV_H // 2
R_EXT = 150
R_INT = 85

# Legenda grid
CARD_W    = 200
CARD_COLS = 4

# Prazo
PRAZO_MIN = 1
PRAZO_MAX = 30
PRAZO_DEFAULT = 5


def formatar_brl(valor):
    """Formata valor numérico pro padrão brasileiro (ponto como separador de milhar)."""
    return f"R$ {valor:,.0f}".replace(",", ".")
