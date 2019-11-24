from src.euchre.euchre import pickDealer, Euchre


def test_pickDealer():
    x, y = pickDealer()
    assert x != y

