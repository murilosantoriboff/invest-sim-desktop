"""Constantes e configurações globais do simulador."""

# Cores
BG       = "#F7F5F2"
PANEL    = "#FFFFFF"
BORDER   = "#E8E5DE"
HOVER    = "#D4D4D4"
TXT      = "#18181B"
TXT_SEC  = "#71717A"
GREEN    = "#16A34A"
RED      = "#DC2626"
BLUE     = "#3B6FE0"
BLUE_D   = "#2952B8"
CARD_BG    = "#F0EEEB"
ERRO_BG    = "#FEE2E2"
TOOLTIP_BG = "#FFFFE0"

# códigos iguais aos da vw_indicadores_investimento
INVESTIMENTOS = {
    "SELIC": {
        "nome_exibicao": "Tesouro Selic",
        "cor": "#3B6FE0",
        "descricao": "Título público federal que acompanha a taxa Selic, a taxa básica de juros. Considerado o investimento mais seguro do Brasil, com liquidez diária.",
    },
    "CDI": {
        "nome_exibicao": "CDB 100% CDI",
        "cor": "#DC4437",
        "descricao": "Certificado de Depósito Bancário que rende um percentual do CDI (taxa entre bancos, próxima à Selic). Tem garantia do FGC até R$ 250 mil por instituição.",
    },
    "IPCA": {
        "nome_exibicao": "Tesouro IPCA+",
        "cor": "#16A34A",
        "descricao": "Título público que paga IPCA (inflação oficial) + uma taxa fixa. Protege o poder de compra ao longo do tempo, ideal para prazos mais longos.",
    },
    "POUPANCA": {
        "nome_exibicao": "Poupança",
        "cor": "#9333EA",
        "descricao": "Investimento tradicional dos bancos, isento de Imposto de Renda. Rende 70% da Selic + TR quando a Selic está acima de 8,5% a.a.",
    },
    "IGPM": {
        "nome_exibicao": "IGP-M",
        "cor": "#EAB308",
        "descricao": "Índice Geral de Preços do Mercado, usado em contratos e aluguéis. Reflete a inflação no atacado e tende a ser mais volátil que o IPCA.",
    },
    "CAMBIO": {
        "nome_exibicao": "Dólar",
        "cor": "#14B8A6",
        "descricao": "Variação da cotação do dólar americano frente ao real. Funciona como proteção contra desvalorização da moeda local.",
    },
}

# Prazo
PRAZO_MIN = 1
PRAZO_MAX = 30
PRAZO_DEFAULT = 5


def formatar_brl(valor):
    return f"R$ {valor:,.0f}".replace(",", ".")
