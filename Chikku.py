#!/usr/bin/env python
# coding: utf-8

# In[29]:


import pandas as pd
import os
import numpy as np
from collections import OrderedDict


# In[13]:





# In[14]:

unique_columns = []
column_names = {}
for file in os.listdir():
    if file.endswith(".csv") and file != "Combiner_Columns.csv":
        column_names[file] = []


# In[15]:


for file in os.listdir():
    if file.endswith(".csv") and file != "Combiner_Columns.csv":
        df = pd.read_csv(file)
        unique_columns.extend(df.columns)
        column_names[file].extend(sorted(df.columns.tolist()))


# In[16]:


for x in column_names:
    column_names[x].insert(0,x)


# In[17]:


combiner_column_list = []
for key,value in column_names.items():
    value = str(value).replace("'","")[1:-1]
    combiner_column_list.append(value)
unique_columns = sorted(set(unique_columns))
unique_columns.insert(0,"All unique columns")
combiner_column_list.append("**********************")
combiner_column_list.append(str(unique_columns).replace('[','').replace(']','').replace('"','').replace("'",''))
#print(combiner_column_list)
combiner_column_list.append("Write Columns to combine below [Row Wise]")


# In[20]:


with open('Combiner_Columns.csv', 'w') as f:
    f.writelines('\n'.join(combiner_column_list))


# In[21]:


os.system("libreoffice Combiner_Columns.csv")


# In[25]:


file = open("Combiner_Columns.csv","r+")
file_text = file.readlines()


# In[26]:


final_columns = {}
j = 0
for line in file_text:
    if line.startswith("Write Columns to combine below"):
        j = 1
    if j == 1:
        line = line.split(",")
        fin_col = []
        for x in line:
            if x != "" and x != "\n":
                fin_col.append(x.strip())
        if len(fin_col) == 1:
            final_columns[fin_col[0]] = fin_col
        else:
            final_columns[fin_col[0]] = fin_col[1:]
print(final_columns)
del(final_columns['Write Columns to combine below [Row Wise]'])            


# In[30]:


for key in final_columns:
    final_columns[key] = list(OrderedDict.fromkeys(final_columns[key]))


# In[33]:


file_list2 = []
for file in os.listdir():
    if file.endswith(".csv") and file != "Combiner_Columns.csv":
        file_name = file.split(".")[0]
        df = pd.read_csv(file)
        for k in final_columns:
            for v in final_columns[k]:
                df.rename({v:k},axis=1,inplace=True)
        for k_col in final_columns.keys():
            if k_col not in df.columns:
                df[k_col] = ""
        df = df[final_columns.keys()]
        df.to_csv(f"{file_name}_chikku_combined.csv",index=False)
        file_list2.append(f"{file_name}_chikku_combined.csv")
        print(f"Formating {file}")
    


# In[34]:


combiner_list = []
for file in file_list2:
    if file.endswith(".csv"):
        print(f"Combining {file}")
        df = pd.read_csv(file, index_col=None, header=0)
        combiner_list.append(df)
frame = pd.concat(combiner_list, axis=0, ignore_index=True)
frame.to_csv("Combined.csv",index=False)
print("Done! combined and saved in Combined.csv")


# In[ ]:



