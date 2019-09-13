#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import imagekit
import imgkit
get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


from Drive import GDriveAuthenticator,Gdrive


# In[3]:


dir()


# In[4]:


auth=GDriveAuthenticator.GDriveAuthenticator('Drive\\client_secret.json')
drive=Gdrive.Gdrive(auth.authenticate())


# In[5]:


drive.download()


# In[6]:


excel_sheet=pd.read_excel('Student Gradebook.xlsx',sheet_name=None,usecols=range(0,10))


# In[7]:


len(excel_sheet)


# In[8]:


data_july=excel_sheet['July'].copy()
data_august=excel_sheet['August'].copy()


# In[9]:


data_july.head()


# In[10]:


data_august.head()


# In[11]:


data=pd.concat([data_july,data_august]).reset_index().drop(columns=['index'])


# In[12]:


del data_july
del data_august


# In[13]:


data


# In[14]:


data=data.dropna(how='all',axis=0)


# In[15]:


data.info()


# # Task column

# In[16]:


data['Task'].value_counts().sort_values(ascending=False)


# AjKyaUkhada has two spellings in july data, need to fix it.

# In[17]:


data.replace('Ajkyaukhada','AjKyaUkhada',inplace=True)


# In[18]:


data['Task'].value_counts().sort_values(ascending=False)


# # Date columns

# In[19]:


data.head()


# In[20]:


data.info()


# July has date time dtype but august doesn't, let's fix it.

# In[21]:


225+746


# In[22]:


data['Date']=pd.to_datetime(data['Date'],errors='ignore',infer_datetime_format=True,dayfirst=True)


# In[23]:


data.info()


# In[24]:


data[data['Date'].dt.month==8]


# # Module Column

# In[25]:


data['Module'].value_counts()


# No problem with module column, also no null values

# # Type column

# In[26]:


data['Type'].value_counts()


# No problem in type column, nothing so to understand

# # Student column

# We know from above info(), data_august has some null values, let's see to it

# In[27]:


data[data['Student'].isnull()]


# Since, there is no way to correctly fill this data, we are just gonna drop those rows.

# In[28]:


data.dropna(subset=['Student'],inplace=True)


# In[29]:


data.info()


# In[30]:


np.sort(data['Student'].unique())


# #### Spelling error fixings
# From the above 2 rows, we can see that there are different names in the data, Sushree and Siddhishikha is the same person, same for Swaastik and Swaastick.

# In[31]:


data.replace('Swaastik','Swaastick',inplace=True)


# In[32]:


data.replace('Sushree','Siddhishikha',inplace=True)


# In[33]:


np.sort(data['Student'].unique())


# The name problem has been resolved.

# In[34]:


data.head()


# In[35]:


niteshIndex=data[data['Student']=='Nitish'].index
data.drop(niteshIndex,inplace=True)


# # Total Marks of students

# In[36]:


total_marks=data.groupby('Student')['Points'].sum().sort_values(ascending=False).reset_index()
total_marks


# In[37]:


# Task Marks
knowledge='Knowledge Sharing'
myday='AjKyaUkhada'
task_marks=data[(data['Task']!=knowledge) & (data['Task']!=myday)].groupby('Student')['Points'].sum().sort_values(ascending=False).reset_index()
task_marks


# In[38]:


# MyDay marks
myday_count=data[data['Task']==myday].groupby('Student')['Points'].count().sort_values(ascending=False).reset_index().style.hide_index()
myday_marks=data[data['Task']==myday].groupby('Student')['Points'].sum().sort_values(ascending=False).reset_index().style.hide_index()
myday_count


# In[39]:


# Knowledge Sharing marks
knowledge_marks=data[data['Task']==knowledge].groupby('Student')['Points'].sum().sort_values(ascending=False).reset_index().style.hide_index()
knowledge_marks


# # Analysing the consistency of each student in myday and knowledge sharing rituals
# For this, first we need to make a cleaning script for both the rituals, the rules to be followed are:-  
# - There should be only one myday for each date, students giving more than one myday in a particular date need to be checked for
# - Knowledge sharing has 2 marks, but each student is alloted a specific day in which he/she will get marks for sharing knowledge. 

# # Myday Cleaner Script

# The data that we need for these scripts must be added to DataFrame first, they are:- Date in month (note: there is already a date column), Month, Year, Day of week.

# In[40]:


data['Month']=data['Date'].dt.month_name()
data['Year']=data['Date'].dt.year
data['DayName']=data['Date'].dt.weekday_name
data['Date']=data['Date'].dt.day


# In[41]:


data.info()


# In[42]:


