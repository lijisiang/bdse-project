# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 14:27:44 2022

@author:
"""

import pandas as pd


raw_orders = pd.read_csv('orders.csv')
prior = pd.read_csv('order_products__prior.csv')

# user_total_order
df_1 = raw_orders[['user_id','order_number']].sort_values(['user_id','order_number'])
df_1 = df_1.drop_duplicates(['user_id'], keep='last')

# mix_times_order
df_2 = pd.merge(prior, raw_orders[['order_id','user_id']], how='left', on='order_id').drop_duplicates()
df_3 = df_2.value_counts(['user_id','product_id'])
df_3 = df_3.to_frame().reset_index()
df_3 = df_3.sort_values(['user_id','product_id']).reset_index(drop=1).rename(columns={0:'times_order'})

# mix_order_rate
f_302 = pd.merge(df_3, df_1, how='left', on='user_id')
f_302['order_rate'] = f_302['times_order'] / f_302['order_number']

f_302.to_csv('302_mix_order_rate.csv', index = False)
