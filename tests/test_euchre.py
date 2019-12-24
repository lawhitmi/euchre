from src.euchre.euchre import pickDealer, Euchre


def test_pickDealer():
    x, y = pickDealer()
    # Ensure only one dealer is chosen
    assert x != y


def test_Euchre():
    #game = Euchre()
    NotImplemented


