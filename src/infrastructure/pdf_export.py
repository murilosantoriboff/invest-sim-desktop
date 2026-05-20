"""
pdf_export.py — Exporta a simulação atual para um PDF simples (texto + tabela).
"""

from datetime import datetime

from fpdf import FPDF

from core.calculator import calcular_totais
from core.constants import formatar_brl


def exportar_pdf(dados_grafico, anos, data_atualizacao, caminho):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_margins(15, 15, 15)

    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "Simulador de Investimentos", ln=True)
    pdf.set_font("Helvetica", "", 9)
    pdf.cell(0, 5, f"Gerado em {datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True)
    pdf.cell(0, 5, f"Período: {anos} anos", ln=True)
    pdf.ln(4)

    if not dados_grafico:
        pdf.set_font("Helvetica", "I", 10)
        pdf.cell(0, 8, "Nenhum investimento na carteira.", ln=True)
        pdf.output(caminho)
        return

    larg = [55, 30, 32, 38, 25]
    headers = ["Investimento", "Investido", "Projeção", "Ganho", "Taxa a.a."]
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_fill_color(230, 230, 230)
    for i, h in enumerate(headers):
        pdf.cell(larg[i], 7, h, border=1, align="C", fill=True)
    pdf.ln()

    pdf.set_font("Helvetica", "", 9)
    for d in dados_grafico:
        sinal = "+" if d["ganho"] >= 0 else "-"
        pdf.cell(larg[0], 7, d["nome_exibicao"], border=1)
        pdf.cell(larg[1], 7, formatar_brl(d["valor"]), border=1, align="R")
        pdf.cell(larg[2], 7, formatar_brl(d["valor_futuro"]), border=1, align="R")
        pdf.cell(larg[3], 7, f"{sinal} {formatar_brl(abs(d['ganho']))}", border=1, align="R")
        pdf.cell(larg[4], 7, f"{d['taxa_exibicao']:.2f}%", border=1, align="R")
        pdf.ln()

    totais = calcular_totais(dados_grafico)
    pdf.ln(4)
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 6, f"Total investido: {formatar_brl(totais['total_investido'])}", ln=True)
    pdf.cell(0, 6, f"Projeção em {anos} anos: {formatar_brl(totais['total_futuro'])}", ln=True)
    sinal_total = "+" if totais["total_ganho"] >= 0 else "-"
    pdf.cell(0, 6, f"Ganho total: {sinal_total} {formatar_brl(abs(totais['total_ganho']))}", ln=True)

    if data_atualizacao:
        pdf.ln(8)
        pdf.set_font("Helvetica", "I", 8)
        pdf.set_text_color(110, 110, 110)
        pdf.cell(0, 5, f"Taxas atualizadas em {data_atualizacao}", ln=True)

    pdf.output(caminho)
