# Simulador de Investimentos

Trabalho da disciplina de Projeto Temático I - UCS

**Grupo:** Grégori Barizon Muterle, Murilo Santori Boff, Pedro Henrique Scopel da Silva

---

## Sobre o projeto

Um simulador de investimentos desktop feito em Python. A ideia é simples: você coloca quanto quer investir, escolhe o tipo de investimento e o prazo em anos, e o programa mostra um gráfico de rosca com a projeção de rendimento.

O diferencial é que as taxas não são fixas no código. Elas estão sempre atualizadas, a partir da API do Banco Central do Brasil, onde são carregadas e tratadas em um banco no Supabase. Assim, o simulador sempre usa os dados reais do mercado (Selic, CDI, IPCA).

## Funcionalidades

- Adicionar e remover investimentos da carteira
- Simular vários investimentos ao mesmo tempo, lado a lado
- Escolher o prazo de investimento
- Gráfico de rosca: parte interna = valor investido, parte externa = rendimento projetado
- Taxas reais puxadas do Banco Central via Supabase
- Carteira salva localmente em JSON

## Tecnologias

- **Python** com Tkinter para a interface
- **Pillow** para renderizar o gráfico com antialiasing
- **Supabase** banco PostgreSQL para armazenar os indicadores do BCB
- **requests** para consumo das APIs

## Como rodar

Clone o repositório e instale as dependências:

```bash
git clone https://github.com/murilosantoriboff/invest-sim-desktop.git
cd invest-sim-desktop
pip install -r requirements.txt
python src/main.py
```

## Estrutura do projeto

```
invest-sim-desktop/
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

| Semana |         Foco          |   Situação   |
|--------|-----------------------|--------------|
|   01   | Setup e arquitetura   | Concluído    |
|   02   | Persistência de dados | Em andamento |
|   03   | Regra de negócio      | Aguardando   |
|   04   | Integração inicial    | Aguardando   |
|   05   | Interface             | Aguardando   |
|   06   | Integração completa   | Aguardando   |
|   07   | Testes funcionais     | Aguardando   |
|   08   | Testes não funcionais | Aguardando   |
|   09   | Refinamento final     | Aguardando   |

---

*Documentação completa em `/docs/`*
