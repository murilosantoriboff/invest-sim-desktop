# Especificação de Testes Funcionais e de Integração

Este documento descreve os cenários de testes automatizados implementados para validar o motor de cálculo, os mecanismos de persistência local e a integração com fontes de dados externas do simulador de investimentos.

---

## 1. Testes Unitários da Regra de Negócio (`testar_calculator.py`)

Estes testes validam isoladamente as funções matemáticas e de mapeamento contidas no motor de cálculo (`core/calculator`), garantindo que as projeções financeiras sigam as regras macroeconômicas estipuladas.

### 1.1 Projeção de Valor Futuro
* **Cenário 1: Juros Compostos Fixos**
  * **Objetivo:** Garantir que um aporte inicial sob uma taxa fixa e constante ao longo de 5 anos capitalize corretamente via juros compostos.
  * **Validação:** Um valor de R$ 10.000,00 a uma taxa estável de 14,75% ao ano deve render aproximadamente R$ 19.895,89.
* **Cenário 2: Taxa Zero**
  * **Objetivo:** Verificar a estabilidade do motor de cálculo se a taxa de juros for nula.
  * **Validação:** O valor futuro deve ser exatamente igual ao valor investido original (R$ 1.000,00 com taxa de 0% por 1 ano resulta em R$ 1.000,00).
* **Cenário 3: Taxas Variáveis Anualizadas**
  * **Objetivo:** Validar o comportamento da projeção quando as taxas mudam a cada ano de referência (comportamento esperado de projeções reais do mercado).
  * **Validação:** Avaliar progressivamente o rendimento de um aporte de R$ 10.000,00 sob a curva de juros variável (Ano 1: 14,75%, Ano 2: 12,50%, Ano 3: 10,00%).
* **Cenário 4: Extrapolação de Curva de Juros (*Flat fallback*)**
  * **Objetivo:** Testar o comportamento do sistema quando o período solicitado de projeção (ex: 5 anos) é maior que a quantidade de anos com taxas cadastradas na base (ex: 3 anos).
  * **Validação:** O sistema deve aplicar as taxas conhecidas para os primeiros anos e replicar a última taxa disponível (*flat*) para os anos restantes.

### 1.2 Funções Auxiliares e Métricas
* **Cenário 5: Cálculo de Ganho Nominal**
  * **Objetivo:** Garantir que o rendimento absoluto seja a diferença simples entre o valor futuro e o valor investido.
* **Cenário 6: Cálculo de Ganho Percentual**
  * **Objetivo:** Validar o cálculo do retorno percentual sobre o capital inicial.
  * **Validação:** Proteção contra divisão por zero se o valor investido for igual a R$ 0,00 (deve retornar 0,0% de ganho).

### 1.3 Preparação de Dados para Interface Visual
* **Cenário 7: Estruturação dos Indicadores**
  * **Objetivo:** Validar se a função `_organizar_taxas` agrupa corretamente uma lista plana de dicionários em um mapa indexado pelo código do investimento e ano.
* **Cenário 8: Filtro de Ativos Desconhecidos**
  * **Objetivo:** Garantir que ativos na carteira que não possuam correspondência de taxas ou indexadores válidos sejam ignorados na plotagem do gráfico para evitar quebras visuais.

---

## 2. Testes de Persistência Local (`testar_persistencia.py`)

Valida o comportamento do componente `json_repository.py` na leitura, escrita e resiliência de falhas dos arquivos locais de configuração e dados da carteira.

### 2.1 Ciclo de Vida da Carteira (`carteira.json`)
* **Cenário 1: Inicialização Limpa**
  * **Objetivo:** Garantir que, se o arquivo não existir ou for limpo, o repositório retorne uma lista vazia `[]` em vez de estourar um erro de arquivo não encontrado.
* **Cenário 2: Escrita e Leitura Efêmera**
  * **Objetivo:** Salvar uma carteira com 3 ativos (SELIC, CDI, POUPANÇA), confirmar a criação física do arquivo e validar se a ordem e os tipos de dados (float/string) foram preservados no carregamento.
