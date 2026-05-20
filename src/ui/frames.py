"""
frames.py — Interface do simulador (Tkinter puro).
"""

import tkinter as tk
from tkinter import ttk

from core.constants import (
    INVESTIMENTOS, BG, PANEL, BORDER, TXT, TXT_SEC, BLUE, BLUE_D, GREEN, RED,
    CV_W, CV_H, CX, CY, R_EXT, R_INT, CARD_COLS, formatar_brl,
)
from core.calculator import calcular_totais
from ui.tooltip import Tooltip, abrir_glossario


def configurar_estilos():
    s = ttk.Style()
    s.theme_use("clam")

    s.configure("Pill.TButton", font=("Arial", 9),
                relief="flat", borderwidth=0, padding=(10, 6),
                background=BORDER, foreground=TXT_SEC)
    s.map("Pill.TButton",
          background=[("active", "#D4D4D4")],
          foreground=[("active", TXT)])

    s.configure("Add.TButton", font=("Arial", 10, "bold"),
                relief="flat", borderwidth=0, padding=(18, 8),
                background=BLUE, foreground="white")
    s.map("Add.TButton",
          background=[("active", BLUE_D)])

    for cod, config in INVESTIMENTOS.items():
        s.configure(f"Pill_{cod}.TButton", font=("Arial", 9, "bold"),
                    relief="flat", borderwidth=0, padding=(10, 6),
                    background=config["cor"], foreground="white")
        s.map(f"Pill_{cod}.TButton",
              background=[("active", config["cor"])])


def criar_header(root, data_atualizacao=None, on_exportar_pdf=None):
    f = tk.Frame(root, bg=BG)
    f.pack(fill="x", pady=(18, 8), padx=30)

    direita = tk.Frame(f, bg=BG)
    direita.pack(side="right", anchor="ne")

    ajuda = tk.Label(
        direita, text="?", font=("Arial", 11, "bold"),
        bg=BORDER, fg=TXT, padx=8, pady=1, cursor="hand2",
    )
    ajuda.pack(side="right", padx=(8, 0))
    ajuda.bind("<Button-1>", lambda _e: abrir_glossario(root))

    if on_exportar_pdf is not None:
        btn_pdf = tk.Label(
            direita, text="Exportar PDF", font=("Arial", 9, "bold"),
            bg=BLUE, fg="white", padx=10, pady=3, cursor="hand2",
        )
        btn_pdf.pack(side="right", padx=(8, 0))
        btn_pdf.bind("<Button-1>", lambda _e: on_exportar_pdf())
        Tooltip(btn_pdf, "Exportar a simulação atual como PDF")

    if data_atualizacao:
        tk.Label(direita, text=f"Taxas atualizadas em {data_atualizacao}",
                 font=("Arial", 8), bg=BG, fg=TXT_SEC).pack(side="right")

    esquerda = tk.Frame(f, bg=BG)
    esquerda.pack(side="left", anchor="w")
    tk.Label(esquerda, text="Simulador de Investimentos",
             font=("Arial", 18, "bold"), bg=BG, fg=TXT).pack(anchor="w")
    tk.Label(esquerda, text="Adicione investimentos e compare os rendimentos",
             font=("Arial", 9), bg=BG, fg=TXT_SEC).pack(anchor="w")


def _validar_valor(novo_texto):
    # Aceita dígitos, ponto (separador de milhar) e vírgula (decimal, no máximo 1).
    if novo_texto == "":
        return True
    if not all(c.isdigit() or c in ".," for c in novo_texto):
        return False
    if novo_texto.count(",") > 1:
        return False
    return True


