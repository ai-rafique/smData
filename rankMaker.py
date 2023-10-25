# import necessary libraries
import pandas as pd

# import the dataset
df = pd.read_csv('https://raw.githubusercontent.com/ai-rafique/smData/main/projectData.csv')

# extract info about elements of the dataset
df.info()

# List of metric names used in loaded dataset
col_list=[
 'LCOM( badness ratio)',
 'I',
 'CBO (median aggreg)',
 'MPC',
 'v(G)tot',
 'RFC (median aggreg)',
 'D',
 'C',
 'METH',
 'LOC',
 'TCOM_RAT',
 'Jc']

# dataframe to enlist all package names
packed = pd.DataFrame(df['Package'].unique())

# Split the dataset by version name into 7 distinct dataframes
df1 = df[df['VersionName'] == '3.0.3']
df2 = df[df['VersionName'] == 'nightly-187a2b3']
df3 = df[df['VersionName'] == 'nightly-6d119b1']
df4 = df[df['VersionName'] == 'nightly-47c3f74']
df5 = df[df['VersionName'] == '3.1.0']
df6 = df[df['VersionName'] == 'nightly-2020-06-25']
df7 = df[df['VersionName'] == '3.2.0']

# list of split by version datasets 
df_list=[df1,df2,df3,df4,df5,df6,df7]

# Dataset to collect package name and ranking value. The list is converted to pandas dataframe.
column_names = ["Names", "Value"]
df_improv = pd.DataFrame(columns=column_names)



"""
The code iterates over 7 versions
In each version, we will get one metric, and sort them in descending order xcept for TCOM_RAT and Jc metric
At the end of 1 cycle, a single version rank document will be generated along with an aggregation (group by sum from name) document.
At the end of 7 cycles, all aggregation documents are stitched to show sum of all metric ranks in all versions.

The file is called Aggregation.csv
"""
for x in range(0,len(df_list)):
  df_val=[]
  df_col=[]
  counter=1
  for j in range(0, len(col_list)):
    if col_list[j] == "TCOM_RAT":
      for i in df_list[x].sort_values(by=[col_list[j]],ascending=True).iloc[:,2]:
        #print(j+1,i)
        df_val.append(counter)
        df_col.append(i)
        counter = counter+1
    elif col_list[j] == "Jc":
      for i in df_list[x].sort_values(by=[col_list[j]],ascending=True).iloc[:,2]:
        #print(j+1,i)
        df_val.append(counter)
        df_col.append(i)
        counter = counter+1
    else:
      for i in df_list[x].sort_values(by=[col_list[j]],ascending=False).iloc[:,2]:
        #print(j+1,i)
        df_val.append(counter)
        df_col.append(i)
        counter = counter+1
    counter = 1
  print()
  df_val=pd.Series(df_val)
  df_col=pd.Series(df_col)
  df_improv['Value']=df_val
  df_improv['Names']=df_col
  df_improv.to_csv(f"{x+1}.csv",index=False)
  df1_reader = pd.read_csv(f"{x+1}.csv")
  df1_reader= df1_reader.groupby('Names').sum()
  df1_reader.to_csv(f"{x+1}_aggreg.csv",index=False)
  df_collect=pd.read_csv(f"{x+1}_aggreg.csv")
  packed[f"v{x+1}"]=df_collect
packed.to_csv('Aggregation.csv',index=False)
