import pytest
from dicm import DependencyManager

@pytest.fixture
def dm():
    dm = DependencyManager(scopenames=['one', 'two'])
    dm.enter_scope('one')
    return dm


def test_invoke_simple(dm):

    def invokeme(arg):
        assert arg == 1
        return 1

    dm.scopes.set('arg', 1)

    result = dm.call(invokeme)
    assert result == 1

