#include <stdexcept>
#include<iostream>

//#include <unordered_set>
#include <utility>
#include <vector>
#include "edge_swapper.hpp"
//#include <math.h>

namespace swapper {


    RandomSwapper::RandomSwapper () {}

    RandomSwapper::RandomSwapper(int64_t* top_vector, int64_t* bot_vector, int64_t* top_index,  int64_t* top_degree, int64_t n_edges) {

    //RandomSwapper::RandomSwapper (std::unordered_set<swapper::Edge> edge_set) {
        this->n_edges = n_edges;
        this->top_vector = top_vector;
        this->bot_vector = bot_vector;
        this->top_index = top_index;
        this->top_degree = top_degree;
    }

    RandomSwapper::~RandomSwapper () {}
    
     
    // check if a link exists
    bool RandomSwapper::link_exists (std::pair<int64_t,int64_t> edge) {
        int64_t top_idx = edge.first;
        int64_t bot_idx = edge.second;
        //int64_t* top_edge_min = bot_vector + top_idx;
        //int64_t top_u_deg = *(top_degree + top_idx);
        //int64_t* top_edge_max = bot_vector + top_idx + top_u_deg;

        for (int idx = top_idx; idx< top_idx + top_degree[top_idx]; idx++) {
            if (bot_vector[idx] == bot_idx) {
                return true;
            }
        }
        return false;
        //return std::find(top_edge_min, top_edge_max, bot_idx);
        //return std::find(bot_vector + top_idx, bot_vector + top_idx + top_degree, bot_idx)

    }
    
    // replace edges
    void RandomSwapper::swap_edges(std::pair<int64_t,int64_t> edge, std::pair<int64_t,int64_t> other_edge){
        
        bot_vector[edge.first] = other_edge.second;
        bot_vector[other_edge.first] = edge.second;
    }
    
    void RandomSwapper::random_swaps(int N_swaps){
        int n_swap = 0;

        // random seed
        srand (time(0));
        while (n_swap < N_swaps) {
            if (n_swap %1000000 == 0){
                std::cout << n_swap << " done\n"; 
            }

            // pick random edge
            int64_t edge = rand() % n_edges;
            int64_t other_edge = rand() % n_edges;

            // skip case where both random edges are equal
            if (edge == other_edge) {
                continue;
            }

            // edge1 and edge2 are the selected edges, new_edge1 and new_edge2 are the new edges after the swap.
            std::pair<int64_t,int64_t> edge1 = std::make_pair(edge, bot_vector[edge]);
            std::pair<int64_t,int64_t> edge2 = std::make_pair(other_edge, bot_vector[other_edge]);

            std::pair<int64_t,int64_t> new_edge1 = std::make_pair(top_vector[edge], bot_vector[other_edge]);
            std::pair<int64_t,int64_t> new_edge2 = std::make_pair(top_vector[other_edge], bot_vector[edge]);

            // only perform swap if new edges don't already exist
            bool ne1_exists =  link_exists(new_edge1);
            bool ne2_exists =  link_exists(new_edge2);

            if (!ne1_exists && !ne2_exists) {
                swap_edges(edge1, edge2);
                ++n_swap;
            }


        }

    }
    
    int64_t* RandomSwapper::get_top(){
        return top_vector;
    }

    int64_t* RandomSwapper::get_bot(){
        return bot_vector;
    }
}
