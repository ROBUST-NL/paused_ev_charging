# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 10:23:34 2024

@author: 4013425
"""

import pandas as pd
from helper_functions.cost_minimization_model import cost_optimization
import datetime as dt
import pytz
import numpy as np
from helper_functions.uncontrolled_charging_peak_model import uncontrolled_peak

sample_ev_data = pd.read_csv('ev_sample_data.csv',index_col=0,parse_dates=['START_rounded_CET','STOP_rounded_CET_lim'])
DA_prices_NL=pd.read_pickle('C:/Users/4013425/Documents/GitHub/paused_ev_charging/DA_prices_NL.pkl')
timesteps=pd.date_range(dt.datetime(2022,1,1,tzinfo=pytz.timezone('CET')),dt.datetime(2022,12,31,23,45,tzinfo=pytz.timezone('CET')),freq='15Min')
from helper_functions.uncontrolled_charging_model import uncontrolled_profile
from helper_functions.flexibility_offering_model_nico import flexibility_provision_optimization

baseline_profile=uncontrolled_profile(sample_ev_data,timesteps)

from helper_functions.uncontrolled_charging_model import uncontrolled_profile
from helper_functions.flexibility_offering_model_nico import flexibility_provision_optimization

baseline_profile=uncontrolled_profile(sample_ev_data,timesteps) #baseline profile is the uncontrolled charging profile

#we consider one example hour
timesteps_flex=pd.date_range(dt.datetime(2022,8,31,22,tzinfo=pytz.timezone('CET')),dt.datetime(2022,8,31,22,45,tzinfo=pytz.timezone('CET')),freq='15Min')

#Running the model for smart charging with charging pauses
sample_ev_data['P_MIN']=[0]*len(sample_ev_data) #minimum charging current in this case is 0 kW
flex_0A=flexibility_provision_optimization(sample_ev_data,timesteps,timesteps_flex,baseline_profile)
print('Downward flexibility potential for considered hour for smart charging with charging pauses equals: '+str(round(flex_0A,2))+' kW')

#Running the model for smart charging without charging pauses
sample_ev_data['P_MIN']=sample_ev_data['PHASE']*6*230/1000
sample_ev_data['P_MIN']=np.where(sample_ev_data['P_MIN']>sample_ev_data['P_MAX'],sample_ev_data['P_MAX'],sample_ev_data['P_MIN'])
flex_6A=flexibility_provision_optimization(sample_ev_data,timesteps,timesteps_flex,baseline_profile)
print('Downward flexibility potential for considered hour for smart charging without charging pauses equals: '+str(round(flex_6A,2))+' kW')