# Code to remove duplicate mydays
def mydayCleaner():
    idx=np.array([])
    for date,month in zip(data['Date'].values,data['Month'].values):
        date_mask=data['Date']==date
        month_mask=data['Month']==month
        task_mask=data['Task']=='AjKyaUkhada'
        d=data[date_mask & month_mask & task_mask].sort_values('Student')
        idx=np.append(idx,d[d.duplicated(subset=['Student'],keep='last')].index)
    data.drop(idx,inplace=True)


# In[43]:


mydayCleaner()


# In[44]:


data


# # Knowledge cleaner script

# In[45]:


data['DayName'].unique()


# In[46]:


np.sort(data['Student'].unique())


# In[47]:


knowledge_sharing_days={'Monday':['Kunal','Bhavna','Apurwa'],                       'Tuesday':['Chandrima','Purbita','Prasoon'],                        'Wednesday':['Roumyak','Kaushal','Ujjainee'],                       'Thursday':['Siddhishikha','Dipam','Shakib'],                        'Friday':['Sonali','Durga','Sonali'],                       'Saturday':['Swaastick','Sharika','Vishal'],                       'Sunday':['Anjali','Arya','Surabhi']} 


# In[48]:


date_month_dayname_unique=data[['Date','Month','DayName']].drop_duplicates()


# In[49]:


dateMask=data['Date']==9
monthMask=data['Month']=='September'
daynameMask=data['DayName']=='Monday'
taskMask=data['Task']=='Knowledge Sharing'
temp=data[dateMask & monthMask & daynameMask & taskMask]
temp


# In[50]:


# official code to remove duplicate and no proper day marks of knowledge sharing
def knowledgeSharingCleaner():
    idx=np.array([])
    for date,month,dayname in zip(date_month_dayname_unique['Date'].values.tolist(),date_month_dayname_unique['Month'].values.tolist(),date_month_dayname_unique['DayName'].values.tolist()):
        dateMask=data['Date']==date
        monthMask=data['Month']==month
        daynameMask=data['DayName']==dayname
        taskMask=data['Task']=='Knowledge Sharing'
        temp=data[dateMask & monthMask & daynameMask & taskMask]

        # Below for loop filters out those rows for which students and daynames dont match
        # Example:- if dipam posts on gyan on monday, then he wont be given marks
        for index,name in zip(temp.Student.index,temp.Student.values):
            if name not in knowledge_sharing_days[dayname]:
                idx=np.append(idx,index)
        # After the first loop is run (description given on top), now it's time to filter out
        # those who put more than one post in gyan channel on the same day
        idx=np.append(idx,temp[temp.duplicated(subset=['Student'],keep='last')].index)
    data.drop(idx,inplace=True)


# In[51]:


knowledgeSharingCleaner()


# In[52]:


# Make sure to change both dayname and date, otherwise false error u will think
dateMask=data['Date']==9
monthMask=data['Month']=='September'
daynameMask=data['DayName']=='Monday'
taskMask=data['Task']=='Knowledge Sharing'
temp=data[dateMask & monthMask & daynameMask & taskMask]
temp


# In[55]:


#idx=np.array([])


# In[56]:


#np.append(idx,a)


# In[57]:


#temp['Student'].index.tolist()


# In[58]:


#idx=np.array([])
#for i,name in zip(temp.Student.index,temp.Student.values):
#    if name not in knowledge_sharing_days['Monday']:
#        print(i)
#        idx=np.append(idx,i)


# In[59]:


#idx


# In[60]:


#idx=np.array([])
#for i,name in zip(temp.Student.index,temp.Student.values):
#    if name not in knowledge_sharing_days['Monday']:
#        idx=np.append(idx,i)


# In[61]:


#idx


# # Marks after all cleaning

# In[62]:


total_marks=data.groupby('Student')['Points'].sum().sort_values(ascending=False).reset_index()
total_marks


# In[63]:


# Task Marks
knowledge='Knowledge Sharing'
myday='AjKyaUkhada'
task_marks=data[(data['Task']!=knowledge) & (data['Task']!=myday)].groupby('Student')['Points'].sum().sort_values(ascending=False).reset_index()
task_marks


# In[66]:


# MyDay marks
myday_count=data[data['Task']==myday].groupby('Student')['Points'].count().sort_values(ascending=False).reset_index().style.hide_index()
myday_marks=data[data['Task']==myday].groupby('Student')['Points'].sum().sort_values(ascending=False).reset_index().style.hide_index()
myday_marks


# In[65]:


# Knowledge Sharing marks
knowledge_marks=data[data['Task']==knowledge].groupby('Student')['Points'].sum().sort_values(ascending=False).reset_index().style.hide_index()
knowledge_marks


# In[ ]:




