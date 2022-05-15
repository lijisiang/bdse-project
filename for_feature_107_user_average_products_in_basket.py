# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 10:23:21 2022

@author: LiJiSiang
"""

import pandas as pd

df=pd.read_csv('main_v2.csv',usecols=['user_id','order_number','product_id'])
df_1=pd.pivot_table(df,index=('user_id','order_number'),values='product_id',aggfunc='count')
df_1.rename(columns={'product_id':'total_purchase'},inplace=True)
df_107=pd.pivot_table(df_1,index=('user_id'),values='total_purchase',aggfunc='mean')
df_107.rename(columns={'total_purchase':'average_purchase'},inplace=True)
df_107.to_csv('107_user_average_products_in_basket.csv')
