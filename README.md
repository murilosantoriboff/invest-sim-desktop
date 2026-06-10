# Simulador de Investimentos

Trabalho da disciplina de Projeto Temático I - UCS

Grupo: Grégori Barizon Muterle, Murilo Santori Boff, Pedro Henrique Scopel da Silva

## Sobre o projeto

Um simulador de investimentos desktop feito em Python, com interface em Tkinter. Você escolhe o tipo de investimento, coloca o valor e o prazo, e o programa mostra um gráfico de rosca com a projeção de rendimento.

As taxas são atualizadas automaticamente a partir da API do Banco Central do Brasil, armazenadas e tratadas em um banco PostgreSQL no Supabase. O simulador sempre usa os dados reais do mercado.

## Funcionalidades

- Adicionar, editar e remover investimentos da carteira
- Simular vários investimentos ao mesmo tempo
- Escolher o prazo de 1 a 30 anos
- Gráfico de rosca mostrando a proporção de cada investimento
- Cards com o detalhamento de cada aplicação (valor futuro, ganho, taxa)
- Tooltips explicativos e glossário completo dos investimentos (botão ? no cabeçalho)
- Exportação da simulação atual em PDF
- Taxas reais do BCB via Supabase (com cache offline)
- Carteira salva localmente em JSON

## Como rodar

```
git clone https://github.com/murilosantoriboff/invest-sim-desktop.git
cd invest-sim-desktop
pip install -r requirements.txt
cd src
python main.py
```

## Estrutura do projeto

O código Python fica em src, separado em core (cálculos), ui (interface) e dados (Supabase, JSON local e PDF), com os scripts de teste em testes. A pasta supabase tem a Edge Function que busca os dados do BCB e as migrations do banco. A documentação de cada etapa está em docs.

```
invest-sim-desktop/
├── src/
│   ├── main.py
│   ├── core/
│   │   ├── calculator.py
│   │   └── constants.py
│   ├── ui/
│   │   ├── interface.py
│   │   └── tooltip.py
│   ├── dados/
│   │   ├── supabase_client.py
│   │   ├── armazenamento.py
│   │   └── pdf_export.py
│   └── testes/
│       ├── testar_calculator.py
│       ├── testar_persistencia.py
│       ├── testar_integracao.py
│       └── testar_desempenho.py
├── supabase/
│   ├── functions/
│   │   └── f_indicadores_bcb/index.ts
│   └── migrations/
├── docs/
└── requirements.txt
```

## Status

| Semana | Foco | Situação |
|---|---|---|
| 01 | Setup e arquitetura | Concluído |
| 02 | Persistência de dados | Concluído |
| 03 | Regra de negócio | Concluído |
| 04 | Integração inicial | Concluído |
| 05 | Interface | Concluído |
| 06 | Integração completa | Concluído |
| 07 | Testes funcionais | Concluído |
| 08 | Testes não funcionais | Concluído |
| 09 | Refinamento final | Concluído |

---

*Documentação completa em `/docs/`*