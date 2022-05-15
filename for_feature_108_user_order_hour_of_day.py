# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 10:46:59 2022

@author: LiJiSiang
"""
import pandas as pd

df=pd.read_csv('main_v2.csv',usecols=['user_id','order_number','order_hour_of_day'])
df_108=pd.pivot_table(df,index=('user_id','order_number'),values='order_hour_of_day')
df_108.to_csv('108_user_order_hour_of_day.csv')