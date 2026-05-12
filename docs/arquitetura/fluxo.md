# Fluxo de Integração

## Caminho dos dados no sistema

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
            frames.desenhar_grafico()
```

## Detalhamento

### 1. Obter taxas

Na inicialização, o sistema tenta buscar as taxas do Supabase via `buscar_indicadores()`. Se conseguir, salva no cache local com `salvar_cache_taxas()`. Se falhar (sem internet, erro de API), carrega do cache com `carregar_cache_taxas()`.

### 2. Carregar carteira

A carteira do usuário é carregada do JSON local com `carregar_carteira()`. Retorna lista vazia se for a primeira vez.

### 3. Calcular projeções

`preparar_dados_grafico()` recebe a carteira e as taxas, aplica juros compostos ano a ano com taxas variáveis, e retorna uma lista com tudo que o gráfico precisa.

`calcular_totais()` agrega os valores da carteira inteira.

### 4. Interações do usuário

| Ação | O que acontece |
|---|---|
| Adicionar investimento | Insere na carteira → salva JSON → recalcula → redesenha |
| Remover investimento | Remove da carteira → salva JSON → recalcula → redesenha |
| Mudar prazo | Recalcula com novo prazo → redesenha |

## Módulos envolvidos

| Camada | Módulo | Papel |
|---|---|---|
| Persistência remota | `supabase_client.py` | Busca taxas do Supabase |
| Persistência local | `json_repository.py` | Cache de taxas + carteira |
| Regra de negócio | `calculator.py` | Projeção financeira |
| Configuração | `constants.py` | Investimentos e cores |
| Interface | `frames.py` | Gráfico e interação |

## Validação

`src/tests/testar_integracao.py` testa o fluxo completo:

- **Online**: busca do Supabase → salva cache → calcula
- **Offline**: cache simulado → salva/carrega carteira → calcula → adicionar/remover

Rodar a partir de `src/`: `python tests/testar_integracao.py`

---

*Última atualização: Semana 5 — 05/05/2026*
