# Rastreabilidade

## Regra de negócio

| Requisito | Procedimento | Código | Teste | Resultado |
|---|---|---|---|---|
| Render com juros compostos | Aplica a taxa ano a ano em cima do valor | `core/calculator.py` → `projetar_valor()` | auto — `testar_calculator` cen. 1 a 4 | OK |
| Usar taxa diferente pra cada ano | Pega a taxa de cada ano de referência; se acabar, repete a última | `core/calculator.py` → `projetar_valor()` | auto — `testar_calculator` cen. 3 e 4 | OK |
| Projetar o Dólar pela cotação | Multiplica pela razão cotação_final / cotação_inicial (não é %) | `core/calculator.py` → `projetar_cotacao()` | auto — `testar_calculator` cen. 10 a 12 | OK |
| Mostrar a taxa equivalente no card | Calcula a média geométrica das taxas do período | `core/calculator.py` → `preparar_dados_grafico()` | auto — `testar_calculator` cen. 9 | OK |
| Somar os totais da carteira | Agrega investido, futuro e ganho de todos os itens | `core/calculator.py` → `calcular_totais()` | auto — `testar_calculator` cen. 5 e 6 | OK |
| Ignorar ativo sem taxa | Item que não tem taxa cadastrada fica de fora do gráfico | `core/calculator.py` → `preparar_dados_grafico()` | auto — `testar_calculator` cen. 8 | OK |

## Persistência

| Requisito | Procedimento | Código | Teste | Resultado |
|---|---|---|---|---|
| Salvar a carteira | Grava os itens num JSON local | `infrastructure/storage/json_repository.py` → `salvar_carteira()` | auto — `testar_persistencia` cen. 2 e 3 | OK |
| Carregar a carteira | Lê o JSON na inicialização (vazia se for a 1ª vez) | `json_repository.py` → `carregar_carteira()` | auto — `testar_persistencia` cen. 1 a 3 | OK |
| Não quebrar com JSON corrompido | Se o arquivo tiver lixo, devolve lista vazia em vez de crashar | `json_repository.py` → `carregar_carteira()` / `_ler_json()` | auto — `testar_persistencia` cen. 4 | OK |
| Guardar cache das taxas | Salva as taxas pra usar offline depois | `json_repository.py` → `salvar_cache_taxas()` | auto — `testar_persistencia` cen. 6 | OK |
| Usar cache quando offline | Se o Supabase falhar, lê as taxas do cache | `json_repository.py` → `carregar_cache_taxas()` | auto — `testar_persistencia` cen. 5 e 6 | OK |
| Buscar taxas reais do BCB | Consulta a view no Supabase e traz as taxas | `infrastructure/database/supabase_client.py` → `buscar_indicadores()` | auto — `testar_integracao` cen. 1 e 2 | OK |

## Interface e fluxo

| Requisito | Procedimento | Código | Teste | Resultado |
|---|---|---|---|---|
| Adicionar investimento | Pega valor + tipo, valida, joga na carteira e salva | `main.py` → `_adicionar()` + `ui/frames.py` | auto — `testar_integracao` cen. 4 / manual | OK |
| Remover investimento | Clica no "x" do chip e tira da carteira | `main.py` → `_remover()` + `ui/frames.py` | auto — `testar_integracao` cen. 4 / manual | OK |
| Escolher prazo de 1 a 30 anos | Botões + e − ajustam o prazo e recalculam | `main.py` → `_mudar_anos()` | auto — `testar_integracao` cen. 4 / manual | OK |
| Recusar valor inválido | Valor ≤ 0 faz o campo piscar vermelho e não cria nada | `main.py` → `_adicionar()` | manual | OK |
| Desenhar gráfico de rosca + legenda | Monta o donut e a legenda com o detalhe de cada item | `ui/frames.py` → `desenhar_grafico()` / `atualizar_legenda()` | manual | OK |
| Tooltips e glossário | Texto explicativo no hover e janela do "?" | `ui/tooltip.py` | manual | OK |
| Exportar a simulação em PDF | Abre a janela de salvar e gera o PDF com a tabela | `infrastructure/pdf_export.py` → `exportar_pdf()` | manual | OK |
| Mostrar data da última atualização | Formata a data que veio do cache pro header | `main.py` → `_formatar_data_atualizacao()` | manual | OK |

---

*Última atualização: Semana 8 — 02/06/2026*
