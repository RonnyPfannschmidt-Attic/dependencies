import pytest
from dicm import DependencyManager, Scopes
from mock import Mock


one = pytest.mark.enter('one')


@pytest.fixture
def sm(request):
    sm = Scopes(names=['one', 'two'])
    enter = request.keywords.get('enter', ())
    for item in enter:
        for arg in item.args:
            sm.enter(arg)
    return sm


def test_enter_leave_known_scopes(sm):
    sm.enter('one')
    sm.leave('one')

def test_fail_enter_wrong_order(sm):
    with pytest.raises(AssertionError):
        sm.enter('two')


@one
def test_fail_leave_wrong_order(sm):
    sm.enter('two')
    with pytest.raises(AssertionError):
        sm.leave('one')


@one
def test_cleanup(sm):
    m = Mock(name='cleanup')
    sm.add_cleanup(m)
    sm.leave('one')
    assert m.called


@one
def test_set(sm):
    assert 'a' not in sm.current
    sm.set('a', 1)
    assert 'a' in sm.current
