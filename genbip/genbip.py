
import random
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
        random.shuffle(bip.bot_vector)

class GenBipPrunedConfiguration(AbstractGenBip):
    """
        Class implementing the pruned configuration model.
        Delete multilinks, resulting in degree distributions different from the prescribed ones.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def run(self, bip):
        random.shuffle(bip.bot_vector)
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
        random.shuffle(bip.bot_vector)
        i = 1
        while bip.is_multigraph:
            random.shuffle(bip.bot_vector)
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
        neighbors_array = [0] * bip.n_bot
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
