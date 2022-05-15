# -*- coding: utf-8 -*-
"""
Created on Sun Mar 13 10:57:35 2022

@author: Student
"""

import lightgbm as lgb
import pandas as pd

#load
gbm = lgb.Booster(model_file='code/model/model0401_with_cato.txt')

#predict

test=pd.read_csv('code/data/add_for_test.csv')

#test=pd.read_csv('code/data/xgboost_test_v1.csv')

test_orders = test['order_id']
test_products = test['product_id']
test_y = test.drop(columns=['order_id','user_id','product_id'])
#test_y = test_y.drop(columns=['aisle_id','reorder_in_30days'])

#test_y = test_y.drop(columns=['aisle_id'])
for cols in ['aisle_id']:
            test_y[cols] = test_y[cols].astype('category')
            
#categorical_features=['aisle_id']
            
y_result=gbm.predict(test_y)

df_y_result_hat = pd.DataFrame(y_result, columns = ['y'])
test_result = pd.concat([test, df_y_result_hat], axis=1)

test_result.sort_values(['user_id','y'], inplace=True, ascending=False)
test_result['set'] = 1
test_result['rank'] = test_result.groupby(['user_id'])['set'].cumsum()

#y的0&1的標準為:最後一個月的數量(A)
per_month_1=pd.read_csv('code/features/month_1.csv')
test_result= pd.merge(test_result, per_month_1, how='left',on=['user_id'])
test_purchase = test_result.query('purchase_1month>=rank')
#標準為:最後2個月的數量(B)
per_month_2=pd.read_csv('code/features/month_2.csv')
test_result= pd.merge(test_result, per_month_2, how='left',on=['user_id'])
test_purchase = test_result.query('purchase_2months>=rank')
#標準為:最後3個月的數量(C)
per_month_3=pd.read_csv('code/features/month_3.csv')
test_result= pd.merge(test_result, per_month_3, how='left',on=['user_id'])
test_purchase = test_result.query('purchase_3months>=rank')
#標準為:user平均購買數量(D)
test_purchase = test_result.query('average_purchase>=rank')
#標準為:預測購買數量(0.5)
y_result[y_result >= 0.5] =1
y_result[y_result < 0.5] =0 
df_y_result_hat = pd.DataFrame(y_result, columns = ['y'])
test_result = pd.concat([test, df_y_result_hat], axis=1)
test_result_y1 = test_result[test_result['y']==1]
test_product_list = test_result_y1.groupby('user_id').product_id.apply(list).reset_index()
test_kaggle = test[['order_id','user_id']]
test_kaggle = test_kaggle.drop_duplicates()
submission = pd.merge(test_kaggle, test_product_list, on='user_id', how='left')
submission = submission.drop(columns=['user_id'])
submission = submission.rename(columns={'product_id': 'products'})




test_product_list = test_purchase.groupby('user_id').product_id.apply(list).reset_index()
test_kaggle = test[['order_id','user_id']]
test_kaggle = test_kaggle.drop_duplicates()
submission = pd.merge(test_kaggle, test_product_list, on='user_id', how='left')
submission = submission.drop(columns=['user_id'])
submission = submission.rename(columns={'product_id': 'products'})

submission.to_csv('code/for kaggle submit/submission331_C.csv',index=False)

