# -*- coding: utf-8 -*-
"""
Created on Thu Dec 11 19:05:02 2020
@author: O_Mazur
"""

#libs
import pandas as pd
import numpy as np 
import sys

#functions
"""
function: save_result
 params:
     - file_name with tsv format
     - pandas DF
 returns: status(int) 0 - success, 1 - failure     
"""
def save_result(file_path:str , df:pd.core.frame.DataFrame) -> int:
    status = 1
    try:
        df.to_csv(file_path, sep= '\t', index=False)
        status = 0
    except:
       print("something went wrong during export result into a file!") 
    finally:
        return status


"""
function: load_tsv
 params:
    - file_name with tsv foramt
 returns: pandas DF     
"""
def load_tsv(file_name) -> pd.core.frame.DataFrame:
    try:
        data = pd.read_csv(file_name, delimiter = '\t')
    except FileNotFoundError:
        print("please check the file path or file format (tsv format is expected)")   
    return data


"""
function: create_features_structure
 params:
    - features_type_id  (in this case -  2)
    - num_of_features - number of available features for a certain type
 returns: pandas DF     
"""

def create_features_structure(features_type_id: int, num_of_features: int, input_df: pd.core.frame.DataFrame ) -> pd.core.frame.DataFrame: 
    #DF with features
    sub_data_to_process = pd.DataFrame()
    for i in range(1,num_of_features):
        sub_data_to_process['feature_' + str(features_type_id) +'_'+ str(i)] = input_df['features'].apply(lambda x: x.split(',')[i])    
    return  sub_data_to_process
      
       
"""
function: statistics
 params:
    - train_file
    - features_type_id
    - stat: 'mean' or 'std'
 returns: dictionary with statistics     
"""
def statistics (file:str, features_type_id: int, stat:str) -> dict: 

    #data loading
    data = load_tsv(file)
    
    #getting a number of features 
    if(not data.empty): 
        num_of_features = data['features'].apply(lambda x: len(x.split(','))).max()
    else:
        sys.exit('the function "load_tsv" returns an empty DF!')
            
    #DF with features
    sub_data_to_process = create_features_structure(features_type_id, num_of_features, data)
     
    df_columns = list(sub_data_to_process.columns)
        
    # mean, std, max statistics 
    stat_values = {}
        
    if (stat.lower().strip() == 'mean'):
        for df_column in df_columns:
            stat_values[df_column] = sub_data_to_process[df_column].astype('float').mean()
    elif (stat.lower().strip() == 'std'):
        for df_column in df_columns:
            stat_values[df_column] = sub_data_to_process[df_column].astype('float').std()
    elif (stat.lower().strip() == 'max'): 
        for df_column in df_columns:
            stat_values[df_column] = (sub_data_to_process[df_column].astype('int64').max() , \
            sub_data_to_process[sub_data_to_process[df_column].astype('int64') == sub_data_to_process[df_column].astype('int64').max()].index.values[0])         
    else:
        print('wrong "stat" param for "statistics" function , please check and try again!') 
          
    return stat_values



"""
function: job_features_preprocessing
 params:
    - train_file_path 
    - test_file_path
    - result_fname
    - features_type_id
 returns: status(int)  0 - success, 1 - failure
     
"""
def job_features_preprocessing(features_type_id: int, train_file_path: str,  test_file_path: str, result_file_path: str, feature_scaling_method: str = 'z-score' ) -> int:
    
    status = 1
    
    try:
        #data loading
        test_data = load_tsv(test_file_path)
        
        #getting a number of features from the test dataset
        if (not test_data.empty):
            num_of_features = test_data['features'].apply(lambda x: len(x.split(','))).max()
        else:
             sys.exit('the function "load_tsv" returns an empty DF!')
        
        #data processing according to requirements
        
        #DF with features
        sub_data_to_process = create_features_structure(features_type_id, num_of_features, test_data)
        
        df_columns = list(sub_data_to_process.columns)
        
        # mean and std statistics + max_feature and max_feature_index
        mean_values = statistics (train_file_path, features_type_id, 'mean')
        std_values =  statistics (train_file_path, features_type_id, 'std')
        max_values =  statistics (test_file_path,  features_type_id, 'max')
        
        #z-score, max_feature_2_index and max_feature_2_abs_mean_diff culculation 
        for i in range(1,num_of_features):
            #feature_scaling
            if feature_scaling_method.lower().strip()  == 'z-score': 
                denominator =  1 if std_values['feature_' +str(features_type_id) + '_' + str(i)] == 0 else std_values['feature_' + str(features_type_id) +  '_' + str(i)] 
                sub_data_to_process['feature_' + str(features_type_id) + '_stand_'+ str(i)] = sub_data_to_process['feature_' + str(features_type_id) +  '_' + str(i)].apply \
                (lambda x: (float(x) - mean_values['feature_' + str(features_type_id) +'_' + str(i)])  / denominator )
            else:
                 print('wrong "feature_scaling_method" param for "job_features_preprocessing" function , please check and try again!')
            #max_feature_2_index
            sub_data_to_process['max_feature_' + str(features_type_id) + '_index_'+ str(i)] = max_values['feature_' + str(features_type_id) + '_' + str(i)][1]
            #max_feature_2_abs_mean_diff
            sub_data_to_process['max_feature_' + str(features_type_id) +  '_abs_mean_diff_'+ str(i)] = abs(max_values['feature_' + str(features_type_id) +  '_' + \
            str(i)][0] - mean_values['feature_' + str(features_type_id)+ '_' + str(i)]) 
        
        #final data cleaning and data preparation
            
        #dropping unnecessary columns    
        sub_data_to_process = sub_data_to_process.drop(np.array(df_columns), axis = 1)
        job_id_and_features_type_info = pd.DataFrame()
        #list of id_jobs
        job_id_and_features_type_info['id_job'] = test_data['id_job']
        #adding code_of_features_type ( only '2' for current data set)
        job_id_and_features_type_info['code_of_features_type'] = features_type_id #test_data['features'].apply(lambda x: x.split(',')[0])
        ##final data frame
        result = job_id_and_features_type_info.join(sub_data_to_process)
        #data export
        if save_result(result_file_path, result) == 0:
            print ("The files %s has been successfully created!"%result_file_path)
        status = 0
        
    except:
            print("The features preprocessing script has finished its run with error!")
    finally:
            return 'finished with status ' + str(status)        


