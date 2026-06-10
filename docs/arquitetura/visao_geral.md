# Visão Geral da Arquitetura

O simulador é uma aplicação desktop em Python que roda toda na máquina do usuário: interface, cálculos e arquivos de dados. O usuário informa um valor e um tipo de investimento e o sistema desenha um gráfico de rosca mostrando quanto esse dinheiro deve render no prazo escolhido. As taxas de mercado (Selic, CDI, IPCA e as demais) vêm do Supabase, que por sua vez é alimentado diariamente pela API pública do Banco Central. A carteira fica salva num JSON local.

---

## Camadas

O código em src se divide em três pastas, uma por camada.

A pasta ui é a apresentação. O interface.py monta as telas do Tkinter (cabeçalho, painel de entrada, gráfico de rosca, cards e os chips da carteira), configura os estilos e trata os eventos, e o tooltip.py cuida dos tooltips de hover e da janela do glossário, aberta pelo botão de interrogação. Essa camada não faz cálculo nem acessa banco, só exibe o que as outras devolvem.

A pasta core é a regra de negócio. O calculator.py implementa os juros compostos com taxas variáveis por ano, prepara os dados do gráfico e soma os totais da carteira, e o constants.py concentra cores, prazos e o mapeamento dos investimentos. Não tem nenhuma dependência de Tkinter ou Supabase aqui, o que deixa as funções fáceis de testar.

A pasta dados cuida de ler e gravar: o supabase_client.py consulta a view vw_indicadores_investimento, o armazenamento.py salva e carrega a carteira e o cache de taxas em JSON, e o pdf_export.py gera o PDF da simulação com a biblioteca fpdf2.

Quem amarra as três é o main.py, único arquivo que conhece todas as camadas ao mesmo tempo.

## Fluxo principal

```
Usuário abre o app
  └── supabase_client busca taxas
        └── [sem conexão] usa cache local
  └── armazenamento carrega carteira salva

Usuário adiciona investimento
  └── interface.py captura input → valida
  └── calculator.py calcula projeção
  └── interface.py desenha gráfico e legenda
  └── armazenamento salva carteira

Usuário muda prazo
  └── calculator recalcula → interface redesenha
```

---

## Relação entre componentes

```
main.py (orquestrador)
  ├── chama → interface.py (telas)
  ├── chama → calculator.py (projeções)
  ├── chama → supabase_client.py (taxas na inicialização)
  ├── chama → armazenamento.py (salvar/carregar carteira e cache)
  └── chama → pdf_export.py (ao clicar em "Exportar PDF")

calculator.py
  └── depende de → constants.py (mapeamento de investimentos)

interface.py
  └── depende de → constants.py (cores, descrições)
  └── depende de → calculator.py (calcular_totais para o gráfico)
  └── depende de → tooltip.py (tooltips em hover e janela do glossário)

tooltip.py
  └── depende de → constants.py (cores e dicionário INVESTIMENTOS)

pdf_export.py
  └── depende de → calculator.py (calcular_totais para o resumo do PDF)
  └── depende de → constants.py (formatar_brl)
```

---

## Diagrama de histórias de usuário

Link: https://www.figma.com/board/nN0JSuSVPB9LzBQh5qHSJh/Hist%C3%B3rias-de-Usu%C3%A1rio?node-id=0-1&t=l3nvlIuwgJwutzGD-1

![alt text](historias_usuarios.png)

---

*Última atualização: 09/06/2026*