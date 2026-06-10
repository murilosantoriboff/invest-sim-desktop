# Rastreabilidade

Este documento liga cada requisito ao código que o implementa e ao teste que o valida. Os testes automáticos são os scripts de src/testes; o que é visual foi verificado manualmente na interface.

## Regra de negócio

| Requisito | Procedimento | Código | Teste | Resultado |
|---|---|---|---|---|
| Render com juros compostos | Aplica a taxa ano a ano em cima do valor | projetar_valor em calculator.py | auto: testar_calculator, bloco de projeção de valor | OK |
| Usar taxa diferente pra cada ano | Pega a taxa de cada ano de referência; se acabar, repete a última | projetar_valor em calculator.py | auto: testar_calculator, casos de taxas variáveis | OK |
| Projetar o Dólar pela cotação | Multiplica pela razão entre cotação final e inicial (não é %) | projetar_cotacao em calculator.py | auto: testar_calculator, bloco do CAMBIO | OK |
| Mostrar a taxa equivalente no card | Calcula a média geométrica das taxas do período | preparar_dados_grafico em calculator.py | auto: testar_calculator, caso da taxa de exibição | OK |
| Somar os totais da carteira | Agrega investido, futuro e ganho de todos os itens | calcular_totais em calculator.py | auto: testar_calculator, bloco de totais | OK |
| Ignorar ativo sem taxa | Item sem taxa cadastrada fica de fora do gráfico | preparar_dados_grafico em calculator.py | auto: testar_calculator, caso do ativo desconhecido | OK |

## Persistência

| Requisito | Procedimento | Código | Teste | Resultado |
|---|---|---|---|---|
| Salvar a carteira | Grava os itens num JSON local | salvar_carteira em armazenamento.py | auto: testar_persistencia, bloco da carteira | OK |
| Carregar a carteira | Lê o JSON na inicialização (vazia se for a 1ª vez) | carregar_carteira em armazenamento.py | auto: testar_persistencia, bloco da carteira | OK |
| Não quebrar com JSON corrompido | Arquivo com lixo devolve lista vazia em vez de crashar | carregar_carteira em armazenamento.py | auto: testar_persistencia, caso do arquivo corrompido | OK |
| Guardar cache das taxas | Salva as taxas pra usar offline depois | salvar_cache_taxas em armazenamento.py | auto: testar_persistencia, bloco do cache | OK |
| Usar cache quando offline | Se o Supabase falhar, lê as taxas do cache | carregar_cache_taxas em armazenamento.py | auto: testar_integracao, fluxo offline | OK |
| Buscar taxas reais do BCB | Consulta a view no Supabase e traz as taxas | buscar_indicadores em supabase_client.py | auto: testar_integracao, fluxo online | OK |

## Interface e fluxo

| Requisito | Procedimento | Código | Teste | Resultado |
|---|---|---|---|---|
| Adicionar investimento | Pega valor e tipo, valida, joga na carteira e salva | _adicionar em main.py | auto: testar_integracao, fluxo offline; e manual | OK |
| Editar investimento | O lápis do chip abre janela pra digitar o novo valor | _editar em main.py | manual | OK |
| Remover investimento | Clica no x do chip e tira da carteira | _remover em main.py | auto: testar_integracao, fluxo offline; e manual | OK |
| Escolher prazo de 1 a 30 anos | Botões de mais e menos ajustam o prazo e recalculam | _mudar_anos em main.py | auto: testar_integracao, fluxo offline; e manual | OK |
| Recusar valor inválido | Valor zero ou negativo faz o campo piscar vermelho | _adicionar em main.py | manual | OK |
| Desenhar gráfico de rosca e cards | Monta a rosca e os cards com o detalhe de cada item | desenhar_grafico e atualizar_legenda em interface.py | manual | OK |
| Tooltips e glossário | Texto explicativo no hover e janela do botão de interrogação | tooltip.py | manual | OK |
| Exportar a simulação em PDF | Abre a janela de salvar e gera o PDF com a tabela | exportar_pdf em pdf_export.py | manual | OK |
| Mostrar data da última atualização | Formata a data do cache pro cabeçalho | _formatar_data_atualizacao em main.py | manual | OK |

*Última atualização: 09/06/2026*
