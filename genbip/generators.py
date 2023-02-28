"""
Implement bipartite graph generator using different models.
Available models:
- configuration model: 
        pick all edges at random to fit node degrees.
        can give multiple edges.
- pruned configuration model: 
        Configuration model but remove multiple
        edges. 
- repeated configuration whole: 
        Run a complete configuration model 
        until a simple graph is picked.
- repeated configuration asap: 
        Run a configuration model but stop it
        as soon as a multiple edge is picked.
- corrected configuration model: 
        Run a configuration model but 
        when a multiple edge is picked, perform random
        swaps until there a no multiple edges
- Havel-Hakimi model: 
        Run a modified Havel Hakimi to generate
        a bipartite graph.
"""
from edge_swapper import *
import random
import logging
import numpy as np
from genbip.bip import bip

class AbstractGenBip:
    """
        Abstract class for GenBip.
    """
    def __init__(self, **kwargs):
        self.seed = None
        self.logger = None
        if "seed" in kwargs:
            seed = kwargs.pop("seed")
            self.set_random_seed(seed)
        if "logger" in kwargs:
            self.logger = logger
        else:
            logging.basicConfig(
                    level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M'
                    )
            self.logger = logging.getLogger()


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
        This is equivalent to shuffling the bot array of a Bip class.
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
        Class implementing the Repeated configuration model.
        Run a complete configuration model, and try again until a simple graph
        is picked
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def run(self, bip):
        np.random.shuffle(bip.bot_vector)
        i = 1
        while bip.is_multigraph:
            np.random.shuffle(bip.bot_vector)
            i += 1
            #if bip.verbose:
            self.logger.debug(f"{i}")
        #if bip.verbose:
        self.logger.debug(f"genbip_repeated_configuration_whole: {i} global shufflings performed\n")

class GenBipRepeatedConfigurationAsap(AbstractGenBip):
    """
        Class implementing the repeated configuration ASAP model.
        Run a configuration model but stop it as soon a multiple edge is
        picked and try again.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def run(self, bip):
        # Re-order top nodes by decreasing degree
        bip.reorder_top_decreasing_degree()
        neighbors_array = np.zeros(bip.n_bot, dtype=np.int64)
        rounds = 0
        multi = True
        while (multi or rounds < 1000):
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
            #if bip.verbose:
            self.logger.debug(f"{rounds}")
        self.logger.info(f"genbip_repeated_configuration_asap: {rounds} rounds\n")

class GenBipCorrectedConfiguration(AbstractGenBip):
    """
        Class implementing the corrected configuration model.
        Run a configuration model but when a multiple edge is picked,
        perform random swaps until there are no multiple edges left.
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
            #if bip.verbose:
            self.logger.debug(f"{swaps} swaps")
        #if bip.verbose:
        self.logger.debug(f"swaps at each round\ngenbip_corrected_configuration: {rounds} rounds, {nswaps} swaps total\n")

class GenBipHavelHakimi(AbstractGenBip):
    """
        Class implementing the Havel-Hakimi model, modified to generate
        bipartite graphs.
        This implementation includes a method to run a fixed number of edge swap after generation, to get a 
        uniform sample from the set of graph with given degree sequences.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def random_swaps(self, bip):
        """
           Run an implementation of random edge swap in Cython. 
           Implementation can be found in share/edge_swapper.cpp,
           with cython translation in edge_swapper.pyx.
            
        """
        n_swap = 0
        n_edges = bip.m
        N_swap = 10* n_edges
        self.logger.debug(f'{N_swap} swaps needed')

        # run C++ random swaps
        rdm_swapper = pyRandomSwapper(bip.top_vector, bip.bot_vector, bip.top_index, bip.top_degree)
        bot_vector = rdm_swapper.pyRandom_swaps(N_swap)
        #bip.bot_vector = bot_vector #rdm_swapper.pyRandom_swaps(N_swap)
        return bot_vector

    def run(self, bip):
        """
           Run Havel Hakimi for bipartite graphs, then run random swaps to get uniform samples. 
           Random swap implementation can be found in share/edge_swapper.cpp,
           with cython translation in edge_swapper.pyx
        """
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

        # generation is done, run random swaps
        bot_vector = self.random_swaps(bip)

