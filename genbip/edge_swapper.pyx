# distutils: language = c++
cimport numpy as np
import numpy as np
from cython.operator import dereference

from libcpp cimport bool
from libcpp.vector cimport vector
from libcpp.utility cimport pair

#from genbip.edge_swapper cimport RandomSwapper


def main():
    # This is only to make cython compile the right way (using python.h)
    pass
cdef extern from "share/edge_swapper.cpp":
    # compile cpp file
    pass

cdef extern from "share/edge_swapper.hpp" namespace "swapper":
    cdef cppclass RandomSwapper "swapper::RandomSwapper":
        RandomSwapper() except +
        RandomSwapper(np.int64_t* top_vector, np.int64_t* bot_vector, np.int64_t* top_index,  np.int64_t* top_degree, np.int64_t n_edges) except +

        bool link_exists(int top_index, int bot_index) except +
        # replace all tuples by the two integers ... 
        void swap_edges(pair[int,int] edge, pair[int,int] other_edge) except +
        void random_swaps(int N_swaps) except +
        np.int64_t* get_top() except +
        np.int64_t* get_bot() except +

cdef class pyRandomSwapper():
    cdef RandomSwapper* _this
    cdef np.int64_t size
    def __cinit__(self, top_vector, bot_vector, top_index, top_degree):

        top_size = len(top_vector)
        cdef np.ndarray[np.int64_t, ndim=1] top_vector_c 
        self.size = bot_vector.shape[0]
        top_vector_c = np.ascontiguousarray(top_vector, dtype=np.int64)
        cdef np.ndarray[np.int64_t, ndim=1] bot_vector_c
        bot_vector_c = np.ascontiguousarray(bot_vector, dtype=np.int64)
        cdef np.ndarray[np.int64_t, ndim=1] top_index_c
        top_index_c = np.ascontiguousarray(top_index, dtype=np.int64)
        cdef np.ndarray[np.int64_t, ndim=1] top_degree_c
        top_degree_c = np.ascontiguousarray(top_degree, dtype=np.int64)
        self._this = new RandomSwapper(&top_vector_c[0], &bot_vector_c[0], &top_index_c[0], &top_degree_c[0], len(top_vector))

    def pyRandom_swaps(self, N_swaps):
        self._this.random_swaps(N_swaps)
        cdef np.int64_t* bot_vector
        bot_vector = self._this.get_bot()
        _bot_vector = np.asarray(<np.int64_t [:self.size]> bot_vector)

        return _bot_vector
