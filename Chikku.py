#!/usr/bin/env python
# coding: utf-8

# In[29]:


import pandas as pd
import os
from collections import OrderedDict


# In[13]:
def divide_chunks(l, n):
      
    # looping till length l
    for i in range(0, len(l), n): 
        yield l[i:i + n]

def get_first_columns(file):
    with open(file,"r",encoding='utf-8') as f:
        first_line = f.readline().strip()
    return first_line.split(",")


# In[14]:

unique_columns = []
column_names = {}
for file in os.listdir():
    if file.endswith(".csv") and file != "Combiner_Columns.csv":
        column_names[file] = []


# In[15]:


print("Starting the script")
print("\nReading all csv files in the current directory\n***********")
try:
    os.remove("Combiner_Columns.csv")
except:
    pass
for file in os.listdir():
    if file.endswith(".csv") and file != "Combiner_Columns.csv":
        print(f"Reading {file} columns")
        file_columns = get_first_columns(file)

        unique_columns.extend(file_columns)
        column_names[file].extend(sorted(file_columns))
   


# In[16]:


for x in column_names:
    column_names[x].insert(0,x)


# In[17]:

print(f"\nCreating Combiner_Columns.csv file for combiner configuration\n***********")
combiner_column_list = []
combiner_column_list.append(f"File Names,Columns")
combiner_column_list.append("***********")
for key,value in column_names.items():
    value = str(value).replace("'","")[1:-1]
    combiner_column_list.append(value)
unique_columns = sorted(set(unique_columns))
# unique_columns.insert(0,"All unique columns")
combiner_column_list.append("**********************")
combiner_column_list.append("All unique columns")
unique_columns = list(divide_chunks(unique_columns, 7))
# print(x)
for each_row in unique_columns:
    combiner_column_list.append(",".join(each_row))
# combiner_column_list.append(",".join(unique_columns))
# print(combiner_column_list)
combiner_column_list.append("")
combiner_column_list.append("Write Columns to combine below [Row Wise]")


# In[20]:

with open('Combiner_Columns.csv', 'w') as f:
    f.writelines('\n'.join(combiner_column_list))


print(f"Done Creating Combiner_Columns.csv file")

# In[21]:

# try:
#     os.system("libreoffice Combiner_Columns.csv")
# except:
#     os.system("Start Excel Combiner_Columns.csv")
print("\nPlease edit the Combiner_Columns.csv file that is created in the current directory")

usr_input = input("\nDone editing the Combiner_Columns.csv file[Y/N] ")
if "y" in usr_input.lower():
    pass
else:
    print(f"Run the script again.")
    exit()

# In[25]:
print()

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

del(final_columns['Write Columns to combine below [Row Wise]'])            


# In[30]:


for key in final_columns:
    final_columns[key] = list(OrderedDict.fromkeys(final_columns[key]))


# In[33]:


file_list2 = []
for file in os.listdir():
    if file.endswith(".csv") and file != "Combiner_Columns.csv":
        file_name = file.split(".")[0]
        df = pd.read_csv(file,low_memory=False)
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
    
del df

# In[34]:

print("Combing the files\n***********")
combiner_list = []
for file in file_list2:
    if file.endswith(".csv"):
        print(f"Combining {file}")
        df = pd.read_csv(file, index_col=None, header=0,low_memory=False)
        combiner_list.append(df)
frame = pd.concat(combiner_list, axis=0, ignore_index=True)
frame.to_csv("Combined.csv",index=False)

for fi in os.listdir():
    if fi.endswith("_chikku_combined.csv"):
        os.remove(fi)
        
print("Done! combined and saved in Combined.csv")
