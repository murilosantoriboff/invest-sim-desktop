-- Tabela de configuração dos investimentos disponíveis no simulador
create table public.cfg_indicadores_investimento (
  cod_investimento character varying(20) not null,
  des_investimento character varying(100) not null,
  des_indicador    character varying(100) null,
  ind_calculado    boolean null default false,
  constraint cfg_indicadores_investimento_pkey primary key (cod_investimento)
);

-- Tabela de staging com os dados brutos da API do Banco Central
create table public.stg_indicadores_bcb (
  id               bigint generated always as identity not null,
  des_indicador    text not null,
  dat_indicador    date not null,
  ano_referencia   integer not null,
  vlr_mediana      numeric(15, 6) not null,
  dat_atualizacao  timestamp without time zone null default now(),
  constraint stg_indicadores_bcb_pkey primary key (id)
);

-- Índice único para evitar duplicatas no upsert da Edge Function
create unique index if not exists uq_stg_indicadores_bcb
  on public.stg_indicadores_bcb (des_indicador, dat_indicador, ano_referencia);
