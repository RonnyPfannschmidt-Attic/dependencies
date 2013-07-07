import pytest
from dicm import DependencyManager, Scopes

@pytest.fixture
def sm():
    return Scopes(names=['one', 'two'])


def test_enter_leave_known_scopes(sm):
    sm.enter('one')
    sm.leave('one')
