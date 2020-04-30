# -*- coding: utf-8 -*-
import urllib3
import requests
import cherrypy
import jinja2
import matplotlib
import pandas as pd
import os

def download_all():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    i = 1
    while i <= 27: #загрузка файлов
        url1 = 'https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_TS_admin.php?country=UKR&provinceID='
        url2 = str(i)
        url3 = '&year1=1981&year2=1990&type=Mean'
        url = url1+url2+url3
        req = requests.get(url)
        vhi_con = req.content
        file1 = 'vhi_id_'
        file2 = '.csv'
        filename=file1+url2+file2
        filev = open(filename,'wb') #пропустить 1 строчку
        filev.write(vhi_con)
        filev.close()
        data = pd.read_csv(filename,skiprows=1)
        data.drop(data.tail(1).index,inplace=True) #треба буде далі мучати
        data.to_csv(filename)
        i = i+1
        
def createdf(filename,k): #создача фрейма   #загрузить все в 1 датафрейм, добавить колонку региона
    columns=['row','year','week', 'NDVI', 'PBT', 'VCI', 'TCI', 'VHI']
    data = pd.read_csv(filename,index_col=False, sep=',',header=None,names=columns) 
    df = pd.DataFrame(data)
    df = df[(df.VHI>=0)]
    df['Region']=k
    return(df)

def massive_df():
    i=1
    masdf=pd.DataFrame()
    path=os.getcwd()
    with os.scandir(path) as listOfVHI:
        for entry in listOfVHI:
            if entry.is_file() and entry.name.startswith('vhi_id'):
                df=createdf(entry.name,i)
                masdf=masdf.append(df)
                i=i+1
    masdf['month']=(masdf['week']/4.34).astype('int32')+1
    masdf=masdf.sort_values(by='Region')
    return(masdf) 
    
    
def extremum_per_year_per_region(df, vari):
    eternal=df[['month', vari]] 
    eternal2=eternal.groupby(['month'],as_index=False).max()
    eternal2=eternal2.rename(columns={vari: vari+" Max"})
    eternal=eternal.groupby(['month'],as_index=False).min()
    eternal=eternal.rename(columns={'month': 'ded'})
    eternal=eternal.rename(columns={vari: vari+" Min"})
    eternal2=eternal2.join(eternal)
    eternal2=eternal2.drop(['ded'], axis=1)
    return(eternal2)
