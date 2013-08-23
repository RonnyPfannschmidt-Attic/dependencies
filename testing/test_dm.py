import pytest
from dicm import DependencyManager

@pytest.fixture
def dm():
    dm = DependencyManager(scopenames=['one', 'two'])
    dm.enter_scope('one')
    return dm

