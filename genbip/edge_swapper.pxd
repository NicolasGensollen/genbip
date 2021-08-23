from cython.operator import dereference

from libcpp cimport bool
from libcpp.utility cimport pair
from libcpp.vector cimport vector
#from libcpp.unordered_set cimport unordered_set

#cimport numpy as np
#import numpy as np

cdef extern from "share/edge_swapper.cpp":
    # compile cpp file
    pass

cdef extern from "share/edge_swapper.hpp" namespace "swapper":
    cdef cppclass RandomSwapper "swapper::RandomSwapper":
       RandomSwapper() except +
        #RandomSwapper(np.int64_t[::1] top_vector, np.int64_t[::1] bot_vector, np.int64_t[::1] top_index, np.int64_t[::1] bot_index, np.int64_t[::1] top_degree) except +
        #RandomSwapper(np.int64_t* top_vector, np.int64_t* bot_vector, np.int64_t* top_index, np.int64_t* bot_index, np.int64_t* top_degree) except +
        RandomSwapper(int* top_vector, int* bot_vector, int* top_index, int* bot_index, int* top_degree) except +
#        #
#
#        #RandomSwapper( unordered_set[Edge]) except +
#        #vector[Edge] edges
#        bool link_exists(int top_index, int bot_index) except +
#        #void replaceEdge_Array(int, int, Edge, Edge) except +
#        # replace all tuples by the two integers ... 
#        void swap_edges(pair[int,int] edge, pair[int,int] other_edge) except +
#        void random_swaps(int N_swaps) except +
#        int* get_top() except +
#        int* get_bot() except +

