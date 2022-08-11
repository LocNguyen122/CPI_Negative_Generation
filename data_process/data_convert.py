"""
All convert module


"""


import pubchempy as pcp
from rdkit.Chem import AllChem
from rdkit import Chem
import numpy as np
import pandas as pd


def convert_canonical_smile(smi):
    # Convert smile to canonical
    compound    = pcp.get_compounds(smi, 'smiles')
    if len(compound) == 1:
        canonical   = compound[0].canonical_smiles
    else:
        raise ValueError(f"{len(compound)} compound in this smile")
    return canonical

def convert_2_fingerprint(smi, nBits = 2048):
    # Convert smile to fingerprint
    mol     = Chem.MolFromSmiles(smi)
    fp      = Chem.AllChem.GetMorganFingerprintAsBitVect(mol, useChirality=True, radius=2, nBits = nBits) 
    vec     = np.array(fp)
    return vec

def merge_list_dict(ls):
    result = {}
    for d in ls:
        result.update(d)
    return result

def dict_to_csv(dict, path_save):
    key_ls, value_ls = [], []
    for key, value in dict.items():
        key_ls.append(key)
        value_ls.append(value)
    df = pd.DataFrame(np.vstack(value_ls))
    df.insert(loc=0, column='Name', value=key_ls)
    df.to_csv(path_save, index = False)