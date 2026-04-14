import { serve } from "https://deno.land/std@0.168.0/http/server.ts"
import { createClient } from "https://esm.sh/@supabase/supabase-js@2"

const json = (body: any, status = 200) =>
  new Response(JSON.stringify(body), { status, headers: { "Content-Type": "application/json" } })

serve(async () => {
  try {
    const supabase = createClient(
      Deno.env.get("SUPABASE_URL")!,
      Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!
    )

    // Busca a data mais recente disponível na API do BCB
    const base = "https://olinda.bcb.gov.br/olinda/servico/Expectativas/versao/v1/odata/ExpectativasMercadoAnuais"
    const resUltima = await fetch(`${base}?$format=json&$orderby=Data%20desc&$top=1`)
    const { value: [primeiro] } = await resUltima.json()
    if (!primeiro) return json({ erro: "Nenhuma data encontrada no BCB" }, 500)

    const dataMaisRecente = primeiro.Data

    // Busca todos os registros da data
    const resCompleta = await fetch(`${base}?$format=json&$filter=Data%20eq%20%27${dataMaisRecente}%27`)
    const { value: dados } = await resCompleta.json()
    if (!dados?.length) return json({ erro: "Nenhum dado retornado do BCB" }, 500)

    // Transforma e deduplica (a API pode trazer registros repetidos)
    const mapa = new Map<string, any>()
    for (const item of dados) {
      const detalhe = item.IndicadorDetalhe?.trim()
      const registro = {
        des_indicador:  detalhe ? `${item.Indicador} ${detalhe}` : item.Indicador,
        dat_indicador:  item.Data?.split("T")[0],
        ano_referencia: parseInt(item.DataReferencia),
        vlr_mediana:    item.Mediana,
      }
      mapa.set(`${registro.des_indicador}|${registro.dat_indicador}|${registro.ano_referencia}`, registro)
    }
    const transformado = Array.from(mapa.values())

    // Grava no Supabase em lotes de 100
    const erros: any[] = []
    let totalInseridos = 0

    for (let i = 0; i < transformado.length; i += 100) {
      const lote = transformado.slice(i, i + 100)
      const { error } = await supabase
        .from("stg_indicadores_bcb")
        .upsert(lote, { onConflict: "des_indicador,dat_indicador,ano_referencia" })

      if (error) erros.push({ lote: `${i}-${i + lote.length}`, ...error })
      else totalInseridos += lote.length
    }

    return json({
      sucesso:             erros.length === 0,
      data_utilizada:      dataMaisRecente,
      total_registros_bcb: dados.length,
      total_apos_dedup:    transformado.length,
      total_inseridos:     totalInseridos,
      erros:               erros.length > 0 ? erros : undefined,
    }, erros.length > 0 ? 207 : 200)

  } catch (err: any) {
    return json({ erro: err.message, stack: err.stack }, 500)
  }
})
