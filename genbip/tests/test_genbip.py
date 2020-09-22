
from ..bip import bip
from ..genbip import GenBipConfiguration, GenBipPrunedConfiguration, GenBipRepeatedConfigurationWhole, GenBipRepeatedConfigurationAsap

def test_instantiation_genbip_configuration():
    genbip_conf = GenBipConfiguration()
    assert genbip_conf.seed is None
    assert not genbip_conf.is_seeded
    genbip_conf.set_random_seed(123)
    assert genbip_conf.seed == 123
    assert genbip_conf.is_seeded
    genbip_conf = GenBipConfiguration(seed=176)
    assert genbip_conf.seed == 176
    assert genbip_conf.is_seeded

def test_genbip_configuration():
    test_bip = bip.from_sequences([2,1,3,2],[2,2,2,2], ["a","b","c","d"], ["alpha", "beta", "gamma", "delta"])
    genbip_conf = GenBipConfiguration(seed=123)
    assert genbip_conf.seed == 123
    genbip_conf.run(test_bip)
    assert test_bip.top_degree == [2,1,3,2]
    assert test_bip.bot_degree == [2,2,2,2]
    assert test_bip.top_index == [0,2,3,6]
    assert test_bip.top_vector == [0,0,1,2,2,2,3,3]
    assert test_bip.bot_vector == [0,2,2,3,1,3,1,0]
    assert test_bip.top_names == ["a","b","c","d"]
    assert test_bip.bot_names == ["alpha","beta","gamma","delta"]
    assert test_bip.small
    assert test_bip.n_top == 4
    assert test_bip.n_bot == 4
    assert test_bip.m == 8
    assert test_bip.max_top_deg == 3
    assert test_bip.min_top_deg == 1
    assert test_bip.max_bot_deg == 2
    assert test_bip.min_bot_deg == 2
    assert test_bip.is_multigraph

def test_genbip_pruned_configuration():
    test_bip = bip.from_sequences([2,1,3,2],[2,2,2,2], ["a","b","c","d"], ["alpha", "beta", "gamma", "delta"])
    genbip_pruned_conf = GenBipPrunedConfiguration(seed=123)
    genbip_pruned_conf.run(test_bip)
    assert test_bip.top_degree == [2,1,2,2]
    assert test_bip.bot_degree == [1,1,1,2,1,1]
    assert test_bip.top_index == [0,2,3,5]
    assert test_bip.top_vector ==  [0,0,1,2,2,3,3]
    assert test_bip.bot_vector ==  [0,2,2,1,3,0,1]
    assert test_bip.small
    assert test_bip.n_top == 4
    assert test_bip.n_bot == 6
    assert test_bip.m == 7
    assert test_bip.max_top_deg == 2
    assert test_bip.min_top_deg == 1
    assert test_bip.max_bot_deg == 2
    assert test_bip.min_bot_deg == 1
    assert not test_bip.is_multigraph

def test_genbip_repeated_configuration_whole():
    test_bip = bip.from_sequences([2,1,3,2],[2,2,2,2], ["a","b","c","d"], ["alpha", "beta", "gamma", "delta"])
    genbip_rep_conf = GenBipRepeatedConfigurationWhole(seed=123)
    genbip_rep_conf.run(test_bip)
    assert test_bip.top_degree == [2,1,3,2]
    assert test_bip.bot_degree == [2,2,2,2]
    assert test_bip.top_index == [0,2,3,6]
    assert test_bip.top_vector ==  [0,0,1,2,2,2,3,3]
    assert test_bip.bot_vector ==  [3,0,2,3,1,2,1,0]
    assert test_bip.small
    assert test_bip.n_top == 4
    assert test_bip.n_bot == 4
    assert test_bip.m == 8
    assert test_bip.max_top_deg == 3
    assert test_bip.min_top_deg == 1
    assert test_bip.max_bot_deg == 2
    assert test_bip.min_bot_deg == 2
    assert not test_bip.is_multigraph

def test_genbip_repeated_configuration_asap():
    test_bip = bip.from_sequences([2,1,3,2],[2,2,2,2], ["a","b","c","d"], ["alpha", "beta", "gamma", "delta"])
    genbip_rep_asap = GenBipRepeatedConfigurationAsap(seed=123)
    genbip_rep_asap.run(test_bip)
    assert test_bip.top_degree == [2,1,3,2]
    assert test_bip.bot_degree == [2,2,2,2]
    assert test_bip.top_index == [0,2,3,6]
    assert test_bip.top_vector ==  [0,0,1,2,2,2,3,3]
    assert test_bip.bot_vector ==  [0,1,1,3,0,2,2,3]
    assert test_bip.small
    assert test_bip.n_top == 4
    assert test_bip.n_bot == 4
    assert test_bip.m == 8
    assert test_bip.max_top_deg == 3
    assert test_bip.min_top_deg == 1
    assert test_bip.max_bot_deg == 2
    assert test_bip.min_bot_deg == 2
    assert not test_bip.is_multigraph

