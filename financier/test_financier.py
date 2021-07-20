import pytest
import json

import financier 

def test_join():
    strings = ["hello", "world"]
    assert financier.join_items(*strings) == "hello world"

def test_sum_previous():
    val1 = "20.00"
    val2 = "-10.00"
    val3= "100"
    assert financier.sum_previous(val1, val2, val3) == "10.00"

def test_run_special():
    format_json = json.loads(('{"fields":'
            '{'
                '"item1":"",'
                '"item2":"",'
                '"$func":{"name":"sum_previous","input":["item1"], "result":"balance"}'
            '}}'))
    row = {"item1":"10", "item2":"5"}
    previous = {"item1":20, "item2":10}
    next_row = {"item1":20, "item2":10}
    row = financier.run_special(row, previous, next_row, format_json)
