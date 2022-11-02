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


rated_varaibles =    ['IOS', 'Bound', 'likability', 'Similarity', 'Willing_to_know_others',
                      'Willing_to_help_other', 'Willing_to_recieve_help', 'Fun_in_vr', 
                      'Embaracment or annoyed', 'Hardness of moves', 'ENjoyment_in_vr', 
                      'Sucess_in_moves', 'Synchrony', 'Mimivking', 'Lightining', 'Being_mimicked', 
                      'Controled_by_real', 'Accomponied', 'Controlling_environment', 
                      'Controlled_by_environment', 'SocialClosness_score']

synch_rate=[]
unsynch_rate= [] 
random_rate = []
i=0 

    
for study_group in group_name: 
     Data_Root =  os.path.join('C:\\','Users','milad','Desktop','D',
                               'Thesis_Phd','data','raw_data', study_group)
     Sub_Address.extend( glob(os.path.join(Data_Root,'*')))

subjects = [Subject(path ) for path in  Sub_Address]
for i in rated_varaibles: 
        for sb in subjects : 
            if sb.name != 'amir_azadi' and sb.name != 'shahin_hajizade' :
                sb.loadVrQuestionnaire()
                quesoionare = sb.VR
                if sb.group == 'synch_folder':
                   synch_rate.append(quesoionare[i][0])
                if sb.group == 'unsynch_folder':
                   unsynch_rate.append(quesoionare[i][0])
                if sb.group == 'unsynch_random_folder':
                   random_rate.append(quesoionare[i][0])
        
        df = pd.DataFrame(data={
            'scn': np.concatenate([synch_rate, 
                                   unsynch_rate, 
                                   random_rate]), 
            'grp': np.concatenate([np.full((len(synch_rate), 1), "synch", dtype=object),
                                   np.full((len(unsynch_rate), 1), "unsynch", dtype=object),
                                   np.full((len(random_rate), 1), "random", dtype=object)]).flatten()})
        fig, ax = plt.subplots(1, 1, figsize=(16, 9))
        sns.barplot(x="grp", y="scn", data=df, alpha=.2, errwidth=5)
        sns.stripplot(x="grp", y="scn", data=df, size=10)
        ax.set_ylabel("")
        ax.set_xlabel("")
        ax.tick_params(axis='both', which='major', labelsize=28)
        #ax.set_title(key, fontsize=36)
        ax.set(title=i)
        sns.despine()
        fig.tight_layout()
        print(i)
        print(sp.posthoc_ttest(df, val_col='scn', group_col='grp', p_adjust='holm'))
        print("")
        synch_rate.clear()
        unsynch_rate.clear()
        random_rate.clear()
        