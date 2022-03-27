from hash_table import HashTable, BLANK
import pytest

def test_should_insert_key_value_pairs():
    hash_table = HashTable(capacity=100)

    hash_table["hola"] = "hello"
    hash_table[98.6] = 37
    hash_table[False] = True


    assert ("hola", "hello") in hash_table._pairs
    assert (98.6, 37) in hash_table._pairs
    assert (False, True) in hash_table._pairs


    assert len(hash_table) == 100
    
def test_should_not_contain_none_value_when_created():
    assert None not in HashTable(capacity=100)._pairs

def test_should_create_empty_value_slots():
    assert HashTable(capacity=3)._pairs == [BLANK, BLANK, BLANK]

def test_should_insert_none_value():
    hash_table = HashTable(capacity=100)
    values = [pair.value for pair in hash_table._pairs if pair]
    assert None not in values

def test_should_find_value_by_key(hash_table):
    assert hash_table["hola"] == "hello"
    assert hash_table[98.6] == 37
    assert hash_table[False] is True

def test_should_raise_error_on_missing_key():
    hash_table = HashTable(capacity=100)
    with pytest.raises(KeyError) as exception_info:
        hash_table["missing_key"]
    assert exception_info.value.args[0] == "missing_key"

def test_should_get_value(hash_table: HashTable):
    assert hash_table.get("hola") == "hello"

def test_should_get_none_when_missing_key(hash_table: HashTable):
    assert hash_table.get("missing_key") is None

def test_should_get_default_value_when_missing_key(hash_table: HashTable):
    assert hash_table.get("missing_key", "default") == "default"

def test_should_get_value_with_default(hash_table: HashTable):
    assert hash_table.get("hola", "default") == "hello"

def test_should_raise_key_error_when_deleting(hash_table: HashTable):
    with pytest.raises(KeyError) as exception_info:
        del hash_table["missing_key"]
        assert exception_info.value.args[0] == "missing_key"

if __name__=='__main__':
    hash_table = HashTable(capacity=100)
    hash_table["hola"] = "hello"
    hash_table[98.6] = 37
    hash_table[False] = True

    # test_should_insert_key_value_pairs()
    # test_should_not_contain_none_value_when_created()
    # test_should_create_empty_value_slots()
    # test_should_insert_none_value()
    # test_should_raise_error_on_missing_key()
    # test_should_get_value(hash_table)
    # test_should_get_none_when_missing_key(hash_table)
    # test_should_get_default_value_when_missing_key(hash_table)
    # test_should_get_value_with_default(hash_table)
    # test_should_raise_key_error_when_deleting(hash_table)

    print(hash_table.keys)





