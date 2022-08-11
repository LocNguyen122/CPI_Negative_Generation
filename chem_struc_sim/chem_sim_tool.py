


from itertools import combinations
from sklearn.metrics import jaccard_score
from math import comb


def get_jaccard_score_dict(dict):
    print('*** Start calculate Jaccard score ***')
    Jaccard_dict = {}
    c = combinations(dict.keys(), 2)
    print(f'*** Having {len(dict.keys())} -> get {comb(len(dict.keys()), 2)} pairs ***')
    for pair in list(c):
        # print(jaccard_score(dict[pair[0]], dict[pair[1]]))
        key = f'{pair[0]}&{pair[1]}'
        Jaccard_dict[key] = jaccard_score(dict[pair[0]], dict[pair[1]])
    return Jaccard_dict


    