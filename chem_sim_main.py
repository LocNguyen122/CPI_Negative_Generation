


import pandas as pd
from data_process.data_process import thread_drugbank_dict
from chem_struc_sim.chem_sim_tool import *
from data_process.data_convert import dict_to_csv


if __name__ == '__main__':
    database = pd.read_csv('./database/Drugbank_sample.csv')
    step     = 100
    dict_drug, dict_uniprot, dict_both = thread_drugbank_dict(database, step)
    Jaccard_dict = get_jaccard_score_dict(dict_drug)
    dict_to_csv(Jaccard_dict, 'Jaccard_dict.csv')
    
    
