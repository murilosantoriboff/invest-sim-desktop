# Simulador de Investimentos

Trabalho da disciplina de Projeto Temático I — Universidade de Caxias do Sul, 2026.

**Grupo:** Grégori Barizon Muterle, Murilo Santorini Boff, Pedro Henrique Scopel da Silva

---

## O que é isso

Um simulador de investimentos desktop feito em Python. A ideia é simples: você coloca quanto quer investir, escolhe o tipo (CDB, Tesouro Direto, LCI/LCA, Poupança) e o prazo em anos — o programa mostra um gráfico de rosca animado com a projeção de rendimento.

O diferencial é que as taxas não são fixas no código. Elas vêm da API do Banco Central do Brasil, são salvas no Supabase e atualizadas automaticamente todo dia. Assim o simulador sempre usa os dados reais do mercado (Selic, CDI, IPCA).

## Funcionalidades

- Adicionar e remover investimentos da carteira
- Simular vários investimentos ao mesmo tempo, lado a lado
- Escolher prazo de 1 a 30 anos (o gráfico atualiza na hora)
- Gráfico de rosca animado: parte interna = capital, parte externa = rendimento projetado
- Taxas reais puxadas do Banco Central via Supabase
- Carteira salva localmente em JSON — reabre onde parou

## Tecnologias

- **Python 3.11+** com Tkinter para a interface
- **Pillow** para renderizar o gráfico com antialiasing
- **Supabase** (PostgreSQL) para armazenar os indicadores do BCB
- **requests** para consumo das APIs

## Como rodar

```bash
git clone https://github.com/murilosantoriboff/Projeto_Tematico_UCS.git
cd Projeto_Tematico_UCS
pip install -r requirements.txt
python src/main.py
```

Sem configuração adicional. O banco de dados já está conectado.

## Estrutura do projeto

```
Projeto_Tematico_UCS/
├── src/
│   ├── main.py                         # ponto de entrada
│   ├── core/
│   │   ├── calculator.py               # cálculos financeiros (juros compostos etc.)
│   │   └── constants.py                # configurações e constantes globais
│   ├── ui/
│   │   ├── frames.py                   # telas e interações do Tkinter
│   │   ├── canvas_render.py            # renderização do gráfico com Pillow
│   │   └── styles.py                   # tema visual (cores, fontes, estilos ttk)
│   └── infrastructure/
│       ├── database/
│       │   └── supabase_client.py      # acesso aos dados remotos
│       └── storage/
│           └── json_repository.py      # persistência local da carteira
├── docs/
│   ├── arquitetura/
│   ├── api/
│   ├── testes/
│   ├── rastreabilidade/
│   ├── decisoes/
│   └── interface/
├── assets/
│   ├── fonts/
│   └── icons/
├── .gitignore
└── requirements.txt
```

## Status

| Semana | Foco | Situação |
|--------|------|----------|
| 1 | Setup e arquitetura | Concluído |
| 2 | Persistência de dados | Em andamento |
| 3 | Regra de negócio | Aguardando |
| 4 | Integração inicial | Aguardando |
| 5 | Interface | Aguardando |
| 6 | Integração completa | Aguardando |
| 7 | Testes funcionais | Aguardando |
| 8 | Testes não funcionais | Aguardando |
| 9 | Refinamento final | Aguardando |

---

*Documentação completa em `/docs/`*
