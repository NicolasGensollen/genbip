"""Bipartite Graph
A bipartite graph is stored by three data structures: 
    - top vector : 
                        Stores each top "stub" by it's top node name. 
                        E.G. when node '5' has a degree of 2, the top
                        vector will contain [...,5,5,...].
                        The top vector is ordered.
    - top index : 
                        For each node, store the index of first occurence 
                        of this node name in the top vector
    - bottom vector : 
                        Stores each bottom "stub" by it's bottom node name.
                        The bottom vector is unordered.
    - top/bottom names : 
                        The names of the nodes.
                        
Then, an edge in the bipartite graph is represented by the values of
the top vector and bottom vector at a given index.

For example: 
The bipartite graph:

>>> top_vector    = [0,0,1]
>>> top_index     = [0, 2]
>>> bottom_vector = [0,1,2]
>>> top_names     = [a, b]
>>> bottom_names  = [alpha, beta, gamma]

contains the edges:

>>> a - alpha
>>> a - beta
>>> b - gamma

"""
import gzip
import random
import numpy as np

from genbip.utils import is_bigraphic_gale_ryser

SMALL_SIZE = 100

class bip:
    """ Bi-partite class

        Attributes
        ==========

        top_filename: str,
            path to the file containing the top degree sequence, in the
            format:
                node1 degree1
                node2 degree2
        bottom_filename: str,
            path to the file containing the bottom degree sequence, same
            format as top_filename.
        top_degree: list of int,
            list of top nodes degree. Position in list gives node index.
        bot_degree: list of int,
            list of bottom nodes degree. Position in list gives node index.
        top_names: list of str,
            list of the top node names. Position in list gives node index.
        bot_names: list of str,
            list of the bottom node names. Position in list gives node index.
        verbose: bool,
            enable to be more verbose
    """

    def __init__(self, top_filename, bot_filename, top_degree, bot_degree, top_names, bot_names, top_names2idx=None, bot_names2idx=None, verbose=False):
        # Filenames
        self.top_filename = top_filename
        self.bot_filename = bot_filename

        self.verbose = verbose

        # Degree sequences
        if len(top_degree) != len(top_names):
            raise ValueError("Top degree and top names should have the same length.")

        if len(bot_degree) != len(bot_names):
            raise ValueError("Bot degree and bot names should have the same length.")

        self.top_degree = np.array(top_degree, dtype=np.int64)
        self.bot_degree = np.array(bot_degree, dtype=np.int64)

        # Labels
        self.top_names = np.array(top_names)
        self.bot_names = np.array(bot_names)

        # Keep mapping to indexes. Useful when using several bip instances.
        self.top_names2idx = top_names2idx
        self.bot_names2idx = bot_names2idx


        if self.n_top <= 0:
            raise ValueError("Size of top degree is <= 0.")

        if self.n_bot <= 0:
            raise ValueError("Size of bot degree is <= 0.")

        # Check that all top degree values are larger than 0 and less than the number of bottom nodes
        if not np.all((0 < self.top_degree) & (self.top_degree <= self.n_bot)):
            raise ValueError("Not all top degree values are larger than 0 or less than the number of bottom nodes.")

        # Same check for bot degree values
        if not np.all((0 < self.bot_degree) & (self.bot_degree <= self.n_top)):
            raise ValueError("Not all bot degree values are larger than 0 or less than the number of top nodes.")

        # Check that the degree sequences are bigraphic
        if not self.is_bigraphic_gale_ryser():
            raise ValueError("Degree sequences are not bigraphic.")

        if self.verbose:
            print(f"n_top = {self.n_top}")
            print(f"n_bot = {self.n_bot}")
            print(f"Sum top degree = {self.m}")
            print(f"Max top deg = {self.max_top_deg}")
            print(f"Min top deg = {self.min_top_deg}")
            print(f"Max bot deg = {self.max_bot_deg}")
            print(f"Min bot deg = {self.min_bot_deg}")
            print("Bigraphic degree sequences: OK.")

        self.small = True
        if self.n_top > SMALL_SIZE or self.n_bot > SMALL_SIZE:
            self.small = False

        if self.verbose and self.small:
            print(self.__repr__())

        self.initialize_vectors()


    def initialize_vectors(self):
        """Initialize and fill top and bot vectors as well as top index."""
        # Size = sum of top degrees
        # top_index[i] is the index in top_vector at which
        self.top_index = np.zeros(self.n_top, dtype=np.int64)

        # top_vector[i] = j means that
        self.top_vector = np.zeros(self.m, dtype=np.int64)
        self.bot_vector = np.zeros(self.m, dtype=np.int64)

        i = 0
        for v in range(self.n_top):
            self.top_index[v] = i
            for j in range(self.top_degree[v]):
                self.top_vector[i] = v
                i += 1
        assert i == self.m

        i = 0
        for v in range(self.n_bot):
            for j in range(self.bot_degree[v]):
                self.bot_vector[i] = v
                i += 1
        assert i == self.m


    @classmethod
    def from_files(cls, top_filename, bot_filename, keep_idx=False, verbose=False):
        """ Get top and bottom degree list and node names from
            the input files, to initialize bip object.
        """
        if verbose:
            print("Read input degree sequences, and store names")
        top_degree = []
        top_names = []
        bot_degree = []
        bot_names = []

        # keep indexes
        if keep_idx:
            top_names2idx = dict()
            bot_names2idx = dict()
        else:
            top_names2idx = None 
            bot_names2idx = None 

        for (f,degree,names, names2idx) in ((gzip.open(top_filename),top_degree,top_names, top_names2idx),(gzip.open(bot_filename),bot_degree,bot_names, bot_names2idx)):
            for line in f:
                l = line.decode('utf-8').strip().split(" ")
                assert len(l)==2
                names.append(l[0])
                degree.append(int(l[1]))
                if keep_idx:
                    names2idx[l[0]] = len(names) - 1

        return cls(top_filename, bot_filename, top_degree, bot_degree, top_names, bot_names, top_names2idx, bot_names2idx, verbose=verbose)

    @classmethod
    def from_sequences(cls, top_degree, bot_degree, top_names, bot_names, verbose=False):
        """ Initialize bip object from top and bottom degree lists 
            and node names.
        """
        return cls("", "", top_degree, bot_degree, top_names, bot_names, verbose=verbose)

    @property
    def n_top(self):
        """Number of top nodes"""
        return self.top_degree.shape[0]

    @property
    def n_bot(self):
        """Number of bottom nodes"""
        return self.bot_degree.shape[0]

    @property
    def m(self):
        """Number of edges"""
        return sum(self.top_degree)

    @property
    def max_top_deg(self):
        # Handle the special case of empty top degree
        if self.n_top == 0:
            return 0
        return max(self.top_degree)

    @property
    def max_bot_deg(self):
        # Handle the special case of empty bot degree
        if self.n_bot == 0:
            return 0
        return max(self.bot_degree)

    @property
    def min_top_deg(self):
        # Handle the special case of empty top degree
        if self.n_top == 0:
            return 0
        return min(self.top_degree)

    @property
    def min_bot_deg(self):
        # Handle the special case of empty bot degree
        if self.n_bot == 0:
            return 0
        return min(self.bot_degree)

    @property
    def is_multigraph(self):
        neighbors_array = np.zeros(self.n_bot, dtype=np.int64)
        for u in range(self.n_top):
            for i in range(self.top_index[u], self.top_index[u]+self.top_degree[u]):
                v = self.bot_vector[i]
                if neighbors_array[v] != 0:
                    return True
                neighbors_array[v] = 1
            for i in range(self.top_index[u], self.top_index[u]+self.top_degree[u]):
                neighbors_array[self.bot_vector[i]] = 0
        return False

    def reorder_top_decreasing_degree(self):
        mask = np.flip(np.argsort(self.top_degree))
        self.top_degree = self.top_degree[mask]
        self.top_names  = self.top_names[mask]
        self.initialize_vectors()

    def reorder_bot_decreasing_degree(self):
        mask = np.flip(np.argsort(self.bot_degree))
        self.bot_degree = self.bot_degree[mask]
        self.bot_names  = self.bot_names[mask]
        self.initialize_vectors()

    def is_bigraphic_gale_ryser(self):
        return is_bigraphic_gale_ryser(self.top_degree, self.bot_degree)

    def top_neighbors(self, u):
        return set(self.bot_vector[self.top_index[u]:self.top_index[u]+self.top_degree[u]])

    def update_from_vectors(self, top_vector, bot_vector):
        """
        Update bip with the provided vectors.
        This might modify the degree distributions.
        """
        val = -1
        top_degree = []
        top_index = []
        for i,tv in enumerate(top_vector):
            if tv == val:
                top_degree[-1] += 1
            else:
                val += 1
                top_index.append(i)
                top_degree.append(1)
        bot_degree = []
        val = -1
        for bv in bot_vector:
            if bv == val:
                bot_degree[-1] += 1
            else:
                val += 1
                bot_degree.append(1)
        self.top_degree = np.array(top_degree, dtype=np.int64)
        self.bot_degree = np.array(bot_degree, dtype=np.int64)
        self.top_index  = np.array(top_index,  dtype=np.int64)
        self.top_vector = np.array(top_vector, dtype=np.int64)
        self.bot_vector = np.array(bot_vector, dtype=np.int64)

    def swap(self, i, j):
        """Swap edges top_names[i] - bot_names[i] and 
           top_names[j] - bot_names[j]
        """
        self.bot_vector[i],self.bot_vector[j] = self.bot_vector[j],self.bot_vector[i]

    def random_swap(self, i):
        """Given an edge top_names[i] - bot_names[i], randomly pick
           an edge to swap it with.
        """

        self.swap(i, random.randrange(self.m))

    def link_exists(self, u, v):
        """
        Returns True if there exists a link between top node u and bottom node v, else returns False.
        """
        return (v in self.bot_vector[self.top_index[u]:self.top_index[u]+self.top_degree[u]])

    def dump(self, filename):
        """Write the bi-partite graph to file filename."""
        with open(filename,"w") as fp:
            for i in range(self.m):
                fp.write(f"{self.top_names[self.top_vector[i]]} {self.bot_names[self.bot_vector[i]]}\n")

    def __repr__(self):
        string = f"names:\n\t{self.top_names}\n\t{self.bot_names}\ndegrees:\n\t{self.top_degree}\n\t{self.bot_degree}\nlinks:\n\t{self.top_vector}\n\t{self.bot_vector}\n"
        return string
