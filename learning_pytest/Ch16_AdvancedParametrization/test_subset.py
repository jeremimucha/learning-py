import pytest
import cards
from cards import Card


@pytest.mark.parametrize(
    "user", ["admin", "team_member", "visitor"], indirect=["user"]
)
def test_access_rights(user):
    print(f"Test access rights for {user}")

@pytest.fixture(params=["admin", "team_member", "visitor"])
def user(request):
    role = request.param
    print(f"\nLog in as {role}")
    yield role
    print(f"\nLog out {role}")

def test_everyone(user):
    print(f"Test access rights for {user}")

@pytest.mark.parametrize("user", ["admin"], indirect=["user"])
def test_subset(user):
    print(f"Test access rights for {user}")
