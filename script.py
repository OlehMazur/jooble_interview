# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 22:40:15 2020

@author: O_Mazur
"""
#lib
from jooble_pkg import jooble

#params
features_type_id = 2
train_file_path = 'D:\\py_project\\data\\train.tsv' 
test_file_path = 'D:\\py_project\\data\\test.tsv'
result_file_path = 'D:\\py_project\\tests\\test_proc.tsv'
feature_scaling_method = 'z-score'

#features preprocessing script
jooble.job_features_preprocessing(features_type_id, train_file_path, test_file_path, result_file_path, feature_scaling_method )

