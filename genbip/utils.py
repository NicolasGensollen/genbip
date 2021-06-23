import ipdb
import numpy as np


def linear_sort(sequence):
    """Sort the provided sequence in linear time and return the sorted sequence."""
    xmax = max(sequence)
    nb = [0] * (xmax+1)
    sorted = [0] * len(sequence)
    pos = [0] * (xmax+1)
    for x in sequence:
        nb[x] += 1
    for x in range(1, xmax+1):
        pos[x] = pos[x-1] + nb[x-1]
    for x in sequence:
        sorted[pos[x]] = x
        pos[x] += 1
    # check; may be removed
    #assert all(sorted[i]<=sorted[i+1] for i in range(len(sorted)-1))
    #freq = [0] * (xmax+1)
    #for x in sorted:
    #    freq[x] += 1
    #for x in sequence:
    #    freq[x] -= 1
    #assert freq == [0] * (xmax+1)
    return sorted

def conjugate(seq):
    resu = np.zeros(max(seq)+1, dtype=np.int64)
    for x in seq:
        resu[x] += 1
    for i in range(len(resu)-2,-1,-1):
        resu[i] += resu[i+1]
    return(resu)

def is_bigraphic_gale_ryser(seq1, seq2):
    a = np.flip(np.sort(seq1))
    b = np.sort(seq2)
    if sum(a) != sum(b):
        return False
    bprime = conjugate(b)
    a_sum = 0
    bprime_sum = 0
    for i in range(min(len(a),len(bprime))):
        a_sum += a[i]
        bprime_sum += bprime[i]
        if a_sum > bprime_sum:
            return False
    return True

def map_bip_names(bip, other_bip):
    """ When two seperate bip instance share the same nodes, with one
        set included in the other, this maps the position of the names from
        one set to the other
    """
    # loop over nodes names of bip
    # assume bip is smaller than other_bip
    top_bip2other = dict()
    top_other2bip = dict()
    bot_bip2other = dict()
    bot_other2bip = dict()

    # map top names indexes
    # parcourir top_names le plus grand
    for idx, name in enumerate(bip.top_names):
        #try:
        #    other_idx = np.where(other_bip.top_names == name)[0][0]
        #except:
        #    # if node isn't in othe graph, shouldn't happen
        #    # but can if bip is normal and other_bip is anomaly
        #    continue
        if name in other_bip.top_names2idx:
            other_idx = other_bip.top_names2idx[name]
        top_bip2other[idx] = other_idx
        top_other2bip[other_idx] = idx

    # map bot names indexes
    for idx, name in enumerate(bip.bot_names):
        #try:
        #    other_idx = np.where(other_bip.bot_names == name)[0][0]
        #except:
        #    # if node isn't in othe graph, shouldn't happen
        #    # but can if bip is normal and other_bip is anomaly
        #    continue
        if name in other_bip.bot_names2idx:
            other_idx = other_bip.bot_names2idx[name]
        bot_bip2other[idx] = other_idx
        bot_other2bip[other_idx] = idx

    ## parcourir les array en indexant
    return top_bip2other, top_other2bip, bot_bip2other, bot_other2bip

