from ..utils import *

def test_linear_sort():
    assert linear_sort([3,1,2,6,4,5]) == [1,2,3,4,5,6]

def test_is_bigraphic_gale_ryser():
    assert is_bigraphic_gale_ryser([2,4,1,2], [2,2,3,1,1])
    assert not is_bigraphic_gale_ryser([2,4,1,2], [2,2,5,1,1])
    assert is_bigraphic_gale_ryser([3,4,4,5], [4,4,4,3,1])
