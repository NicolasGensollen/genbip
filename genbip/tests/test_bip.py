
import os

from genbip.bip import bip

current_directory = os.path.realpath(os.path.dirname(__file__))

def test_raw_instantiation():
    test_bip = bip("","",[1,3,2,4],[2,4,1,1,2],["a","b","c","d"],["1","2","3","4","5"])
    assert test_bip.top_filename == ""
    assert test_bip.bot_filename == ""
    assert test_bip.top_degree.tolist() == [1,3,2,4]
    assert test_bip.bot_degree.tolist() == [2,4,1,1,2]
    assert test_bip.top_index.tolist()  == [0,1,4,6]
    assert test_bip.top_vector.tolist() == [0,1,1,1,2,2,3,3,3,3]
    assert test_bip.bot_vector.tolist() == [0,0,1,1,1,1,2,3,4,4]
    assert test_bip.top_names.tolist()  == ["a","b","c","d"]
    assert test_bip.bot_names.tolist()  == ["1","2","3","4","5"]
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
    top_file = os.path.join(current_directory,"data/toy_1/toy_top.gz")
    bot_file = os.path.join(current_directory, "data/toy_1/toy_bot.gz")
    toy1_bip = bip.from_files(top_file,bot_file)
    assert toy1_bip.top_filename == top_file
    assert toy1_bip.bot_filename == bot_file
    assert toy1_bip.top_degree.tolist() == [2,1,3,2]
    assert toy1_bip.bot_degree.tolist() == [2,2,2,2]
    assert toy1_bip.top_index.tolist()  == [0,2,3,6]
    assert toy1_bip.top_vector.tolist() == [0,0,1,2,2,2,3,3]
    assert toy1_bip.bot_vector.tolist() == [0,0,1,1,2,2,3,3]
    assert toy1_bip.top_names.tolist()  == ["a","b","c","d"]
    assert toy1_bip.bot_names.tolist()  == ["alpha","beta","gamma","delta"]
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
    assert from_seq_bip.top_degree.tolist() == [2,1,3,2]
    assert from_seq_bip.bot_degree.tolist() == [2,2,2,2]
    assert from_seq_bip.top_index.tolist()  == [0,2,3,6]
    assert from_seq_bip.top_vector.tolist() == [0,0,1,2,2,2,3,3]
    assert from_seq_bip.bot_vector.tolist() == [0,0,1,1,2,2,3,3]
    assert from_seq_bip.top_names.tolist()  == ["a","b","c","d"]
    assert from_seq_bip.bot_names.tolist()   == ["alpha","beta","gamma","delta"]
    assert from_seq_bip.small
    assert from_seq_bip.n_top == 4
    assert from_seq_bip.n_bot == 4
    assert from_seq_bip.m == 8
    assert from_seq_bip.max_top_deg == 3
    assert from_seq_bip.min_top_deg == 1
    assert from_seq_bip.max_bot_deg == 2
    assert from_seq_bip.min_bot_deg == 2
    assert from_seq_bip.is_multigraph

def test_update_from_vectors():
    """
    Update the top and bot vector with the exact same ones as bip already has.
    The resulting bip should be exactly the same.
    """
    test_bip = bip.from_sequences([2,1,3,2],[2,2,2,2], ["a","b","c","d"], ["alpha", "beta", "gamma", "delta"])
    test_bip.update_from_vectors(test_bip.top_vector, test_bip.bot_vector)
    assert test_bip.top_degree.tolist() == [2,1,3,2]
    assert test_bip.bot_degree.tolist() == [2,2,2,2]
    assert test_bip.top_index.tolist()  == [0,2,3,6]
    assert test_bip.top_vector.tolist() == [0,0,1,2,2,2,3,3]
    assert test_bip.bot_vector.tolist() == [0,0,1,1,2,2,3,3]
    assert test_bip.top_names.tolist()  == ["a","b","c","d"]
    assert test_bip.bot_names.tolist()  == ["alpha","beta","gamma","delta"]
    assert test_bip.small
    assert test_bip.n_top == 4
    assert test_bip.n_bot == 4
    assert test_bip.m == 8
    assert test_bip.max_top_deg == 3
    assert test_bip.min_top_deg == 1
    assert test_bip.max_bot_deg == 2
    assert test_bip.min_bot_deg == 2
    assert test_bip.is_multigraph

def test_instantiation_from_only_ones_sequences():
    from_seq_bip = bip.from_sequences([1,1,1,1],[1,1,1,1], ["a","b","c","d"], ["alpha", "beta", "gamma", "delta"])
    assert from_seq_bip.top_filename == ""
    assert from_seq_bip.bot_filename == ""
    assert from_seq_bip.top_degree.tolist() == [1,1,1,1]
    assert from_seq_bip.bot_degree.tolist() == [1,1,1,1]
    assert from_seq_bip.top_index.tolist()  == [0,1,2,3]
    assert from_seq_bip.top_vector.tolist() == [0,1,2,3]
    assert from_seq_bip.bot_vector.tolist() == [0,1,2,3]
    assert from_seq_bip.top_names.tolist()  == ["a","b","c","d"]
    assert from_seq_bip.bot_names.tolist()  == ["alpha","beta","gamma","delta"]
    assert from_seq_bip.small
    assert from_seq_bip.n_top == 4
    assert from_seq_bip.n_bot == 4
    assert from_seq_bip.m == 4
    assert from_seq_bip.max_top_deg == 1
    assert from_seq_bip.min_top_deg == 1
    assert from_seq_bip.max_bot_deg == 1
    assert from_seq_bip.min_bot_deg == 1
    assert not from_seq_bip.is_multigraph

def test_reorder_top_decreasing_degree():
    test_bip = bip.from_sequences([3,1,4,2,6,1,1,3,2],[2,1,8,3,1,1,2,1,4], ["a","b","c","d","e","f","g","h","i"], ["alpha", "beta", "gamma", "delta", "epsilon", "omega", "eta", "upsilon", "zeta"])
    assert test_bip.top_degree.tolist() == [3,1,4,2,6,1,1,3,2]
    assert test_bip.top_names.tolist()  == ["a","b","c","d","e","f","g","h","i"]
    test_bip.reorder_top_decreasing_degree()
    assert test_bip.top_degree.tolist() == [6,4,3,3,2,2,1,1,1]
    assert test_bip.top_names.tolist()  == ['e','c','h','a','i','d','g','f','b']

def test_reorder_bot_decreasing_degree():
    test_bip = bip.from_sequences([3,1,4,2,6,1,1,3,2],[2,1,8,3,1,1,2,1,4], ["a","b","c","d","e","f","g","h","i"], ["alpha", "beta", "gamma", "delta", "epsilon", "omega", "eta", "upsilon", "zeta"])
    assert test_bip.bot_degree.tolist() == [2,1,8,3,1,1,2,1,4]
    assert test_bip.bot_names.tolist()  == ["alpha","beta","gamma","delta","epsilon","omega","eta","upsilon","zeta"]
    test_bip.reorder_bot_decreasing_degree()
    assert test_bip.bot_degree.tolist() == [8,4,3,2,2,1,1,1,1]
    assert test_bip.bot_names.tolist()  == ['gamma','zeta','delta','eta','alpha','upsilon','omega','epsilon','beta']
