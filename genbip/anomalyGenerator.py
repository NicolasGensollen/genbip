import numpy as np

from genbip.bip import bip

def generate_anomaly(n_anomaly, m_anomaly, seed = None):
    if seed is not None:
        np.random.seed(seed)
    ## TODO move to bip.py as "from_n_m" ?
    ## TODO allow different number of top/bottom nodes .. ? 
    top_names = list(range(n_anomaly))
    bot_names = list(range(n_anomaly))
    
    # prick rdm edges
    n_edges = 0
    edges = []
    while (n_edges < m_anomaly):
        u_idx = np.random.choice(n_anomaly)
        v_idx = np.random.choice(n_anomaly)
        if (u_idx, v_idx) in edges:
            continue
        
        edges.append((u_idx, v_idx))
        n_edges += 1
    
    # get top and bot vectors
    prev_u = -1
    top_degree = np.zeros(n_anomaly, dtype=np.int64)
    bot_degree = np.zeros(n_anomaly, dtype=np.int64)
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
    top_index = np.zeros(n_anomaly, dtype=np.int64)
    prev_node = -1
    n_idx = 0 # node index
    for u_idx in range(m_anomaly):
        if top_vector[u_idx] != prev_node:
            top_index[n_idx] = u_idx
            n_idx += 1
            prev_node = top_vector[u_idx]
        else:
            continue

    # initialize bip
    #ipdb.set_trace()
    return bip(top_filename=None, bot_filename=None,
              top_degree=top_degree,
              bot_degree=bot_degree,
              top_names=top_names, bot_names=bot_names), edges

def select_nodes_anomaly(an_bip, norm_bip,edges, seed=None):
    if seed is not None:
        np.random.seed(seed)

    # get nodes 
    #assume anomaly generated
    has_duplicate = True
    top_selection = []
    bot_selection = []
    top_mapping = {}
    bot_mapping = {}
    #ipdb.set_trace()
    while (has_duplicate):
        for an_node, an_degree in enumerate(an_bip.top_degree):
            #ipdb.set_trace()

            candidates = np.where(norm_bip.top_degree >= an_degree)
            candidate_idx = np.random.choice(candidates[0])

            if candidate_idx in top_selection:
                has_duplicate = True
                top_selection = []
                top_mapping = {}
                break
            else:
                top_selection.append(candidate_idx)
                top_mapping[an_node] = candidate_idx
        else:
            has_duplicate = False
    has_duplicate=True
    while (has_duplicate):
        for an_node, an_degree in enumerate(an_bip.bot_degree):
            candidates = np.where(norm_bip.bot_degree >= an_degree)
            candidate_idx = np.random.choice(candidates[0])

            if candidate_idx in bot_selection:
                has_duplicate = True
                bot_selection = []
                bot_mapping  = {}
                break
            else:
                bot_selection.append(candidate_idx)
                bot_mapping[an_node] =  candidate_idx
        else:
            has_duplicate = False
    for an_degree, norm_top_idx in zip(an_bip.top_degree,top_selection):
        norm_bip.top_degree[norm_top_idx] -= an_degree

    for an_degree, norm_bot_idx in zip(an_bip.bot_degree, bot_selection):
        norm_bip.bot_degree[norm_bot_idx] = norm_bip.bot_degree[norm_bot_idx] - an_degree
    norm_bip.initialize_vectors()

    #anomaly_edges = {}
    anomaly_edges = []
    for u_idx, v_idx in edges:
        anomaly_edges.append((top_mapping[u_idx], bot_mapping[v_idx]))

        #if top_mapping[u_idx] in anomaly_edges:
        #    anomaly_edges[vtop_mapping[u_idx]].append(bot_mapping[v_idx])
        #else:
        #    anomaly_edges[top_mapping[u_idx]] = [bot_mapping[v_idx]]
    return anomaly_edges


def check_multiple_edges(norm_bip, anomaly_edges, seed=None):
    if seed is not None:
        np.random.seed(seed)
    multiple_edges = []
    for top_pos, _ in enumerate(norm_bip.top_index[:-1]):
        for vect_idx in range(norm_bip.top_index[top_pos], norm_bip.top_index[top_pos + 1]):
            edge = (norm_bip.top_vector[vect_idx], norm_bip.bot_vector[vect_idx])
            #norm_edges.add((norm_bip.top_vector[vect_idx], norm_bip.bot_vector[vect_idx]))
            #norm_edges.add(edge)
            if edge in anomaly_edges:
                multiple_edges.append(vect_idx)
    return multiple_edges

def target_multiple_edges(norm_bip, an_bip, anomaly_edges, multiple_edges, seed=None):
    if seed is not None:
        np.random.seed(seed)
    ### swap specifically multiple edges
    n_swap = 0
    for edge in multiple_edges:
        accepted = False
        while (not accepted):#n_swap <len(multiple_edges):
            other_edge = np.random.choice(norm_bip.m)
            if other_edge == edge:
                continue
            
            # check if multiple edge
            new_edge1 = (norm_bip.top_vector[edge], norm_bip.bot_vector[other_edge])
            new_edge2 = (norm_bip.top_vector[other_edge], norm_bip.bot_vector[edge])
            if new_edge1 in anomaly_edges or new_edge2 in anomaly_edges: 
                continue

            if not norm_bip.link_exists(norm_bip.top_vector[edge], norm_bip.bot_vector[other_edge]):
                n_swap += 1
                edge1 =  (norm_bip.top_vector[edge], norm_bip.bot_vector[edge])
                edge2 =  (norm_bip.top_vector[other_edge], norm_bip.bot_vector[other_edge])
                accepted = True
                norm_bip.swap(edge,other_edge)


