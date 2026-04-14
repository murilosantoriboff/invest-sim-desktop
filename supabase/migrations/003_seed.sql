-- Dados iniciais dos investimentos disponíveis no simulador
-- CDI e POUPANCA são calculados a partir da Selic
-- Os demais são buscados diretamente da API do BCB pelo des_indicador
insert into public.cfg_indicadores_investimento
  (cod_investimento, des_investimento, des_indicador, ind_calculado)
values
  ('CAMBIO',   'Dólar',         'Câmbio', false),
  ('CDI',      'CDB 100% CDI',  null,     true),
  ('IGPM',     'IGP-M',         'IGP-M',  false),
  ('IPCA',     'Tesouro IPCA+', 'IPCA',   false),
  ('POUPANCA', 'Poupança',      null,     true),
  ('SELIC',    'Tesouro Selic', 'Selic',  false);
