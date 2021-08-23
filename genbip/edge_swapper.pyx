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
        #bool link_exists(int top_index, int bot_index) except +
        RandomSwapper() except +
        #RandomSwapper(np.int64_t[::1] top_vector, np.int64_t[::1] bot_vector, np.int64_t[::1] top_index, np.int64_t[::1] bot_index, np.int64_t[::1] top_degree) except +
        RandomSwapper(np.int64_t* top_vector, np.int64_t* bot_vector, np.int64_t* top_index,  np.int64_t* top_degree, np.int64_t n_edges) except +
        #RandomSwapper(int* top_vector, int* bot_vector, int* top_index, int* bot_index, int* top_degree) except +
        #

        bool link_exists(int top_index, int bot_index) except +
        #void replaceEdge_Array(int, int, Edge, Edge) except +
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
        #cdef np.ndarray[npndarray, ndim=1, mode="c"] top_vector_c
        cdef np.ndarray[np.int64_t, ndim=1] top_vector_c 
        #cdef np.int64_t[::1] top_vector_c 
        self.size = bot_vector.shape[0]
        print(self.size)
        print(bot_vector[:20])
        print(bot_vector[-20:])
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
        #cdef np.ndarray[np.int64_t, ndim=1] top_vector# = <float [:cpp_vector.size()]>cpp_vector.data()

        #cdef np.ndarray[np.int64_t, ndim=1] bot_vector# = <float [:cpp_vector.size()]>cpp_vector.data()
        cdef np.int64_t* bot_vector
        #top_vector = self._this.get_top().data()
        bot_vector = self._this.get_bot()
        #_bot_vector = <np.int64_t [:40]> bot_vector
        _bot_vector = np.asarray(<np.int64_t [:self.size]> bot_vector)

        print(len(_bot_vector))
        print(_bot_vector[:20])
        print(_bot_vector[-20:])
        #return top_vector, bot_vector
        return _bot_vector
#
#
##class Main():
##    def __init__():
##        a=None
##        pass
##
##a=None
