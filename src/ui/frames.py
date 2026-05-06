"""
frames.py — Interface do simulador (Tkinter puro, sem dependências externas).
"""

import tkinter as tk
from tkinter import ttk

try:
    from src.core.constants import (
        INVESTIMENTOS, BG, PANEL, BORDER, TXT, TXT_SEC, BLUE, BLUE_D, GREEN,
        CV_W, CV_H, CX, CY, R_EXT, R_INT,
    )
    from src.core.calculator import calcular_totais
except ModuleNotFoundError:
    from core.constants import (
        INVESTIMENTOS, BG, PANEL, BORDER, TXT, TXT_SEC, BLUE, BLUE_D, GREEN,
        CV_W, CV_H, CX, CY, R_EXT, R_INT,
    )
    from core.calculator import calcular_totais


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

    s.configure("Step.TButton", font=("Arial", 12, "bold"),
                relief="flat", borderwidth=0, padding=(6, 2),
                background=BORDER, foreground=TXT)
    s.map("Step.TButton",
          background=[("active", "#D4D4D4")])

    for cod, config in INVESTIMENTOS.items():
        s.configure(f"Pill_{cod}.TButton", font=("Arial", 9, "bold"),
                    relief="flat", borderwidth=0, padding=(10, 6),
                    background=config["cor_rgb"], foreground="white")
        s.map(f"Pill_{cod}.TButton",
              background=[("active", config["cor_rgb"])])


def criar_header(root):
    f = tk.Frame(root, bg=BG)
    f.pack(fill="x", pady=(18, 8), padx=30)
    tk.Label(f, text="Simulador de Investimentos",
             font=("Arial", 18, "bold"), bg=BG, fg=TXT).pack(anchor="w")
    tk.Label(f, text="Adicione investimentos e compare os rendimentos",
             font=("Arial", 9), bg=BG, fg=TXT_SEC).pack(anchor="w")


def criar_input_panel(root, tipo_var, anos_var, on_adicionar, on_mudar_anos):
    tk.Frame(root, bg=BORDER, height=1).pack(fill="x")
    painel = tk.Frame(root, bg=PANEL)
    painel.pack(fill="x")
    inner = tk.Frame(painel, bg=PANEL)
    inner.pack(padx=30, pady=14, anchor="w")

    # tipo
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
    selecionar(primeiro)

    # valor
    tk.Label(inner, text="Valor (R$)", font=("Arial", 10, "bold"),
             bg=PANEL, fg=TXT).grid(row=0, column=1, sticky="w", padx=(0, 20))
    valor_entry = tk.Entry(inner, width=12, font=("Arial", 12),
                           bg=PANEL, fg=TXT, relief="solid", bd=1)
    valor_entry.insert(0, "10000")
    valor_entry.grid(row=1, column=1, sticky="w", padx=(0, 20))
    valor_entry.bind("<Return>", lambda e: on_adicionar())

    # prazo
    tk.Label(inner, text="Prazo", font=("Arial", 10, "bold"),
             bg=PANEL, fg=TXT).grid(row=0, column=2, sticky="w", padx=(0, 20))
    prazo_f = tk.Frame(inner, bg=PANEL)
    prazo_f.grid(row=1, column=2, sticky="w", padx=(0, 20))
    ttk.Button(prazo_f, text="−", style="Step.TButton",
               command=lambda: on_mudar_anos(-1)).pack(side="left")
    tk.Label(prazo_f, textvariable=anos_var, font=("Arial", 14, "bold"),
             bg=PANEL, fg=TXT, width=3, anchor="center").pack(side="left")
    tk.Label(prazo_f, text="anos", font=("Arial", 9),
             bg=PANEL, fg=TXT_SEC).pack(side="left", padx=(2, 0))
    ttk.Button(prazo_f, text="+", style="Step.TButton",
               command=lambda: on_mudar_anos(+1)).pack(side="left")

    # botão
    ttk.Button(inner, text="Adicionar →", style="Add.TButton",
               cursor="hand2", command=on_adicionar).grid(row=1, column=3, sticky="w")

    tk.Frame(root, bg=BORDER, height=1).pack(fill="x")

    return {"valor_entry": valor_entry, "pill_btns": pill_btns}


def criar_area_grafico(root):
    area = tk.Frame(root, bg=BG)
    area.pack(fill="x", padx=30, pady=10)

    canvas = tk.Canvas(area, width=CV_W, height=CV_H,
                       bg=BG, highlightthickness=0)
    canvas.pack(side="left")

    legenda = tk.Frame(area, bg=BG)
    legenda.pack(side="left", fill="y", padx=(20, 0))

    return canvas, legenda


