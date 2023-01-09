# -*- coding: utf-8 -*-
"""
Created on Tue Aug  2 16:20:32 2022

@author: ranga
"""

from sqlite3 import dbapi2
import pandas as pd
import os
import warnings
import time
warnings.filterwarnings("ignore")
from sdv import load_demo
from sdv import Metadata

import mysql.connector as sql
from sdv.relational import HMA1


os.chdir('S:/Summer/PDS/')

# ld = HMA1.load('sdv-HMA1-t1.pkl')

# n_data = ld.sample()

# print(n_data)

df = pd.read_csv('data/AviationData.txt', delimiter='|')

col_names = [x.strip() for x in list(df.columns)]

df.columns = col_names
# df.info()

for col in col_names:
    df[col] = df[col].str.strip()


print(df)

df.to_csv('AviationData.csv')
exit()
# metadata, tables = load_demo(metadata=True)

# print(type(tables))


dbname = 'umn_cs_prereqs'

conn = sql.connect(host='localhost',
                    user = 'root',
                    password='T3sdg$D2',                             
                    database=dbname)

df = pd.read_sql("select * from INFORMATION_SCHEMA.KEY_COLUMN_USAGE WHERE table_schema = '"+dbname+"'", conn)

df = df[['CONSTRAINT_NAME', 'TABLE_NAME', 'COLUMN_NAME', 'REFERENCED_TABLE_NAME', 'REFERENCED_COLUMN_NAME']]





metadata = Metadata()

mycursor = conn.cursor()
 
mycursor.execute("Show tables;")
myresult = mycursor.fetchall()

print(myresult)

l = {}
table_cols = []
for table in myresult:
    print(type(table))
    df_temp = pd.read_sql("select * from "+table[0]+"", conn)
    print(df_temp)
    l[table[0]] = df_temp
    table_cols.append(list(df_temp.columns))

    ####### Adding table info to metadata

    df = pd.read_sql("select * from INFORMATION_SCHEMA.KEY_COLUMN_USAGE WHERE table_schema = '"+dbname+"'", conn)

    df = df[['CONSTRAINT_NAME', 'TABLE_NAME', 'COLUMN_NAME', 'REFERENCED_TABLE_NAME', 'REFERENCED_COLUMN_NAME']]
    print(df)

    df_table_pk_temp = df[(df['TABLE_NAME'] ==  table[0]) & (df['CONSTRAINT_NAME'] == 'PRIMARY')]    
    df_table_fk_temp = df[(df['TABLE_NAME'] ==  table[0]) & (df['CONSTRAINT_NAME'] != 'PRIMARY')]   

    if len(df_table_pk_temp) != 0 and len(df_table_fk_temp) != 0  :
        p_key = df_table_pk_temp.iloc[0]['COLUMN_NAME']
        f_key = df_table_fk_temp.iloc[0]['COLUMN_NAME']
        parent_table = df_table_fk_temp.iloc[0]['REFERENCED_TABLE_NAME']
        
        metadata.add_table(name = table[0], data = df_temp, primary_key=p_key, parent = parent_table, foreign_key = f_key)
    elif len(df_table_pk_temp) != 0 :
        p_key = df_table_pk_temp.iloc[0]['COLUMN_NAME']
        metadata.add_table(name = table[0], data = df_temp, primary_key=p_key)
    elif len(df_table_fk_temp) != 0  :
        f_key = df_table_fk_temp.iloc[0]['COLUMN_NAME']
        parent_table = df_table_fk_temp.iloc[0]['REFERENCED_TABLE_NAME']

        print('xxxxxxxxxxxxxxxxxx')
        metadata.add_table(name = table[0], data = df_temp, parent = parent_table, foreign_key = f_key)
    else:
        metadata.add_table(name = table[0], data = df_temp)



    

conn.close()



# print(metadata.get_table_meta('course'))

# print(metadata)





# print(l)


model_HMA1 = HMA1(metadata)

model_HMA1.fit(l)

model_HMA1.save('sdv-HMA1-t1.pkl')
# print(table_cols)









# metadata, tables = load_demo(metadata=True)


# print(metadata.visualize())