def check_multiple(normal_bip, anomaly_bip, mappers):
    """ check multiple edges between normal and anomaly bip"""

    def _compare_neighbours(bip, u, other_bip, other_u, top_mapper, bot_mapper):
        """given a node u present in two bip, compare their neighbours"""
        common_neighbours = []
        #ipdb.set_trace()
        for v_idx, v in enumerate(bip.bot_vector[bip.top_index[u]: bip.top_index[u] + bip.top_degree[u]]):

            # check if bot node exist in other bip
            if not (bip.bot_names[v] in other_bip.bot_names):
                continue

            # get corresponding v in other bip - TODO might do mapping..?
            #other_v = np.where(other_bip.bot_names == bip.bot_names[v])[0][0]
            #ipdb.set_trace()
            try:
                other_v = bot_mapper[v]
            except:
                ipdb.set_trace()
                other_v = bot_mapper[v]
            # check if other_v is a neighbour of other_u
            try:
                other_vIdx = np.where(other_bip.bot_vector[other_bip.top_index[other_u]:other_bip.top_index[other_u]+other_bip.top_degree[other_u]] == other_v)[0][0]
                common_neighbours.append((v_idx+bip.top_index[u], other_vIdx + other_bip.top_index[other_u]))
            except IndexError:
                continue

            #if other_bip.link_exists(other_u, other_v):
            #    common_neighbours.append(v, other_v)
            #else:
            #    continue
        return common_neighbours
    top_an2norm, top_norm2an, bot_an2norm, bot_norm2an = mappers

    multiedges = []
    #print('multiple edges check')
    #print(normal_bip)
    #print(anomaly_bip)
    #ipdb.set_trace()
    for u_an, u_anName in enumerate(anomaly_bip.top_names):
        #u_anIdx = anomaly_bip.top_names.index(u)
        _u_norm = np.where(normal_bip.top_names == u_anName)[0]#[0]
        if len(_u_norm) == 0:
            continue
        u_norm = _u_norm[0]
        # iterate in graph in which node has smallest degree
        if normal_bip.top_degree[u_norm] > anomaly_bip.top_degree[u_an]:
            #print('parkour anomaly')
            _multiedge = _compare_neighbours(anomaly_bip, u_an, normal_bip, u_norm, top_an2norm, bot_an2norm)
            # keep normal bot index as first
            multiedges += [(v2, v1) for v1, v2 in _multiedge]
        else:
            #print('parkour normal')
            _multiedge = _compare_neighbours(normal_bip, u_norm, anomaly_bip, u_an, top_norm2an, bot_norm2an)
            multiedges += _multiedge

        ## when multiple edge detected, add to list to be swapped later
        #if is_multiedge:
        #    multiedge.append((u, v))
        #norm_deg = top_degree
        #an_deg = an_degree
        # parcourir celui de degré plus faible à chaque fois
    return multiedges

def swap_multiple(normal_bip, anomaly_bip, multiple_edges, mappers, logger):
    """ target multiple edges to swap them"""

    def _swap_edges(bip, other_bip, i, other_i, top_mapper, bot_mapper, logger, threshold=500):
        acceptable = False
        u = bip.top_vector[i]

        #other_u = other_bip.top_vector[other_i]
        other_u = top_mapper[u]
        v = bip.bot_vector[i]
        #other_v = other_bip.bot_vector[other_i]
        other_v = bot_mapper[v]

        # break when can't find acceptable swap after threshold try
        idx_try = 0
        while not acceptable and idx_try < threshold:
            #j = random.randrange(bip.m)
            j = np.random.randint(low=0, high=bip.m)

            # get index of same bot node in other bip
            new_v = bip.bot_vector[j]
            if bip.bot_names[new_v] in other_bip.bot_names:
                #other_v = np.where(other_bip.bot_names == bip.bot_names[new_v])[0][0]
                other_new_v = bot_mapper[new_v]
                if bip.link_exists(bip.top_vector[i], bip.bot_vector[j]) or other_bip.link_exists(other_u, other_v):
                    acceptable = False
                    logger.debug('not accepting swap')
                    idx_try += 1
                else:
                    acceptable = True
                    idx_try = 0
            elif bip.link_exists(bip.top_vector[i], bip.bot_vector[j]):
                    logger.debug('not accepting swap')
                    acceptable = False
                    idx_try += 1

            #if v in other_bip.bot_vector:
            #    other_j = other_bip.bot_vector[other_bip.top_index[other_u]:other_bip.top_index[other_u] + other_bip.top_degree[other_u]].index(v)

            # check if acceptable 
        if idx_try >= threshold:
            raise RuntimeError('Unable to find acceptable swap in Edge swap')
        bip.swap(u,v)
    top_an2norm, top_norm2an, bot_an2norm, bot_norm2an = mappers
    # swap each multiple edge
    logger.debug('{} multiple edge to swap'.format(len(multiple_edges)))
    for norm_idx, an_idx in multiple_edges:
        if np.random.uniform(0,1) >= 0.5:
            #normal_bip.random_swap(u)
            _swap_edges(normal_bip, anomaly_bip, norm_idx, an_idx, top_norm2an, bot_norm2an)
        else:
            _swap_edges(anomaly_bip, normal_bip, an_idx, norm_idx, top_an2norm, bot_an2norm)

