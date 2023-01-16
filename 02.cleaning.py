"""
@author: annegaelle-sng
"""

# This is the part 2 of cosmetic recommendation: analyzing cosmetic items similarities based on their ingredients
# You can also daownload the csv file from same repository: cosmetic.csv

import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt

# step 1. cleaning data
cosm_data = pd.read_csv('datasets/cosmetic.csv')
cosm_data.info()

#Label
cosm_data.Label[cosm_data['Label'] == 'laver'] = str('Wash')
cosm_data.Label[cosm_data['Label'] == 'soi'] = str('Treatment')
cosm_data.Label[cosm_data['Label'] == 'coiffer'] = str('Styling')

# name -> duplicated item
df_2 = cosm_data['name'].drop_duplicates()

df_2.head()



