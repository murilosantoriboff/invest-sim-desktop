# Visão Geral da Arquitetura

## Descrição

O simulador é uma aplicação desktop feita em Python que roda localmente. A interface, os cálculos e o arquivo de dados ficam na própria máquina do usuário. O usuário informa um valor e um tipo de investimento, e o sistema desenha um gráfico mostrando quanto esse dinheiro vai render ao longo do tempo.

Os dados de mercado (taxas Selic, CDI, IPCA) vêm do Supabase, que é alimentado diariamente pela API pública do Banco Central do Brasil. A carteira do usuário fica salva num arquivo JSON local.

---

## Camadas do sistema

### Camada de Apresentação — `src/ui/`

Responsável por tudo que o usuário vê e interage.

- `frames.py` — monta as telas do Tkinter (header, painel de input, gráfico de rosca, legenda, chips da carteira), configura os estilos visuais e gerencia os eventos
- `tooltip.py` — componente reutilizável de tooltip em hover (aparece após ~500ms ao passar o mouse) e a janela do glossário de investimentos (acessada pelo botão "?" no header)

Essa camada não faz cálculo nenhum e não acessa banco de dados. Ela só chama a camada de negócio e exibe o resultado.

### Camada de Regra de Negócio — `src/core/`

O coração do sistema. Aqui ficam os cálculos e as regras.

- `calculator.py` — implementa juros compostos com taxas variáveis por ano, prepara os dados pro gráfico, calcula totais da carteira
- `constants.py` — constantes globais: dimensões do canvas, cores, mapeamento de investimentos

Nenhuma dependência de Tkinter ou Supabase aqui. Funções puras, fáceis de testar.

### Camada de Persistência — `src/infrastructure/`

Cuida de ler e gravar dados, seja na nuvem ou localmente.

- `database/supabase_client.py` — conecta ao Supabase e consulta a view `vw_indicadores_investimento`
- `storage/json_repository.py` — salva e carrega a carteira do usuário e o cache de taxas em arquivos JSON locais
- `pdf_export.py` — gera um PDF da simulação atual (título, tabela com cada investimento e totais) usando a biblioteca `fpdf2`

---

## Banco de dados (Supabase)

O PostgreSQL no Supabase tem duas tabelas e uma view:

- `cfg_indicadores_investimento` — configuração estática dos investimentos disponíveis
- `stg_indicadores_bcb` — dados brutos da API Focus/BCB, atualizados diariamente por Edge Function
- `vw_indicadores_investimento` — view que junta as duas tabelas e entrega as taxas prontas (CDI derivado da Selic, Poupança calculada conforme regra, etc.)

O simulador só lê dessa view. Nunca escreve nada no Supabase.

---

## Fluxo principal

```
Usuário abre o app
  └── supabase_client busca taxas
        └── [sem conexão] usa cache local
  └── json_repository carrega carteira salva

Usuário adiciona investimento
  └── frames.py captura input → valida
  └── calculator.py calcula projeção
  └── frames.py desenha gráfico e legenda
  └── json_repository salva carteira

Usuário muda prazo
  └── calculator recalcula → frames redesenha
```

---

## Relação entre componentes

```
main.py (orquestrador)
  ├── chama → frames.py (interface)
  ├── chama → calculator.py (projeções)
  ├── chama → supabase_client.py (taxas na inicialização)
  ├── chama → json_repository.py (salvar/carregar carteira e cache)
  └── chama → pdf_export.py (ao clicar em "Exportar PDF")

calculator.py
  └── depende de → constants.py (mapeamento de investimentos)

frames.py
  └── depende de → constants.py (cores, dimensões, descrições)
  └── depende de → calculator.py (calcular_totais para o gráfico)
  └── depende de → tooltip.py (tooltips em hover e janela do glossário)

tooltip.py
  └── depende de → constants.py (cores e dicionário INVESTIMENTOS)

pdf_export.py
  └── depende de → calculator.py (calcular_totais para o resumo do PDF)
  └── depende de → constants.py (formatar_brl)
```

---

## Diagrama de histórias de usuário

Link: https://www.figma.com/board/nN0JSuSVPB9LzBQh5qHSJh/Hist%C3%B3rias-de-Usu%C3%A1rio?node-id=0-1&t=l3nvlIuwgJwutzGD-1

![alt text](historias_usuarios.png)

---

*Última atualização: Semana 7 — 20/05/2026*