def criar_input_panel(root, tipo_var, anos_var, on_adicionar, on_mudar_anos):
    tk.Frame(root, bg=BORDER, height=1).pack(fill="x")
    painel = tk.Frame(root, bg=PANEL)
    painel.pack(fill="x")
    inner = tk.Frame(painel, bg=PANEL)
    inner.pack(padx=30, pady=14, anchor="w")

    tk.Label(inner, text="Tipo", font=("Arial", 10, "bold"),
             bg=PANEL, fg=TXT).grid(row=0, column=0, sticky="w", padx=(0, 20))
    pill_f = tk.Frame(inner, bg=PANEL)
    pill_f.grid(row=1, column=0, sticky="w", padx=(0, 20))

    pill_btns = {}
    primeiro = list(INVESTIMENTOS.keys())[0]

    def selecionar(cod):
        tipo_var.set(cod)
        for c, btn in pill_btns.items():
            btn.config(style=f"Pill_{c}.TButton" if c == cod else "Pill.TButton")

    for cod, config in INVESTIMENTOS.items():
        b = ttk.Button(pill_f, text=config["nome_exibicao"],
                       style="Pill.TButton", cursor="hand2",
                       command=lambda c=cod: selecionar(c))
        b.pack(side="left", padx=(0, 4))
        pill_btns[cod] = b
        Tooltip(b, config.get("descricao", ""))
    selecionar(primeiro)

    tk.Label(inner, text="Valor (R$)", font=("Arial", 10, "bold"),
             bg=PANEL, fg=TXT).grid(row=0, column=1, sticky="w", padx=(0, 20))
    vcmd = (root.register(_validar_valor), "%P")
    valor_entry = tk.Entry(inner, width=12, font=("Arial", 12),
                           bg=PANEL, fg=TXT, relief="solid", bd=1,
                           validate="key", validatecommand=vcmd)
    valor_entry.insert(0, "10000")
    valor_entry.grid(row=1, column=1, sticky="w", padx=(0, 20))
    valor_entry.bind("<Return>", lambda e: on_adicionar())

    tk.Label(inner, text="Prazo", font=("Arial", 10, "bold"),
             bg=PANEL, fg=TXT).grid(row=0, column=2, sticky="w", padx=(0, 20))
    prazo_f = tk.Frame(inner, bg=PANEL)
    prazo_f.grid(row=1, column=2, sticky="w", padx=(0, 20))
    tk.Button(prazo_f, text="−", font=("Arial", 12, "bold"),
              bg=BORDER, fg=TXT, relief="flat", bd=0,
              width=4, cursor="hand2",
              command=lambda: on_mudar_anos(-1)).pack(side="left")
    tk.Label(prazo_f, textvariable=anos_var, font=("Arial", 14, "bold"),
             bg=PANEL, fg=TXT, width=3, anchor="center").pack(side="left")
    tk.Label(prazo_f, text="anos", font=("Arial", 9),
             bg=PANEL, fg=TXT_SEC).pack(side="left", padx=(2, 0))
    tk.Button(prazo_f, text="+", font=("Arial", 12, "bold"),
              bg=BORDER, fg=TXT, relief="flat", bd=0,
              width=4, cursor="hand2",
              command=lambda: on_mudar_anos(+1)).pack(side="left")

    ttk.Button(inner, text="Adicionar →", style="Add.TButton",
               cursor="hand2", command=on_adicionar).grid(row=1, column=3, sticky="w")

    tk.Frame(root, bg=BORDER, height=1).pack(fill="x")

    return {"valor_entry": valor_entry, "pill_btns": pill_btns}


def criar_area_grafico(root):
    """Gráfico à esquerda, grid de cards à direita com scroll condicional."""
    area = tk.Frame(root, bg=BG)
    area.pack(fill="both", expand=True, padx=30, pady=10)

    # gráfico à esquerda
    canvas = tk.Canvas(area, width=CV_W, height=CV_H,
                       bg=BG, highlightthickness=0)
    canvas.pack(side="left", anchor="n")

    # lado direito: container com scroll condicional
    right = tk.Frame(area, bg=BG)
    right.pack(side="left", fill="both", expand=True, padx=(15, 0))

    scroll_canvas = tk.Canvas(right, bg=BG, highlightthickness=0)
    scrollbar = ttk.Scrollbar(right, orient="vertical", command=scroll_canvas.yview)

    legenda_frame = tk.Frame(scroll_canvas, bg=BG)

    legenda_frame.bind("<Configure>", lambda e: _atualizar_scroll(scroll_canvas, scrollbar))
    scroll_canvas.create_window((0, 0), window=legenda_frame, anchor="nw")
    scroll_canvas.configure(yscrollcommand=scrollbar.set)

    scroll_canvas.pack(side="left", fill="both", expand=True)
    # scrollbar não é packada agora — só quando necessário

    def _on_mousewheel(event):
        scroll_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    scroll_canvas.bind("<MouseWheel>", _on_mousewheel)
    legenda_frame.bind("<MouseWheel>", _on_mousewheel)

    # guarda referências pro scroll condicional
    legenda_frame._scroll_canvas = scroll_canvas
    legenda_frame._scrollbar = scrollbar

    return canvas, legenda_frame


def _atualizar_scroll(scroll_canvas, scrollbar):
    scroll_canvas.configure(scrollregion=scroll_canvas.bbox("all"))
    scroll_canvas.update_idletasks()
    content_h = scroll_canvas.bbox("all")
    visible_h = scroll_canvas.winfo_height()
    if content_h and visible_h > 1 and content_h[3] > visible_h:
        scrollbar.pack(side="right", fill="y")
    else:
        scrollbar.pack_forget()
        scroll_canvas.yview_moveto(0)


