# O que nossos testes fazem (Especificação de Testes)

Este documento foi feito para explicar, de forma simples e direta, o que cada um dos nossos scripts de teste valida automaticamente. Cobrimos desde a matemática dos cálculos de investimento até como o sistema se comporta salvando arquivos locais ou buscando dados na nuvem.

---

## 1. Testes do Motor de Cálculo (`testar_calculator.py`)

Aqui nós testamos as funções matemáticas e as regras de negócio do arquivo `core/calculator.py`. O objetivo é garantir que as contas de projeção financeira estão certas e não vão quebrar na frente do usuário.

### 1.1 Projeções de Valor Futuro
* **Cenário 1: Juros Compostos com Taxa Fixa**
  * **O que testa:** Se um dinheiro investido com uma taxa fixa e bonita rende o esperado ao longo de 5 anos usando juros compostos.
  * **O que valida:** Se você colocar R$ 10.000,00 a uma taxa firme de 14,75% ao ano, o resultado no final precisa ser de aproximadamente R$ 19.895,89.
* **Cenário 2: E se a Taxa for Zero?**
  * **O que testa:** Se o motor de cálculo é estável caso o investimento não renda nada.
  * **O que valida:** O valor futuro não pode mudar (R$ 1.000,00 com 0% de taxa por 1 ano tem que continuar sendo exatamente R$ 1.000,00).
* **Cenário 3: Taxas que Mudam todo Ano (Variáveis)**
  * **O que testa:** Como o sistema lida com o mundo real, onde a taxa de juros muda ano após ano.
  * **O que valida:** O rendimento passo a passo de um aporte de R$ 10.000,00 mudando as taxas a cada ano (Ano 1: 14,75%, Ano 2: 12,50%, Ano 3: 10,00%).
* **Cenário 4: Falta de Taxas no Futuro (*Flat fallback*)**
  * **O que testa:** O que acontece quando o usuário pede uma simulação longa (ex: 5 anos), mas só temos taxas cadastradas para os primeiros 3 anos.
  * **O que valida:** O sistema aplica as taxas que conhece nos primeiros anos e repete a última taxa disponível para o resto do tempo, sem travar a conta.

### 1.2 Métricas e Contas Auxiliares
* **Cenário 5: Conta de Ganho Real (Em Reais)**
  * **O que testa:** Se o lucro em dinheiro é calculado certinho (Valor Futuro menos o Valor Investido).
* **Cenário 6: Conta de Ganho em Percentual**
  * **O que testa:** Se a porcentagem de lucro sobre o valor inicial está correta.
  * **O que valida:** Um teste de segurança para garantir que se o valor investido for R$ 0,00, o sistema não tente dividir por zero e quebre (deve retornar 0,0% de ganho).

### 1.3 Preparando Dados para o Gráfico
* **Cenário 7: Organização das Taxas**
  * **O que testa:** Se a função `_organizar_taxas` consegue pegar aquela lista bagunçada que vem do banco e arrumar tudo num mapa organizado por tipo de investimento e ano.
* **Cenário 8: Ignorar Investimentos Desconhecidos**
  * **O que testa:** Se o usuário tiver um ativo estranho na carteira (que não tem taxa cadastrada), o sistema não pode bugar.
  * **O que valida:** O ativo desconhecido é deixado de lado na hora de montar o gráfico para evitar que a tela quebre ou exiba dados errados.

---

## 2. Testes de Armazenamento Local (`testar_persistencia.py`)

Aqui nós testamos o `json_repository.py`. Queremos ter certeza de que o sistema consegue ler e salvar arquivos locais sem perder dados e que sabe se virar se algo der errado.

### 2.1 Salvando e Carregando a Carteira (`carteira.json`)
* **Cenário 1: Começando do Zero**
  * **O que testa:** Se o arquivo ainda não existir (ou se a carteira for limpa), o sistema precisa devolver uma lista vazia `[]` em vez de estourar um erro na tela.
* **Cenário 2: Salvar e Ler sem Perder Nada**
  * **O que testa:** Criamos uma carteira com 3 investimentos (SELIC, CDI e POUPANÇA), salvamos no arquivo e depois lemos de volta para ver se os valores e nomes continuam iguaizinhos.
