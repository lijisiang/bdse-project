# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 19:35:38 2022

@author: LiJiSiang
"""
import pandas as pd

df=pd.read_csv('main_v2.csv',usecols=['user_id','product_id','order_number','days_since_prior_order','reordered'])
df = df.fillna(0)

#取user2
df=df.query('user_id == 2')

# reorder days by order
df_ord_days=pd.pivot_table(df,index=('user_id','order_number'),values='days_since_prior_order',aggfunc='mean')
df_ord_days.rename(columns={'days_since_prior_order':'reorder_days'},inplace=True)
df_ord_days['cumsum_days'] = df_ord_days['reorder_days'].groupby(['user_id']).cumsum()
df_ord_days=df_ord_days.reset_index('order_number')

#reorderdays by product
df_pro_re_days=pd.pivot_table(df,index=('user_id','product_id','order_number'),values='days_since_prior_order')
df_pro_re_days.rename(columns={'days_since_prior_order':'product_reorder_days'},inplace=True)
#max,min
df_order_max_min=pd.pivot_table(df,index=('user_id','product_id'),values='order_number',aggfunc=['min','max'])
df_order_max_min.columns=df_order_max_min.columns.droplevel(0)
df_order_max_min =df_order_max_min.set_axis(['ord_min', 'ord_max'], axis=1, inplace=False)

#reorder次數
df_pro_re_times=pd.pivot_table(df,index=('user_id','product_id'),values='order_number',aggfunc='count')
df_pro_re_times.rename(columns={'order_number':'reoder_times'},inplace=True)
df_pro_re_times['reoder_times'] = df_pro_re_times['reoder_times']-1

#df_124 & df_ord_days
df_124 = df_pro_re_times.join(df_order_max_min)
left1=df_124[['reoder_times','ord_min']]
left2=df_124[['ord_max']]
right1=pd.DataFrame.copy(df_ord_days)
right1.rename(columns={'order_number':'ord_min','cumsum_days':'cumsum_days_min','reorder_days':'reorder_days_min'},inplace=True)
right2=pd.DataFrame.copy(df_ord_days)
right2.rename(columns={'order_number':'ord_max','cumsum_days':'cumsum_days_max','reorder_days':'reorder_days_max'},inplace=True)
left1=left1.reset_index()
left2=left2.reset_index()
result1= pd.merge(left1, right1, how='left',on=['ord_min','user_id'])
result2= pd.merge(left2, right2, how='left',on=['ord_max','user_id'])
final= pd.merge(result1, result2, how='left',on=['user_id','product_id'])

def apply_diff_days_func(x):
    return x.cumsum_days_max-x.cumsum_days_min
final['diff_days'] = final.apply(apply_diff_days_func,axis=1)

final=final.query('reoder_times >0')

def prod_avg_reorder_func(x):
    return x.diff_days/x.reoder_times
final['avg'] = final.apply(prod_avg_reorder_func,axis=1)

# to csv 
# final.to_csv('124_org.csv')

final_124=final[['user_id','product_id','reoder_times','avg']]
final_124.to_csv('124_prod_reorder_times.csv')