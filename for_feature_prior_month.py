# -*- coding: utf-8 -*-
"""
Created on Tue Mar 29 13:12:45 2022

@author: Student
"""

import pandas as pd
import numpy as np


df=pd.read_csv('00.original_data/2.process_result/main_v2.csv',usecols=['user_id','product_id','order_number','days_since_prior_order','reordered','department','aisle'])
df = df.fillna(0)


# reorder days by order
df_ord_days=pd.pivot_table(df,index=('user_id','order_number'),values='days_since_prior_order',aggfunc='mean')
df_ord_days.rename(columns={'days_since_prior_order':'reorder_days'},inplace=True)
df_ord_days['cumsum_days'] = df_ord_days['reorder_days'].groupby(['user_id']).cumsum()
df_ord_days=df_ord_days.reset_index('order_number')



df_cum_max=pd.pivot_table(df_ord_days,index=('user_id'),values='cumsum_days',aggfunc='max')
df_cum_max.rename(columns={'cumsum_days':'cum_max'},inplace=True)

result1= pd.merge(df_ord_days, df_cum_max, how='left',on=['user_id'])

def func1(x):
    return x.cum_max-x.cumsum_days
result1['day_diff'] = result1.apply(func1,axis=1)

def func(x):
    return x.day_diff/30
result1['for_month'] = result1.apply(func,axis=1)

result1['prior_month'] = np.ceil(result1['for_month'])
result1=result1.reset_index()

df_dep=df[['user_id','order_number','department','aisle','product_id']]
df_dep_month= pd.merge(df_dep, result1, how='left',on=['user_id','order_number'])
df_prior=df_dep_month.query('prior_month < 2')
df_prior=df_prior[['user_id','order_number','product_id','department','aisle','prior_month']]
df_prior.to_csv('code/diff_dep_month.csv')

#result2=pd.pivot_table(result1,index=('month'),values='order_number',aggfunc='count')