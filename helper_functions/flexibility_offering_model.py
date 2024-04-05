# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 11:04:48 2024

@author: 4013425
"""

# -*- coding: utf-8 -*-

import numpy as np
import gurobipy as gp
import datetime
import pandas as pd

def flexibility_provision_optimization(session_data,timesteps,timesteps_flex,baseline_profile):
    """
    In this model, the charging schedules for all considered charging sessions are optimized to minimize the total peak grid load. 

    Parameters
    ----------
    session_data : pd.DataFrame
        Pandas dataframe containing information about the considered charging sessions. It should contain the following columns:
            'START_ROUNDED_CET': the arrival time of the EV to the charging station in CET, rounded to the nearest 15-minute timestamp.
            'STOP_ROUNDED_CET_lim': the departure time of the EV from the charging station in CET, rounded to the nearest 15-minute timestamp. 
            If the connection time to the charging station exceeds 24 hours, the departure time is set to 24 hours after the arrival time
            'VOL': the charging volume of the charging session in kWh. 
            'P_MAX': Maximum charging power of the charging session in kW.
            'P_MIN': Minimum charging power of the charging session in kW. Equal to 0 if delayed and paused charging is possible. 
    timesteps : list
        List of all considered timesteps in the optimization, in CET. 
    timesteps_flex : list
        List of all considered timesteps for the considered flexibility timeframe, in CET. 
    baseline_profile : pd.DataFrame90
        Pandas dataframe containing the baseline charging profile in kW. It should contain the following column:
            'EV_chargingpower' : charging power in kW

    Returns
    -------
    m.objVal: float
        Objective value of the optimization model

    """
    
    session_data['TR_NO']=list(range(len(session_data)))
    session_data.index=session_data['TR_NO'].copy()
    m = gp.Model() #set up model
    m.Params.LogToConsole = 0

    model_resolution=15 #model resolution is 15 minutes
    p_ch_tr = {}
    E_ch_tr = {}
    binary={}    
    for tr in range(len(session_data.index)):
        plugintime=session_data['START_rounded_CET'][tr] #arrival time of charging session tr        
        plugouttime=session_data['STOP_rounded_CET_lim'][tr] #departure time of charging session tr
        timesteps_tr=[x for x in timesteps if x>=plugintime and x<plugouttime] #all timesteps at which the considered charging session is connected to the charging station.
        volume=session_data['VOL'][tr] #charging volume of charging session tr
        p_ch_tr[tr] = m.addVars(timesteps_tr) #create charging power variables for all timesteps for charging session 'tr'
        E_ch_tr[tr] = m.addVars(timesteps_tr,lb=0,ub=volume) #create charging energy variables for all timesteps for charging session 'tr', with 'volume' as the upper bound'.
        binary[tr]=m.addVars(timesteps_tr,vtype=gp.GRB.BINARY) #create binary variables for all timesteps for charging session 'tr', that equals 1 if the EV is charging, and 0 if it has stopped charging. 
    binary[tr]=m.addVars(timesteps_tr,vtype=gp.GRB.BINARY) #create binary variables for all timesteps for charging session 'tr', that equals 1 if the EV is charging, and 0 if it has stopped charging. 
    p_ev_tot=m.addVars(timesteps_flex) #create a variable for the total EV charging demand
    p_flex=m.addVar() #create a variable for the total flexibility that can be provided during the flexibility time window   
    for tr in range(len(session_data.index)):
       plugintime=session_data['START_rounded_CET'][tr] #arrival time of charging session tr       
       plugouttime=session_data['STOP_rounded_CET_lim'][tr] #departure time of charging session tr
       p_min=session_data['P_MIN'][tr] #min charging power of charging session tr
       p_max=session_data['P_MAX'][tr] #max charging power of charging session tr
       timesteps_tr=[x for x in timesteps if x>=plugintime and x<plugouttime] #all timesteps at which the considered charging session is connected to the charging station.
       m.addConstr(p_ch_tr[tr][timesteps_tr[0]]>=0) #The minimum charging power is not considered at the first timestep after arrival for each EV charging session to avoid model infeasibility, which is caused by the fact that the charging demand of some charging sessions can not be exactly met when considering 15-minute timesteps and a minimum and maximum charging power
       m.addConstrs(p_ch_tr[tr][timesteps_tr[t]]>=p_min*binary[tr][timesteps_tr[t]] for t in range(1,len(timesteps_tr)))#If the EV is charging, it should charge at least with the minimum charging power.
       m.addConstrs(p_ch_tr[tr][timesteps_tr[t]]<=p_max*binary[tr][timesteps_tr[t]] for t in range(0,len(timesteps_tr))) #If the EV is charging, it should charge at maximum with the maximum charging power.
       m.addConstrs(binary[tr][timesteps_tr[t]]<=binary[tr][timesteps_tr[t-1]] for t in range(1,len(timesteps_tr))) #The binary variable assures that once the EV has stopped charging, it cannot resume charging. 
       
    for tr in range(len(session_data.index)):
       plugintime=session_data['START_rounded_CET'][tr] #arrival time of charging session tr       
       plugouttime=session_data['STOP_rounded_CET_lim'][tr] #departure time of charging session tr
       timesteps_tr=[x for x in timesteps if x>=plugintime and x<plugouttime] #all timesteps at which the considered charging session is connected to the charging station.
       volume=session_data['VOL'][tr] #charging volume of charging session tr
       m.addConstr(E_ch_tr[tr][timesteps_tr[-1]]==volume) #the charging demand of charging session tr should be met at its departure from the charging station
       m.addConstr(E_ch_tr[tr][timesteps_tr[0]]==(p_ch_tr[tr][timesteps_tr[0]])*(model_resolution/60)) #update of the total charged volume during charging session tr
       m.addConstrs(E_ch_tr[tr][timesteps_tr[t]]==E_ch_tr[tr][timesteps_tr[t-1]]+(p_ch_tr[tr][timesteps_tr[t]])*(model_resolution/60) for t in range(1,len(timesteps_tr))) ##update of the total charged volume during charging session tr for the first timestep of the charging session 

    for t in timesteps_flex:
        transactionlist=session_data[(t>=session_data['START_rounded_CET']) & (t<session_data['STOP_rounded_CET_lim'])] #all charging sessions connected to a charging station at timestep t
        p_baseline=baseline_profile.loc[t,'EV_chargingpower'] #the baseline charging power at the considered timestep
        m.addConstr(p_ev_tot[t]==gp.quicksum(p_ch_tr[tr][t] for tr in transactionlist['TR_NO']))  #the total EV load at timestep t is equal to the sum of the charging power of all charging sessions at this timestep      
        m.addConstr(p_flex==p_baseline-p_ev_tot[t])  #the total flexibility is equal to the difference between the baseline charging power and the optimized total EV charging power.
        
    
    obj=p_flex #the objective is to maximize the provided flexibility

    m.setObjective(obj, gp.GRB.MAXIMIZE) #set objective of the model
    m.update()
    m.optimize()     #optimize model
    return m.objVal