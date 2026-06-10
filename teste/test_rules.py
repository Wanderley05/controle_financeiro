def calcular_saldo(receitas, despesas):
    return receitas - despesas

def test_saldo():

    resultado = calcular_saldo(
        5000,
        2000
    )

    assert resultado == 3000