* **Cenário 3: Colocar e Tirar Itens da Carteira**
  * **O que testa:** Simula o usuário mexendo na carteira — adicionando um novo ativo (IPCA) e depois removendo outro (CDI) — checando se o arquivo atualiza certinho a cada passo.
* **Cenário 4: O que fazer se o Arquivo Corromper?**
  * **O que testa:** Um teste de fogo. Injetamos um texto quebrado e inválido (`{json invalido!!!`) direto no arquivo para fingir que ele corrompeu.
  * **O que valida:** O sistema precisa perceber o erro, ignorar o arquivo quebrado e devolver uma lista vazia por segurança, sem travar o aplicativo.

### 2.2 Cache de Taxas Local (`cache_taxas.json`)
* **Cenário 5: Verificando se o Cache Existe**
  * **O que testa:** Garante que o sistema sabe quando não tem nada salvo no cache local (`cache_taxas_existe() == False`).
* **Cenário 6: Alimentando o Cache**
  * **O que testa:** Salva uma lista de taxas de teste no arquivo e checa se o sistema passa a reconhecer que o cache existe e mostra a data/hora em que foi atualizado.

---

## 3. Testes de Integração de Ponta a Ponta (`testar_integracao.py`)

Estes testes juntam todas as peças do quebra-cabeça. Eles fazem o fluxo completo: buscam os dados (na internet ou no cache), salvam no arquivo local, mandam pro motor de cálculo e geram os resultados finais.

[Supabase / Cache] ──> [JSON Repository] ──> [Core Calculator] ──> [Resultados Finais]


### 3.1 Fluxo Online (Conectado com o Supabase)
* **Cenário 1: Conversando com o Banco de Dados**
  * **O que testa:** Vê se o nosso código consegue se conectar de verdade com o Supabase na internet e trazer a lista de taxas atualizadas.
* **Cenário 2: Atualização Silenciosa do Cache**
  * **O que testa:** Garante que assim que os dados novos chegam da internet, eles são salvos na hora no arquivo de cache local.
* **Cenário 3: Olhar Clínico sobre o Rendimento**
  * **O que testa:** Passa esses dados reais por uma simulação de 5 anos para ver se a lógica de mercado faz sentido (em renda fixa, o valor final precisa ser maior que o dinheiro que você colocou no início).

### 3.2 Fluxo Offline (Usando apenas o Cache Local)
* **Cenário 4: Simulação Completa sem Internet**
  * **O que testa:** Alimenta o sistema com taxas simuladas de 2025 a 2027 para vários investimentos (SELIC, CDI, IPCA, POUPANÇA) com o computador offline.
  * **O que valida:** 
    * Checa se a soma total investida bate certinho com o que foi digitado (R$ 18.000,00).
    * Testa se, ao aumentar o tempo da simulação de 5 para 10 anos, o motor de cálculo aumenta o lucro de forma exponencial por causa dos juros compostos.

---

## 4. Tabela Resumo dos Testes

Para entender rápido o foco de cada arquivo de teste:

| Arquivo de Teste | O que ele foca | Estilo do Teste | O que ele garante |
| :--- | :--- | :--- | :--- |
| `testar_calculator.py` | Lógica das contas e funções financeiras | Direto na função (Unitário) | Contas de juros perfeitas, proteção contra valores zerados e formatação de cores para o gráfico. |
| `testar_persistencia.py` | Criação, leitura e exclusão de arquivos | Mexendo em arquivos (I/O) | Gravação correta no HD, pastas criadas no lugar certo e segurança contra arquivos corrompidos. |
| `testar_integracao.py` | O caminho do dado do início ao fim | Fluxo completo (Integração) | Conexão com o banco na nuvem, atualização automática de cache e coerência dos lucros a longo prazo. |

---

## 5. Como rodar os testes?

Para rodar essa suíte de testes e ver se está tudo funcionando perfeitamente, abra o terminal na raiz da pasta `src/` e execute:

```bash
# Para testar a matemática e regras do motor de cálculo
python tests/testar_calculator.py

# Para testar o salvamento de arquivos e cache local
python tests/testar_persistencia.py

# Para testar o fluxo completo juntando tudo (Online e Offline)
python tests/testar_integracao.py