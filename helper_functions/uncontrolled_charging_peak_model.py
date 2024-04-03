# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 17:10:58 2024

@author: 4013425
"""


import pandas as pd
import datetime
import pytz
import warnings
warnings.filterwarnings("ignore")
def uncontrolled_peak(session_data,timesteps,non_evload):
    resultdf=pd.DataFrame(index=timesteps)
    resultdf['EV_chargingpower']=[0]*len(resultdf)
    resultdf['non_evload']=non_evload['Non-EV load'].copy()
    session_data.index=list(range(len(session_data)))
    for tr in range(len(session_data.index)):
       plugintime=session_data['START_rounded_CET'][tr]       
       plugouttime=session_data['STOP_rounded_CET_lim'][tr]          
       timesteps_tr=[x for x in timesteps if x>=plugintime and x<plugouttime]
       volume=session_data['VOL'][tr]
       p_max=session_data['P_MAX'][tr]
       required_timesteps=volume/p_max*4
       full_timesteps=timesteps_tr[:int(required_timesteps)]
       for t in full_timesteps:
           resultdf.at[t,'EV_chargingpower']+=p_max
       remainder=required_timesteps-int(required_timesteps)
       partial_timesteps=timesteps_tr[int(required_timesteps):int(required_timesteps)+1]
       for t in partial_timesteps:
           resultdf.at[t,'EV_chargingpower']+=(p_max*remainder)
    
    resultdf['Total load']=resultdf['EV_chargingpower']+resultdf['non_evload']
    return resultdf['Total load'].max()
       
    
    