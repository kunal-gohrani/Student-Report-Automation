#!/usr/bin/env python
# coding: utf-8

# In[1]:


#!pip install reportlab


# In[8]:


from reportlab.platypus import SimpleDocTemplate, Paragraph,Spacer, Table, PageBreak,LongTable,TableStyle
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import *
from reportlab.lib.pagesizes import *
from reportlab.lib.enums import TA_CENTER,TA_JUSTIFY,TA_LEFT,TA_RIGHT
from reportlab.lib import colors
import numpy as np
import AnalysisScript,SupportFunctions
import os


# In[9]:


class PdfMaker:
    def __init__(self):
        self.a=AnalysisScript.Analysis()
        self.data=self.a.data
    def month_check(self,month,month_list):
        if (month in month_list):
            return True
        else:
            return False
        
    def row_table_builder2(self,dataframe):
        row_list=np.array([])
        row_list=np.append(row_list,dataframe.columns.tolist()).reshape(1,8)
        data=np.array(dataframe).astype('str')
        #print(data)
        for i in np.nditer(data,flags = ['external_loop'], order = 'C'):
            row_list=np.append(row_list,[i],axis=0)
        return row_list.tolist()
    
    def generate_report_monthly(self,month,name):
        if not os.path.exists('pdfs'):
            os.mkdir('pdfs')
        data=self.data
        a=self.a
        previous_month={'January':'December','February':'January','March':'February','April':'March','May':'April',                        'June':'May','July':'June','August':'July','September':'August','October':'September',                        'November':'October','December':'November'}
        if self.month_check(month,a.months):
            file_name=name+'_'+month+'.pdf'
            path=os.path.join('pdfs',file_name)
            doc=SimpleDocTemplate(path,pagesize=A4,topMargin=10,bottomMargin=20,leftMargin=25,rightMargin=25)
            flowables=[]
            style=getSampleStyleSheet()

            # Setting style
            style['Heading1'].leading=35
            style['Normal'].fontName='Helvetica'
            style['Normal'].fontSize=12
            style['Normal'].leading=20

            # title of the report
            title="""<para align=center><font face=helvetica size=24 color=blue><b>CampusX Monthly Report</b>
                    <br/></font></para>"""
                    #Month: {m}<br/></font></para>""".format(m=month)

            # Appending to flowables list
            flowables.append(Paragraph(title,style=style['Heading1']))
            flowables.append(Spacer(1,40))

            # greeting
            nameText="""<font face=Helvetica><b>Hi <i>{}</i>, This is your monthly report for the month of {}.</b></font>""".format(name,month)

            # Appending to flowables list
            flowables.append(Paragraph(nameText,style=style['Normal']))
            flowables.append(Spacer(1,40))

            # Extracting data for first table
            rank=str(a.get_rank(name=name,month_name=month))
            total_marks=str(a.get_total_marks(name=name,month_name=month))
            late_submissions=str(SupportFunctions.get_count_late_submission(data=data,name=name,month_name=month))
            task_won=str(SupportFunctions.get_count_task_won(data=data,name=name,month_name=month))

            # For myday and knowledge count, we need to check for null values, so below code checks for null values
            # my day
            myday_count=a.student_myday(name=name,month_name=month)[0]['Number of days'].values.tolist()
            if len(myday_count)>0:
                myday_count=myday_count[0]
            else:
                myday_count=0

            # knowledge
            knowledge_sharing_count=a.student_knowledge_marks(name=name,month_name=month)[0]['Number of days'].values.tolist()
            if len(knowledge_sharing_count)>0:
                knowledge_sharing_count=knowledge_sharing_count[0]
            else:
                knowledge_sharing_count=0
            initialColumns=['Rank','Total Marks','MyDay Count','Knowledge Sharing Count','Late Submissions','Task\'s Won']

            # Creating first table and appending to flowables
            initial_tbl_data=[initialColumns,[rank,total_marks,myday_count,knowledge_sharing_count,late_submissions,task_won]]
            first_table=Table(initial_tbl_data,hAlign='CENTER')
            tblstyle=TableStyle([('FONT',(0,0),(-1,0),'Helvetica-Bold',10)])
            first_table.setStyle(tblstyle)
            flowables.append(first_table)
            flowables.append(Spacer(1,30))

            # Tasks
            text=Paragraph('<para align=left><font face=helvetica size=15><b>Tasks:</b></font></para>',style=style['Heading2'])
            flowables.append(text)
            task_data=self.row_table_builder2(dataframe=a.student_task_marks(name=name,month_name=month)[0])
            task_table=Table(task_data,hAlign='LEFT')
            tblstyle=TableStyle([('FONT',(0,0),(-1,0),'Helvetica-Bold',10)])
            task_table.setStyle(tblstyle)
            flowables.append(task_table)

            # Leaderboard
            #flowables.append(PageBreak())
            flowables.append(Spacer(1,15))
            text=Paragraph('<para align=left><font face=helvetica size=15><b>Leaderboard:</b></font></para>',style=style['Heading2'])
            flowables.append(text)
            leaderboard_monthly_table=self.row_table_builder2(dataframe=a.total_marks_leaderboard(month_name=month)[0])
            leaderboard_monthly_table = LongTable(leaderboard_monthly_table,hAlign='CENTER')
            tblstyle = TableStyle ([('FONT',(0,0),(-1,0),'Helvetica-Bold',9),
                                    ( 'FONT' , ( 0 ,1), ( - 1 , -1 ), 'Helvetica' , 6 ),
                                   ('BOX',(0,0),(-1,-1),0.5,colors.black),
                                   ('INNERGRID',(0,0),(-1,-1),0.5,colors.black)
                                    ])
                                   #( 'ROWBACKGROUNDS' , ( 0 , 1 ), ( - 1 , - 1 ), [ colors . gray , colors . white ]),
                                    #('COLBACKGROUNDS',(0,0),(-1,0),[colors.aqua])
                                   #])
            leaderboard_monthly_table.setStyle(tblstyle)
            flowables.append(leaderboard_monthly_table)

            flowables.append(PageBreak())
            text=Paragraph('<para align=left><font face=helvetica size=15><b>Previous Month\'s Leaderboard:</b></font></para>',style=style['Heading2'])
            flowables.append(text)
            flowables.append(Spacer(1,20))
            leaderboard_prev_month_data=self.row_table_builder2(dataframe=a.total_marks_leaderboard(month_name=previous_month[month])[0])
            leaderboard_prev_month_table=LongTable(leaderboard_prev_month_data,hAlign='CENTER')
            tblstyle = TableStyle ([('FONT',(0,0),(-1,0),'Helvetica-Bold',9),
                                    ( 'FONT' , ( 0 ,1), ( - 1 , -1 ), 'Helvetica' , 6 ),
                                   ('BOX',(0,0),(-1,-1),0.5,colors.black),
                                   ('INNERGRID',(0,0),(-1,-1),0.5,colors.black)
                                    ])
                                   #( 'ROWBACKGROUNDS' , ( 0 , 1 ), ( - 1 , - 1 ), [ colors . gray , colors . white ]),
                                    #('COLBACKGROUNDS',(0,0),(-1,0),[colors.aqua])
                                   #])
            leaderboard_prev_month_table.setStyle(tblstyle)
            flowables.append(leaderboard_prev_month_table)
            doc.build(flowables)
        
if __name__=='__main__':
    obj=PdfMaker()
    obj.generate_report_monthly('September','Kunal')


# In[ ]:




