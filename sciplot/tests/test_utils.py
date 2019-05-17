"""
Test utility functions
"""
from sciplot.utils.general import round_list

def test_round_list():
    list_under_test = [0.111, 0.222, 0.555]

    list_round_3 = [0.111, 0.222, 0.555]
    list_round_2 = [0.11, 0.22, 0.56]

    assert round_list(list_under_test, 3) == list_round_3
    assert round_list(list_under_test, 2) == list_round_2