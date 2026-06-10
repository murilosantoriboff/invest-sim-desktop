"""
testar_desempenho.py - testes não funcionais de desempenho.

Mede o tempo das operações principais e confere se ficam dentro de
limites aceitáveis. Os tempos medidos são impressos para registro.

Rodar a partir de src/: python testes/testar_desempenho.py
(abre e fecha uma janela rapidamente para medir a inicialização)
"""

import os
import sys
import tempfile
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from _runner import teste, resumo
from core.calculator import preparar_dados_grafico, calcular_totais
from dados.pdf_export import exportar_pdf

CODIGOS = ["SELIC", "CDI", "IPCA", "POUPANCA", "IGPM", "CAMBIO"]


def montar_taxas():
    # taxas simuladas no formato da view (6 investimentos x 5 anos)
    taxas = []
    for cod, base in [("SELIC", 12.0), ("CDI", 11.9), ("IPCA", 5.5),
                      ("POUPANCA", 7.3), ("IGPM", 5.0), ("CAMBIO", 5.2)]:
        for ano in range(2026, 2031):
            taxas.append({"cod_investimento": cod, "ano_referencia": ano, "vlr_mediana": base})
    return taxas


def main():
    print("=" * 60)
    print("TESTE DE DESEMPENHO")
    print("=" * 60)

    taxas = montar_taxas()

    print("\n--- Cálculo ---\n")

    # carteira típica: 6 investimentos projetados a 30 anos, 1000 vezes
    carteira = [{"cod_investimento": c, "valor": 10000.0} for c in CODIGOS]
    inicio = time.perf_counter()
    for _ in range(1000):
        dados = preparar_dados_grafico(carteira, taxas, anos=30, ano_inicio=2026)
        calcular_totais(dados)
    media_ms = (time.perf_counter() - inicio)  # 1000x em segundos = média em ms
    print(f"  simulação completa (6 itens, 30 anos): {media_ms:.3f} ms em média")
    teste("Recálculo médio abaixo de 10 ms", media_ms < 10)

    # carteira exagerada, muito acima do uso normal
    carteira_grande = [{"cod_investimento": CODIGOS[i % 6], "valor": 1000.0}
                       for i in range(600)]
    inicio = time.perf_counter()
    preparar_dados_grafico(carteira_grande, taxas, anos=30, ano_inicio=2026)
    grande_ms = (time.perf_counter() - inicio) * 1000
    print(f"  carteira com 600 itens, 30 anos: {grande_ms:.2f} ms")
    teste("600 itens calculados em menos de 500 ms", grande_ms < 500)

    print("\n--- Exportação de PDF ---\n")

    dados = preparar_dados_grafico(carteira, taxas, anos=30, ano_inicio=2026)
    with tempfile.TemporaryDirectory() as tmp:
        caminho = os.path.join(tmp, "teste.pdf")
        inicio = time.perf_counter()
        exportar_pdf(dados, 30, "09/06/2026 10:00", caminho)
        pdf_ms = (time.perf_counter() - inicio) * 1000
        tamanho = os.path.getsize(caminho)
        print(f"  PDF com 6 investimentos: {pdf_ms:.1f} ms, {tamanho} bytes")
        teste("PDF gerado em menos de 2 s", pdf_ms < 2000)
        teste("PDF não ficou vazio", tamanho > 500)

    print("\n--- Abertura do app ---\n")

    inicio = time.perf_counter()
    import main as app_main
    app = app_main.App()
    app.update_idletasks()
    app.update()
    abertura_s = time.perf_counter() - inicio
    app.destroy()
    print(f"  abertura até a primeira tela: {abertura_s:.2f} s")
    teste("App abre em menos de 10 s", abertura_s < 10)

    return resumo()


if __name__ == "__main__":
    sys.exit(main())
