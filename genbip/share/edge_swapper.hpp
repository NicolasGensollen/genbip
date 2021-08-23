#ifndef EDGE_SWAPPER_HPP_
#define EDGE_SWAPPER_HPP_

//#include <numpy/arrayobject.h>
//#include <cstdint>
#include <cmath>
#include <sstream>
#include <complex>
#include <math.h>
#include <array>
#include <tuple>
#include <iostream>
//#include <limits>
//#include <stdexcept>
//#include <unordered_set>
#include <utility>
#include <vector>

//using namespace std;

namespace swapper {


    class RandomSwapper {
        public: 
            //std::vector<int> top_vector;
            //std::vector<int> bot_vector;
            int64_t* top_vector;
            int64_t* bot_vector;
            int64_t* top_index;
            int64_t* top_degree;
            int64_t  n_edges;
            RandomSwapper();
            //RandomSwapper(std::vector<int> top_vector, std::vector<int> bot_vector);
            RandomSwapper(int64_t* top_vector, int64_t* bot_vector, int64_t* top_index, int64_t* top_degree, int64_t n_edges);
            ~RandomSwapper();

             
            // check if link exists
            bool link_exists(std::pair<int64_t, int64_t> edge);
             
            // replace edges
            void swap_edges (std::pair<int64_t,int64_t> edge, std::pair<int64_t,int64_t> other_edge);
            
            // perform all edges swaps
            void random_swaps (int N_swaps);

            // get edges
            //std::vector<int> get_top();
            //std::vector<int> get_bot();
            int64_t* get_top();
            int64_t* get_bot();

    };
}


#endif
