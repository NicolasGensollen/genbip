from ..bip import bip

def test_raw_instantiation():
    test_bip = bip("","",[1,3,2,4],[2,4,1,1,2],["a","b","c","d"],["1","2","3","4","5"])
    assert test_bip.top_filename == ""
    assert test_bip.bot_filename == ""
    assert test_bip.top_degree == [1,3,2,4]
    assert test_bip.bot_degree == [2,4,1,1,2]
    assert test_bip.top_index == [0,1,4,6]
    assert test_bip.top_vector == [0,1,1,1,2,2,3,3,3,3]
    assert test_bip.bot_vector == [0,0,1,1,1,1,2,3,4,4]
    assert test_bip.top_names == ["a","b","c","d"]
    assert test_bip.bot_names == ["1","2","3","4","5"]
    assert test_bip.small
    assert test_bip.n_top == 4
    assert test_bip.n_bot == 5
    assert test_bip.m == 10
    assert test_bip.max_top_deg == 4
    assert test_bip.min_top_deg == 1
    assert test_bip.max_bot_deg == 4
    assert test_bip.min_bot_deg == 1
    assert test_bip.is_multigraph

def test_instantiation_from_files_toy_1():
    toy1_bip = bip.from_files("./data/toy_1/toy_top.gz","./data/toy_1/toy_bot.gz")
    assert toy1_bip.top_filename == "./data/toy_1/toy_top.gz"
    assert toy1_bip.bot_filename == "./data/toy_1/toy_bot.gz"
    assert toy1_bip.top_degree == [2,1,3,2]
    assert toy1_bip.bot_degree == [2,2,2,2]
    assert toy1_bip.top_index == [0,2,3,6]
    assert toy1_bip.top_vector == [0,0,1,2,2,2,3,3]
    assert toy1_bip.bot_vector == [0,0,1,1,2,2,3,3]
    assert toy1_bip.top_names == ["a","b","c","d"]
    assert toy1_bip.bot_names == ["alpha","beta","gamma","delta"]
    assert toy1_bip.small
    assert toy1_bip.n_top == 4
    assert toy1_bip.n_bot == 4
    assert toy1_bip.m == 8
    assert toy1_bip.max_top_deg == 3
    assert toy1_bip.min_top_deg == 1
    assert toy1_bip.max_bot_deg == 2
    assert toy1_bip.min_bot_deg == 2
    assert toy1_bip.is_multigraph

def test_instantiation_from_sequences():
    from_seq_bip = bip.from_sequences([2,1,3,2],[2,2,2,2], ["a","b","c","d"], ["alpha", "beta", "gamma", "delta"])
    assert from_seq_bip.top_filename == ""
    assert from_seq_bip.bot_filename == ""
    assert from_seq_bip.top_degree == [2,1,3,2]
    assert from_seq_bip.bot_degree == [2,2,2,2]
    assert from_seq_bip.top_index == [0,2,3,6]
    assert from_seq_bip.top_vector == [0,0,1,2,2,2,3,3]
    assert from_seq_bip.bot_vector == [0,0,1,1,2,2,3,3]
    assert from_seq_bip.top_names == ["a","b","c","d"]
    assert from_seq_bip.bot_names == ["alpha","beta","gamma","delta"]
    assert from_seq_bip.small
    assert from_seq_bip.n_top == 4
    assert from_seq_bip.n_bot == 4
    assert from_seq_bip.m == 8
    assert from_seq_bip.max_top_deg == 3
    assert from_seq_bip.min_top_deg == 1
    assert from_seq_bip.max_bot_deg == 2
    assert from_seq_bip.min_bot_deg == 2
    assert from_seq_bip.is_multigraph


def test_instantiation_from_only_ones_sequences():
    from_seq_bip = bip.from_sequences([1,1,1,1],[1,1,1,1], ["a","b","c","d"], ["alpha", "beta", "gamma", "delta"])
    assert from_seq_bip.top_filename == ""
    assert from_seq_bip.bot_filename == ""
    assert from_seq_bip.top_degree == [1,1,1,1]
    assert from_seq_bip.bot_degree == [1,1,1,1]
    assert from_seq_bip.top_index == [0,1,2,3]
    assert from_seq_bip.top_vector == [0,1,2,3]
    assert from_seq_bip.bot_vector == [0,1,2,3]
    assert from_seq_bip.top_names == ["a","b","c","d"]
    assert from_seq_bip.bot_names == ["alpha","beta","gamma","delta"]
    assert from_seq_bip.small
    assert from_seq_bip.n_top == 4
    assert from_seq_bip.n_bot == 4
    assert from_seq_bip.m == 4
    assert from_seq_bip.max_top_deg == 1
    assert from_seq_bip.min_top_deg == 1
    assert from_seq_bip.max_bot_deg == 1
    assert from_seq_bip.min_bot_deg == 1
    assert not from_seq_bip.is_multigraph


