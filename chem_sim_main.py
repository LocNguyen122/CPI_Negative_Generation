


import time
import pandas as pd
from data_process.data_process import thread_drugbank_dict
from chem_struc_sim.chem_sim_tool import *
from data_process.data_convert import dict_to_csv


if __name__ == '__main__':
    start_time = time.time()
    database = pd.read_csv('./database/Drugbank_human.csv')
    step     = 200
    dict_drug, dict_uniprot, dict_both  = thread_drugbank_dict(database, step)
    Jaccard_dict = get_jaccard_score_dict(dict_drug)
    dict_to_csv(Jaccard_dict, 'Jaccard_dict.csv')

    end  = time.time()
    print(f"Process time: {end - start_time}")

    
