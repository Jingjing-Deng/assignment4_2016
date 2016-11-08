
# coding: utf-8

# In[10]:

from pandas import *
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


#define a function to extract patient_name from the excel
def patient_name(row):
    sample=row['Sample ID'].strip().split()
    for value in row['Sample ID'].strip().split():
        if value in ['v1','v2','v3','V1','V2','V3','10','100','1000','10000','100000','1000000','10000000']:
            sample.remove(value)
    return '_'.join(sample)


#define a function to return a name set for each sheet
def patient_name_set(df):
    set_name=set()
    for i, row in df.iterrows():
        set_name.add(row['patient_name'])
    return set_name

#define a function to extract the patient title
def plot_title(df):
    titles={}
    for i, row in df.iterrows():
        if isinstance(row['Hospital '], str):
            titles[row["patient_name"]] = "_".join([row['Hospital '], str(row['Age']), 'year', str(row['Gender']),molecule])
    return titles
   
def plot_for_standard(df, molecule,i):
    fig, ax = plt.subplots(1,1)
    df.plot(ax=ax,x='dilution1',y=molecule,marker='o',title=['sheet'+str(i)+'standard', molecule])
    ax.set_xscale('log')
    ax.set_yscale('log')
    plt.xlabel("Dilution")
    plt.ylabel("Intensity")
    fig.savefig('./output/' + 'sheet'+str(i)+'Standard' + "_" + molecule.replace(" ", "") + ".png")
    plt.close(fig)

    
def plot_for_patient(df, molecule):
    fig, ax = plt.subplots(1,1)
    labels = []

    for key, grp in df.groupby(['visit_time']):
        ax.set_xscale('log')
        ax.set_yscale('log')
        ax = grp.plot(ax=ax, kind='line', x='dilution1', y= molecule, marker='o',title=plot_title(df_sp))
        labels.append(key)
    plt.xlabel("Dilution")
    plt.ylabel("Intensity")
              
    lines, _ = ax.get_legend_handles_labels()
    ax.legend(lines, labels, loc='best')
    fig.savefig('./output/' + patient + "_" + molecule.replace(" ", "") + ".png")
    plt.close(fig)
    



# In[2]:

#list of target moleculars for plots
colls=['PSMalpha2', 'PSMalpha3',
       'psmalpah4', 'BSA', 'Betatoxin', 'hIgA', 'LDL', 'SEB',
       'S.Pyogenese arcA', 'LukE', 'Pn PS12', 'LukD', 'Pn PS23', 'HLA-1',
       'SpA domD5-WT', 'Glom.extract', 'SpA domD5FcNull', 'SEN', 'hIgG', 'SEU',
       'HLA', 'SEI', 'LukAB(Lab)', 'SEM', 'LukAB(cc30)', 'surface protein ext',
       'SEB.1', 'cytoplasmic ext', 'Hemolysin gamma A', 'Pn CWPS',
       'Hemolysin gamma B', 'ABA', 'Hemolysin gamma C', 'PC-12', 'LukS-PV',
       'SEO', 'SP', 'SEG', 'PLY', 'HSA', 'Exoprotein ext', 'Rabbit IgG',
       'LukF-PV', 'PSM 4variant', 'PC4', 'PNAG', 'PC16', 'HLA -2',
       'Tetanus Toxoid']



# In[3]:

dfs=[]
for i in range(11):
    #read all the sheets to a list of dataframes
    dfs.append(pandas.read_excel(open('06222016 Staph Array Data.xlsx','rb'), skiprows=1, sheetname=i))
#modify some value in the excel sheets
dfs[1].ix[0,0]='Standard 10'
dfs[1].ix[1,0]='Standard 100'
dfs[1].ix[2,0]='Standard 1000'
dfs[1].ix[3,0]='Standard 10000'
dfs[1].ix[4,0]='Standard 100000'
dfs[1].ix[5,0]='Standard 1000000' 
dfs[1].ix[6,0]='Standard 10000000'
dfs[5].ix[0,0]='Standard 10'
dfs[5].ix[1,0]='Standard 100'
dfs[5].ix[2,0]='Standard 1000'
dfs[5].ix[43,0]='99361 V2 100'
dfs[6].ix[0,0]='Standard 10'
dfs[6].ix[1,0]='Standard 100'
dfs[6].ix[2,0]='Standard 1000'
dfs[7].ix[0,0]='Standard 10'
dfs[7].ix[1,0]='Standard 100'
dfs[7].ix[2,0]='Standard 1000'
dfs[8].ix[0,0]='Standard 10'
dfs[8].ix[1,0]='Standard 100'
dfs[8].ix[2,0]='Standard 1000'
dfs[10]['Hospital '] =""
dfs[10]['Age '] =""
dfs[10]['Gender'] =""

print(str(dfs[0].ix[8,2]))


# In[11]:

for i in range(11):
    #extract dilution value from the excel
    dfs[i]['dilution']=dfs[i].apply(lambda row: row['Sample ID'].strip().split()[-1], axis=1)
    #extract visit times from the excel
    dfs[i]['visit_time']=dfs[i].apply(lambda row: row['Sample ID'].strip().split()[-2] if len(row['Sample ID'].strip().split())>2 and row['Sample ID'].strip().split()[-2] in ['v1','v2','v3','V1','V2','V3'] else '', axis=1)
    #extract dilution value from the excel
    dfs[i]['patient_name']=dfs[i].apply(patient_name,axis=1)
    #use the function to get the patien_name list
    patient_names=patient_name_set(dfs[i])
    for patient in patient_names:
        #filtered dataframe to one patient
        df_sp=dfs[i].loc[dfs[i]['patient_name'] == patient]
        #plotting for each patient for specific molecule
        for molecule in colls:
            patient_title=plot_title(df_sp)         
            #filtered dataframe to one patient, one molecule
            df_sp_sm=df_sp.ix[:,[molecule,'visit_time','dilution','Sample ID']]
            #transfer column-dilution to interger
            df_sp_sm["dilution1"] = df_sp_sm.apply(lambda row: int(row["dilution"]), axis=1)
            if np.isnan(df_sp_sm.iloc[0][molecule]): #skip nan value in the dataframe
                continue
            #ploting lines in one plot, one line for one visit
            #plot for standard1,2,,7 without dilution provided                      
            if 'Standard' == patient:
                plot_for_standard(df_sp_sm, molecule,i)
            else:
                plot_for_patient(df_sp_sm, molecule)


                


# In[ ]:


    


# In[ ]:


    


# In[ ]:




# In[ ]:



