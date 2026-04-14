from supabase import create_client, Client

SUPABASE_URL = "https://gmrwxpkovgsmzlyoxjyy.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imdtcnd4cGtvdmdzbXpseW94anl5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzI2NDcwODksImV4cCI6MjA4ODIyMzA4OX0.plWL1pT5kENCD1w05B1ankZmXD3fq3-FLW3AZrhpl7M"


def _get_client() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)


def buscar_indicadores() -> list[dict]:
    cliente = _get_client()
    resposta = cliente.table("vw_indicadores_investimento").select("*").execute()
    return resposta.data


def buscar_indicadores_por_ano(ano: int) -> list[dict]:
    cliente = _get_client()
    resposta = (
        cliente.table("vw_indicadores_investimento")
        .select("*")
        .eq("ano_referencia", ano)
        .execute()
    )
    return resposta.data
