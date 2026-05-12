# Simulador de Investimentos

Trabalho da disciplina de Projeto Temático I - UCS

**Grupo:** Grégori Barizon Muterle, Murilo Santori Boff, Pedro Henrique Scopel da Silva

---

## Sobre o projeto

Um simulador de investimentos desktop feito em Python. Você escolhe o tipo de investimento, coloca o valor e o prazo, e o programa mostra um gráfico de rosca com a projeção de rendimento.

As taxas são atualizadas automaticamente a partir da API do Banco Central do Brasil, armazenadas e tratadas em um banco PostgreSQL no Supabase. O simulador sempre usa os dados reais do mercado.

## Funcionalidades

- Adicionar e remover investimentos da carteira
- Simular vários investimentos ao mesmo tempo
- Escolher o prazo de 1 a 30 anos
- Gráfico de rosca mostrando a proporção de cada investimento
- Legenda com detalhamento de cada aplicação (valor futuro, ganho, taxa)
- Taxas reais do BCB via Supabase (com cache offline)
- Carteira salva localmente em JSON

## Tecnologias

- **Python** com Tkinter para a interface
- **Supabase** (PostgreSQL) para os indicadores do BCB

## Como rodar

```bash
git clone https://github.com/murilosantoriboff/invest-sim-desktop.git
cd invest-sim-desktop
pip install -r requirements.txt
cd src
python main.py
```

## Estrutura do projeto

```
invest-sim-desktop/
├── src/
│   ├── main.py                         # ponto de entrada
│   ├── core/
│   │   ├── calculator.py               # cálculos financeiros
│   │   └── constants.py                # configurações e constantes
│   ├── ui/
│   │   └── frames.py                   # interface Tkinter
│   ├── infrastructure/
│   │   ├── database/
│   │   │   └── supabase_client.py      # acesso ao Supabase
│   │   └── storage/
│   │       └── json_repository.py      # persistência local
│   └── tests/
│       ├── testar_persistencia.py
│       ├── testar_calculator.py
│       └── testar_integracao.py
├── supabase/
│   ├── functions/
│   │   └── f_indicadores_bcb/index.ts  # Edge Function (ETL do BCB)
│   └── migrations/
│       ├── 001_create_tables.sql
│       ├── 002_create_views.sql
│       └── 003_seed.sql
├── docs/
│   ├── arquitetura/
│   ├── api/
│   └── rastreabilidade/
├── .gitignore
└── requirements.txt
```

## Status

| Semana | Foco | Situação |
|--------|------|----------|
| 01 | Setup e arquitetura | Concluído |
| 02 | Persistência de dados | Concluído |
| 03 | Regra de negócio | Concluído |
| 04 | Integração inicial | Concluído |
| 05 | Interface | Concluído |
| 06 | Integração completa | Em andamento |
| 07 | Testes funcionais | Aguardando |
| 08 | Testes não funcionais | Aguardando |
| 09 | Refinamento final | Aguardando |

---

*Documentação completa em `/docs/`*
