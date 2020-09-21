
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
    resu = [0 for x in range(max(seq)+1)]
    for x in seq:
        resu[x] += 1
    for i in range(len(resu)-2,-1,-1):
        resu[i] += resu[i+1]
    return(resu)

def is_bigraphic_gale_ryser(seq1, seq2):
    a = np.sort(seq1)
    a = np.flip(a)
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

