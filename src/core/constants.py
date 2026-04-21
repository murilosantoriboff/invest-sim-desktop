"""
constants.py — Constantes e configurações globais do simulador.
"""

# Cores do tema
BG       = "#F7F5F2"
PANEL    = "#FFFFFF"
BORDER   = "#E8E5DE"
CARD_SH  = "#EDEDEA"
TXT      = "#18181B"
TXT_SEC  = "#A1A1AA"
TXT_GAIN = "#52525B"
GREEN    = "#16A34A"
BLUE     = "#3B6FE0"
BLUE_D   = "#2952B8"

# Investimentos disponíveis (códigos alinhados com a vw_indicadores_investimento)
INVESTIMENTOS = {
    "SELIC": {
        "nome_exibicao": "Tesouro Selic",
        "cor_rgb":       (59, 111, 224),
        "cor_hex":       "#3B6FE0",
    },
    "CDI": {
        "nome_exibicao": "CDB 100% CDI",
        "cor_rgb":       (220, 68, 55),
        "cor_hex":       "#DC4437",
    },
    "IPCA": {
        "nome_exibicao": "Tesouro IPCA+",
        "cor_rgb":       (22, 163, 74),
        "cor_hex":       "#16A34A",
    },
    "POUPANCA": {
        "nome_exibicao": "Poupança",
        "cor_rgb":       (147, 51, 234),
        "cor_hex":       "#9333EA",
    },
    "IGPM": {
        "nome_exibicao": "IGP-M",
        "cor_rgb":       (234, 179, 8),
        "cor_hex":       "#EAB308",
    },
    "CAMBIO": {
        "nome_exibicao": "Dólar",
        "cor_rgb":       (20, 184, 166),
        "cor_hex":       "#14B8A6",
    },
}

# Canvas e gráfico
WIN_W    = 1060
CV_W     = 1060
CV_H     = 520
CX       = CV_W // 2
CY       = CV_H // 2 + 6

R_HOLE   = 86
R_PRINC  = 152
GAP_DEG  = 2.4

# Animação
ANIM_STEP_BASE = 0.038
ANIM_STEP_ADD  = 0.012
ANIM_FPS_MS    = 16

# Fontes Poppins
FONT_DIR  = "assets/fonts"
F_REG     = f"{FONT_DIR}/Poppins-Regular.ttf"
F_MED     = f"{FONT_DIR}/Poppins-Medium.ttf"
F_BOLD    = f"{FONT_DIR}/Poppins-Bold.ttf"
F_LIGHT   = f"{FONT_DIR}/Poppins-Light.ttf"

# Limites de prazo
PRAZO_MIN = 1
PRAZO_MAX = 30
PRAZO_DEFAULT = 5
