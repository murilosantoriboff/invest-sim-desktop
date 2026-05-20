# Especificação de Testes Funcionais e de Integração

Este documento foi feito para explicar, de forma simples e direta, o que cada um dos nossos scripts de teste valida automaticamente. Cobrimos desde a matemática dos cálculos de investimento até como o sistema se comporta salvando arquivos locais ou buscando dados na nuvem.

---

## 1. Testes do Motor de Cálculo (`testar_calculator.py`)

Estes testes validam isoladamente as funções matemáticas e de mapeamento contidas no motor de cálculo (`core/calculator`), garantindo que as projeções financeiras sigam as regras de negocio.

### 1.1 Projeção de Valor Futuro
* **Cenário 1: Juros Compostos Fixos**
  * **Objetivo:** Garantir que um aporte inicial sob uma taxa fixa e constante ao longo de 5 anos capitalize corretamente via juros compostos.
  * **Validação:** Um valor de R$ 10.000,00 a uma taxa estável de 14,75% ao ano deve render aproximadamente R$ 19.895,89.
* **Cenário 2: Taxa Zero**
  * **Objetivo:** Verificar a estabilidade do motor de cálculo se a taxa de juros for nula.
  * **Validação:** O valor futuro deve ser exatamente igual ao valor investido original (R$ 1.000,00 com taxa de 0% por 1 ano resulta em R$ 1.000,00).
* **Cenário 3: Taxas Variáveis**
  * **Objetivo:** Como o sistema lida com o mundo real, onde a taxa de juros muda ano após ano.
  * **Validação:** Avaliar progressivamente o rendimento de um aporte de R$ 10.000,00 sob a curva de juros variável (Ano 1: 14,75%, Ano 2: 12,50%, Ano 3: 10,00%).
* **Cenário 4: EFalta de Taxas no Futuro**
  * **Objetivo:** Testar o comportamento do sistema quando o período solicitado de projeção (ex: 5 anos) é maior que a quantidade de anos com taxas cadastradas na base (ex: 3 anos).
  * **Validação:** O sistema deve aplicar as taxas conhecidas para os primeiros anos e replicar a última taxa disponível (*flat*) para os anos restantes.

### 1.2 Funções Auxiliares e Métricas
* **Cenário 5: Cálculo de Ganho**
  * **Objetivo:** Garantir que o rendimento absoluto seja a diferença simples entre o valor futuro e o valor investido.
* **Cenário 6: Cálculo de Ganho em Percentual**
  * **Objetivo:** Validar o cálculo do retorno percentual sobre o capital inicial.
  * **Validação:** Proteção contra divisão por zero se o valor investido for igual a R$ 0,00 (deve retornar 0,0% de ganho).

### 1.3 Preparação de Dados para Interface Visual
* **Cenário 7: Estruturação dos Indicadores**
  * **Objetivo:** Validar se a função `_organizar_taxas` agrupa corretamente a lista de dicionários em um mapa indexado pelo código do investimento e ano.
* **Cenário 8: Filtro de Ativos Desconhecidos**
  * **Objetivo:** Garantir que ativos na carteira que não possuam correspondência de taxas ou indexadores válidos sejam ignorados no gráfico para evitar quebras visuais.

---

## 2. Testes de Persistência Local (`testar_persistencia.py`)

Valida o comportamento do componente `json_repository.py` na leitura, escrita e resiliência de falhas dos arquivos locais de configuração e dados da carteira.

### 2.1 Salvando e Carregando a Carteira (`carteira.json`)
* **Cenário 1: Começando do Zero**
  * **Objetivo:** Se o arquivo ainda não existir (ou se a carteira for limpa), o sistema precisa devolver uma lista vazia `[]`;
* **Cenário 2: Leitura e Escrita sem Perda**
  * **Objetivo:** Salvar uma carteira com 3 ativos (SELIC, CDI, POUPANÇA), confirmar a criação física do arquivo e validar se a ordem e os tipos de dados (float/string) foram preservados no carregamento.
