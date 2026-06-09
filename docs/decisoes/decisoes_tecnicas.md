# Decisões Técnicas

Esse documento junta as principais decisões que tomamos durante o projeto e o motivo de cada uma. A ideia é que quem pegar o repositório entenda não só como o sistema funciona, mas por que ele ficou desse jeito.

## Python com Tkinter

Como o grupo já tinha experiência com Python, se tornou uma escolha simples. Pra interface usamos o Tkinter porque ele já vem junto com o Python, sem precisar instalar nada além do pip install -r requirements.txt. Como o simulador é um programa de uma janela só, ele dá conta sem complicação. Uma versão web precisaria de servidor, deploy e mais tecnologias, o que não cabia no prazo da disciplina.

## Supabase entre o app e o Banco Central

As taxas vêm da API de expectativas de mercado do Banco Central (Focus), mas o app não consulta essa API diretamente. Criamos uma Edge Function no Supabase que roda uma vez por dia, busca os dados do BCB, trata e grava num banco PostgreSQL. O simulador só lê uma view pronta chamada vw_indicadores_investimento.

Fizemos assim porque a API do BCB devolve milhares de registros brutos que precisam de filtragem e limpeza de duplicados, e algumas taxas são derivadas: o CDI é calculado a partir da Selic e a poupança tem regra própria (70% da Selic quando ela passa de 8,5%). Se cada abertura do app tivesse que fazer esse tratamento, ia ficar lento e com regra de negócio espalhada no lugar errado. Com a view, o app faz uma consulta única e recebe tudo pronto.

## Arquivos JSON locais

Tanto a carteira do usuário quanto a última cópia das taxas ficam em arquivos JSON na pasta data. Os dados são pequenos, o formato dá pra ler no bloco de notas (o que ajudou bastante na hora de debugar) e o módulo json já vem no Python. Um banco local como o SQLite seria só mais uma coisa pra gerenciar sem necessidade nesse volume de dados.

Esse cache local também é o que permite usar o simulador sem internet: se a consulta ao Supabase falhar, o app carrega as taxas da última execução. E se algum arquivo estiver corrompido, ele ignora e segue com a carteira vazia em vez de travar.

## Cálculo do dólar e taxa mostrada no card

No caso do câmbio, a mediana que vem do Focus não é uma taxa percentual e sim a cotação esperada do dólar em reais (por exemplo 5,30). Aplicar juros compostos em cima disso daria resultado sem sentido, então o dólar tem uma função de projeção separada, que multiplica o valor investido pela razão entre a cotação final e a inicial.

Outra decisão de cálculo foi a taxa que aparece no card de cada investimento. Como as taxas mudam de ano pra ano, mostrar só a do primeiro ano enganava o usuário. O card mostra a taxa fixa que produziria o mesmo valor futuro no prazo escolhido, e assim dá pra comparar investimentos diferentes na mesma unidade.

## Testes sem framework

Os testes são scripts simples que imprimem OK ou FALHOU em cada cenário e um resumo no final. Rodam com Python puro, sem instalar nada, e a saída é simples e direta. O pytest faria o mesmo papel, mas pro tamanho do projeto ia ser mais configuração do que benefício.

## PDF com a biblioteca fpdf2

A exportação gera um PDF com cabeçalho, tabela dos investimentos e totais. Usamos a fpdf2 por ser leve e simples de usar. Desenhar o gráfico de rosca dentro do PDF daria bem mais trabalho por pouco ganho, já que a tabela tem todos os números da simulação.

*Última atualização: 09/06/2026*
