#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
from Drive import *
import AnalysisDataCleaner
import SupportFunctions


# In[2]:


class Analysis:
    def __init__(self):
        self.fileDownloader()
        self.data=self.data_importer()
        self.data=AnalysisDataCleaner.data_cleaner(self.data)
        self.months=['January','February','March','April','May',                     'June','July','August','September','October',                     'November','December']
        
    def fileDownloader(self):
        """Downloads Student Gradebook.xlsx from GDrive"""
        try:
            auth=GDriveAuthenticator.GDriveAuthenticator('Drive\\client_secret.json')
            drive=Gdrive.Gdrive(auth.authenticate())
            drive.download()
        except:
            print('Problem in DRIVE API usage')
            raise
            
    def data_importer(self):
        """imports the data and merges into one dataframe and returns it"""
        excel_sheet=pd.read_excel('Student Gradebook.xlsx',sheet_name=None,usecols=range(0,10))
        list_data=[]
        for i in excel_sheet:
            list_data.append(excel_sheet[i])
        #data_july=excel_sheet['July'].copy()
        #data_august=excel_sheet['August'].copy()
        data=pd.concat(list_data).reset_index().drop(columns=['index'])
        #del data_july
        #del data_august
        return data
    
    def total_marks_leaderboard(self,month_name=None):
        """Returns a leaderboard of students containing data such as :- total, task, myday, knowledge sharing marks and
        count of late submissions and task won.
        Arguements:-
        :month_name - [Default: None] if any other value then returns leaderboard for the specified month. Make sure first
        letter of month is capital.

        Returns:
        tuple:- (dataframe object,dataframe with hidden indexes)"""
        data=self.data
        if month_name==None:
            total_marks=data.groupby('Student')['Points'].sum().sort_values(ascending=False).reset_index()
            total_marks.rename(columns={'Points':'Marks'})
            total_marks['Total Marks']=total_marks['Student'].apply(SupportFunctions.get_highest_marks,args=[data])
            total_marks['Task Marks']=total_marks['Student'].apply(SupportFunctions.get_task,args=[data])
            total_marks['MyDay Marks']=total_marks['Student'].apply(SupportFunctions.get_myday,args=[data])
            total_marks['Knowledge Sharing Marks']=total_marks['Student'].apply(SupportFunctions.get_gyan,args=[data])
            total_marks['Late Submissions']=total_marks['Student'].apply(SupportFunctions.get_count_late_submission,args=[data])
            total_marks['Tasks Won']=total_marks['Student'].apply(SupportFunctions.get_count_task_won,args=[data])
            return tuple((total_marks,total_marks.style.hide_index()))
        
        elif month_name in self.months:
            temp=data[data['Month']==month_name]
            total_marks=data[data['Month']==month_name].groupby('Student')['Points'].sum().sort_values(ascending=False).reset_index()
            total_marks.rename(columns={'Points':'Marks'})
            total_marks['Total Marks']=total_marks['Student'].apply(SupportFunctions.get_highest_marks,args=[temp,month_name])
            total_marks['Task Marks']=total_marks['Student'].apply(SupportFunctions.get_task,args=[temp,month_name])
            total_marks['MyDay Marks']=total_marks['Student'].apply(SupportFunctions.get_myday,args=[temp,month_name])
            total_marks['Knowledge Sharing Marks']=total_marks['Student'].apply(SupportFunctions.get_gyan,args=[temp,month_name])
            total_marks['Late Submissions']=total_marks['Student'].apply(SupportFunctions.get_count_late_submission,args=[temp,month_name])
            total_marks['Tasks Won']=total_marks['Student'].apply(SupportFunctions.get_count_task_won,args=[temp,month_name])
            return tuple((total_marks,total_marks.style.hide_index()))
        
        else:
            raise ValueError('month_name has wrong spelling supplied')
            
    def student_task_marks(self,name=None,month_name=None):
        """Returns the task and points of the given student name in DataFrame
        Arguments:
            data: dataframe from which marks need to be extracted
            name: name of the student, only the first name and first letter capital.
            monthWise: default: False
                        set to True if dataframe needed only for a particular month
            month_name: default None.
                        if monthWise True and month_name is name of the month then
                        Dataframe of that particular month is given.

        Returns:
            tuple:- (dataframe object,dataframe with hidden indexes)
        """
        data=self.data
        if name==None:
            raise ValueError('Input a Name')
            
        if month_name!=None:
            if month_name in self.months:
                task_marks=data[(data['Task']!='Knowledge Sharing') & (data['Task']!='AjKyaUkhada') &                                     (data['Student']==name) &                                      (data['Month']==month_name)]
                
            else:
                raise ValueError('Wrong month spelling given')
                
        elif month_name==None:
            task_marks=data[(data['Task']!='Knowledge Sharing') & (data['Task']!='AjKyaUkhada') &                                 (data['Student']==name)]
        task_marks=task_marks[['Date','Month','Task','Student','Points','Total','Late Submission','Task Winner']]
        task_marks['Late Submission'].replace([0,1],['No','Yes'],inplace=True)
        task_marks['Task Winner'].replace([0,1],['No','Yes'],inplace=True)
        return tuple((task_marks,task_marks.style.hide_index()))
    
    def student_myday(self,name=None,month_name=None):
        """Gets the myday marks of the given student
        Arguements:
        name - name of the student
        month_name - [Default: None] name of month to check the dataframe for.

        Returns:
        tuple:- (dataframe object,dataframe with hidden indexes)"""
        data=self.data
        myday='AjKyaUkhada'
        if name==None:
            raise ValueError('Input a name')
        if month_name==None:
            myday_marks=data[(data['Task']==myday) & (data['Student']==name)].groupby('Student')['Points'].                sum().sort_values(ascending=False).reset_index()
            myday_marks.rename(columns={'Points':'Myday Marks'},inplace=True)
            myday_count=data[(data['Task']==myday) & (data['Student']==name)].groupby('Student')['Points'].                count().sort_values(ascending=False).reset_index()
            myday_count.rename(columns={'Points':'Number of days'},inplace=True)
            myday_data=myday_marks.merge(myday_count,on='Student')
            return tuple((myday_data,myday_data.style.hide_index()))
        elif month_name in self.months:
            myday_marks=data[(data['Month']==month_name) & (data['Task']==myday) &                             (data['Student']==name)].groupby('Student')['Points'].                            sum().sort_values(ascending=False).reset_index()
            myday_marks.rename(columns={'Points':'Myday Marks'},inplace=True)
            myday_count=data[(data['Month']==month_name) & (data['Task']==myday) &                              (data['Student']==name)].groupby('Student')['Points'].                            count().sort_values(ascending=False).reset_index()
            myday_count.rename(columns={'Points':'Number of days'},inplace=True)
            myday_data=myday_marks.merge(myday_count,on='Student')
            return tuple((myday_data,myday_data.style.hide_index()))

    def student_knowledge_marks(self,name=None,month_name=None):
        """Gets the knowledge sharing marks of the given student
        Arguements:
        name - name of the student
        month_name - [Default: None] name of month to check the dataframe for.

        Returns:
        tuple:- (dataframe object, dataframe with hidden indexes)
        """
        data=self.data
        knowledge='Knowledge Sharing'
        if name==None:
            raise ValueError('Input a name')
        if month_name==None:
            knowledge_marks=data[(data['Task']==knowledge) & (data['Student']==name)].groupby('Student')['Points'].sum().sort_values(ascending=False).reset_index()
            knowledge_marks.rename(columns={'Points':'Knowledge Sharing Marks'},inplace=True)
            knowledge_count=data[(data['Task']==knowledge) & (data['Student']==name)].groupby('Student')['Points'].count().sort_values(ascending=False).reset_index()
            knowledge_count.rename(columns={'Points':'Number of days'},inplace=True)
            knowledge_data=knowledge_marks.merge(knowledge_count,on='Student')
            return tuple((knowledge_data,knowledge_data.style.hide_index()))
        elif month_name in self.months:
            knowledge_marks=data[(data['Month']==month_name) & (data['Task']==knowledge) & (data['Student']==name)].groupby('Student')['Points'].sum().sort_values(ascending=False).reset_index()
            knowledge_marks.rename(columns={'Points':'Knowledge Sharing Marks'},inplace=True)
            knowledge_count=data[(data['Month']==month_name) & (data['Task']==knowledge) & (data['Student']==name)].groupby('Student')['Points'].count().sort_values(ascending=False).reset_index()
            knowledge_count.rename(columns={'Points':'Number of days'},inplace=True)
            knowledge_data=knowledge_marks.merge(knowledge_count,on='Student')
            return tuple((knowledge_data,knowledge_data.style.hide_index()))
    
    def get_rank(self,name=None,month_name=None):
        """Get the rank of the student, either from the global leaderboard, or from a months leaderboard (if month name
        given)
        :name - name of the student
        :month_name - [Default:None] enter a month to run the function on.

        Returns:
        rank of the student in string format"""
        data=self.data
        
        if name==None:
            raise ValueError('Input a name')

        if month_name==None:
            leaderboard=self.total_marks_leaderboard()[0]
            leaderboard=leaderboard[leaderboard['Student']==name].index
            if len(leaderboard)>0:
                return str(leaderboard[0]+1) #index starts from zero, so index+1 is rank
            else:
                raise Exception('Name wrong.')
        elif month_name in self.months:
            leaderboard=self.total_marks_leaderboard(month_name=month_name)[0]
            leaderboard=leaderboard[leaderboard['Student']==name].index
            if len(leaderboard)>0:
                return str(leaderboard[0]+1) #index starts from zero, so index+1 is rank
            else:
                raise Exception('Wrong name.')
        else:
            raise Exception('Please check spelling of month and try again')
            
    def get_total_marks(self,name=None,month_name=None):
        data=self.data
        if name==None:
            raise ValueError('input name')
        if month_name==None:
            leaderboard=self.total_marks_leaderboard()[0]
            leaderboard=leaderboard[leaderboard['Student']==name]['Points'].values
            if len(leaderboard)>0:
                return str(leaderboard[0]) # returning total marks of the student as string
            else:
                raise Exception('Name wrong.')
        elif month_name in self.months:
            leaderboard=self.total_marks_leaderboard(month_name=month_name)[0]
            leaderboard=leaderboard[leaderboard['Student']==name]['Points'].values
            if len(leaderboard)>0:
                return str(leaderboard[0]) # returning total marks of the student as string
            else:
                raise Exception('Wrong name.')
        else:
            raise Exception('Please check spelling of month and try again')


