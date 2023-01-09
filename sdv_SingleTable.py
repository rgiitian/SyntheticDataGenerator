
import pandas as pd
import os
import numpy as np
from multiprocessing import Process, Manager 


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

# start = time.time()

# df = pd.read_csv('S:/CreditCard.csv')
# df = pd.read_csv('data/imdb.csv')
# df = df.iloc[:,0:21]




def mtd_CopulaGAN(df):

    start = time.time()
    model_CopulaGAN = CopulaGAN(epochs = 10)
    model_CopulaGAN.fit(df)
    model_CopulaGAN.save("sdv-CopulaGAN.pkl")

    ld = CopulaGAN.load('sdv-CopulaGAN.pkl')
    sdata = ld.sample(200)
    ev = evaluate(df, sdata)
    rtime = time.time() - start

    metrics = ['CopulaGan', ev, rtime]

    return metrics


def mtd_TVAE(df, ns):

    df_temp_metric = ns.df_metric

    start = time.time()
    model_TVAE = TVAE(epochs = 10)
    model_TVAE.fit(df)
    model_TVAE.save("sdv_TVAE.pkl")

    ld = TVAE.load('sdv-TVAE.pkl')
    sdata = ld.sample(200)
    ev = evaluate(df, sdata)
    rtime = time.time() - start

    metrics = ['TVAE', ev, rtime]

    df_temp_metric.loc[len(df_temp_metric)] = metrics
    ns.df_metric = df_temp_metric

    return 



def mtd_CTGAN(df):

    start = time.time()
    model_CTGAN = CTGAN(epochs = 10)
    model_CTGAN.fit(df)

    fname = "sdv_CTGAN.pkl"
    model_CTGAN.save(fname)

    ld= CTGAN.load(fname)
    sdata = ld.sample(200)
    ev = evaluate(df, sdata)
    rtime = time.time() - start

    metrics = ['CTGAN', ev, rtime]

    return metrics



# df = pd.read_csv('S:/CreditCard.csv')

# df = df.iloc[:,0:21]

# # cat_columns = ['Attrition_Flag', 'Gender', 'Education_Level', 'Marital_Status', 'Card_Category',
#                   # 'Income_Category']


# df_modelcomp = pd.DataFrame(columns = ['Model', 'Similarity_Ind', 'Runtime'])
# # df_modelcomp.columns = ['Model', 'Similarity_Ind', 'Runtime']

# mgr = Manager()
# ns = mgr.Namespace()

# ns.df_metric = pd.DataFrame(columns = ['Model', 'Similarity_Ind', 'Runtime'])


# p1 = Process(target = mtd_TVAE, args=(df, ns,))
# p2 = Process(target = mtd_CopulaGAN, args=(df,))
# p3 = Process(target = mtd_CTGAN, args=(df,))


# p1.start()
# p2.start()
# p3.start()

# p1.join()
# p2.join()
# p3.join()



# models = ['TVAE','CTGAN', 'CopulaGAN']

# for model in models:


#     # mtd = 'mtd_'+model


#     if model == 'TVAE':
#         metrics = mtd_TVAE(df)
#     elif model == 'CTGAN':
#         metrics = mtd_CTGAN(df)
#     else:
#         metrics = mtd_CopulaGAN(df)
#     # metrics = eval(mtd+'('+df+')')

    # print(model + "  training completed")
    # df_modelcomp.loc[len(df_modelcomp)] = metrics

    # print(df_modelcomp)

# print(ns.df_metric)



if __name__=="__main__":

    df = pd.read_csv('S:/CreditCard.csv')
    df = df.iloc[:,0:21]

    mgr = Manager()
    ns = mgr.Namespace()

    ns.df_metric = pd.DataFrame(columns = ['Model', 'Similarity_Ind', 'Runtime'])

    p1 = Process(target = mtd_TVAE, args=(df, ns,))
    # p2 = Process(target = mtd_CopulaGAN, args=(df,))
    # p3 = Process(target = mtd_CTGAN, args=(df,))

    p1.start()
    # p2.start()
    # p3.start()

    p1.join()

    print(ns.df_metric)







    



