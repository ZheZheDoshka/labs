# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 22:22:03 2020

@author: User
"""
import urllib3
import requests
import datetime
import pandas as pd
import os
http = urllib3.PoolManager()
now = datetime.datetime.now()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
today=str("+{}+{}+{}".format(now.day, now.month, now.year))
i = 1
while i <= 5: #загрузка файлов
    now = datetime.datetime.now()
    url1 = 'https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_TS_admin.php?country=UKR&provinceID='
    url2 = str(i)
    url3 = '&year1=1981&year2=1990&type=Mean'
    url = url1+url2+url3
    req = requests.get(url)
    vhi_con = req.content
    file1 = 'vhi_id_'
    file2 = '.csv'
    vremya=str("+{}+{}+{}".format(now.hour, now.minute, now.second))
    filename=file1+url2+today+vremya+file2
    if i==1:
        print(filename)
        primary=filename
    filev = open(filename,'wb') #пропустить 1 строчку
    filev.write(vhi_con)
    filev.close()
    data = pd.read_csv(filename,skiprows=1)
    data.drop(data.tail(1).index,inplace=True) #треба буде далі мучати
    data.to_csv(filename)
    i = i+1
    print ("VHI"+url2+" is downloaded..." )   
    
    
'''def regionchange(): #поменять на словарь
    print("choose the region (enter id)")
    k=int(input())
    dict = { 1:24, 2:25, 3:5, 4:6, 5:20, 6:23, 7:26, 8:7, 9:11, 10:13, 11:14,
            12:15, 13:16, 14:17, 15:18, 16:19, 17:21, 18:22, 19:8, 20:9, 21:10,
            22:1, 23:3, 24:2, 25:4, 26:12}
    if k>26:
        print("there are no such regions")
        i=regionchange()
    elif k<1:
        print("there are no such regions")
        i=regionchange()
    else:
        i=dict.get(k)
    return(i)'''
    
def regionchange_passive(k): #поменять на словарь
    dict = { 1:24, 2:25, 3:5, 4:6, 5:20, 6:23, 7:26, 8:7, 9:11, 10:13, 11:14,
            12:15, 13:16, 14:17, 15:18, 16:19, 17:21, 18:22, 19:8, 20:27, 21:10,
            22:1, 23:3, 24:2, 25:4, 26:12, 27:9}
    i=dict.get(k)
    return(i)
    
       #заменить массив файлов с использованием os(operation system)

def createdf(filename,k): #создача фрейма   #загрузить все в 1 датафрейм, добавить колонку региона
    columns=['row','year','week', 'NDVI', 'PBT', 'VCI', 'TCI', 'VHI']
    data = pd.read_csv(filename,index_col=False, sep=',',header=None,names=columns) 
    df = pd.DataFrame(data)
    df = df[(df.VHI>=0)]
    i=regionchange_passive(k)
    
    df['Region']=i
    return(df)
  
def massive_df(primary):
    i=1
    masdf=pd.DataFrame()
    path=os.getcwd()
    with os.scandir(path) as listOfVHI:
        for entry in listOfVHI:
            if entry.is_file() and entry.name.startswith('v'):
                df=createdf(entry.name,i)
                masdf=masdf.append(df)
                i=i+1
    masdf['month']=(masdf['week']/4.34).astype('int32')+1
    masdf=masdf.sort_values(by='Region')
    print(masdf)
    return(masdf)    
    
mdf=massive_df(primary)
                                                        #три стовпчики: рік, мін, макс для всіх років
                                                        #три стовпчики: рік, мін, макс для всіх років і всіх регіонів (рік і регіон)
                                                        #по місяцях :с перше завдання. (на три кусочки)
def extremum(df):
    print("select_the_region")
    i = int(input())
    temp=df[(df.Region==i)][['year','VHI']]
    temp2=temp.groupby(['year']).max()
    temp2=temp2.rename(columns={"VHI": "VHI_max"})
    temp=temp.groupby(['year']).min()
    temp=temp.rename(columns={"VHI": "VHI_min"})
    temp=temp.join(temp2) 
    temp['Region']=int(i)
    print(temp)                     
    
extremum(mdf)    

def extremum_auto(df, i):
    temp=df[(df.Region==i)][['year','VHI']]
    temp2=temp.groupby(['year']).max()
    temp2=temp2.rename(columns={"VHI": "VHI_max"})
    temp=temp.groupby(['year']).min()
    temp=temp.rename(columns={"VHI": "VHI_min"})
    temp=temp.join(temp2)
    temp['Region']=i
    return(temp)

def extremum_all(df):
    i=2
    alltemp=extremum_auto(df,1)
    while i<=26:
        temp=extremum_auto(df, i)
        alltemp=alltemp.append(temp)
        i=i+1
    print(alltemp)
    
    
extremum_all(mdf)

'''
def extremum_per_year_per_region(df,i,yr):
    m=1
    k=1
    temp=df[(df.Region==i)&(df.year==yr)][['week','VHI']]
    eternal=df[(df.Region==0)&(df.year==0)][['week','VHI']]
    eternal=eternal.sort_values(by='week')
    while m<=12:
        temp2=temp[(temp.week>=k)&(temp.week<=(k+3+(m%2)))]   
        temp2=temp2.replace({k: m*100, k+1: m*100, k+2: m*100, k+3: m*100, (k+3+(m%2)): m*100})
        k=k+4+(m%2)
        m=m+1
        eternal=eternal.append(temp2)
    eternal=eternal.sort_values(by='week')
    eternal=eternal.rename(columns={"week": "month"})
    eternal2=eternal.groupby(['month']).max()
    eternal2=eternal2.rename(columns={"VHI": "VHI_max"})
    eternal=eternal.groupby(['month']).min()
    eternal=eternal.rename(columns={"VHI": "VHI_min"})
    eternal=eternal.join(eternal2)
    eternal['Region']=i
    eternal['year']=yr
    return(eternal)
  '''   
def extremum_per_year_per_region(df):
    eternal=df[['month','VHI']] 
    eternal2=eternal.groupby(['month']).max()
    eternal2=eternal2.rename(columns={"VHI": "VHI_max"})
    eternal=eternal.groupby(['month']).min()
    eternal=eternal.rename(columns={"VHI": "VHI_min"})
    eternal=eternal.join(eternal2)
    print(eternal)
    return(eternal)
                                            #peb8?
    
def extremum_all_month(df):
    i=1
    d=(df['year'].max())
    alltemp=df[(df.Region==0)&(df.year==0)][['Region']]
    while i<=26:
        k=(df['year'].min())
        while k<=d:
            temp=extremum_per_year_per_region(df,i,k)
            alltemp=alltemp.append(temp)
            k=k+1
        i=i+1 
    print(alltemp)
        
extremum_all_month(mdf)     

def all_years_extrem(df): #засухи за все года 
    print("vvedit_vidcotok_posuh_pomirnih ta id")
    percent = int(input())
    i = int(input())
    print(df[(df.Region==i)][['year','week','VHI','Region']])
    print("posuhi v taki roki:")
    k=int(df[(df.Region==i)]['year'].min())
    d=int(df[(df.Region==i)]['year'].max())
    while k<=d:
        num_weeks=df[(df.Region==i)&(df.year==k)].shape[0]
        num_weeks=num_weeks+1
        num_zasuhas=df[(df.Region==i)&(df.year==k)&(df.VHI<=15)].shape[0]
        num_zasuhas=num_zasuhas+1
        per2=100*(num_zasuhas)/(num_weeks)
        if per2>percent:
            print(k)
        k=k+1
        
        
all_years_extrem(mdf)


def all_years_pomir(df): #засухи за все года среднии
    print("vvedit_vidcotok_posuh_pomirnih ta id")
    percent = int(input())
    i = int(input())
    print(df[(df.Region==i)][['year','week','VHI','Region']])
    print("posuhi v taki roki:")
    k=int(df[(df.Region==i)]['year'].min())
    d=int(df[(df.Region==i)]['year'].max())
    while k<=d:
        num_weeks=df[(df.Region==i)&(df.year==k)].shape[0] #размеры датафрейма, 0 - рядки, 1 - колонки
        num_weeks=num_weeks+1
        num_zasuhas=df[(df.Region==i)&(df.year==k)&(df.VHI<=35)&(df.VHI>15)].shape[0]
        num_zasuhas=num_zasuhas+1
        per2=100*(num_zasuhas)/(num_weeks)
        if per2>percent:
            print(k)
        k=k+1
               
all_years_pomir(mdf)

'''replace({k: m*100, k+1: m*100, 
                                                     k+2: m*100, k+3: m*100, (k+3+(m%2)): m*100}, inplace=True)  '''