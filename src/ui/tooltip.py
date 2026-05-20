"""
tooltip.py — Tooltip em hover e janela de glossário dos investimentos.
"""

import tkinter as tk
from tkinter import ttk

from core.constants import INVESTIMENTOS, BG, PANEL, BORDER, TXT, TXT_SEC


_DELAY_MS = 500
_WRAPLENGTH = 280


class Tooltip:
    def __init__(self, widget, texto):
        self._widget = widget
        self._texto = texto
        self._top = None
        self._after_id = None
        widget.bind("<Enter>", self._on_enter, add="+")
        widget.bind("<Leave>", self._on_leave, add="+")
        widget.bind("<ButtonPress>", self._on_press, add="+")

    def _on_enter(self, _event=None):
        self._cancelar()
        self._after_id = self._widget.after(_DELAY_MS, self._mostrar)

    def _on_leave(self, _event=None):
        # Confere depois de um tick se o ponteiro saiu mesmo do widget e descendentes.
        # Isso evita esconder ao passar para um filho (Label dentro de Frame).
        self._widget.after(30, self._verificar_saida)

    def _on_press(self, _event=None):
        self._cancelar()
        self._esconder()

    def _verificar_saida(self):
        try:
            x, y = self._widget.winfo_pointerxy()
            alvo = self._widget.winfo_containing(x, y)
        except Exception:
            alvo = None
        if not self._eh_descendente(alvo):
            self._cancelar()
            self._esconder()

    def _eh_descendente(self, alvo):
        if alvo is None:
            return False
        atual = alvo
        while atual is not None:
            if atual is self._widget:
                return True
            atual = getattr(atual, "master", None)
        return False

    def _cancelar(self):
        if self._after_id is not None:
            try:
                self._widget.after_cancel(self._after_id)
            except Exception:
                pass
            self._after_id = None

    def _mostrar(self):
        if self._top is not None or not self._texto:
            return

        x = self._widget.winfo_rootx() + 12
        y = self._widget.winfo_rooty() + self._widget.winfo_height() + 6

        top = tk.Toplevel(self._widget)
        top.wm_overrideredirect(True)
        top.attributes("-topmost", True)

        frame = tk.Frame(top, bg=TXT, bd=0)
        frame.pack()
        label = tk.Label(
            frame, text=self._texto, justify="left",
            bg="#FFFFE0", fg=TXT, font=("Arial", 9),
            wraplength=_WRAPLENGTH, padx=8, pady=6,
            bd=1, relief="solid",
        )
        label.pack()

        # Posiciona usando coordenadas absolutas do widget (rootx/rooty já
        # consideram o desktop virtual, então funciona em múltiplos monitores).
        # Evitamos clampar com winfo_screenwidth/height porque no Windows essas
        # funções retornam apenas o monitor primário, jogando o tooltip pra tela
        # errada quando o app está num monitor secundário.
        top.wm_geometry(f"+{x}+{y}")

        self._top = top

    def _esconder(self):
        if self._top is not None:
            try:
                self._top.destroy()
            except Exception:
                pass
            self._top = None


def abrir_glossario(root):
    win = tk.Toplevel(root)
    win.title("Glossário de Investimentos")
    win.configure(bg=BG)
    win.transient(root)
    try:
        win.grab_set()
    except Exception:
        pass

    largura = 520
    altura = 480
    root.update_idletasks()
    # Centraliza relativo ao root (funciona em qualquer monitor — rootx/rooty
    # já estão em coordenadas absolutas do desktop virtual).
    x = root.winfo_rootx() + (root.winfo_width() // 2) - (largura // 2)
    y = root.winfo_rooty() + (root.winfo_height() // 2) - (altura // 2)
    win.geometry(f"{largura}x{altura}+{x}+{y}")
    win.minsize(420, 360)

    tk.Label(
        win, text="Glossário de Investimentos",
        font=("Arial", 14, "bold"), bg=BG, fg=TXT,
    ).pack(anchor="w", padx=20, pady=(18, 4))
    tk.Label(
        win, text="Resumo rápido de cada tipo disponível no simulador.",
        font=("Arial", 9), bg=BG, fg=TXT_SEC,
    ).pack(anchor="w", padx=20, pady=(0, 10))

    tk.Frame(win, bg=BORDER, height=1).pack(fill="x", padx=20)

    # Área com scroll vertical
    scroll_wrap = tk.Frame(win, bg=BG)
    scroll_wrap.pack(fill="both", expand=True, padx=20, pady=10)

    scroll_canvas = tk.Canvas(scroll_wrap, bg=BG, highlightthickness=0)
    scrollbar = ttk.Scrollbar(scroll_wrap, orient="vertical", command=scroll_canvas.yview)
    scroll_canvas.configure(yscrollcommand=scrollbar.set)

    scroll_canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    container = tk.Frame(scroll_canvas, bg=BG)
    janela_id = scroll_canvas.create_window((0, 0), window=container, anchor="nw")

    def _atualizar_scroll(_e=None):
        scroll_canvas.configure(scrollregion=scroll_canvas.bbox("all"))

    def _ajustar_largura(event):
        scroll_canvas.itemconfigure(janela_id, width=event.width)

    container.bind("<Configure>", _atualizar_scroll)
    scroll_canvas.bind("<Configure>", _ajustar_largura)

    def _on_mousewheel(event):
        scroll_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    scroll_canvas.bind("<MouseWheel>", _on_mousewheel)
    container.bind("<MouseWheel>", _on_mousewheel)

    for cod, config in INVESTIMENTOS.items():
        item = tk.Frame(container, bg=PANEL, bd=1, relief="solid")
        item.pack(fill="x", pady=4)
        item.bind("<MouseWheel>", _on_mousewheel)

        header = tk.Frame(item, bg=PANEL)
        header.pack(fill="x", padx=10, pady=(8, 2))
        header.bind("<MouseWheel>", _on_mousewheel)
        tk.Label(
            header, text="●", font=("Arial", 12),
            bg=PANEL, fg=config["cor"],
        ).pack(side="left")
        nome_lbl = tk.Label(
            header, text=f"  {config['nome_exibicao']}",
            font=("Arial", 10, "bold"), bg=PANEL, fg=TXT,
        )
        nome_lbl.pack(side="left")

        desc_lbl = tk.Label(
            item, text=config.get("descricao", ""),
            font=("Arial", 9), bg=PANEL, fg=TXT_SEC,
            wraplength=440, justify="left",
        )
        desc_lbl.pack(anchor="w", padx=10, pady=(0, 8))

        for w in (nome_lbl, desc_lbl):
            w.bind("<MouseWheel>", _on_mousewheel)

    tk.Frame(win, bg=BORDER, height=1).pack(fill="x", padx=20)

    rodape = tk.Frame(win, bg=BG)
    rodape.pack(fill="x", padx=20, pady=12)
    tk.Button(
        rodape, text="Fechar", font=("Arial", 10),
        bg=BORDER, fg=TXT, relief="flat", bd=0,
        cursor="hand2", padx=18, pady=6,
        command=win.destroy,
    ).pack(side="right")

    win.bind("<Escape>", lambda _e: win.destroy())
    win.focus_set()
