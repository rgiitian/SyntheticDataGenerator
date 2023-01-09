# -*- coding: utf-8 -*-
"""
Created on Tue Aug  2 00:23:53 2022

@author: ranga
"""

import pandas as pd
import os
import numpy as np
# from pandas_profiling import ProfileReport

    

from sdv.evaluation import evaluate
from sdv.metrics.tabular import CSTest, KSTest, LogisticDetection, SVCDetection
from sdv.tabular import CTGAN, TVAE, CopulaGAN, GaussianCopula

from table_evaluator import load_data, TableEvaluator

import warnings
import time
warnings.filterwarnings("ignore")

os.chdir("S:/Summer/PDS/")
print(os.getcwd())

start = time.time()

# df = pd.read_csv('S:/CreditCard.csv')
df = pd.read_csv('data/imdb.csv')
# df = df.iloc[:,0:21]

# print(df)

# cat_columns = ['Attrition_Flag', 'Gender', 'Education_Level', 'Marital_Status', 'Card_Category',
                  # 'Income_Category']


# model = CTGAN(epochs = 5)
# model.fit(df)

# print('K')
# model.save("sdv-ctgan.pkl")
# # new_data = model.sample(200)
# # print(new_data.head())


# ld = CTGAN.load('sdv-ctgan.pkl')
# n_data = ld.sample(200)

# print(n_data.head(5))

# print(evaluate(df, n_data))



######################################################

# model_TVAE = TVAE(primary_key = 'CLIENTNUM')

# model_TVAE.fit(df)
# model_TVAE.save("sdv-TVAE_2.pkl")

# ld_2 = TVAE.load('sdv-TVAE_2.pkl')
# n2_data = ld_2.sample(200)

# print(evaluate(df, n2_data))


# end = time.time()
# total_time = end - start
# print("\n"+ str(total_time))


######################################################

# model_CopulaGAN = CopulaGAN(epochs = 5)
# model_CopulaGAN.fit(df)
# model_CopulaGAN.save("sdv-CopulaGAN_imdb.pkl")

ld_3 = CopulaGAN.load('sdv-CopulaGAN_imdb.pkl')
n3_data = ld_3.sample(1000)

ev = evaluate(df, n3_data, aggregate = False)
print(ev)


###################################################


table_evaluator = TableEvaluator(df, n3_data)
table_evaluator.visual_evaluation()

end = time.time()
total_time = end - start
print("\n"+ str(total_time))
    




