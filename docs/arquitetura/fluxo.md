# Fluxo de Integração

## Caminho dos dados no sistema

O simulador conecta três camadas independentes num fluxo único:

```
Supabase (API BCB)
    │
    ▼
supabase_client.buscar_indicadores()
    │
    ├── [sucesso] → salvar_cache_taxas() → usa os dados
    └── [falha]   → carregar_cache_taxas() → usa cache local
                            │
                            ▼
              calculator.preparar_dados_grafico()
                    │               │
        carregar_carteira()     taxas (lista)
                    │
                    ▼
            dados prontos pro gráfico
                    │
                    ▼
            canvas_render (semana 5)
```

## Detalhamento

### 1. Obter taxas

Na inicialização, o sistema tenta buscar as taxas do Supabase via `buscar_indicadores()`. Se conseguir, salva no cache local com `salvar_cache_taxas()` pra ter os dados disponíveis offline. Se falhar (sem internet, erro de API), carrega do cache com `carregar_cache_taxas()`.

### 2. Carregar carteira

A carteira do usuário é carregada do arquivo local com `carregar_carteira()`. Retorna lista vazia se for a primeira vez.

### 3. Calcular projeções

`preparar_dados_grafico()` recebe a carteira e as taxas, aplica juros compostos ano a ano com taxas variáveis, e retorna uma lista com tudo que o gráfico precisa: valor investido, valor futuro, ganho, percentual, cores.

`calcular_totais()` agrega os valores da carteira inteira.

### 4. Interações do usuário

Cada ação do usuário dispara um recálculo:

| Ação | O que acontece |
|---|---|
| Adicionar investimento | Insere na carteira → `salvar_carteira()` → recalcula |
| Remover investimento | Remove da carteira → `salvar_carteira()` → recalcula |
| Mudar prazo | Recalcula com novo número de anos |

A carteira é persistida a cada alteração pra sobreviver ao fechamento do app.

## Módulos envolvidos

| Camada | Módulo | Papel |
|---|---|---|
| Persistência remota | `supabase_client.py` | Busca taxas do Supabase |
| Persistência local | `json_repository.py` | Cache de taxas + carteira do usuário |
| Regra de negócio | `calculator.py` | Projeção financeira + dados do gráfico |
| Configuração | `constants.py` | Mapeamento de investimentos e cores |

## Validação

`src/tests/testar_integracao.py` testa o fluxo completo em dois cenários:

- **Online**: busca do Supabase real → salva cache → calcula (pula se a lib não estiver instalada)
- **Offline**: usa cache simulado → salva/carrega carteira → calcula → simula adicionar/remover investimentos e mudar prazo

Rodar: `python src/tests/testar_integracao.py`

---

*Última atualização: Semana 4 — 28/04/2026*
