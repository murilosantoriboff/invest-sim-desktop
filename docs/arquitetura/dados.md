# Modelo e Persistência de Dados

O sistema trabalha com dois tipos de dados em locais diferentes:

| Dado | Onde fica | Quem escreve | Quem lê |
|---|---|---|---|
| Indicadores de mercado (Selic, CDI, IPCA, etc.) | Supabase (PostgreSQL) | Edge Function automática | `supabase_client.py` |
| Cache local das taxas | `data/cache_taxas.json` | `armazenamento.py` | `armazenamento.py` |
| Carteira do usuário | `data/carteira.json` | `armazenamento.py` | `armazenamento.py` |

---

## Banco no Supabase

São duas tabelas e uma view.

A cfg_indicadores_investimento é a configuração estática: uma linha por investimento, com o código (SELIC, CDI, IPCA, POUPANCA, IGPM, CAMBIO), o nome de exibição, o nome do indicador correspondente na API do BCB e uma marcação de quando a taxa é calculada a partir de outra, que é o caso do CDI e da Poupança, derivados da Selic.

A stg_indicadores_bcb recebe os dados brutos extraídos da API Focus do Banco Central: nome do indicador, data da consulta, ano de referência da projeção, a mediana da expectativa de mercado e a data e hora em que o registro foi inserido.

A vw_indicadores_investimento é o que o simulador realmente consulta. Ela filtra só os registros da data mais recente, junta as duas tabelas e calcula as taxas derivadas: o CDI sai como Selic menos 0 10, e a Poupança como 70% da Selic quando esta fica até 8.5%, ou 6.17% fixos quando passa disso. O app recebe o código, o nome, o ano de referência, o valor e a data do indicador, tudo pronto pra usar.

Quem alimenta a stg é a Edge Function f_indicadores_bcb, agendada pra rodar uma vez por dia no Supabase. Ela consulta a API pública de expectativas anuais do BCB, pega todos os registros da data mais recente disponível e grava na tabela, atualizando o que já existia.

## Arquivos locais

A carteira do usuário fica em data/carteira.json: um objeto com a data da última gravação e a lista de itens, cada item com o código do investimento e o valor aplicado. O armazenamento.py oferece a salvar_carteira, que recebe a lista e grava, e a carregar_carteira, que devolve a lista (vazia se o arquivo não existir ou estiver corrompido). Esse arquivo é regravado toda vez que o usuário adiciona, edita ou remove um investimento.

O cache de taxas fica em data/cache_taxas.json e é uma cópia do que veio da view do Supabase, no mesmo formato, junto com a data em que foi salvo. Na inicialização o app tenta buscar as taxas online e, conseguindo, regrava o cache com salvar_cache_taxas. Se a busca falhar, carregar_cache_taxas devolve a última cópia salva e o simulador funciona offline. A data_cache_taxas informa quando foi a última atualização, que é a data mostrada no cabeçalho da interface.

## Validação

O testar_persistencia.py cobre essas funções numa pasta temporária: salvar, carregar, atualizar e remover itens da carteira, o comportamento com JSON corrompido (que devolve lista vazia) e o ciclo completo do cache de taxas, incluindo a data de atualização. Roda a partir da pasta src com python testes/testar_persistencia.py.

*Última atualização: 09/06/2026*
