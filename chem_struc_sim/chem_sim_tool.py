


from itertools import combinations
from sklearn.metrics import jaccard_score
from math import comb


def get_jaccard_score_dict(dict):
    Jaccard_dict = {}
    c = combinations(dict.keys(), 2)
    print(f'*** Having {len(dict.keys())} -> get {comb(len(dict.keys()), 2)} pairs ***')
    for pair in list(c):
        Jaccard_dict[f'{pair[0]}_{pair[1]}'] == jaccard_score(dict[pair[0]], dict[pair[1]])
    return Jaccard_dict


    