"""Helpers compartilhados pelos testes: teste(), aprox() e resumo()."""

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
