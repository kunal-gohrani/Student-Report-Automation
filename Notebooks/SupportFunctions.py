#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
from Drive import *


# In[2]:


months=['January','February','March','April','May',                     'June','July','August','September','October',                     'November','December']


# In[3]:


def get_myday(name,data,month_name=None):
    if name==None:
        raise ValueError('No name provided')
    if month_name==None:
        myday='AjKyaUkhada'
        myday_marks=data[data['Task']==myday].groupby('Student')['Points'].sum().sort_values(ascending=False).reset_index()
        temp=myday_marks[myday_marks['Student']==name]['Points'].values
        if len(temp)>0:
            return temp[0]
        else:
            return 0
    elif month_name in months:
        myday='AjKyaUkhada'
        myday_marks=data[(data['Task']==myday) & (data['Month']==month_name)].groupby('Student')['Points'].sum().sort_values(ascending=False).reset_index()
        temp=myday_marks[myday_marks['Student']==name]['Points'].values
        if len(temp)>0:
            return temp[0]
        else:
            return 0
    else:
        raise ValueError('month_name has wrong spelling supplied')


# In[4]:


def get_task(name,data,month_name=None):
    knowledge='Knowledge Sharing'
    myday='AjKyaUkhada'
    if month_name==None:
        task_marks=data[(data['Task']!=knowledge) & (data['Task']!=myday)].groupby('Student')['Points'].        sum().sort_values(ascending=False).reset_index()
        temp=task_marks[task_marks['Student']==name]['Points'].values
        if len(temp)>0:
            return temp[0]
        else:
            return 0
    elif month_name in months:
        task_marks=data[(data['Task']!=knowledge) & (data['Task']!=myday) & (data['Month']==month_name)].groupby('Student')['Points'].        sum().sort_values(ascending=False).reset_index()
        temp=task_marks[task_marks['Student']==name]['Points'].values
        if len(temp)>0:
            return temp[0]
        else:
            return 0
    else:
        raise ValueError('month_name has wrong spelling supplied')


# In[5]:


def get_gyan(name,data,month_name=None):
    if month_name==None:
        knowledge_marks=data[data['Task']=='Knowledge Sharing'].groupby('Student')['Points'].sum().sort_values(ascending=False).        reset_index()
        temp=knowledge_marks[knowledge_marks['Student']==name]['Points'].values
        if len(temp)>0:
            return temp[0]
        else:
            return 0
    elif month_name in months:
        knowledge_marks=data[(data['Task']=='Knowledge Sharing') & (data['Month']==month_name)].groupby('Student')['Points'].sum().sort_values(ascending=False).        reset_index()
        temp=knowledge_marks[knowledge_marks['Student']==name]['Points'].values
        if len(temp)>0:
            return temp[0]
        else:
            return 0
    else:
        raise ValueError('month_name has wrong spelling supplied')


# In[6]:


def get_count_late_submission(name,data,month_name=None):
    if month_name==None:
        count=data[data['Late Submission']==1].groupby('Student')['Late Submission'].count().sort_values(ascending=False).        reset_index()
        temp=count[count['Student']==name]['Late Submission'].values
        if len(temp)>0:
            return temp[0]
        else:
            return 0
    elif month_name in months:
        count=data[(data['Late Submission']==1) & (data['Month']==month_name)].groupby('Student')['Late Submission'].count().        reset_index()
        temp=count[count['Student']==name]['Late Submission'].values
        if len(temp)>0:
            return temp[0]
        else:
            return 0
    else:
        raise ValueError('Month wrongly spelled')


# In[7]:


def get_highest_marks(name,data,month_name=None):
    if name==None:
        raise ValueError('Name:',name)
    if month_name==None:
        temp=data.groupby('Student')['Total'].sum().reset_index()
        temp=temp[temp['Student']==name]['Total'].values
        if len(temp)>0:
            return temp[0]
        else:
            return 0
    elif month_name in months:
        temp=data[data['Month']==month_name].groupby('Student')['Total'].sum().reset_index()
        temp=temp[temp['Student']==name]['Total'].values
        if len(temp)>0:
            return temp[0]
        else:
            return 0
    else:
        raise ValueError('month spelled wrong')


# In[8]:


def get_count_task_won(name,data,month_name=None):
    if month_name==None:
        count=data[data['Task Winner']==1].groupby('Student')['Task Winner'].count().sort_values(ascending=False).        reset_index()
        temp=count[count['Student']==name]['Task Winner'].values
        if len(temp)>0:
            return temp[0]
        else:
            return 0
    elif month_name in months:
        count=data[(data['Task Winner']==1) & (data['Month']==month_name)].groupby('Student')['Task Winner'].count().        reset_index()
        temp=count[count['Student']==name]['Task Winner'].values
        if len(temp)>0:
            return temp[0]
        else:
            return 0
    else:
        raise ValueError('Month wrongly spelled')

