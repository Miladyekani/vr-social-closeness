from logging import error
import scipy.io
import glob
import pandas as pd
import numpy as np

class Subject:

 
# this is list shows the order of the movies fro all participants 
  movieOrder = ['happy_100_1', 'angry_100_1',
 'happy_70_4', 'angry_70_1', 'angry_100_4',
 'happy_100_4', 'angry_70_4', 'happy_70_4',
 'happy_70_4', 'angry_100_1', 'angry_100_4',
 'happy_100_1', 'happy_100_4', 'angry_100_1',
 'happy_70_1', 'angry_100_1', 'angry_100_4',
 'happy_70_4', 'happy_70_1', 'angry_70_1',
 'happy_100_1', 'angry_70_1', 'happy_100_4',
 'angry_70_1', 'angry_100_4', 'happy_70_1',
 'angry_70_4', 'happy_70_1', 'angry_70_4',
 'happy_100_1', 'angry_70_4', 'happy_100_4']
# 8 types of stimuli that we have presented to the subjects 
  movieTypes = ['happy_100_1', 'happy_100_4',
 'happy_70_1', 'happy_70_4', 'angry_100_1',
 'angry_100_4', 'angry_70_1', 'angry_70_4']


# items are presenting positive affect in panas
  positive_variables = ['faal.png','zoghzadegi.png','motvajeh va daghigh.png'
  ,'nirumandi.png','shur o shogh.png','hoshyari.png'
  ,'ghurur va eftekhar.png','khoshzoghi.png','alaghemandi.png','mosamam.png'] 
# items are presenting negative affect in panas
  negative_variables = ['harasan.png','ehsase gonah.png','tars o vahshat.png',
  'khusumat.png','delshore.png','parishani.png','bigharari.png',
  'narahati va ashoftegi.png','sharmsari.png','zudranji.png'] 

# I dont know what this function does? 
  def __init__(self, path):
      # the path can be accesible by this varaible 
    self.path = path
      # the name of the partiicpant can be accesccable by this varaible 
    self.name = path.split('\\')[9]
      # the group of the particpants can be accessible by this varaible 
    self.group = path.split('\\')[8]

    # this list has the rating of the preVR task for each stimuli 
    self.respPre = {'happy_100_1':[], 'happy_100_4':[],
    'happy_70_1':[], 'happy_70_4':[], 'angry_100_1':[],
    'angry_100_4':[], 'angry_70_1':[], 'angry_70_4':[]    
    }
    # this list has the rating of the postVR task for each stimuli 
    self.respPost = {'happy_100_1':[], 'happy_100_4':[],
    'happy_70_1':[], 'happy_70_4':[], 'angry_100_1':[],
    'angry_100_4':[], 'angry_70_1':[], 'angry_70_4':[]    
    }

