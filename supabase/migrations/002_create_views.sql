-- View que consolida os indicadores do BCB e calcula as taxas derivadas
-- CDI = Selic - 0.10 | Poupança = 70% da Selic se Selic <= 8.5%, senão 6.17% fixo
create view public.vw_indicadores_investimento as
with
  data_recente as (
    select max(dat_indicador) as dat_indicador
    from stg_indicadores_bcb
  ),
  indicadores_focus as (
    select
      cfg.cod_investimento,
      cfg.des_investimento,
      stg.ano_referencia,
      stg.vlr_mediana,
      stg.dat_indicador
    from cfg_indicadores_investimento cfg
    join stg_indicadores_bcb stg on stg.des_indicador = cfg.des_indicador::text
    join data_recente dr on stg.dat_indicador = dr.dat_indicador
    where cfg.ind_calculado = false
  ),
  selic as (
    select ano_referencia, vlr_mediana, dat_indicador
    from indicadores_focus
    where cod_investimento::text = 'SELIC'::text
  ),
  calculados as (
    select
      'CDI'::text          as cod_investimento,
      'CDB 100% CDI'::text as des_investimento,
      ano_referencia,
      vlr_mediana - 0.10   as vlr_mediana,
      dat_indicador
    from selic
    union all
    select
      'POUPANCA'::text,
      'Poupança'::text,
      ano_referencia,
      case
        when vlr_mediana > 8.5 then 6.17
        else vlr_mediana * 0.7
      end,
      dat_indicador
    from selic
  )
select cod_investimento, des_investimento, ano_referencia, vlr_mediana, dat_indicador
from indicadores_focus
union all
select cod_investimento, des_investimento, ano_referencia, vlr_mediana, dat_indicador
from calculados
order by 1, 3;
