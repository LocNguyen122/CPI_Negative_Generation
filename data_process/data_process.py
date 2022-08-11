"""
Data process main


"""

from msilib.schema import Error
from re import I
import numpy as np
import pandas as pd
import time
from data_process.data_convert import *
from threading import Thread
from multiprocessing import Process

class extract_dict_drugbank(Thread):
    def __init__(self, database, dict_drug_ls, dict_uniprot_ls, dict_both_ls, idx_start, idx_end):
        # super(extract_dict_drugbank, self).__init__()
        Thread.__init__(self)
        self.database       = database
        self.idx_start      = idx_start
        self.idx_end        = idx_end
        self.dict_drug_ls   = dict_drug_ls
        self.dict_uniprot_ls= dict_uniprot_ls
        self.dict_both_ls   = dict_both_ls

        # dict_drug_ls, dict_uniprot_ls, dict_both_ls, idx_start, idx_end

    def __extract_dict(self):
        dict_drug, dict_uniprot, dict_both, dict_check = {}, {}, {}, {}
        for idx, row in self.database[self.idx_start : self.idx_end].iterrows():
            try:

                # Drug data process
                if row['Drugbank_ID'] +'_' + row['Drug_name'] not in dict_drug.keys():
                    try:
                        canonical_smiles = convert_canonical_smile(row['Drug_smile'])
                        try:
                            fp = convert_2_fingerprint(canonical_smiles)
                            dict_drug[row['Drugbank_ID'] +'_' + row['Drug_name']] = fp
                            dict_check[row['Drugbank_ID'] +'_' + row['Drug_name']] = canonical_smiles
                        except:
                            print(f'Fingerprint problems at: {row["Drug_smile"]} at thread {self.idx_start}')
                    except:
                        print(f'canonical_smiles problems at: {row["Drug_smile"]} at thread {self.idx_start}')

                else:
                    canonical_smiles = convert_canonical_smile(row['Drug_smile'])
                    if dict_check[row['Drugbank_ID'] +'_' + row['Drug_name']] != canonical_smiles:
                        raise ValueError(f"!!! Different fp from drug_ID: {row['Drugbank_ID'] +'_' + row['Drug_name']}")
                    else:
                        pass

                # Uniprot process
                try:
                    if row['Uniprot_ID'] not in dict_uniprot.keys():
                        dict_uniprot[row['Uniprot_ID']] = row['Uniprot_Seq']
                    else:
                        if dict_uniprot[row['Uniprot_ID']] != row['Uniprot_Seq']:
                            raise ValueError(f"!!! Different Seq from Uniprot_ID: {row['Uniprot_ID']}")
                        else:
                            pass
                except:
                    print('Error in Uniprot process at thread {self.idx_start}')
                # Both process
                try:
                    if row['Drugbank_ID'] +'_' + row['Drug_name'] not in dict_both.keys():
                        dict_both[row['Drugbank_ID'] +'_' + row['Drug_name']] = row['Uniprot_ID']
                    else:
                        if dict_both[row['Drugbank_ID'] +'_' + row['Drug_name']] != row['Uniprot_ID']:
                            # raise ValueError(f"!!! Different Drugbank_ID from Uniprot_ID: {row['Uniprot_ID']}")
                            pass
                        else:
                            pass
                except:
                    print('Error in Uniprot process at thread {self.idx_start}')
            # # print 
            # if idx % 100 == 0:
            #     print(f'Process done {idx} ...')

            except:
                print(f'Wrong at idx: {idx}')
        return  dict_drug, dict_uniprot, dict_both     

    def run(self):
        # try:
        print(f"Start Thread: {self.idx_start} - {self.idx_end}")
        dict_drug, dict_uniprot, dict_both = self.__extract_dict()
        self.dict_drug_ls.append(dict_drug)
        self.dict_uniprot_ls.append(dict_uniprot)
        self.dict_both_ls.append(dict_both)
        print(f"End Thread: {self.idx_start} - {self.idx_end}")
        # except:
            # print(f"!!! Something went wrong at thread {self.idx_start} - {self.idx_end} !!!")



# if __name__ == '__main__':
#     start_time = time.time()
#     database = pd.read_csv('./database/Drugbank_sample.csv')
#     step = 100
#     idx_ls = [t for t in range(0, len(database), step)]
#     idx_ls.append(len(database) - 2)

#     # idx_ls = [t for t in range(0, 100, int(100/5))] # Test
#     # idx_ls.append(100 -2)
        
#     print(f'All idx split: {idx_ls}')
#     threads = []
#     dict_drug_ls, dict_uniprot_ls, dict_both_ls = [], [], []

#     for i in range(len(idx_ls) - 1):
#         # print(f'Start new thread: {i}')
#         extract = extract_dict_drugbank(database, dict_drug_ls, dict_uniprot_ls, dict_both_ls, idx_ls[i], idx_ls[i+1] + 1)
#         extract.start()
#         threads.append(extract)

#     print('Start join thread')
#     for thread in threads:
#         thread.join()

#     # Merge all dict in list -> type dict
#     dict_drug       = merge_list_dict(dict_drug_ls)
#     dict_uniprot    = merge_list_dict(dict_uniprot_ls)
#     dict_both       = merge_list_dict(dict_both_ls)
    
#     # Save dict 2 csv
#     dict_to_csv(dict_drug, 'dict_drug.csv')
#     dict_to_csv(dict_uniprot, 'dict_uniprot.csv')
#     dict_to_csv(dict_both, 'dict_both.csv')

#     #
#     print ("===== END Main ====")
#     end  = time.time()
#     print(f"Dict Process time: {round((end - start_time)/60 , 2)}") # 2309.532948255539 old 1000 chat -> 11min
    
########################################

def thread_drugbank_dict(database, step, save_csv = False):
    start_time = time.time()
    # Split idx 
    idx_ls = [t for t in range(0, len(database), step)]
    idx_ls.append(len(database) - 1)
    print(f'All idx split: {idx_ls}')
    # Start thread
    threads, dict_drug_ls, dict_uniprot_ls, dict_both_ls = [], [], [], []
    for i in range(len(idx_ls) - 1):
        extract = extract_dict_drugbank(database, dict_drug_ls, dict_uniprot_ls, dict_both_ls, idx_ls[i], idx_ls[i+1] + 1)
        extract.start()
        threads.append(extract)
    print('Start join thread')
    for thread in threads:
        thread.join()
    ### Saving file ###
    if save_csv == True:
    # Merge all dict in list -> type dict
        dict_drug       = merge_list_dict(dict_drug_ls)
        dict_uniprot    = merge_list_dict(dict_uniprot_ls)
        dict_both       = merge_list_dict(dict_both_ls)
    # Save dict 2 csv
        dict_to_csv(dict_drug, 'dict_drug.csv')
        dict_to_csv(dict_uniprot, 'dict_uniprot.csv')
        dict_to_csv(dict_both, 'dict_both.csv')

    end  = time.time()
    ### Print status ###
    print(f"Dict Process time: {round((end - start_time)/60 , 2)}") # 2309.532948255539 old 1000 chat -> 11min
    print ("===== END Thread Drugbank ====")
    return dict_drug, dict_uniprot, dict_both

