"""Simulador de Investimentos. Rodar de dentro da pasta src/: python main.py"""

import sys
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import traceback
from datetime import datetime

from core.constants import BG, PANEL, ERRO_BG, INVESTIMENTOS, PRAZO_MIN, PRAZO_MAX, PRAZO_DEFAULT
from core.calculator import preparar_dados_grafico
from dados.armazenamento import (
    salvar_carteira, carregar_carteira,
    salvar_cache_taxas, carregar_cache_taxas, data_cache_taxas,
)
from dados.pdf_export import exportar_pdf
from ui.interface import (
    configurar_estilos, criar_header, criar_input_panel,
    criar_area_grafico, desenhar_grafico, atualizar_legenda,
    criar_chips_bar, atualizar_chips,
)


def _converter_valor(texto):
    # aceita o formato brasileiro: ponto de milhar e vírgula decimal ("10.000,50")
    try:
        return float(texto.replace(".", "").replace(",", "."))
    except ValueError:
        return 0


class App(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Simulador de Investimentos")
        self.configure(bg=BG)

        self._taxas = []
        self._carteira = []
        self._dados_grafico = []

        self._tipo_var = tk.StringVar(value=list(INVESTIMENTOS.keys())[0])
        self._anos_var = tk.IntVar(value=PRAZO_DEFAULT)

        self._carregar_taxas()
        self._carteira = carregar_carteira()

        configurar_estilos()
        self._montar_ui()
        self._recalcular()
        self._redesenhar()

        x = (self.winfo_screenwidth() - 1280) // 2
        y = (self.winfo_screenheight() - 720) // 2
        self.geometry(f"1280x720+{x}+{y}")
        self.minsize(1280, 720)

    def _carregar_taxas(self):
        try:
            from dados.supabase_client import buscar_indicadores
            taxas = buscar_indicadores()
        except Exception:
            taxas = []

        if taxas:
            self._taxas = taxas
            salvar_cache_taxas(taxas)
        else:
            self._taxas = carregar_cache_taxas()

    def _formatar_data_atualizacao(self):
        iso = data_cache_taxas()
        if not iso:
            return None
        try:
            return datetime.fromisoformat(iso).strftime("%d/%m/%Y %H:%M")
        except (ValueError, TypeError):
            return None

    def _montar_ui(self):
        criar_header(
            self, self._formatar_data_atualizacao(),
            on_exportar_pdf=self._exportar_pdf,
        )
        self._valor_entry = criar_input_panel(
            self, self._tipo_var, self._anos_var,
            on_adicionar=self._adicionar,
            on_mudar_anos=self._mudar_anos,
        )
        self._chip_bar = criar_chips_bar(self)
        self._canvas, self._legenda = criar_area_grafico(self)

    def _recalcular(self):
        self._dados_grafico = preparar_dados_grafico(
            self._carteira, self._taxas, self._anos_var.get(),
        )

    def _redesenhar(self):
        desenhar_grafico(self._canvas, self._dados_grafico, self._anos_var.get())
        atualizar_legenda(self._legenda, self._dados_grafico)
        atualizar_chips(self._chip_bar, self._carteira, self._remover, self._editar)

    def _adicionar(self):
        entry = self._valor_entry
        valor = _converter_valor(entry.get())

        if valor <= 0:
            entry.config(bg=ERRO_BG)
            self.after(500, lambda: entry.config(bg=PANEL))
            return

        self._carteira.append({
            "cod_investimento": self._tipo_var.get(),
            "valor": valor,
        })
        salvar_carteira(self._carteira)
        entry.delete(0, "end")
        entry.insert(0, "10000")
        self._recalcular()
        self._redesenhar()

    def _editar(self, idx):
        item = self._carteira[idx]
        atual = f"{item['valor']:.2f}".replace(".", ",")
        resposta = simpledialog.askstring(
            "Editar valor", "Novo valor (R$):",
            initialvalue=atual, parent=self,
        )
        if resposta is None:
            return

        valor = _converter_valor(resposta)
        if valor <= 0:
            return

        item["valor"] = valor
        salvar_carteira(self._carteira)
        self._recalcular()
        self._redesenhar()

    def _remover(self, idx):
        if 0 <= idx < len(self._carteira):
            self._carteira.pop(idx)
            salvar_carteira(self._carteira)
            self._recalcular()
            self._redesenhar()

    def _mudar_anos(self, delta):
        novo = max(PRAZO_MIN, min(PRAZO_MAX, self._anos_var.get() + delta))
        self._anos_var.set(novo)
        self._recalcular()
        self._redesenhar()

    def _exportar_pdf(self):
        nome_padrao = f"simulacao_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
        caminho = filedialog.asksaveasfilename(
            parent=self, title="Salvar simulação como PDF",
            defaultextension=".pdf", initialfile=nome_padrao,
            filetypes=[("PDF", "*.pdf")],
        )
        if not caminho:
            return
        try:
            exportar_pdf(
                self._dados_grafico, self._anos_var.get(),
                self._formatar_data_atualizacao(), caminho,
            )
            messagebox.showinfo("PDF gerado", f"Arquivo salvo em:\n{caminho}", parent=self)
        except Exception as e:
            messagebox.showerror("Erro ao gerar PDF", str(e), parent=self)


if __name__ == "__main__":
    try:
        app = App()
        app.mainloop()
    except Exception:
        err = traceback.format_exc()
        with open("erro_simulador.txt", "w") as f:
            f.write(err)
        print(err, file=sys.stderr)
        input("Pressione ENTER para fechar...")
