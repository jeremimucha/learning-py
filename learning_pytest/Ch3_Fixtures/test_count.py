from pathlib import Path
from tempfile import TemporaryDirectory
import pytest
import cards


# Test fixtures can and should be used to encapsulate
# the setup necessary to execute the test itself.
#
# To more closely trace a test uses a given fixture
# execute pytest with `--setup-show`
# `pytest --setup-show test_count.py`


# Without using a fixture - lots of manual setup,
# and risk for leaking resources.
@pytest.mark.skip()
def test_empty_no_fixture():
    with TemporaryDirectory() as db_dir:
        db_path = Path(db_dir)
        db = cards.CardsDB(db_path)

        count = db.count()
        db.close()

        assert count == 0


# With using a pytest fixture:
@pytest.fixture()
def cards_db():
    with TemporaryDirectory() as db_dir:
        db_path = Path(db_dir)
        db = cards.CardsDB(db_path)
        yield db
        db.close()


def test_empty(cards_db):
    assert cards_db.count() == 0


def test_Two(cards_db):
    cards_db.add_card(cards.Card("first"))
    cards_db.add_card(cards.Card("second"))
    assert cards_db.count() == 2

