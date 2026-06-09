# Integração Completa

Nas semanas anteriores cada parte do sistema já estava funcionando, mas meio separada. Aqui é onde a gente mostra tudo junto, conectado e rodando do começo ao fim.

## As três camadas conversando

O sistema tem três camadas:

- A interface (pasta ui), que é tudo que o usuário vê. Ela não faz conta nem mexe em banco, só pega o que o usuário fez, pede pra camada de cálculo resolver e desenha o resultado na tela.
- A regra de negócio (pasta core), que são as funções de cálculo. Recebe os dados, faz as contas e devolve. Ela não sabe nem que existe Tkinter ou Supabase.
- Os dados (pasta dados), que cuida de guardar e buscar informação: o Supabase pras taxas do Banco Central e os arquivos JSON pra carteira e pro cache. O pdf_export.py também ficou aqui porque gera arquivo.

Quem junta tudo isso é o main.py. Ele é o único arquivo que conhece as três camadas ao mesmo tempo.

## O que acontece quando abre o app

Quando o usuário abre o programa, o main.py faz nessa ordem:

1. Tenta buscar as taxas no Supabase.
2. Se conseguiu, salva no cache local. Se não conseguiu (sem internet, por exemplo), carrega o cache que já tinha salvo antes.
3. Carrega a carteira do JSON. Se for a primeira vez, vem vazia.
4. Monta a tela (cabeçalho, painel de adicionar, gráfico, legenda e os chips da carteira).
5. Faz um primeiro cálculo pra já abrir mostrando o estado certo.

Depois disso o app fica esperando o usuário fazer alguma coisa.

## Os caminhos principais

Adicionar investimento: o usuário digita o valor, escolhe o tipo e clica em adicionar. O programa valida o valor (se for zero ou negativo, o campo pisca vermelho e não faz nada), coloca o item na carteira, salva no JSON, recalcula tudo e redesenha o gráfico. São cinco passos, mas repara que ele passa pelas três camadas numa tacada só.

Remover investimento: cada item da carteira tem um xizinho. Clicou, ele tira da carteira, salva de novo e redesenha.

Mudar o prazo: tem os botões de mais e menos que vão de 1 até 30 anos. Aqui ele só recalcula e redesenha, não salva no JSON, porque o prazo é só um jeito de visualizar e não faz parte da carteira em si.

Exportar PDF: clica no botão no cabeçalho, abre uma janela pra escolher onde salvar e o programa gera o PDF com a tabela da simulação.

---

Última atualização: Semana 8 — 02/06/2026
