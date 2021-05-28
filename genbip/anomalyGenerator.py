"""
    TODO : still some work to clarify how to add anomaly...
    Given top and bottom degree sequences, and anomaly parameters,
    generate an anomaly using an Erdos Renyi model, and randomly select nodes
    with high enough degree to 'host' the anomaly. Substract the anomaly 
    degrees to the node degrees.
"""
import logging
import numpy as np

from genbip.bip import bip

class AnomalyGenerator():

    def __init__(self, n_anomaly, m_anomaly, seed=None, logger=None):
        # anomaly parameters
        self.n_anomaly = n_anomaly
        self.m_anomaly = m_anomaly

        # random seed
        if seed is not None:
            np.random.seed(seed)

        if logger is not None:
            self.logger = logger
        else:
            logging.basicConfig(
                    level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M'
                    )
            self.logger = logging.getLogger()


    def generate_anomaly(self):
        """ Generate anomaly by picking random nodes (u,v), 
            u in top nodes and v in bottom nodes, and adding (u,v) to graph
            if (u,v) doesn't already exist.
            TODO: for now same number of nodes in top and bottom
        """
        top_names = list(range(self.n_anomaly))
        bot_names = list(range(self.n_anomaly))
        
        # prick m_anomaly random edges
        n_edges = 0
        edges = []
        while (n_edges < self.m_anomaly):
            u_idx = np.random.choice(self.n_anomaly)
            v_idx = np.random.choice(self.n_anomaly)
            if (u_idx, v_idx) in edges:
                continue
            
            edges.append((u_idx, v_idx))
            n_edges += 1
        
        # get top and bot vectors
        prev_u = -1
        top_degree = np.zeros(self.n_anomaly, dtype=np.int64)
        bot_degree = np.zeros(self.n_anomaly, dtype=np.int64)
        top_vector = []
        bot_vector = []
        for u_idx, v_idx in edges:
            top_vector.append(top_names[u_idx])
            bot_vector.append(bot_names[v_idx])
            top_degree[u_idx] += 1
            bot_degree[v_idx] += 1
        
        # sort bot and top vector to have top vector ordered
        vectors = sorted(zip(top_vector, bot_vector), key= lambda x:x[0])
        top_vector = [u for u,v in vectors]
        bot_vector = [v for u,v in vectors]
        
        # generate top index
        top_index = np.zeros(self.n_anomaly, dtype=np.int64)
        prev_node = -1
        n_idx = 0 # node index
        for u_idx in range(self.m_anomaly):
            if top_vector[u_idx] != prev_node:
                top_index[n_idx] = u_idx
                n_idx += 1
                prev_node = top_vector[u_idx]
            else:
                continue
    
        # initialize bip
        return bip(top_filename=None, bot_filename=None,
                  top_degree=top_degree,
                  bot_degree=bot_degree,
                  top_names=top_names, bot_names=bot_names), edges
    
    def select_nodes_anomaly(self, an_bip, norm_bip, edges, seed=None):
        """ Select nodes on bipartite Global graph on which to 'plug' 
        the anomaly. A node can be chosen if it has high enough degree
        """
        if seed is not None:
            np.random.seed(seed)
    
        # get nodes 
        # assume anomaly generated
        has_duplicate = True
        top_selection = []
        bot_selection = []
        top_mapping = {}
        bot_mapping = {}
        top_anomaly2norm = {}
        bot_anomaly2norm = {}

        # loop until top nodes have been place without independently
        # without replacement
        while (has_duplicate):
            for an_node, an_degree in enumerate(an_bip.top_degree):
    
                # nodes with degree high enough
                candidates = np.where(norm_bip.top_degree >= an_degree)
                candidate_idx = np.random.choice(candidates[0])

                # check if node has already been selected
                if candidate_idx in top_selection:
                    has_duplicate = True
                    top_selection = []
                    top_mapping = {}
                    top_anomaly2norm = {}
                    break
                else:
                    top_selection.append(candidate_idx)
                    top_mapping[an_node] = candidate_idx
                    top_anomaly2norm[candidate_idx] = an_node
            else:
                has_duplicate = False

        # same process with bot nodes
        has_duplicate=True
        while (has_duplicate):
            for an_node, an_degree in enumerate(an_bip.bot_degree):
                candidates = np.where(norm_bip.bot_degree >= an_degree)
                candidate_idx = np.random.choice(candidates[0])
    
                if candidate_idx in bot_selection:
                    has_duplicate = True
                    bot_selection = []
                    bot_mapping  = {}
                    bot_anomaly2norm = {}
                    break
                else:
                    bot_selection.append(candidate_idx)
                    bot_mapping[an_node] =  candidate_idx
                    bot_anomaly2norm[candidate_idx] = an_node
            else:
                has_duplicate = False

        # get remaining degrees for 'normal' bipartite
        for an_degree, norm_top_idx in zip(an_bip.top_degree,top_selection):
            norm_bip.top_degree[norm_top_idx] -= an_degree
    
        for an_degree, norm_bot_idx in zip(an_bip.bot_degree, bot_selection):
            norm_bip.bot_degree[norm_bot_idx] = norm_bip.bot_degree[norm_bot_idx] - an_degree
        norm_bip.initialize_vectors()
    
        # store anomaly edges to check for multiple edges later
        anomaly_edges = []
        for u_idx, v_idx in edges:
            anomaly_edges.append((top_mapping[u_idx], bot_mapping[v_idx]))
    
        return anomaly_edges
    
    
    def check_multiple_edges(self, norm_bip, anomaly_edges, seed=None):
        """ check that there are no multiple edges between 'normal graph' and 
            'anomaly' graph
        """
        if seed is not None:
            np.random.seed(seed)

        # get all multiple edges
        multiple_edges = []
        for top_pos, _ in enumerate(norm_bip.top_index[:-1]):
            for vect_idx in range(norm_bip.top_index[top_pos], norm_bip.top_index[top_pos + 1]):
                edge = (norm_bip.top_vector[vect_idx], norm_bip.bot_vector[vect_idx])
                if edge in anomaly_edges:
                    multiple_edges.append(vect_idx)

        return multiple_edges
    
    def target_multiple_edges(self, norm_bip, an_bip, anomaly_edges, multiple_edges, seed=None):
        """when a multiple edge is detected, swap it with a randomly pick edge
          to get simple graph"""
        if seed is not None:
            np.random.seed(seed)

        # swap specifically multiple edges
        n_swap = 0
        for edge in multiple_edges:
            accepted = False

            # loop until a swap is accepted
            while (not accepted):#n_swap <len(multiple_edges):
                

                other_edge = np.random.choice(norm_bip.m)
                if other_edge == edge:
                    continue
                
                # check if multiple edge
                new_edge1 = (norm_bip.top_vector[edge], norm_bip.bot_vector[other_edge])
                new_edge2 = (norm_bip.top_vector[other_edge], norm_bip.bot_vector[edge])
                if new_edge1 in anomaly_edges or new_edge2 in anomaly_edges: 
                    continue

                # if edge doesn't already exist, accept swap 
                if not norm_bip.link_exists(norm_bip.top_vector[edge], norm_bip.bot_vector[other_edge]):
                    n_swap += 1
                    edge1 =  (norm_bip.top_vector[edge], norm_bip.bot_vector[edge])
                    edge2 =  (norm_bip.top_vector[other_edge], norm_bip.bot_vector[other_edge])
                    accepted = True
                    norm_bip.swap(edge,other_edge)

    def _swap_edges(self, edge, bip, other_bip, other_edges, mapping):
        other_edge = np.random.choice(bip.m)
        if other_edge == edge:
            return
        
        # check if multiple edge
        new_edge1 = (bip.top_vector[edge], bip.bot_vector[other_edge])
        new_edge2 = (bip.top_vector[other_edge], bip.bot_vector[edge])
        #if new_edge1 in anomaly_edges or new_edge2 in other_edges: 
        #    continue
        if (other_bip.link_exists(mapping[new_edge1[0]], mapping[new_edge1[1]]) or
            other_bip.link_exists(mapping[new_edge1[0]], mapping[new_edge1[1]])):
            return

        # if edge doesn't already exist, accept swap 
        if not bip.link_exists(bip.top_vector[edge], bip.bot_vector[other_edge]):
            n_swap += 1
            edge1 =  (bip.top_vector[edge], bip.bot_vector[edge])
            edge2 =  (bip.top_vector[other_edge], bip.bot_vector[other_edge])
            accepted = True
            bip.swap(edge,other_edge)