# this function is loading the EMG signal for every participant
  def loadEMG(self):
    print('subject name: ' + self.name )
    
    pth = glob.glob(self.path+'/emg1/result_1_b*.mat')
    if len(pth)==0:
      error('there is no result_1_b in ' + self.path)
      return
    mat = scipy.io.loadmat(pth[0])
    self.emg1_times = mat['Times']
    
    pth = glob.glob(self.path+'/emg2/result_1_a*.mat')
    if len(pth)==0:
      error('there is no result_1_a in ' + self.path)
      return
    mat = scipy.io.loadmat(pth[0])
    self.emg2_times = mat['Times']


    pth = glob.glob(self.path+'/SN*/EMG_1.mat')
    if len(pth)==0:
      error('there is no EMG_1 in ' + self.path)
      return
    mat = scipy.io.loadmat(pth[0])
    if 'EMG_1' in mat.keys() :
      var_name = 'EMG_1'
    elif 'data' in mat.keys() :
      var_name = 'data'
    else:
      error('there is no signal in the first mat file in ' + sb.path)
      return
    

    if mat[var_name].shape == (1,4):
      tt = np.squeeze(mat[var_name])
      self.emg1_sig = np.array([np.squeeze(tt[i]) for i in range(4)]).T
    else:
      self.emg1_sig = mat[var_name]
      
    if np.sum(self.emg1_sig[:,3]<-0.1)>500:
      error('the first trigger signal is noisy: ' + self.path)
      return

    a = np.where(self.emg1_sig[:,3]>2)
    if len(a[0])<100:
      error('number of triggers are not true. the first mat file of  ' + self.path)
      return
    tmp = [a[0][0]]
    for smple in a[0][1:]:
      if smple - tmp[-1] > 100:
        tmp.append(smple)
    self.emg1_trigs = np.array(tmp)
        


    pth = glob.glob(self.path+'/SN*/EMG_2.mat')
    if len(pth)==0:
      error('there is no EMG_2 in ' + self.path)
      return
    mat = scipy.io.loadmat(pth[0])
    if 'EMG_2' in mat.keys() :
      var_name = 'EMG_2'
    elif 'data' in mat.keys() :
      var_name = 'data'
    else:
      error('there is no signal in the second mat file in ' + sb.path)
      return
    

    if mat[var_name].shape == (1,4):
      tt = np.squeeze(mat[var_name])
      self.emg2_sig = np.array([np.squeeze(tt[i]) for i in range(4)]).T
    else:
      self.emg2_sig = mat[var_name]
      
    if np.sum(self.emg2_sig[:,3]<-0.1)>500:
      error('the second trigger signal is noisy: ' + self.path)
      return
    a = np.where(self.emg2_sig[:,3]>2)
    if len(a[0])<100:
      error('number of triggers are not true. the second mat file of  ' + self.path)
      return
    tmp = [a[0][0]]
    for smple in a[0][1:]:
      if smple - tmp[-1] > 100:
        tmp.append(smple)
    self.emg2_trigs = np.array(tmp)
    
    # print('num of trigers1:' + str(len(self.emg1_trigs)))
    # print('num of trigers2:' + str(len(self.emg2_trigs)))

    
