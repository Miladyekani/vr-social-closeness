# -*- coding: utf-8 -*-
"""
Created on Fri Sep 30 18:29:32 2022

@author: milad
"""

# import sys 
import os
os.chdir('C:/Users/milad/Desktop/D/vr-social-closeness')
from glob import glob
from subject import Subject
import numpy as np 
import pandas as pd 

import json
with open('./utils/dirs.json') as f:
    dirs = json.load(f)

from matplotlib import pyplot as plt
import seaborn as sns
from scipy.stats import ttest_rel

#%%
# normalized by this method 
# sum(emotion) / sum(allrating)

sub_dirs = []  

group_name = ['synch_folder',
              'unsynch_folder',
              'unsynch_random_folder']

for study_group in group_name: 
     data_root = os.path.join(dirs['data'], study_group)
     sub_dirs.extend(glob(os.path.join(data_root, '*')))

subjects = [Subject(path) for path in  sub_dirs]

#%%

def generate_scatter_plots(df1, df2, legend):
    fig, axs = plt.subplots(2, 4, figsize=(16, 9))
    axs = axs.flatten()
    
    for i, (movieName, _d) in enumerate(df1.groupby("mname")):
        tmp = {}
        for phase, d in _d.groupby("phase"):
            tmp[phase] = d.mean_rate
            
        axs[i].scatter(tmp[1], tmp[2])
        xlim = axs[i].get_xlim()
        ylim = axs[i].get_ylim()
        lim = [min((xlim[0], ylim[0])), max((xlim[1], ylim[1]))]
        axs[i].plot(lim, lim, c='gray', ls='--', label='_nolegend_')
        axs[i].set_xlabel("pre", fontsize=14)
        axs[i].set_ylabel("post", fontsize=14)
        axs[i].set_title(movieName, fontsize=20)
        axs[i].axis('square')
    
    for i, (movieName, _d) in enumerate(df2.groupby("mname")):
        tmp = {}
        for phase, d in _d.groupby("phase"):
            tmp[phase] = d.mean_rate
            
        axs[i].scatter(tmp[1], tmp[2])
        xlim = axs[i].get_xlim()
        ylim = axs[i].get_ylim()
        lim = [min((xlim[0], ylim[0])), max((xlim[1], ylim[1]))]
        axs[i].plot(lim, lim, c='gray', ls='--', label='_nolegend_')
        axs[i].set_xlabel("pre", fontsize=14)
        axs[i].set_ylabel("post", fontsize=14)
        # axs[i].set_title(f"{movieName}-pval:{ttest_rel(tmp[1], tmp[2])[1]:.2f}", fontsize=20)
        axs[i].axis('square')
    
    for ax in axs:
        ax.legend(legend, frameon=False, fontsize=16)
        # ax.legend(["synch", "unsynch", "random"], frameon=False, fontsize=16)
    
    fig.tight_layout()
    sns.despine()
    # plt.savefig(os.path.join('C:\\','Users','milad','Desktop','D',
    #                                'Thesis_Phd','results','scater_raw_overtotalsum_synch_vs_unsynch.png'),dpi=600)

#%%
normalized_rate = []
emotion = []
character = []
intensity = [] 
phase = [] 
group = [] 
sub_number = []
phase = []

for i,sb in enumerate(subjects):
  sb.loadTaskResponses()
  for stimulus  in Subject.movieTypes:
     # print('the stimulus is ' , stimulus)
     ##### pre ratings
     sub_number.append(i)
     group.append(sb.group)
     phase.append(1)
     emotion.append(stimulus.split('_')[0])
     intensity.append(stimulus.split('_')[1])
     character.append(stimulus.split('_')[2])
     sum_ratings = sum(np.abs(sb.respPreAll))     
     rate = sum(np.abs(sb.respPre[stimulus]))/sum_ratings
     normalized_rate.append(rate)
     ###### post ratings 
     sub_number.append(i)
     group.append(sb.group)
     phase.append(2)
     emotion.append(stimulus.split('_')[0])
     intensity.append(stimulus.split('_')[1])
     character.append(stimulus.split('_')[2])
     sum_ratings = sum(np.abs(sb.respPostAll))     
     rate = sum(np.abs(sb.respPost[stimulus]))/sum_ratings
     normalized_rate.append(rate)
     


