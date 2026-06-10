# Testes Funcionais e de Integração

Enquanto o documento de testes não funcionais olha pra qualidade (desempenho, robustez, usabilidade), aqui o foco é se o sistema faz a coisa certa: as contas das projeções, a gravação dos arquivos e o caminho completo do dado, do Supabase até o gráfico. São três scripts em src/testes, e todos imprimem OK ou FALHOU em cada verificação, com um resumo no final.

## Cálculos (testar_calculator.py)

São 30 verificações sobre as funções do calculator.py, rodando isoladas, sem arquivo nem banco envolvido.

O bloco de projeção de valor confere os juros compostos. R$ 10.000 a 14,75% fixos por 5 anos têm que chegar perto de R$ 19.895,89, taxa zero não pode alterar o valor, e com taxas que mudam de ano pra ano (14,75%, depois 12,50%, depois 10%) o teste acompanha o acumulado em 1, 2 e 3 anos. Tem ainda o caso do prazo maior que as taxas cadastradas: pedindo 5 anos com só 3 taxas na base, a última taxa vale pros anos restantes.

O dólar tem um bloco próprio porque a conta é outra: vale a razão entre as cotações, não juros compostos. R$ 10.000 com a cotação saindo de 5,10 pra 5,17 em um ano viram R$ 10.137,25, prazo além do último ano disponível usa a última cotação conhecida, e cotação inicial zerada devolve o valor original, justamente pra não estourar uma divisão por zero.

Nos auxiliares, o ganho é a diferença simples entre o futuro e o investido, o percentual é sobre o valor inicial e um investimento de R$ 0 devolve 0% em vez de quebrar. Também é testada a organização das taxas que chegam do Supabase (agrupar a lista por código e por ano, descartando registros inválidos) e o filtro de ativo desconhecido: um código que não existe na configuração, tipo BITCOIN, fica de fora do gráfico sem derrubar nada.

Fechando, a preparação dos dados do gráfico: uma carteira com SELIC e Poupança sai com os dois itens, cada um com cor, valor futuro maior que o investido e totais corretos. E o teste da taxa do card garante que a taxa exibida é a anualizada equivalente, não a do primeiro ano: com a Selic caindo de 13,25% pra 10,50% em três anos, o card tem que mostrar perto de 11,75% ao ano.

## Persistência (testar_persistencia.py)

Valida o armazenamento.py usando uma pasta temporária, pra não encostar nos dados reais do usuário.

Na carteira, começa do zero: sem arquivo, o carregamento devolve lista vazia. Depois salva três ativos e confere que o arquivo foi criado e que tudo volta igual, na mesma ordem e com os mesmos tipos. Na sequência simula o uso normal, adicionando um IPCA e removendo o CDI, conferindo a consistência a cada passo. O caso mais importante é o do arquivo corrompido: o teste escreve um JSON inválido de propósito e a leitura precisa devolver lista vazia em vez de travar o app.

No cache de taxas a lógica é parecida. Antes de existir cache, a data de atualização vem como None e a lista vem vazia; depois de salvar cinco registros de exemplo, todos voltam completos e a data passa a existir.

## Integração (testar_integracao.py)

Esse junta persistência e cálculo no fluxo de ponta a ponta, em dois modos.

No modo online o teste conecta de verdade no Supabase, confere que vieram dados, salva o cache e roda uma simulação de 5 anos com as taxas reais, verificando que em renda fixa o valor final supera o investido. Sem internet ou sem a biblioteca instalada, esse bloco é pulado com aviso em vez de falhar.

No modo offline as taxas são simuladas (2025 a 2027 pra SELIC, CDI, IPCA e Poupança). O teste grava uma carteira de R$ 18.000 em três ativos, confere os totais, remove um item, adiciona um IPCA e por fim estica o prazo de 5 pra 10 anos, verificando que o ganho cresce junto com o tempo.

## Como rodar

A partir da pasta src:

python testes/testar_calculator.py

python testes/testar_persistencia.py

python testes/testar_integracao.py

*Última atualização: 19/05/2026*
