#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
from Drive import *


# In[2]:


def mydayCleaner(data):
    idx=np.array([])
    for date,month in zip(data['Date'].values,data['Month'].values):
        date_mask=data['Date']==date
        month_mask=data['Month']==month
        task_mask=data['Task']=='AjKyaUkhada'
        d=data[date_mask & month_mask & task_mask].sort_values('Student')
        idx=np.append(idx,d[d.duplicated(subset=['Student'],keep='last')].index)
    data.drop(idx,inplace=True)
    return data


# In[3]:


def knowledgeSharingCleaner(data):
    idx=np.array([])
    knowledge_sharing_days={'Monday':['Kunal','Bhavna','Apurwa'],                       'Tuesday':['Chandrima','Purbita','Prasoon'],                        'Wednesday':['Roumyak','Kaushal','Ujjainee'],                       'Thursday':['Siddhishikha','Dipam','Shakib'],                        'Friday':['Sonali','Durga','Sonali'],                       'Saturday':['Swaastick','Sharika','Vishal'],                       'Sunday':['Anjali','Arya','Surabhi']} 
    date_month_dayname_unique=data[['Date','Month','DayName']].drop_duplicates()
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
    return data


# In[4]:


def data_cleaner(data):
    """This method will clean the data thoroughly and return the cleaned dataframe"""
    data=data.dropna(how='all',axis=0)
    data.replace('Ajkyaukhada','AjKyaUkhada',inplace=True)
    data['Date']=pd.to_datetime(data['Date'],errors='ignore',infer_datetime_format=True,dayfirst=True)
    data.dropna(subset=['Student'],inplace=True)
    data.replace('Swaastik','Swaastick',inplace=True)
    data.replace('Sushree','Siddhishikha',inplace=True)
    niteshIndex=data[data['Student']=='Nitish'].index
    data.drop(niteshIndex,inplace=True)
    data['Month']=data['Date'].dt.month_name()
    data['Year']=data['Date'].dt.year
    data['DayName']=data['Date'].dt.weekday_name
    data['Date']=data['Date'].dt.day
    data=mydayCleaner(data)
    data=knowledgeSharingCleaner(data)
    del niteshIndex
    return data