# create a dataframe 


df = pd.DataFrame({'mean_rate' : normalized_rate  , 'emotion':emotion,'character':character ,
'intensity':intensity ,'group': group ,'sub_number' : sub_number , 'phase' : phase})

df['mname'] = df.emotion + "-" + df.intensity + "-" + df.character

df1 = df[df.group == 'synch_folder']
df2 = df[df.group == 'unsynch_folder']
df3 = df[df.group == 'unsynch_random_folder']

generate_scatter_plots(df1, df2, ["synch", "unsynch"])
generate_scatter_plots(df1, df3, ["synch", "random"])
generate_scatter_plots(df2, df3, ["unsynch", "random"])


#%%
# milad transformation



Sub_Address = []  


normalized_rate = []
emotion = []
character = []
intensity = [] 
phase = [] 
group = [] 
sub_number = []
phase = []



group_name = ['synch_folder','unsynch_folder','unsynch_random_folder']



for study_group in group_name: 
     Data_Root =  os.path.join('C:\\','Users','milad','Desktop','D',
                               'Thesis_Phd','data','raw_data', study_group)
     Sub_Address.extend( glob(os.path.join(Data_Root,'*')))
     
subjects = [Subject(path ) for path in  Sub_Address]


for i,sb in enumerate(subjects):
  sb.loadTaskResponses()
  for stimulus  in Subject.movieTypes:
     print('the stimulus is ' , stimulus)
     ##### pre ratings
     sub_number.append(i)
     group.append(sb.group)
     phase.append(1)
     emotion.append(stimulus.split('_')[0])
     intensity.append(stimulus.split('_')[1])
     character.append(stimulus.split('_')[2])
     if stimulus.split('_')[1] == '70' : 
         compliment = '100'
     else:
         compliment = '70'
     compliment_emotion = stimulus.split('_')[0]+'_'+compliment+'_'+stimulus.split('_')[2]
     print('the_compliment is' , compliment_emotion)
     sum_ratings = sum(np.abs(sb.respPre[stimulus]))+sum(np.abs(sb.respPre[compliment_emotion]))     
     rate = sum(np.abs(sb.respPre[stimulus]))/sum_ratings
     normalized_rate.append(rate)
     ###### post ratings 
     sub_number.append(i)
     group.append(sb.group)
     phase.append(2)
     emotion.append(stimulus.split('_')[0])
     intensity.append(stimulus.split('_')[1])
     character.append(stimulus.split('_')[2])
     compliment_emotion = stimulus.split('_')[0]+'_'+compliment+'_'+stimulus.split('_')[2]
     print('the_compliment is' , compliment_emotion)
     sum_ratings = sum(np.abs(sb.respPost[stimulus]))+ sum(np.abs(sb.respPost[compliment_emotion]))     
     rate = sum(np.abs(sb.respPost[stimulus]))/sum_ratings
     normalized_rate.append(rate)
     


# create a dataframe 


df = pd.DataFrame({'mean_rate' : normalized_rate  , 'emotion':emotion,'character':character ,
'intensity':intensity ,'group': group ,'sub_number' : sub_number , 'phase' : phase})

df['mname'] = df.emotion + "-" + df.intensity + "-" + df.character

df1 = df[df.group == 'synch_folder']
df2 = df[df.group == 'unsynch_folder']
df3 = df[df.group == 'unsynch_random_folder']


#%% raw data without transofrmation 

Sub_Address = []  

mean_rate = []
emotion = []
character = []
intensity = [] 
phase = [] 
group = [] 
sub_number = []
phase = []



group_name = ['synch_folder','unsynch_folder','unsynch_random_folder']

for study_group in group_name: 
     Data_Root =  os.path.join('C:\\','Users','milad','Desktop','D',
                               'Thesis_Phd','data','raw_data', study_group)
     Sub_Address.extend( glob(os.path.join(Data_Root,'*')))
     
