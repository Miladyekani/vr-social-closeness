# -*- coding: utf-8 -*-
"""
Created on Sat Oct  1 18:02:13 2022

@author: milad
"""

import sys 
import os 
sys.path.append(os.path.join('C:\\','Users','milad','Desktop','D',
                               'Thesis_Phd','codes'))
from glob import glob
from subject import Subject
import numpy as np 
import pandas as pd 
from matplotlib import pyplot as plt
import seaborn as sns
from scipy.stats import f_oneway as anova
import scikit_posthocs as sp

Sub_Address = []  
group_name = ['synch_folder','unsynch_folder','unsynch_random_folder']

synch_socialcloseness =[]
unsynch_socialcloseness = [] 
random_socialcloseness = []

for study_group in group_name: 
     Data_Root =  os.path.join('C:\\','Users','milad','Desktop','D',
                               'Thesis_Phd','data','raw_data', study_group)
     Sub_Address.extend( glob(os.path.join(Data_Root,'*')))

subjects = [Subject(path ) for path in  Sub_Address]
for sb in subjects : 
    if sb.name != 'amir_azadi' and sb.name != 'shahin_hajizade' :
        sb.loadVrQuestionnaire()
        quesoionare = sb.VR
        if sb.group == 'synch_folder':
           synch_socialcloseness.append(quesoionare['SocialClosness_score'][0])
        if sb.group == 'unsynch_folder':
           unsynch_socialcloseness.append(quesoionare['SocialClosness_score'][0])
        if sb.group == 'unsynch_random_folder':
           random_socialcloseness.append(quesoionare['SocialClosness_score'][0])

df = pd.DataFrame(data={
    'scn': np.concatenate([synch_socialcloseness, 
                           unsynch_socialcloseness, 
                           random_socialcloseness]), 
    'grp': np.concatenate([np.full((len(synch_socialcloseness), 1), "synch", dtype=object),
                           np.full((len(unsynch_socialcloseness), 1), "unsynch", dtype=object),
                           np.full((len(random_socialcloseness), 1), "random", dtype=object)]).flatten()})
fig, ax = plt.subplots(1, 1, figsize=(16, 9))
sns.barplot(x="grp", y="scn", data=df, alpha=.2, errwidth=5)
sns.stripplot(x="grp", y="scn", data=df, size=10)
ax.set_ylabel("")
ax.set_xlabel("")
ax.tick_params(axis='both', which='major', labelsize=28)
ax.set_title(key, fontsize=36)
sns.despine()
fig.tight_layout()

print(sp.posthoc_ttest(df, val_col='scn', group_col='grp', p_adjust='holm'))
print("")