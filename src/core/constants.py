"""
constants.py — Constantes e configurações globais
"""

# Cores
BG       = "#F7F5F2"
PANEL    = "#FFFFFF"
BORDER   = "#E8E5DE"
TXT      = "#18181B"
TXT_SEC  = "#A1A1AA"
GREEN    = "#16A34A"
BLUE     = "#3B6FE0"
BLUE_D   = "#2952B8"

# Investimentos disponíveis
INVESTIMENTOS = {
    "SELIC": {
        "nome_exibicao": "Tesouro Selic",
        "cor_rgb": "#3B6FE0",
    },
    "CDI": {
        "nome_exibicao": "CDB 100% CDI",
        "cor_rgb": "#DC4437",
    },
    "IPCA": {
        "nome_exibicao": "Tesouro IPCA+",
        "cor_rgb": "#16A34A",
    },
    "POUPANCA": {
        "nome_exibicao": "Poupança",
        "cor_rgb": "#9333EA",
    },
    "IGPM": {
        "nome_exibicao": "IGP-M",
        "cor_rgb": "#EAB308",
    },
    "CAMBIO": {
        "nome_exibicao": "Dólar",
        "cor_rgb": "#14B8A6",
    },
}

# Gráfico
CV_W     = 500
CV_H     = 500
CX       = CV_W // 2
CY       = CV_H // 2
R_EXT    = 180
R_INT    = 100

R_HOLE   = 86
R_PRINC  = 152

# Prazo
PRAZO_MIN = 1
PRAZO_MAX = 30
PRAZO_DEFAULT = 5
