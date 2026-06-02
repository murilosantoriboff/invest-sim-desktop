"""
_runner.py — Funções auxiliares compartilhadas pelos testes.

Não é um teste em si: centraliza o contador de resultados e os helpers
teste() / aprox() / resumo() usados pelos três arquivos testar_*.py,
evitando repetir o mesmo código em cada um.
"""

_passou = 0
_falhou = 0


def teste(nome, condicao):
    global _passou, _falhou
    if condicao:
        print(f"  OK  {nome}")
        _passou += 1
    else:
        print(f"  FALHOU  {nome}")
        _falhou += 1


def aprox(a, b, tol=0.01):
    return abs(a - b) < tol


def resumo():
    print("\n" + "=" * 60)
    print(f"RESULTADO: {_passou} passaram, {_falhou} falharam")
    print("=" * 60)
    return 0 if _falhou == 0 else 1
