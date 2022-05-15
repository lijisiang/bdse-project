# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 16:20:41 2022


"""

import pandas as pd

import gc


main = pd.read_csv('main.csv')
# main = main.fillna(0)

prior_month = pd.read_csv('prior_month.csv')
data = pd.merge(main[['order_id','user_id','product_id', 'add_to_cart_order', 'order_number', 'eval_set']], prior_month[['user_id','order_number','day_diff']], how='left', on=['user_id','order_number']).drop_duplicates()

del main
gc.collect()

# f_301 = data.groupby(['user_id','product_id'])['day_diff'].min()
data = data[data['eval_set']=='prior']
data = data.sort_values(['user_id','product_id','day_diff']).reset_index(drop=1)

f_301 = data.drop_duplicates(subset=['user_id', 'product_id'], keep='first')
f_301_final = f_301[['user_id','product_id','day_diff']].rename(columns={'day_diff':'days_since_last_order'})

f_301_final.to_csv('301_mix_days_since_last_order')
