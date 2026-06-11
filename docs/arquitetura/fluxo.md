# Fluxo de Integração

## Caminho dos dados no sistema

Tudo começa nas taxas. Na inicialização, o buscar_indicadores do supabase_client.py consulta a view no Supabase. Dando certo, o resultado é gravado no cache local pelo salvar_cache_taxas; dando errado (sem internet, por exemplo), o carregar_cache_taxas devolve a última cópia salva. Junto disso, o carregar_carteira lê do JSON os investimentos que o usuário já tinha, ou devolve uma lista vazia na primeira execução.

Com taxas e carteira em mãos, o preparar_dados_grafico do calculator.py aplica os juros compostos ano a ano e devolve a lista pronta pro desenho, e o calcular_totais agrega os valores da carteira inteira. A última etapa é da interface, que desenha o gráfico de rosca e os cards a partir dessa lista.
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
            interface.desenhar_grafico()
```

## As ações do usuário

Adicionar, editar e remover investimento seguem o mesmo circuito: a mudança entra na carteira, a carteira é salva no JSON, o calculator recalcula e a interface redesenha. Mudar o prazo é mais simples, só recalcula e redesenha, sem salvar nada, porque o prazo não faz parte da carteira.

## Quem faz o quê

O supabase_client.py é a persistência remota e só busca taxas. O armazenamento.py é a persistência local, do cache e da carteira. O calculator.py faz a projeção financeira sem saber de onde os dados vieram. O constants.py guarda o mapeamento de investimentos e as cores, e o interface.py desenha tudo e captura as interações.

## Validação

O testar_integracao.py percorre esse fluxo de ponta a ponta nos dois modos: online, buscando do Supabase de verdade, salvando o cache e calculando em cima dos dados reais, e offline, com taxas simuladas, exercitando salvar e carregar a carteira, mexer nos itens e mudar o prazo. Roda a partir da pasta src com python testes/testar_integracao.py.

---

*Última atualização: 10/06/2026*