def desenhar_grafico(canvas, dados_grafico, anos):
    canvas.delete("all")

    if not dados_grafico:
        canvas.create_text(CX, CY, text="Adicione um investimento\npara ver o gráfico",
                           font=("Arial", 12), fill=TXT_SEC, justify="center")
        return

    total_valor = sum(d["valor"] for d in dados_grafico)
    totais = calcular_totais(dados_grafico)

    # desenhar arcos da rosca
    start = 90  # começa do topo
    gap = 2 if len(dados_grafico) > 1 else 0

    for d in dados_grafico:
        frac = d["valor"] / total_valor
        extent = frac * 360 - gap
        if extent < 1:
            start -= frac * 360
            continue

        # anel principal
        canvas.create_arc(
            CX - R_EXT, CY - R_EXT, CX + R_EXT, CY + R_EXT,
            start=start, extent=-extent,
            fill=d["cor"], outline=BG, width=2, style="pieslice"
        )
        start -= frac * 360

    # furo central (cria o efeito rosca)
    canvas.create_oval(
        CX - R_INT, CY - R_INT, CX + R_INT, CY + R_INT,
        fill=BG, outline=BG
    )

    # textos no centro
    canvas.create_text(CX, CY - 20,
                       text=f"R$ {totais['total_investido']:,.0f}",
                       font=("Arial", 16, "bold"), fill=TXT)
    canvas.create_text(CX, CY + 2,
                       text="investido", font=("Arial", 9), fill=TXT_SEC)
    canvas.create_text(CX, CY + 24,
                       text=f"+ R$ {totais['total_ganho']:,.0f}",
                       font=("Arial", 12, "bold"), fill=GREEN)
    canvas.create_text(CX, CY + 44,
                       text=f"em {anos} anos", font=("Arial", 9), fill=TXT_SEC)


def atualizar_legenda(legenda, dados_grafico):
    for w in legenda.winfo_children():
        w.destroy()

    if not dados_grafico:
        return

    tk.Label(legenda, text="Detalhamento", font=("Arial", 11, "bold"),
             bg=BG, fg=TXT).pack(anchor="w", pady=(0, 8))

    for d in dados_grafico:
        item_f = tk.Frame(legenda, bg=BG)
        item_f.pack(anchor="w", pady=4, fill="x")

        # bolinha de cor + nome
        tk.Label(item_f, text="●", font=("Arial", 12),
                 bg=BG, fg=d["cor"]).pack(side="left")
        tk.Label(item_f, text=f"  {d['nome_exibicao']}",
                 font=("Arial", 10, "bold"), bg=BG, fg=TXT).pack(side="left")

        # valores
        vals_f = tk.Frame(legenda, bg=BG)
        vals_f.pack(anchor="w", padx=(18, 0), pady=(0, 6))

        tk.Label(vals_f, text=f"Investido: R$ {d['valor']:,.0f}",
                 font=("Arial", 9), bg=BG, fg=TXT_SEC).pack(anchor="w")
        tk.Label(vals_f, text=f"Projeção: R$ {d['valor_futuro']:,.0f}",
                 font=("Arial", 9), bg=BG, fg=TXT).pack(anchor="w")
        tk.Label(vals_f, text=f"Ganho: + R$ {d['ganho']:,.0f} ({d['percentual_ganho']:.1f}%)",
                 font=("Arial", 9), bg=BG, fg=GREEN).pack(anchor="w")
        tk.Label(vals_f, text=f"Taxa: {d['taxa_exibicao']:.2f}% a.a.",
                 font=("Arial", 9), bg=BG, fg=TXT_SEC).pack(anchor="w")


def criar_chips_bar(root):
    chip_outer = tk.Frame(root, bg=BG)
    chip_outer.pack(fill="x", padx=30, pady=(0, 10))
    return chip_outer


def atualizar_chips(chip_outer, itens_carteira, on_remover):
    for w in chip_outer.winfo_children():
        w.destroy()

    if not itens_carteira:
        tk.Label(chip_outer, text="Nenhum investimento adicionado.",
                 font=("Arial", 9), bg=BG, fg=TXT_SEC).pack(side="left")
        return

    for i, item in enumerate(itens_carteira):
        config = INVESTIMENTOS.get(item["cod_investimento"])
        if config is None:
            continue

        chip = tk.Frame(chip_outer, bg=PANEL, relief="solid", bd=1)
        chip.pack(side="left", padx=(0, 6), pady=2)

        tk.Label(chip, text="●", font=("Arial", 9),
                 bg=PANEL, fg=config["cor"], padx=6).pack(side="left")
        tk.Label(chip, text=f"{config['nome_exibicao']} · R$ {item['valor']:,.0f}",
                 font=("Arial", 9), bg=PANEL, fg=TXT).pack(side="left")
        tk.Button(chip, text="×", font=("Arial", 9),
                  bg=PANEL, fg=TXT_SEC, relief="flat", bd=0,
                  cursor="hand2", padx=6,
                  command=lambda k=i: on_remover(k)).pack(side="left")