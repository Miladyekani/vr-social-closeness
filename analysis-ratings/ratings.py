# -*- coding: utf-8 -*-
"""
Created on Sun Sep 25 22:40:57 2022

@author: milad
"""
## To whom may read these lines 
## I am coummenting even the most rudemintory things and I am dyslactic dont juddge me 

import os 
from glob import glob
from scipy.io import loadmat
import pandas as pd 
# choose the grouo that you want ot extract the data from it 

group_name = 'unsynch_random_folder'
# create a list for all responese 
response = [] 
subject = [] 
emotion =  [] 
character = [] 
intensity = [] 
phase = [] 
group = [] 
tname = [] 
info = [] 


# os.path.join makes a string compaible by your is to adreess the path of the file 
Data_Root =  os.path.join('C:\\','Users','milad','Desktop','D','Thesis_Phd','data','raw_data', group_name)
# create a list of all folders inside the Data_root notice that we are using path.join agian 
Data_Dirs = glob(os.path.join(Data_Root,'*'))

#  y is a representaitve of subject number 
for Y , folder in enumerate(Data_Dirs): 
    # find the address of the mat file for task before the VR session inside emg_2 folder
    Mat_File_Address_Before= glob(os.path.join(folder,'emg1','result_1_b_*'))
    # return error for faulty folders 
    assert(len(Mat_File_Address_Before) == 1)
    # load this file
    Mat_File_Before = loadmat(Mat_File_Address_Before[0])
    #find the address of the mat file for task before the VR session inside emg2 folder
    Mat_File_Address_After= glob(os.path.join(folder,'emg2','result_1_a_*'))
    #  return error for faulty folders 
    assert(len(Mat_File_Address_After) == 1)
    # load the mat file 
    Mat_File_After = loadmat(Mat_File_Address_After[0])
    
    for i in range(0,32): 
        # types of each trail stimuli is saved in the moviename 
        # the below varaible is an array with three element [emotion,intesity,character]
        Stimulus_type = Mat_File_Before['moviename'][i][0][0].split('\\')[6].split('.')[0].split('_')
        # load the respons for each stiumuli 
        Rating_response = Mat_File_Before['responses'][0][i]
        # append extracted data to the correspondent list 
        response.append(Rating_response)
        emotion.append(Stimulus_type[0])
        intensity.append(Stimulus_type[1])
        character.append(Stimulus_type[2])
        group.append(group_name)
        subject.append(Y+1)
        phase.append(1)
        
        Stimulus_type = Mat_File_After['moviename'][i][0][0].split('\\')[6].split('.')[0].split('_')
        Rating_response = Mat_File_After['responses'][0][i]
        response.append(Rating_response)
        emotion.append(Stimulus_type[0])
        intensity.append(Stimulus_type[1])
        character.append(Stimulus_type[2])
        subject.append(Y+1)
        phase.append(2)
        group.append(group_name)


        
Df_Rating_Synch = pd.DataFrame({'response' : response ,'subject':subject ,'emotion': emotion ,'character': character  ,'intensity': intensity 
                   ,'phase':phase , 'group':group})

# save data frame in csv format
Save_dir = os.path.join('C:\\','Users','milad','Desktop','D','Thesis_Phd','results', group_name+'.csv')
Df_Rating_Synch.to_csv(Save_dir)