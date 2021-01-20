import random
import numpy as np
from genbip.bip import bip

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
        # Re-order top nodes by decreasing degree
        bip.reorder_top_decreasing_degree()
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

class GenBipHavelHakimi(AbstractGenBip):
    """

    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def random_swaps(self, bip):
        n_swap = 0
        n_edges = bip.m
        N_swap = 10 * n_edges
        #for edge in multiple_edges:
        #accepted = False
        print(f'{N_swap} swaps needed')
        while n_swap < N_swap:
            edge = np.random.choice(n_edges)
            other_edge = np.random.choice(n_edges)
            if other_edge == edge:
                continue
            if n_swap % 1000000 == 0:
                print(f'{n_swap} / {N_swap} done')
            # check if multiple edge
            new_edge1 = (bip.top_vector[edge], bip.bot_vector[other_edge])
            new_edge2 = (bip.top_vector[other_edge], bip.bot_vector[edge])
            #if new_edge1 in anomaly_edges or new_edge2 in anomaly_edges: 
            #    continue

            if not (bip.link_exists(bip.top_vector[edge], bip.bot_vector[other_edge]) or bip.link_exists(bip.top_vector[other_edge], bip.bot_vector[edge])):
                n_swap += 1
                edge1 =  (bip.top_vector[edge], bip.bot_vector[edge])
                edge2 =  (bip.top_vector[other_edge], bip.bot_vector[other_edge])
                bip.swap(edge,other_edge)
        print(f'{n_swap} / {N_swap} done')


    def run(self, bip):
        # Re-order top nodes by decreasing degree
        bip.reorder_top_decreasing_degree()
        # Re-order bot nodes by decreasing degree
        bip.reorder_bot_decreasing_degree()
        sorted_bot = np.flip(np.arange(bip.n_bot))
        d = 0
        bot_deg_pos = -1 * np.ones(bip.max_bot_deg+1, dtype=np.int64)
        for v in range(bip.n_bot):
            bot_deg_pos[bip.bot_degree[v]] = bip.n_bot - 1 - v
        for i in np.flip(np.arange(bip.max_bot_deg)):
            if bot_deg_pos[i] < 0:
                bot_deg_pos[i] = bot_deg_pos[i+1]

        bot_deg = list(bip.bot_degree) # Local copy
        i = 0
        for u in range(bip.n_top):
            bip.top_index[u] = i
            for j in range(bip.n_bot - bip.top_degree[u], bip.n_bot):
                v = sorted_bot[j]
                bip.top_vector[i],bip.bot_vector[i] = u,v
                i += 1
                sorted_bot[j] = sorted_bot[bot_deg_pos[bot_deg[v]]]
                sorted_bot[bot_deg_pos[bot_deg[v]]] = v
                bot_deg_pos[bot_deg[v]] += 1
                bot_deg[v] -= 1
        print('doing swaps')
        self.random_swaps(bip)

