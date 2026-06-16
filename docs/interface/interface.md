# Interface do Simulador

A interface é feita com Tkinter e está em dois arquivos na pasta src/ui: o interface.py, com todos os componentes visuais, e o tooltip.py, com os tooltips e o glossário.

## Estrutura da janela

A janela abre centralizada com quatro seções empilhadas. No topo o cabeçalho, com o título, a data da última atualização das taxas, o botão de exportar PDF e o botão de interrogação que abre o glossário. Abaixo vem o painel de entrada, onde o usuário escolhe o tipo de investimento (um botão por tipo), digita o valor e ajusta o prazo em anos com os botões de mais e menos. Na sequência fica a barra de chips, que lista os investimentos já adicionados: cada chip mostra a cor e o valor do item e tem dois botõezinhos, um lápis pra editar o valor e um xis pra remover. Por fim a área principal, com o gráfico de rosca à esquerda e os cards detalhados à direita, os dois atualizados a cada mudança.

## Componentes do interface.py

O cabeçalho e o painel de entrada são montados por criar_header e criar_input_panel. O campo de valor tem validação em tempo real que só aceita dígitos, ponto e vírgula, e a tecla Enter adiciona direto, sem precisar clicar no botão.

A barra de chips usa um truque: um tk.Text desabilitado serve de container e cada chip é um tk.Frame embutido nele, o que faz os chips quebrarem de linha sozinhos quando a carteira cresce. Clicando no lápis de um chip abre uma janela já preenchida com o valor atual pedindo o novo valor. Se o usuário confirmar um valor válido, a carteira é salva e tudo se redesenha; se cancelar ou digitar algo inválido, nada muda.

O desenhar_grafico monta o gráfico no canvas e escreve no centro o total investido, o ganho (verde quando positivo, vermelho quando negativo) e o prazo. Com a carteira vazia, aparece uma mensagem no lugar do gráfico. O atualizar_legenda reconstrói os cards, cada um com nome, valor investido, projeção, ganho com percentual e a taxa anual equivalente. A área dos cards tem rolagem própria.

## Tooltips e glossário

O Tooltip aparece depois de meio segundo com o mouse parado sobre o componente e some quando o ponteiro sai de verdade. O glossário abre numa janela centralizada com rolagem, listando cada tipo de investimento com nome e descrição, e fecha pelo botão ou pela tecla Escape.

## Detalhes de comportamento

Como o botão nativo do tk não tem estado de hover, a troca de cor ao passar o mouse é feita manualmente. O scroll do mouse é direcionado pro canvas certo conforme a posição do ponteiro. Os estilos ttk ficam concentrados numa função só de configuração, incluindo um estilo por tipo de investimento, usando a cor definida nas constantes.

*Última atualização: 10/06/2026*