# Visão Geral da Arquitetura

## Descrição

O sistema é dividido em três camadas bem separadas: apresentação, regra de negócio e persistência. Essa separação foi uma decisão deliberada desde o início — facilita manutenção, testes e a divisão de tarefas entre os membros do grupo.

A aplicação roda localmente como um programa desktop Python/Tkinter. Os dados de mercado (taxas Selic, CDI, IPCA) vêm do Supabase, que por sua vez é alimentado diariamente pela API pública do Banco Central do Brasil. A carteira do usuário fica salva num arquivo JSON local.

---

## Camadas do sistema

### Camada de Apresentação — `src/ui/`

Responsável por tudo que o usuário vê e com o que interage.

- `frames.py` — monta as telas do Tkinter, gerencia os eventos (cliques, digitação, mudança de prazo)
- `canvas_render.py` — desenha o gráfico de rosca usando Pillow com antialiasing; também controla a animação de entrada
- `styles.py` — define o tema visual: cores, fontes Poppins, estilos dos botões ttk

Essa camada não faz cálculo nenhum e não acessa banco de dados. Ela só chama a camada de negócio e exibe o resultado.

### Camada de Regra de Negócio — `src/core/`

O coração do sistema. Aqui ficam os cálculos e as regras.

- `calculator.py` — implementa a fórmula de juros compostos, calcula projeção de rendimento, gera os dados geométricos para o gráfico
- `constants.py` — constantes globais: dimensões do canvas, configurações de animação, mapeamento de nomes de investimentos

Nenhuma dependência de Tkinter ou Supabase aqui. Funções puras, fáceis de testar.

### Camada de Persistência — `src/infrastructure/`

Cuida de ler e gravar dados, seja na nuvem ou localmente.

- `database/supabase_client.py` — conecta ao Supabase e consulta a view `vw_indicadores_investimento` para obter as taxas atualizadas
- `storage/json_repository.py` — salva e carrega a carteira do usuário em `carteira.json` no diretório local

---

## Banco de dados (Supabase)

O PostgreSQL no Supabase tem duas tabelas e uma view:

`cfg_indicadores_investimento` — configuração estática: quais indicadores do BCB fazem parte do simulador, nome de exibição, como calcular as taxas derivadas.

`stg_indicadores_bcb` — dados brutos da API Focus/BCB, atualizados diariamente por uma Edge Function com pg_cron.

`vw_indicadores_investimento` — view que junta as duas tabelas e já entrega as taxas prontas para o simulador (CDI como % da Selic, Poupança como 70% da Selic quando Selic > 8.5%, etc.).

O simulador só lê dessa view. Nunca escreve nada no Supabase.

---

## Fluxo principal

```
Usuário abre o app
  └── supabase_client busca taxas na vw_indicadores_investimento
        └── [sem conexão] usa taxas do cache local (json)
  └── json_repository carrega carteira salva (se existir)

Usuário adiciona investimento
  └── frames.py captura input → valida → chama calculator.py
        └── calculator calcula projeção com taxa do Supabase
  └── canvas_render.py recebe dados e desenha o gráfico animado
  └── json_repository salva carteira atualizada

Usuário muda prazo
  └── calculator recalcula → canvas_render redesenha (sem animação de entrada)
```

---

## Relação entre componentes

```
frames.py
  ├── chama → calculator.py (para projeções)
  ├── chama → canvas_render.py (para desenhar)
  ├── chama → supabase_client.py (taxas na inicialização)
  └── chama → json_repository.py (salvar/carregar carteira)

calculator.py
  └── depende de → constants.py (configurações)

canvas_render.py
  └── depende de → constants.py (dimensões, cores)
```

---

## Diagrama de histórias de usuário

---

*Última atualização: Semana 1 — 07/04/2026*
