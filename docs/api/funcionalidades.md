# Regra de Negócio

A regra de negócio fica na pasta src/core, em dois módulos: calculator.py, com os cálculos financeiros e a preparação dos dados pro gráfico, e constants.py, com cores, prazos e o mapeamento dos investimentos. Ambos podem ser testados sem abrir a interface.

## Projeção de renda fixa
A função projetar_valor calcula o valor futuro aplicando juros compostos ano a ano, com uma taxa diferente por ano. É usada pra SELIC, CDI, IPCA, Poupança e IGP-M. As taxas vêm da view do Supabase separadas por ano de referência, e quando o prazo pedido passa dos anos disponíveis a última taxa conhecida se repete. Por exemplo, R$ 10.000 com taxas de 14,75% em 2026, 12,50% em 2027 e 10% em 2028, projetados por 5 anos, viram R$ 17.182,38 (2029 e 2030 usam os 10%).

## Projeção do dólar

O câmbio é o único que não usa juros compostos, porque a mediana que o Focus (API do BCB) publica pra ele é a cotação esperada em reais por dólar (5,30, por exemplo), e não uma taxa percentual. A função projetar_cotacao multiplica o valor investido pela razão entre a cotação final e a inicial: R$ 10.000 com a cotação saindo de 5,10 pra 5,17 em um ano viram R$ 10.137,25. Se o prazo passa do último ano com cotação, vale a última conhecida, e se a cotação inicial for inválida a função devolve o valor original.

## Montagem dos dados do gráfico

A preparar_dados_grafico junta a carteira do usuário com as taxas e devolve, pra cada item, o valor investido, o valor futuro, o ganho, o percentual, a taxa de exibição e a cor. Internamente ela escolhe entre projetar_valor e projetar_cotacao conforme o código do investimento, e ignora itens sem taxa cadastrada pra não quebrar o gráfico.

A taxa que vai pro card é a anualizada equivalente (média geométrica), ou seja, a taxa fixa que produziria o mesmo valor futuro no prazo escolhido. Assim todos os cards ficam na mesma unidade de % ao ano, inclusive o dólar, e dá pra comparar investimentos diferentes.

A calcular_totais soma o investido, o futuro e o ganho da carteira inteira, que são os números que aparecem no centro do gráfico.

## Constantes

O dicionário INVESTIMENTOS em constants.py mapeia cada código pro nome de exibição e pra cor usada no gráfico. Os códigos são os mesmos da view vw_indicadores_investimento: SELIC (Tesouro Selic), CDI (CDB 100% CDI), IPCA (Tesouro IPCA+), POUPANCA (Poupança), IGPM (IGP-M) e CAMBIO (Dólar). O mesmo arquivo guarda os limites de prazo, de 1 a 30 anos, e as cores da interface.

## Validação

O testar_calculator.py cobre essas funções com 30 verificações: projeção com taxa fixa e variável, projeção cambial, taxa anualizada equivalente, auxiliares de ganho e a organização das taxas vindas do Supabase. Roda a partir da pasta src com python testes/testar_calculator.py.

*Última atualização: 19/05/2026*
