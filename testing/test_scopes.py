import pytest
from dicm import DependencyManager, Scopes
from mock import Mock

@pytest.fixture
def sm():
    return Scopes(names=['one', 'two'])


def test_enter_leave_known_scopes(sm):
    sm.enter('one')
    sm.leave('one')


def test_cleanup(sm):
    m = Mock(name='cleanup')
    sm.enter('one')
    sm.add_cleanup(m)
    sm.leave('one')
    assert m.called
