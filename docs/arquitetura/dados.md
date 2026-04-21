# Modelo e Persistência de Dados

## Visão geral

O sistema trabalha com dois tipos de dados em locais diferentes:

| Dado | Onde fica | Quem escreve | Quem lê |
|---|---|---|---|
| Indicadores de mercado (Selic, CDI, IPCA, etc.) | Supabase (PostgreSQL) | Edge Function automática | `supabase_client.py` |
| Cache local das taxas | `data/cache_taxas.json` | `json_repository.py` | `json_repository.py` |
| Carteira do usuário | `data/carteira.json` | `json_repository.py` | `json_repository.py` |

---

## Banco de dados — Supabase

### Tabelas

**`cfg_indicadores_investimento`** — configuração estática dos investimentos.

| Coluna | Tipo | Descrição |
|---|---|---|
| `cod_investimento` | varchar(20) PK | Código único (SELIC, CDI, IPCA, POUPANCA, IGPM, CAMBIO) |
| `des_investimento` | varchar(100) | Nome de exibição (Tesouro Selic, CDB 100% CDI, etc.) |
| `des_indicador` | varchar(100) | Nome do indicador na API do BCB (null se calculado) |
| `ind_calculado` | boolean | Se true, a taxa é derivada da Selic (CDI e Poupança) |

**`stg_indicadores_bcb`** — dados brutos extraídos da API Focus do Banco Central.

| Coluna | Tipo | Descrição |
|---|---|---|
| `id` | bigint (identity) | Chave primária |
| `des_indicador` | text | Nome do indicador na API do BCB |
| `dat_indicador` | date | Data da consulta |
| `ano_referencia` | integer | Ano ao qual a projeção se refere |
| `vlr_mediana` | numeric(15,6) | Valor mediana da expectativa de mercado (% a.a.) |
| `dat_atualizacao` | timestamp | Data/hora em que o registro foi inserido |

### View

**`vw_indicadores_investimento`** — calcula as taxas derivadas.

Lógica:
- Filtra apenas os registros da data mais recente em `stg_indicadores_bcb`
- Junta com `cfg_indicadores_investimento` pelo `des_indicador`
- Calcula CDI como `Selic - 0.10`
- Calcula Poupança como `70% da Selic` quando Selic ≤ 8.5%, ou `6.17%` fixo quando Selic > 8.5%

Colunas retornadas:

| Coluna | Tipo | Exemplo |
|---|---|---|
| `cod_investimento` | text | "SELIC" |
| `des_investimento` | text | "Tesouro Selic" |
| `ano_referencia` | integer | 2025 |
| `vlr_mediana` | numeric | 14.75 |
| `dat_indicador` | date | "2026-04-14" |

### Edge Function — `f_indicadores_bcb`

Função do Supabase que executa o pipeline ETL:

1. Consulta a API pública de expectativas do BCB (`ExpectativasMercadoAnuais`)
2. Busca todos os registros da data mais recente disponível
3. Faz upsert na tabela `stg_indicadores_bcb`

Agendada para rodar diariamente no Supabase.

---

## Persistência local — JSON

### Carteira do usuário (`data/carteira.json`)

Salva os investimentos que o usuário adicionou no simulador. Exemplo do arquivo:

```json
{
  "atualizado_em": "2026-04-14T15:30:00.000000",
  "itens": [
    {"cod_investimento": "SELIC", "valor": 10000.0},
    {"cod_investimento": "CDI", "valor": 5000.0},
    {"cod_investimento": "POUPANCA", "valor": 3000.0}
  ]
}
```

Funções disponíveis em `json_repository.py`:
- `salvar_carteira(itens)` — recebe lista de dicts e grava no JSON
- `carregar_carteira()` → retorna lista de dicts (vazia se não existir)
- `limpar_carteira()` — remove o arquivo

### Cache de taxas (`data/cache_taxas.json`)

Cópia local das taxas do Supabase para uso offline. Quando o app inicia, tenta buscar do Supabase e, se falhar, usa o cache. Exemplo:

```json
{
  "atualizado_em": "2026-04-14T15:30:00.000000",
  "indicadores": [
    {
      "cod_investimento": "SELIC",
      "des_investimento": "Tesouro Selic",
      "ano_referencia": 2025,
      "vlr_mediana": 14.75,
      "dat_indicador": "2026-04-14"
    }
  ]
}
```

Funções disponíveis:
- `salvar_cache_taxas(indicadores)` — grava a lista retornada pelo Supabase
- `carregar_cache_taxas()` → retorna lista no mesmo formato da view
- `cache_taxas_existe()` → boolean
- `data_cache_taxas()` → string ISO da última atualização ou None

---

## Fluxo de dados na inicialização

```
App inicia
  └── supabase_client.buscar_indicadores()
        ├── [sucesso] → salvar_cache_taxas(dados) → usa os dados
        └── [falha]   → carregar_cache_taxas() → usa cache local
  └── carregar_carteira() → restaura investimentos do usuário
```

---

## Validação

O script `testar_persistencia.py` em `src/tests/` testa todas as funções de forma isolada:
- Salvar, carregar, atualizar e remover itens da carteira
- Resiliência a JSON corrompido (retorna lista vazia em vez de crashar)
- Salvar e carregar cache de taxas
- Verificação de existência e data do cache

---

*Última atualização: Semana 3 — 21/04/2026*