subjects = [Subject(path ) for path in  Sub_Address]


for i,sb in enumerate(subjects):
  sb.loadTaskResponses()
  for stimulus  in Subject.movieTypes:
     ##### pre ratings
     sub_number.append(i)
     group.append(sb.group)
     phase.append(1)
     emotion.append(stimulus.split('_')[0])
     intensity.append(stimulus.split('_')[1])
     character.append(stimulus.split('_')[2])
     rate = np.mean(sb.respPre[stimulus])
     mean_rate.append(rate)
     ###### post ratings 
     sub_number.append(i)
     group.append(sb.group)
     phase.append(2)
     emotion.append(stimulus.split('_')[0])
     intensity.append(stimulus.split('_')[1])
     character.append(stimulus.split('_')[2])  
     rate = np.mean(sb.respPost[stimulus])
     mean_rate.append(rate)
     


# create a dataframe 
df = pd.DataFrame({'mean_rate' : mean_rate , 'emotion':emotion,'character':character ,
'intensity':intensity ,'group': group ,'sub_number' : sub_number , 'phase' : phase})

df['mname'] = df.emotion + "-" + df.intensity + "-" + df.character

df1 = df[df.group == 'synch_folder']
df2 = df[df.group == 'unsynch_folder']
df3 = df[df.group == 'unsynch_random_folder']

#%%
fig, axs = plt.subplots(1, 1, figsize=(16, 9), sharey=True)
(df[df.phase==2].groupby(["mname", "group"]).mean()['mean_rate'] - 
 df[df.phase==1].groupby(["mname", "group"]).mean()['mean_rate']).unstack().plot.bar(ax=axs)
axs.legend(["random", "synch", "unsynch"], frameon=False, fontsize=20)


#%%
fig, axs = plt.subplots(1, 1, figsize=(16, 9), sharey=True)
df[df.phase==2].groupby(["mname", "group"]).mean()['mean_rate'].unstack().plot.bar(ax=axs)
# axs.legend(["synch", "unsynch", "random"], frameon=False, fontsize=20)
sns.despine()

#%%
# This cell loads the raw data, and applies no tranformation

Sub_Address = []  

mean_rate = []
emotion = []
character = []
intensity = [] 
phase = [] 
group = [] 
sub_number = []
phase = []



group_name = ['synch_folder','unsynch_folder','unsynch_random_folder']

for study_group in group_name: 
     Data_Root =  os.path.join('C:\\','Users','milad','Desktop','D',
                               'Thesis_Phd','data','raw_data', study_group)
     Sub_Address.extend( glob(os.path.join(Data_Root,'*')))
     
subjects = [Subject(path ) for path in  Sub_Address]


for i,sb in enumerate(subjects):
  sb.loadTaskResponses()
  for stimulus  in Subject.movieTypes:
     ##### pre ratings
     sub_number.append(i)
     group.append(sb.group)
     phase.append(1)
     emotion.append(stimulus.split('_')[0])
     intensity.append(stimulus.split('_')[1])
     character.append(stimulus.split('_')[2])
     rate = np.mean(sb.respPre[stimulus])
     mean_rate.append(rate)
     ###### post ratings 
     sub_number.append(i)
     group.append(sb.group)
     phase.append(2)
     emotion.append(stimulus.split('_')[0])
     intensity.append(stimulus.split('_')[1])
     character.append(stimulus.split('_')[2])  
     rate = np.mean(sb.respPost[stimulus])
     mean_rate.append(rate)
     


# create a dataframe 
df = pd.DataFrame({'mean_rate' : mean_rate , 'emotion':emotion,'character':character ,
'intensity':intensity ,'group': group ,'sub_number' : sub_number , 'phase' : phase})

df['mname'] = df.emotion + "-" + df.intensity + "-" + df.character
df.group = df.group.map({'synch_folder': 'synch', 'unsynch_folder': 'unsynch', 'unsynch_random_folder':'random'})


df1 = df[df.group == 'synch_folder']
df2 = df[df.group == 'unsynch_folder']
df3 = df[df.group == 'unsynch_random_folder']
