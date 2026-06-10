from database import add_transaction
from database import get_transactions

def test_insert_transaction():

    add_transaction(
        "Teste",
        100,
        "Outros",
        "Receita"
    )

    dados = get_transactions()

    assert len(dados) > 0