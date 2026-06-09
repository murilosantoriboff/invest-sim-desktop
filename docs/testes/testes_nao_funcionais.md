# Testes Não Funcionais

Enquanto os testes funcionais validam se as contas e o fluxo estão certos, aqui a gente olha pra qualidade do sistema: desempenho, comportamento quando algo dá errado e usabilidade.

## Desempenho

As medições ficam no script testar_desempenho.py, dentro de src/testes. Ele cronometra as operações principais e confere se cada uma fica dentro de um limite folgado. Os números abaixo foram medidos num notebook com Windows 11 e variam um pouco a cada execução.

Uma simulação completa com 6 investimentos projetados a 30 anos leva menos de 0,1 milissegundo (o limite do teste é 10 ms). Isso importa porque cada clique nos botões de prazo refaz a simulação inteira e redesenha o gráfico, então a interface responde na hora, sem travada. Também testamos uma carteira exagerada de 600 itens, bem acima do uso real, e o cálculo ficou em torno de 3 ms, com limite de 500 ms. A geração do PDF leva uns 6 ms e a abertura do app até a primeira tela, rodando offline com o cache local, fica entre 0,2 e 0,5 segundo. Com internet a abertura inclui a busca das taxas no Supabase, então esse tempo depende da conexão.

## Erros e robustez

Se o arquivo carteira.json estiver corrompido, o app ignora e abre com a carteira vazia em vez de travar. Isso é validado automaticamente no cenário 4 do testar_persistencia.

Sem internet ou com o Supabase fora do ar, o app usa o cache local de taxas salvo na última execução, o que também é coberto pelo testar_integracao. Se não tiver nem internet nem cache, ele abre mesmo assim, só que a projeção fica igual ao valor investido até existirem taxas, situação coberta pelo cenário "Sem taxas = valor original" do testar_calculator.

No campo de valor a validação nem deixa digitar letras, e valor zero ou vazio faz o campo piscar vermelho sem adicionar nada. Se der erro na hora de gerar o PDF (por exemplo, o arquivo aberto em outro programa), aparece uma janela de erro em vez do app fechar. E se acontecer um erro inesperado na inicialização, o traceback é gravado no arquivo erro_simulador.txt pra facilitar a investigação. Esses três casos foram verificados manualmente.

## Usabilidade

Verificações manuais feitas na interface:

- passando o mouse em cada tipo de investimento (e nos cards da legenda) aparece uma explicação curta daquele investimento, e o botão ? do cabeçalho abre o glossário completo
- Enter no campo de valor adiciona o investimento e Escape fecha o glossário
- valor inválido pisca vermelho, botões mudam de cor no hover, ganho aparece em verde e perda em vermelho, e cada investimento tem uma cor fixa no gráfico, nos chips e nos cards
- o cabeçalho mostra a data da última atualização das taxas, então o usuário sabe se está vendo dado de hoje ou do cache
- a janela abre centralizada em 1280x720 e pode ser maximizada

## Como rodar

A partir da pasta src:

python testes/testar_desempenho.py

O script abre e fecha uma janela rapidamente, que é a medição do tempo de abertura do app.

*Última atualização: 09/06/2026*