* **Cenário 3: Atualização e Deleção Estágio a Estágio**
  * **Objetivo:** Testar mutações na carteira (inserção de um 4º ativo como IPCA e posterior remoção do ativo CDI), garantindo a consistência do arquivo a cada estado intermediário.
* **Cenário 4: Resiliência a Arquivos Corrompidos**
  * **Objetivo:** Simular uma falha grave de infraestrutura injetando uma string JSON inválida (`{json invalido!!!`) diretamente no arquivo.
  * **Validação:** O repositório deve interceptar a falha de parsing e retornar uma lista vazia com segurança, sem derrubar a aplicação.

### 2.2 Mecanismo de Cache de Indicadores (`cache_taxas.json`)
* **Cenário 5: Estado Inicial do Cache**
  * **Objetivo:** Confirmar que o sistema reconhece a ausência de cache (`cache_taxas_existe() == False`) e retorna data nula (`None`).
* **Cenário 6: Hidratação do Cache Local**
  * **Objetivo:** Persistir uma lista de taxas simuladas, validar que a flag de existência muda para positivo e verificar que o timestamp/data de modificação do cache passa a ficar disponível.

---

## 3. Testes de Integração Ponta a Ponta (`testar_integracao.py`)

Estes testes validam a orquestração mútua dos componentes: o fluxo de dados saindo do banco de dados (ou cache), passando pelo repositório local, sendo processado pelo motor de cálculo e gerando os consolidados de saída.

[Supabase / Cache] ──> [JSON Repository] ──> [Core Calculator] ──> [Métricas Globais]


### 3.1 Fluxo Online (Com Conectividade Supabase)
* **Cenário 1: Integração com Client API**
  * **Objetivo:** Testar se a biblioteca cliente consegue se conectar com o cluster do Supabase, efetuar a autenticação/busca e retornar registros válidos de taxas macroeconômicas.
* **Cenário 2: Atualização Automática de Cache**
  * **Objetivo:** Garantir que os dados novos trazidos da API online sejam imediatamente salvos e reflitam de forma idêntica no cache offline local.
* **Cenário 3: Validação Logística do Rendimento**
  * **Objetivo:** Processar os dados reais obtidos contra uma carteira de testes por 5 anos e verificar a consistência básica do mercado (o valor futuro projetado deve ser estritamente maior que o valor investido original para ativos de renda fixa).

### 3.2 Fluxo Offline (Baseado estritamente em Cache Local)
* **Cenário 4: Simulação de Projeção Multiativos**
  * **Objetivo:** Alimentar o sistema com dados fixados de 2025 a 2027 para múltiplos indexadores (SELIC, CDI, IPCA, POUPANÇA).
  * **Validação:** 
    * Validar se o total somado investido bate precisamente com a entrada (R$ 18.000,00).
    * Testar o incremento dinâmico de prazos de projeção (passar de 5 para 10 anos) e auditar se a regra de negócio calcula corretamente o ganho exponencial proporcional ao aumento do tempo.

---

## 4. Matriz de Cobertura de Asserções

Abaixo está o resumo volumétrico de verificações mínimas realizadas pelas suítes de teste:

| Módulo de Teste | Foco Principal | Tipo de Abordagem | Asserções Principais |
| :--- | :--- | :--- | :--- |
| `testar_calculator.py` | Regras de cálculo e mutação de dados | Unitária / Matemática | Projeções cambiais/juros, tratamento de valores zerados, fallbacks de anos ausentes e aplicação de cores hexadecimais. |
| `testar_persistencia.py` | Manipulação de arquivos I/O | Funcional / Caixa Preta | Escrita, leitura, isolamento de diretórios, deleção física e tratamento de exceção por quebra de sintaxe JSON. |
| `testar_integracao.py` | Ciclo completo de dados da aplicação | Integração de Sistemas | Conectividade externa, persistência em cascata de dados baixados da nuvem e consistência financeira do motor sob prazos longos. |

---

## 5. Instruções para Execução

Para rodar a suíte completa de validações funcionais, execute os comandos a partir da raiz da pasta `src/`:

```bash
# Executar testes unitários do motor de cálculo
python tests/testar_calculator.py

# Executar testes do repositório JSON local
python tests/testar_persistencia.py

# Executar teste de integração completa (Online/Offline)
python tests/testar_integracao.py