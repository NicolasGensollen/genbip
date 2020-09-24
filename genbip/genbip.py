
import random
import numpy as np
from .bip import bip

class AbstractGenBip:
    """
        Abstract class for GenBip.
    """
    def __init__(self, **kwargs):
        self.seed = None
        if "seed" in kwargs:
            seed = kwargs.pop("seed")
            self.set_random_seed(seed)

    def set_random_seed(self, seed):
        if seed is not None:
            self.seed = seed
            random.seed(self.seed)
            np.random.seed(self.seed)

    @property
    def is_seeded(self):
        return not self.seed is None

    def run(self, bip):
        pass

class GenBipConfiguration(AbstractGenBip):
    """
        Class implementing the basic configuration model.
        This is equivalent to shuffling the not array of a Bip class.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def run(self, bip):
        np.random.shuffle(bip.bot_vector)

class GenBipPrunedConfiguration(AbstractGenBip):
    """
        Class implementing the pruned configuration model.
        Delete multilinks, resulting in degree distributions different from the prescribed ones.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def run(self, bip):
        np.random.shuffle(bip.bot_vector)
        new_top, new_bot = [],[]
        for u in range(bip.n_top):
            neighbors = bip.top_neighbors(u)
            new_top.extend([u]*len(neighbors))
            new_bot.extend(neighbors)
        bip.update_from_vectors(new_top,new_bot)

class GenBipRepeatedConfigurationWhole(AbstractGenBip):
    """

    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def run(self, bip):
        np.random.shuffle(bip.bot_vector)
        i = 1
        while bip.is_multigraph:
            np.random.shuffle(bip.bot_vector)
            i += 1
            if bip.verbose:
                print(f"{i}")
        if bip.verbose:
            print(f"genbip_repeated_configuration_whole: {i} global shufflings performed\n")

class GenBipRepeatedConfigurationAsap(AbstractGenBip):
    """

    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def run(self, bip):
        neighbors_array = np.zeros(bip.n_bot, dtype=np.int64)
        rounds = 0
        multi = True
        while multi:
            multi = False
            for v in range(bip.n_top):
                last_i = bip.top_index[v] + bip.top_degree[v]
                for i in range(bip.top_index[v],last_i):
                    j = random.randrange(i,bip.m)
                    if neighbors_array[bip.bot_vector[j]] != 0:
                        multi = True
                        last_i = i
                        break
                    else:
                        neighbors_array[bip.bot_vector[j]] = 1
                        bip.swap(i,j)
                assert last_i > bip.top_index[v] and last_i <= bip.top_index[v]+bip.top_degree[v]
                for j in range(bip.top_index[v],last_i):
                    neighbors_array[bip.bot_vector[j]] = 0
                if multi:
                    break
            rounds += 1
            if bip.verbose:
                print(f"{rounds}")
        print(f"genbip_repeated_configuration_asap: {rounds} rounds\n")

class GenBipCorrectedConfiguration(AbstractGenBip):
    """

    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def run(self, bip):
        rounds, nswaps, swaps = 0, 0, None
        while swaps != 0:
            swaps = 0
            for u in range(bip.n_top):
                neighbors = set()
                for i in range(bip.top_degree[u]):
                    v = bip.bot_vector[bip.top_index[u]+i]
                    if v in neighbors:
                        bip.random_swap(bip.top_index[u]+i)
                        swaps += 1
                    neighbors.add(v)
            rounds += 1
            nswaps += swaps
            if bip.verbose:
                print(f"{swaps} swaps")
        if bip.verbose:
            print(f"swaps at each round\ngenbip_corrected_configuration: {rounds} rounds, {nswaps} swaps total\n")
