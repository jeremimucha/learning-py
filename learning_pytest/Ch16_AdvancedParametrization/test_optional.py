import pytest
import cards
from cards import Card


# Fixtures support optional indirect param handling.
# To do so, check if `param` member is available on the given request.
# Thanks to this technique a single fixture can be used both for tests
# that use indirect params and those that don't.
@pytest.fixture()
def user(request):
    role = getattr(request, "param", "visitor")
    print(f"\nLog in as {role}")
    yield role
    print(f"\nLog out {role}")


# Just rely on the default
def test_unspecified_user(user):
    print(f"Testing with {user}")


# Use indirect parameters
@pytest.mark.parametrize(
    "user", ["admin", "team_member"], indirect=["user"]
)
def test_admin_and_team_member(user):
    print(f"Testing with {user}")
