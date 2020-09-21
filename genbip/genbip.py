
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


