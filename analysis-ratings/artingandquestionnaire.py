# -*- coding: utf-8 -*-
"""
Created on Sun Oct  2 17:19:20 2022

@author: milad
"""

#% correlation between ratings and questionnaires

# import sys 

#%%
import os
os.chdir('C:/Users/milad/Desktop/D/vr-social-closeness')
from glob import glob
from utils.subject import Subject
import numpy as np 
import pandas as pd 

import json
with open('./utils/dirs.json') as f:
    dirs = json.load(f)

from matplotlib import pyplot as plt
import seaborn as sns
from scipy.stats import ttest_rel

#%%
sub_dirs = []  

group_name = ['synch_folder',
              'unsynch_folder',
              'unsynch_random_folder']

for study_group in group_name: 
     data_root = os.path.join(dirs['data'], study_group)
     sub_dirs.extend(glob(os.path.join(data_root, '*')))

subjects = [Subject(path) for path in  sub_dirs]
#%%
sub_id = []
sub_group = []
for i,sb in enumerate(subjects): 
    questionnaire_pth = glob(sb.path+'/panas1/*.csv')
    questionnaire_df = pd.read_csv(questionnaire_pth [0])