def desenhar_grafico(canvas, dados_grafico, anos):
    canvas.delete("all")

    if not dados_grafico:
        canvas.create_text(CX, CY, text="Adicione um investimento\npara ver o gráfico",
                           font=("Arial", 12), fill=TXT_SEC, justify="center")
        return

    total_valor = sum(d["valor"] for d in dados_grafico)
    totais = calcular_totais(dados_grafico)

    start = 90
    gap = 2 if len(dados_grafico) > 1 else 0

    for d in dados_grafico:
        frac = d["valor"] / total_valor
        extent = frac * 360 - gap

        if extent < 1:
            start -= frac * 360
            continue

        if extent >= 360:
            extent = 359.9

        canvas.create_arc(
            CX - R_EXT, CY - R_EXT, CX + R_EXT, CY + R_EXT,
            start=start, extent=-extent,
            fill=d["cor"], outline=BG, width=2, style="pieslice"
        )
        start -= frac * 360

    canvas.create_oval(
        CX - R_INT, CY - R_INT, CX + R_INT, CY + R_INT,
        fill=BG, outline=BG
    )

    canvas.create_text(CX, CY - 20,
                       text=formatar_brl(totais['total_investido']),
                       font=("Arial", 16, "bold"), fill=TXT)
    canvas.create_text(CX, CY + 2,
                       text="investido", font=("Arial", 9), fill=TXT_SEC)

    ganho_total = totais['total_ganho']
    sinal = "+" if ganho_total >= 0 else "−"
    cor_ganho = GREEN if ganho_total >= 0 else RED
    canvas.create_text(CX, CY + 24,
                       text=f"{sinal} {formatar_brl(abs(ganho_total))}",
                       font=("Arial", 12, "bold"), fill=cor_ganho)
    canvas.create_text(CX, CY + 44,
                       text=f"em {anos} anos", font=("Arial", 9), fill=TXT_SEC)


def atualizar_legenda(legenda, dados_grafico):
    for w in legenda.winfo_children():
        w.destroy()

    if not dados_grafico:
        return

    for i, d in enumerate(dados_grafico):
        row = i // CARD_COLS
        col = i % CARD_COLS

        card = tk.Frame(legenda, bg="#F0EEEB", padx=12, pady=10)
        card.grid(row=row, column=col, padx=(0, 8), pady=(0, 8), sticky="nw")

        descricao = INVESTIMENTOS.get(d.get("cod_investimento", ""), {}).get("descricao", "")
        if descricao:
            Tooltip(card, descricao)

        # cabeçalho do card
        header = tk.Frame(card, bg="#F0EEEB")
        header.pack(anchor="w")
        tk.Label(header, text="●", font=("Arial", 11),
                 bg="#F0EEEB", fg=d["cor"]).pack(side="left")
        tk.Label(header, text=f"  {d['nome_exibicao']}",
                 font=("Arial", 10, "bold"), bg="#F0EEEB", fg=TXT).pack(side="left")

        # valores
        tk.Label(card, text=f"Investido: {formatar_brl(d['valor'])}",
                 font=("Arial", 9), bg="#F0EEEB", fg=TXT_SEC).pack(anchor="w", pady=(6, 0))
        tk.Label(card, text=f"Projeção: {formatar_brl(d['valor_futuro'])}",
                 font=("Arial", 9), bg="#F0EEEB", fg=TXT).pack(anchor="w")

        sinal = "+" if d['ganho'] >= 0 else "−"
        cor_ganho = GREEN if d['ganho'] >= 0 else RED
        tk.Label(
            card,
            text=f"Ganho: {sinal} {formatar_brl(abs(d['ganho']))} ({abs(d['percentual_ganho']):.1f}%)",
            font=("Arial", 9), bg="#F0EEEB", fg=cor_ganho,
        ).pack(anchor="w")

        tk.Label(card, text=f"Taxa: {d['taxa_exibicao']:.2f}% a.a.",
                 font=("Arial", 9), bg="#F0EEEB", fg=TXT_SEC).pack(anchor="w")

    # bind mousewheel nos cards novos
    scroll_canvas = legenda._scroll_canvas
    def _on_mousewheel(event):
        scroll_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    for widget in legenda.winfo_children():
        widget.bind("<MouseWheel>", _on_mousewheel)
        for child in widget.winfo_children():
            child.bind("<MouseWheel>", _on_mousewheel)


def criar_chips_bar(root):
    chip_outer = tk.Text(root, bg=BG, relief="flat", bd=0,
                         height=4, cursor="arrow",
                         wrap="word", state="disabled")
    chip_outer.pack(fill="x", padx=30, pady=(0, 10))
    return chip_outer


def atualizar_chips(chip_outer, itens_carteira, on_remover):
    chip_outer.config(state="normal")
    chip_outer.delete("1.0", "end")

    if not itens_carteira:
        chip_outer.config(state="disabled")
        return

    for i, item in enumerate(itens_carteira):
        config = INVESTIMENTOS.get(item["cod_investimento"])
        if config is None:
            continue

        chip = tk.Frame(chip_outer, bg=PANEL, relief="solid", bd=1)

        valor_fmt = formatar_brl(item['valor'])
        tk.Label(chip, text="●", font=("Arial", 9),
                 bg=PANEL, fg=config["cor"], padx=6).pack(side="left")
        tk.Label(chip, text=f"{config['nome_exibicao']} · {valor_fmt}",
                 font=("Arial", 9), bg=PANEL, fg=TXT).pack(side="left")
        tk.Button(chip, text="×", font=("Arial", 9),
                  bg=PANEL, fg=TXT_SEC, relief="flat", bd=0,
                  cursor="hand2", padx=6,
                  command=lambda k=i: on_remover(k)).pack(side="left")

        chip_outer.window_create("end", window=chip, padx=3, pady=2)

    chip_outer.config(state="disabled")
