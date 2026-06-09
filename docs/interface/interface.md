# Interface do Simulador de Investimentos

A interface é construída com Tkinter e organizada em dois arquivos na pasta `src/ui/`: `interface.py`, responsável por todos os componentes visuais, e `tooltip.py`, responsável pelos tooltips e pelo glossário.

---

## Estrutura geral

A janela é composta por quatro seções empilhadas verticalmente:

1. **Header** — título do app, data de atualização das taxas, botão de exportar PDF e botão `?` que abre o glossário.
2. **Painel de input** — onde o usuário configura e adiciona investimentos. Contém seleção de tipo (pills), campo de valor e controle de prazo em anos.
3. **Chips bar** — lista horizontal dos investimentos já adicionados à carteira, cada um com botão de remoção `×`.
4. **Área principal** — gráfico de rosca à esquerda e grid de cards à direita, ambos atualizados em tempo real.

---

## Componentes principais

### `criar_header`
Monta o cabeçalho com o título, subtítulo e botões no lado direito.

### `criar_input_panel`
Renderiza o painel de adição de investimentos. Os tipos disponíveis são lidos de `INVESTIMENTOS` e exibidos como botões pill. O campo de valor tem validação em tempo real que aceita apenas dígitos, ponto e vírgula. O prazo é controlado por botões `−` e `+`.

### `criar_chips_bar` / `atualizar_chips`
Usa um `tk.Text` desabilitado como container para os chips. Cada chip é um `tk.Frame` embutido via `window_create`.

### `criar_area_grafico`
Divide a área principal em canvas (gráfico) à esquerda e um scroll canvas com `legenda_frame` à direita, com barra de rolagem vertical.

### `desenhar_grafico`
Desenha o gráfico de rosca no canvas usando `create_arc`. No centro exibe o total investido, o ganho total (verde/vermelho) e o prazo. Com carteira vazia, exibe uma mensagem automática.

### `atualizar_legenda`
Reconstrói os cards de investimento no grid. Cada card mostra: nome, valor investido, projeção futura, ganho com percentual e taxa anual.

---

## Tooltips e Glossário (`tooltip.py`)

### `Tooltip`
Aparece após 500 ms de hover sobre um widget. Trata o caso de o ponteiro passar para um filho do widget sem sumir o tooltip (`_verificar_saida` + `_eh_descendente`).

### `abrir_glossario`
Abre uma janela centralizada com scroll vertical, listando todos os tipos de investimento com nome e descrição. Fecha com o botão "Fechar" ou pela tecla `Escape`.

---

## Detalhes de UX

- **Hover em botões tk nativos** é feito manualmente via `_adicionar_hover`, já que `tk.Button` não suporta estados CSS.
- **Scroll do mouse** é propagado para o canvas correto via `_bind_scroll`, aplicado ao canvas e a todos os widgets filhos.
- **Estilos ttk** são configurados em `configurar_estilos()`, incluindo um estilo `Pill_{cod}` dinâmico por tipo de investimento, usando a cor definida nas constantes.
