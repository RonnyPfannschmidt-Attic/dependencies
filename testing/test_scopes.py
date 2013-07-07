import pytest
from dicm import DependencyManager

@pytest.fixture
def dm():
    return DependencyManager(scopenames=['one', 'two'])


def test_enter_leave_known_scopes(dm):
    dm.enter_scope('one')
    dm.leave_scope('one')
