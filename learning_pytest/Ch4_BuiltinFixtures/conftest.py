import pytest
import cards


# Instead of directly using the `TemporaryDirectory` tempfile
# like we did in Ch3, we can use the pytest builtin fixture `tmp_path_factory`


@pytest.fixture(scope="session")
def cards_db_session(tmp_path_factory):
    """CardsDb object connected to a temporary database"""
    db_path = tmp_path_factory.mktemp("cards_db")
    db = cards.CardsDB(db_path)
    yield db
    db.close()
