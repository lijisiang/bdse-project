# -*- coding: utf-8 -*-
"""
Created on Sun Mar 13 10:57:35 2022

@author: Student
"""
import gc
import lightgbm as lgb
import pandas as pd
from sklearn.model_selection import train_test_split

df=pd.read_csv('code/data/add_for_train.csv')

#df=pd.read_csv('code/data/main_for_xgboost_v2.csv')


product_id=pd.DataFrame(df,columns=['product_id'])
user_id=pd.DataFrame(df,columns=['user_id'])
drop_cols= ['user_id', 'product_id','y']

del product_id, user_id
gc.collect()

#
train_user=pd.read_csv('code/data/train_user.csv')
train_user_list=train_user['user_id'].tolist()
data=df[df['user_id'].isin(train_user_list)]

#test_user=pd.read_csv('code/data/test_user.csv')
#test_user_list=test_user['user_id'].tolist()
#test=df[df['user_id']].isin(train_user_list)

train_df = data
train_df, val_df = train_test_split(train_df, train_size=.99, random_state=555)

Y_train, Y_val = train_df['y'], val_df['y']
X_train, X_val = train_df.drop(drop_cols, axis=1), val_df.drop(drop_cols, axis=1)

del train_df
gc.collect()

params = {
    'task': 'train',
    'boosting_type':'gbdt',
    'objective' : 'binary',
    'metric': 'binary_logloss',    
    'learning_rate': 0.1,
    'max_depth': 3,
    
  }  
rounds=100

#categorical_features=['aisle_id']
# categorical_feature=categorical_features

for col in ['aisle_id']:
            X_train[col] = X_train[col].astype('category')
            X_val[col] = X_val[col].astype('category')


d_train = lgb.Dataset(X_train, Y_train)
d_valid = lgb.Dataset(X_val, Y_val)

valid_sets = [d_train, d_valid]
valid_names = ['train', 'valid']

for col in ['aisle_id']:
            X_train[col] = X_train[col].astype('category')
            X_val[col] = X_val[col].astype('category')

#開始訓練
gbm = lgb.train(params, d_train,rounds, valid_sets=valid_sets, valid_names=valid_names)


#save model
gbm.save_model('code/model/model0401_with_cato.txt')