* **Cenário 3: Colocar e Tirar Itens da Carteira**
  * **Objetivo:** Simula o usuário mexendo na carteira — adicionando um novo ativo (IPCA) e depois removendo outro (CDI) — garantindo a consistência do arquivo;
* **Cenário 4: Resiliência a Arquivos Corrompidos**
  * **Objetivo:** Simular uma falha grave de infraestrutura injetando uma string JSON inválida (`{json invalido!!!`) diretamente no arquivo.
  * **Validação:** O sistema precisa perceber o erro, ignorar o arquivo quebrado e devolver uma lista vazia por segurança, sem travar o aplicativo.

### 2.2 Cache de Taxas Local (`cache_taxas.json`)
* **Cenário 5: Verificando se o Cache Existe**
  * **Objetivo:** Garante que o sistema sabe quando não tem nada salvo no cache local (`cache_taxas_existe() == False`).
* **Cenário 6: Alimentando o Cache**
  * **Validação:** Salva uma lista de taxas de teste no arquivo e checa se o sistema passa a reconhecer que o cache existe e mostra a data/hora em que foi atualizado.

---

## 3. Testes de Integração de Ponta a Ponta (`testar_integracao.py`)

Estes testes juntam todas as peças do quebra-cabeça. Eles fazem o fluxo completo: buscam os dados (do supabase ou no cache), salvam no arquivo local, mandam pro motor de cálculo e geram os resultados finais.

[Supabase / Cache] ──> [JSON Repository] ──> [Core Calculator] ──> [Resultados Finais]


### 3.1 Fluxo Online (Conectado com o Supabase)
* **Cenário 1: Conversando com o Banco de Dados**
  * **Objetivo:** Testar se a biblioteca cliente consegue se conectar com o cluster do Supabase, efetuar a autenticação/busca e retornar registros válidos das taxas.
* **Cenário 2: Atualização Automática de Cache**
  * **Objetivo:** Garantir que os dados novos trazidos da API online sejam imediatamente salvos e reflitam de forma idêntica no cache offline local.
* **Cenário 3: Validação Logística do Rendimento**
  * **Objetivo:** Passa esses dados reais por uma simulação de 5 anos para ver se a lógica de mercado faz sentido (em renda fixa, o valor final precisa ser maior que o dinheiro que você colocou no início).

### 3.2 Fluxo Offline (Usando apenas o Cache Local)
* **Cenário 4: Simulação Completa sem Internet**
  * **Objetivo:** Alimenta o sistema com taxas simuladas de 2025 a 2027 para vários investimentos (SELIC, CDI, IPCA, POUPANÇA) com o computador offline.
  * **validação:** 
    * Validar se o total somado investido bate precisamente com a entrada (R$ 18.000,00).
    * Testar o incremento dinâmico de prazos de projeção (passar de 5 para 10 anos) e auditar se a regra de negócio calcula corretamente o ganho exponencial proporcional ao aumento do tempo.

---

## 4. Tabela Resumo dos Testes

Para entender rápido o foco de cada arquivo de teste:

| Arquivo de Teste | O que ele foca | Estilo do Teste | O que ele garante |
| :--- | :--- | :--- | :--- |
| `testar_calculator.py` | Lógica das contas e funções financeiras | Direto na função (Unitário) | Calculos de juros, proteção contra valores zerados e formatação de cores para o gráfico. |
| `testar_persistencia.py` | Criação, leitura e exclusão de arquivos | Mexendo em arquivos (I/O) | Gravação correta no HD, pastas criadas no lugar certo e segurança contra arquivos corrompidos. |
| `testar_integracao.py` | O caminho do dado do início ao fim | Fluxo completo (Integração) | Conexão com o banco na nuvem, atualização automática de cache e coerência dos lucros a longo prazo. |

---

## 5. Instrucoes para

Para rodar a suíte completa de validações funcionais, execute os comandos a partir da raiz da pasta `src/`:

```bash
# Para testar a matemática e regras do motor de cálculo
python tests/testar_calculator.py

# Para testar o salvamento de arquivos e cache local
python tests/testar_persistencia.py

# Para testar o fluxo completo juntando tudo (Online e Offline)
python tests/testar_integracao.py