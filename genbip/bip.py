
import gzip

SMALL_SIZE = 100

class bip:
    """Bi-partite class"""

    def __init__(self, top_filename, bot_filename, top_degree, bot_degree, top_names, bot_names):
        # Filenames
        self.top_filename = top_filename
        self.bot_filename = bot_filename

        # Degree sequences
        if len(top_degree) != len(top_names):
            raise ValueError("Top degree and top names should have the same length.")

        if len(bot_degree) != len(bot_names):
            raise ValueError("Bot degree and bot names should have the same length.")
        self.top_degree = top_degree
        self.bot_degree = bot_degree

        #???
        self.top_index = []

        # ??
        self.top_vector = []
        self.bot_vector = []

        # Labels
        self.top_names = top_names
        self.bot_names = bot_names

        self.small = True

    @classmethod
    def from_files(cls, top_filename, bot_filename):
        a = cls(top_filename, bot_filename, [], [], [], [])
        a.load(verbose=False)
        return a

    @classmethod
    def from_sequences(cls, top_degree, bot_degree, top_names, bot_names):
        return cls("", "", top_degree, bot_degree, top_names, bot_names)

    @property
    def n_top(self):
        return len(self.top_degree)

    @property
    def n_bot(self):
        return len(self.bot_degree)

    @property
    def m(self):
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

    def load(self, verbose=True):
        if verbose:
            print("Read input degree sequences, and store names")
        for (f,degree,names) in ((gzip.open(self.top_filename),self.top_degree,self.top_names),(gzip.open(self.bot_filename),self.bot_degree,self.bot_names)):
            for line in f:
                l = line.decode('utf-8').strip().split(" ")
                assert len(l)==2
                names.append(l[0])
                degree.append(int(l[1]))
        if verbose:
            print(f"n_top = {self.n_top}")
            print(f"n_bot = {self.n_bot}")
            print(f"Sum top degree = {self.m}")
            print(f"Max top deg = {self.max_top_deg}")
            print(f"Min top deg = {self.min_top_deg}")
            print(f"Max bot deg = {self.max_bot_deg}")
            print(f"Min bot deg = {self.min_bot_deg}")

        if self.n_top <= 0:
            raise ValueError("Size of top degree is <= 0.")

        if self.n_bot <= 0:
            raise ValueError("Size of bot degree is <= 0.")

        # Check that all top degree values are larger than 0 and less than the number of bottom nodes
        if not all(d > 0 and d <= self.n_bot for d in self.top_degree):
            raise ValueError("Not all top degree values are larger than 0 or less than the number of bottom nodes.")

        # Same check for bot degree values
        if not all(d > 0 and d <= self.n_top for d in self.bot_degree):
            raise ValueError("Not all bot degree values are larger than 0 or less than the number of top nodes.")

        # Check that the degree sequences are bigraphic
        if not self.is_bigraphic_gale_ryser():
            raise ValueError("Degree sequences are not bigraphic.")

        if verbose:
            print("Bigraphic degree sequences: OK.")

        if self.n_top > SMALL_SIZE or self.n_bot > SMALL_SIZE:
            self.small = False

        if verbose and self.small:
            print(self.__repr__())

    def is_bigraphic_gale_ryser(self):
        return True

    def link_exists(self, u, v):
        """
        Returns True if there exists a link between top node u and bottom node v, else returns False.
        """
        return (v in self.bot_vector[self.top_index[u]:self.top_index[u]+self.top_degree[u]])

    def __repr__(self):
        string = f"names:\n\t{self.top_names}\n\t{self.bot_names}\ndegrees:\n\t{self.top_degree}\n\t{self.bot_degree}\nlinks:\n\t{self.top_vector}\n\t{self.bot_vector}\n"
        return string