# this is loading the responses and pouring it inside the list that we had for 
# keeping them 
    
  def loadTaskResponses(self) :
    pth = glob.glob(self.path+'/emg1/result_1_b*.mat')
    if len(pth)>0:
      mat = scipy.io.loadmat(pth[0])
      self.respPreAll = mat['responses'][0,:]
      for i, movieName in enumerate(Subject.movieOrder):
        self.respPre[movieName].append(self.respPreAll[i])

    else:
      error('there is no result_1_b in ' + self.path)
    
    pth = glob.glob(self.path+'/emg2/result_1_a*.mat')
    if len(pth)>0:
      mat = scipy.io.loadmat(pth[0])
      self.respPostAll = mat['responses'][0,:]
      for i, movieName in enumerate(Subject.movieOrder):
        self.respPost[movieName].append(self.respPostAll[i])

    else:
      error('there is no result_1_a in ' + self.path)


  def loadPanas(self):
    pth = glob.glob(self.path+'/panas1/*.csv')
    if len(pth)>0:
      try:
        csvFile = pd.read_csv(pth[0])  
        # print(csvFile['rating.response'])
        positive_score = 0
        negative_score = 0
        if len(csvFile)==0:
          error(' csv file in panas1 in ' + self.path  + ' has no row' )
        # summ all itemms for postive affect pour into the 'positive_score' variable  
        for variable in  Subject.positive_variables: 
            inx = csvFile['pics']==variable
            if sum(inx):
              val = csvFile['rating.response'][inx].values[0]
              if isinstance(val, np.floating):
                positive_score= val + positive_score
              else:
                error(' csv file in panas1 in ' + self.path  + ' has non float val: ' + str(variable))
            else:
              error(' csv file in panas1 in ' + self.path  + ' has no ' + str(variable))
        # summ all itemms for negative affect pour into the 'negative_score'variable 
        for variable in  Subject.negative_variables: 
            inx = csvFile['pics']==variable
            if sum(inx):
              val = csvFile['rating.response'][inx].values[0]
              if isinstance(val, np.floating):
                negative_score = val + negative_score
              else:
                error(' csv file in panas1 in ' + self.path  + ' has non float val: ' + str(variable))
            else:
              error(' csv file in panas1 in ' + self.path  + ' has no ' + str(variable))

        # getting the avarage score for both negative and positive affetcts
        self.panas1n = negative_score/10
        self.panas1p =  positive_score/10
      
      except:
        error('cant load csv file in panas1 in ' + self.path  )
    else:
      error('there is no csv file in panas1 in ' + self.path)


    pth = glob.glob(self.path+'/panas2/*.csv')
    if len(pth)>0:
      try:
        csvFile = pd.read_csv(pth[0])  
        # print(csvFile['rating.response'])
        positive_score = 0
        negative_score = 0
        if len(csvFile)==0:
          error(' csv file in panas1 in ' + self.path  + ' has no row' )
        # summ all itemms for postive affect pour into the 'positive_score' variable  
        for variable in  Subject.positive_variables: 
            inx = csvFile['pics']==variable
            if sum(inx):
              val = csvFile['rating.response'][inx].values[0]
              if isinstance(val, np.floating):
                positive_score= val + positive_score
              else:
                error(' csv file in panas1 in ' + self.path  + ' has non float val: ' + str(variable))
            else:
              error(' csv file in panas1 in ' + self.path  + ' has no ' + str(variable))
        # summ all itemms for negative affect pour into the 'negative_score'variable 
        for variable in  Subject.negative_variables: 
            inx = csvFile['pics']==variable
            if sum(inx):
              val = csvFile['rating.response'][inx].values[0]
              if isinstance(val, np.floating):
                negative_score = val + negative_score
              else:
                error(' csv file in panas1 in ' + self.path  + ' has non float val: ' + str(variable))
            else:
              error(' csv file in panas1 in ' + self.path  + ' has no ' + str(variable))

        # getting the avarage score for both negative and positive affetcts
        self.panas2n = negative_score/10
        self.panas2p =  positive_score/10
      except:
        error('cant load csv file in panas1 in ' + self.path  )
    else:
      error('there is no csv file in panas2 in ' + self.path)

  ####################### this fucntion gets the adreess csv file inside questionaire folder and spites out 
  ####################### a data frame off all mesured items 
  def loadVrQuestionnaire(self): 
    # read csv file related to VR questioinnares 
    pth = glob.glob(self.path+'/questionarie/*.csv')
    if len(pth)==0:
      error('there is no csv file in questionarie in ' + self.path)
      return
    
    data = pd.read_csv(pth[0])
    ##items of post vr questionnaire 
    Data_Questionnaire = {'IOS':[],'Bound': [],'likability': [],'Similarity': [],'Willing_to_know_others': [],
      'Willing_to_help_other': [],'Willing_to_recieve_help': [],'Fun_in_vr': [],'Embaracment or annoyed': [],
      'Hardness of moves': [],'ENjoyment_in_vr': [],'Sucess_in_moves': [],'Synchrony': [],'Mimivking': [],
      'Lightining': [],'Being_mimicked': [],'Controled_by_real': [],'Accomponied': [],'Controlling_environment': [],
      'Controlled_by_environment': [],'SocialClosness_score': []}
    ##########################################################################
    #####load each variable in the DATA_Questionaire list 
    Data_Questionnaire['IOS'].append(data['rating_2.response'][0])
    Data_Questionnaire['Bound'].append(data[data.questions == 'Q_1.png']['rating.response'].values[0])
    Data_Questionnaire['likability'].append(data[data.questions == 'Q_2.png']['rating.response'].values[0])
    Data_Questionnaire['Similarity'].append(data[data.questions == 'Q_3.png']['rating.response'].values[0])
    Data_Questionnaire['Willing_to_know_others'].append(data[data.questions == 'Q_4.png']['rating.response'].values[0])
    Data_Questionnaire['Willing_to_help_other'].append(data[data.questions == 'Q_5.png']['rating.response'].values[0])
    Data_Questionnaire['Willing_to_recieve_help'].append(data[data.questions == 'Q_6.png']['rating.response'].values[0])
    Data_Questionnaire['Fun_in_vr'].append(data[data.questions == 'Q_7.png']['rating.response'].values[0])
    Data_Questionnaire['Embaracment or annoyed'].append(data[data.questions == 'Q_8.png']['rating.response'].values[0])
    Data_Questionnaire['Hardness of moves'].append(data[data.questions == 'Q_9.png']['rating.response'].values[0])
    Data_Questionnaire['ENjoyment_in_vr'].append(data[data.questions == 'Q_10.png']['rating.response'].values[0])
    Data_Questionnaire['Sucess_in_moves'].append(data[data.questions == 'Q_11.png']['rating.response'].values[0])
    Data_Questionnaire['Synchrony'].append(data[data.questions == 'Q_12.png']['rating.response'].values[0])
    Data_Questionnaire['Mimivking'].append(data[data.questions == 'Q_13.png']['rating.response'].values[0])
    Data_Questionnaire['Lightining'].append(data[data.questions == 'Q_14.png']['rating.response'].values[0])
    Data_Questionnaire['Being_mimicked'].append(data[data.questions == 'Q_15.png']['rating.response'].values[0])
    Data_Questionnaire['Controled_by_real'].append(data[data.questions == 'Q_16.png']['rating.response'].values[0])
    Data_Questionnaire['Accomponied'].append(data[data.questions == 'Q_17.png']['rating.response'].values[0])
    Data_Questionnaire['Controlling_environment'].append(data[data.questions == 'Q_18.png']['rating.response'].values[0])
    Data_Questionnaire['Controlled_by_environment'].append(data[data.questions == 'Q_19.png']['rating.response'].values[0])
    ############################################################################
    ####### calculate social closeness and feed into the liest this index it is the avarage of 
    ####### likabilty, similarity, and bound 
    for (score_1,score_2,score_3) in zip (Data_Questionnaire['likability'],Data_Questionnaire['Similarity'],
                                        Data_Questionnaire['Bound']):
        Data_Questionnaire['SocialClosness_score'].append((score_1+  score_2 + score_3 )/3)
    #############################################################################
    ### convert the list to a pandas dataframe 
    self.VR =  pd.DataFrame(Data_Questionnaire) 

  def REVERSE_SCORES (x) :
    y= (5-int(x))+1
    return y 


  def loadIRI(self): 
    # read csv file related to IRI
    pth = glob.glob(self.path+'IRI/IRI.txt')
    if len(pth)==0:
      error('there is no IRI.txt file in IRI directory in ' + self.path)
      return
    # some ratings are in reverse order they are indicated in list below
    # it means the question is negative 
    Negative_Rating  = [4,5,8,13,14,15,16,19,20] 
    # the number of the questions for each factor 
    FS = [2,6,8,13,17,24,27]  
    PD = [7,11,14,18,20,25,28] 
    EC = [3,5,10,15,19,21,23]
    PT = [4,9,12,16,22,26,29]

    #PT = perspective-taking scal
    #FS = fantasy scale 
    #EC = empathic concern scal  
    #PD = personal distress scale
    
    PT_score = 0 
    FS_score = 0 
    PD_score = 0 
    EC_score = 0 
    
    with open(pth[0]) as f : 
        reader= pd.read_csv(f,sep='\t', header=None)
    if not reader.shape==(1,30):
      error('the shape of IRI file is not true: ' + self.path)
      return
    for i in range (2,30):
         if pd.isnull(reader[i].values[0]):
          error('there is a null value in IRI file in: ' + self.path)
          return
         if i in Negative_Rating :
             # make sure its changing the value
             reader[i].values[0] = Subject.REVERSE_SCORES(reader[i].values[0])
         elif i in FS : 
             FS_score = FS_score + int( reader[i].values[0])
         elif i in PD : 
             PD_score= PD_score + int (reader[i].values[0])
         elif i in EC : 
             EC_score = EC_score + int (reader[i].values[0])
         elif i in PT : 
             PT_score = PT_score + int (reader[i].values[0])
    
    self.PT_score = PT_score
    self.EC_score = EC_score
    self.PD_score = PD_score
    self.FS_score = FS_score
  


    



