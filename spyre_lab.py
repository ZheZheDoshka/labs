# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 22:22:03 2020

@author: User
"""
from spyre import server
import pandas as pd
import vhi_downloader as vd
    
class App2(server.App):
    title = "VHI doings"
    
    inputs = [{        "type":'dropdown',
                    "label": 'Parameter',
                    "options" : [ {"label": "VHI", "value":"VHI"},
                                  {"label": "VCI", "value":"VCI"},
                                  {"label": "TCI", "value":"TCI"}],
                    "key": 'variable',
                    "action_id": "update_data"},
    {        "type":'dropdown',
                    "label": 'Region',
                    "options" : [ {"label": "Cherkasy", "value":"1"},
                                  {"label": "Chernihiv", "value":"2"},
                                  {"label": "Chernivtsi", "value":"3"},
                                  {"label": "Crimea", "value":"4"},
                                  {"label": "Dnipropetrovs'k", "value":"5"},
                                  {"label": "Donets'k", "value":"6"},
                                  {"label": "Ivano-Frankivs'k", "value":"7"},
                                  {"label": "Kharkiv", "value":"8"},
                                  {"label": "Kherson", "value":"9"},
                                  {"label": "Khmel'nyts'kyy", "value":"10"},
                                  {"label": "Kiev", "value":"11"},
                                  {"label": "Kiev City", "value":"12"},
                                  {"label": "Kirovohrad", "value":"13"},
                                  {"label": "Luhans'k", "value":"14"},
                                  {"label": "L'viv", "value":"15"},
                                  {"label": "Mykolayiv", "value":"16"},
                                  {"label": "Odessa", "value":"17"},
                                  {"label": "Poltava", "value":"18"},
                                  {"label": "Rivne", "value":"19"},
                                  {"label": "Sevastopol", "value":"20"},
                                  {"label": "Sumy", "value":"21"},
                                  {"label": "Ternopil", "value":"22"},
                                  {"label": "Transcarpathia", "value":"23"},
                                  {"label": "Vinnytsya", "value":"24"},
                                  {"label": "Volyn", "value":"25"},
                                  {"label": "Zaporizhzhya", "value":"26"},
                                  {"label": "Zhytomir", "value":"27"},],
                    "key": 'region',
                    "action_id": "update_data"}, 
     {      "type":'text',
                   "label": 'week1',
                   "value" : '0',
                   "key": 'w1',
                   "action_id": "update_data"},
     {      "type":'text',
                   "label": 'week2',
                   "value" : '20',
                   "key": 'w2',
                   "action_id": "update_data"},
     {      "type":'text',
                   "label": 'year1',
                   "value" : '1985',
                   "key": 'y1',
                   "action_id": "update_data"},
     {      "type":'text',
                   "label": 'year2',
                   "value" : '1986',
                   "key": 'y2',
                   "action_id": "update_data"}]
    

    controls = [{    "type" : "hidden",
                    "id" : "update_data"}]
    
    tabs = ["VHIFrame","MinMax","Plot"]
    
    outputs = [{ "type" : "table",
                    "id" : "vframe",
                    "control_id" : "update_data",
                    "tab" : "VHIFrame",
                    "on_page_load": True},
                { "type" : "table",
                    "id" : "space",       #спейс потому-что пробел забыл и думал чего оно там не матчит
                    "control_id" : "update_data",
                    "tab" : "MinMax",
                    "on_page_load": True},
                { "type" : "plot",          #график 2 вкладки на фильтр и график, переиспользовать vhi max, vhi min по месяцам+график
                "id" : "plot",
                "control_id" : "update_data",
                "tab" : "Plot"},] 
    
    def vframe(self, params):
        region = int(params['region'])           #переиспользовать гетдата и переместить загрузку в модуль       #створити гілку, перейти в неї, додати в індексацію, пулл реквест
        wmin = int(params['w1'])
        wmax = int(params['w2'])
        ymin = int(params['y1'])
        ymax = int(params['y2'])
        df=masdf
        df=df[(df.week>=wmin)&(df.week<=wmax)&(df.Region==region)&(df.year>=ymin)&(df.year<=ymax)]
        return df
    
    def space(self, params):
        df2=self.vframe(params)
        vari=params['variable']
        df2=vd.extremum_per_year_per_region(df2, vari)
        return df2
    
    def getPlot(self, params):
        dfp = self.space(params).drop(['month'], axis=1)
        vari=params['variable']
        vhi_plot = dfp.plot()
        vhi_plot.set_ylabel(vari)
        vhi_plot.set_xlabel("month")
        vhi_plot.set_title(vari+" min and max per month")
        drawn = vhi_plot.get_figure()
        return drawn
#vd.download_all()
masdf=vd.massive_df()
app = App2()
app.launch(port=8083)