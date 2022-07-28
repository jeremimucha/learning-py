import pytest
import cards
from cards import Card

# Indirect parameters are passed in to a fixture first,
# before they get sent to the test function.
# This allows us to perform work based on the parrameter value.

# 1. set `indirect` to a list of parameter names we want to be indirect.
#    This can also be `indirect=True` if all params should be indirect.
# 2. Provide a fixture with the same name as the parameter.

@pytest.mark.parametrize(
    "user", ["admin", "team_member", "visitor"], indirect=["user"]
)
def test_access_rights(user):
    print(f"Test access rights for {user}")

@pytest.fixture()
def user(request):
    role = request.param
    print(f"\nLog in as {role}")
    yield role
    print(f"\nLog out {role}")
