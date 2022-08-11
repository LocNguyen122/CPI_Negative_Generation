"""
Data process main


"""

import numpy as np
import pandas as pd
import time
from data_convert import *

database = pd.read_csv('./database/Drugbank_human.csv')


dict_drug, dict_uniprot, dict_both, dict_check = {}, {}, {}, {}

start = time.time()

for idx, row in database[:100].iterrows():
    # Drug data process
    if row['Drugbank_ID'] +'_' + row['Drug_name'] not in dict_drug.keys():
        canonical_smiles = convert_canonical_smile(row['Drug_smile'])
        fp = convert_2_fingerprint(canonical_smiles)
        dict_drug[row['Drugbank_ID'] +'_' + row['Drug_name']] = fp
        dict_check[row['Drugbank_ID'] +'_' + row['Drug_name']] = canonical_smiles
    else:
        canonical_smiles = convert_canonical_smile(row['Drug_smile'])
        if dict_check[row['Drugbank_ID'] +'_' + row['Drug_name']] != canonical_smiles:
            raise ValueError(f"!!! Different fp from drug_ID: {row['Drugbank_ID'] +'_' + row['Drug_name']}")
        else:
            pass
    # Uniprot process
    if row['Uniprot_ID'] not in dict_uniprot.keys():
        dict_uniprot[row['Uniprot_ID']] = row['Uniprot_Seq']
    else:
        if dict_uniprot[row['Uniprot_ID']] != row['Uniprot_Seq']:
            raise ValueError(f"!!! Different Seq from Uniprot_ID: {row['Uniprot_ID']}")
        else:
            pass
    # Both process
    if row['Drugbank_ID'] +'_' + row['Drug_name'] not in dict_both.keys():
        dict_both[row['Drugbank_ID'] +'_' + row['Drug_name']] = row['Uniprot_ID']
    else:
        if dict_both[row['Drugbank_ID'] +'_' + row['Drug_name']] != row['Uniprot_ID']:
            # raise ValueError(f"!!! Different Drugbank_ID from Uniprot_ID: {row['Uniprot_ID']}")
            pass
        else:
            pass
    # print 
    if idx % 100 == 0:
        print(f'Process done {idx} ...')


# df_dict_drug        = pd.DataFrame(data=dict_drug, index=[1])
# df_dict_uniprot     = pd.DataFrame(data=dict_uniprot, index=[1])
# df_dict_both        = pd.DataFrame(data=dict_both, index=[1])

# with open("dict_drug.csv", 'w') as file:
#     for key, value in dict_drug.items():
#         print(value)
#         file.write(f"{key},{value}\n")

with open("dict_uniprot.csv", 'w') as file:
    for key, value in dict_uniprot.items():
        file.write(f"{key},{value}\n")

with open("dict_both.csv", 'w') as file:
    for key, value in dict_both.items():
        file.write(f"{key},{value}\n")

key_ls, value_ls = [], []
for key, value in dict_drug.items():
    key_ls.append(key)
    value_ls.append(value)

# df = pd.DataFrame(list(zip(key_ls, value_ls)),
#                columns =['Drug', 'FP'])

df = pd.DataFrame(np.vstack(value_ls))
df.insert(loc=0, column='Drug', value=key_ls)

df.to_csv("dict_drug.csv", index = False)
print(df)








    
