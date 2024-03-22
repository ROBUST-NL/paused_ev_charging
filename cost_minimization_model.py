# -*- coding: utf-8 -*-


import gurobipy as gp
import datetime
import pandas as pd
import numpy as np
def optimization(session_data,DA_prices,timesteps):
    """
    In this model, the charging schedules for all considered charging sessions are optimized to minimize the charging costs in the day-ahead electricity market. 
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
    DA_prices : Series
        Day-ahead electricity prices for each timestep, in €/MWh.
    timesteps : list
        List of all considered timesteps in the optimization, in CET. 

    Returns
    -------
    m.objVal: float
        Objective value of the optimization model

    """
    session_data['TR_NO']=list(range(len(session_data)))
    session_data.index=list(range(len(session_data)))
    m = gp.Model() #set up model
    model_resolution=15 #model resolution is 15 minutes
    p_ch_tr = {}
    E_ch_tr = {}
    binary={}
    for tr in range(len(session_data.index)):
        plugintime=session_data['START_rounded_CET'][tr] #arrival time of charging session tr           
        plugouttime=session_data['STOP_rounded_CET_lim'][tr] #departure time of charging session tr           
        volume=session_data['VOL'][tr] #charging volume of charging session tr
        timesteps_tr=[x for x in timesteps if x>=plugintime and x<plugouttime] #all timesteps at which the considered charging session is connected to the charging station.         
        p_ch_tr[tr] = m.addVars(timesteps_tr) #create charging power variables for all timesteps for charging session 'tr'
        E_ch_tr[tr] = m.addVars(timesteps_tr,lb=0,ub=volume) #create charging energy variables for all timesteps for charging session 'tr', with 'volume' as the upper bound'.
        binary[tr]=m.addVars(timesteps_tr,vtype=gp.GRB.BINARY) #create binary variables for all timesteps for charging session 'tr', that equals 1 if the EV is charging, and 0 if it has stopped charging. 

       
    p_ch_tot=m.addVars(timesteps) #create total charging power variables for all timesteps

    for tr in range(len(session_data.index)):
       plugintime=session_data['START_rounded_CET'][tr] #arrival time of charging session tr        
       plugouttime=session_data['STOP_rounded_CET_lim'][tr] #departure time of charging session tr 
       timesteps_tr=[x for x in timesteps if x>=plugintime and x<plugouttime] #all timesteps at which the considered charging session is connected to the charging station.                      
       p_min=session_data['P_MIN'][tr] #min charging power of charging session tr  
       p_max=session_data['P_MAX'][tr] #max charging power of charging session tr
       m.addConstr(p_ch_tr[tr][timesteps_tr[0]]>=0) #The minimum charging power is not considered at the first timestep after arrival for each EV charging session to avoid model infeasibility, which is caused by the fact that the charging demand of some charging sessions can not be exactly met when considering 15-minute timesteps and a minimum and maximum charging power
       m.addConstrs(p_ch_tr[tr][timesteps_tr[t]]>=p_min*binary[tr][timesteps_tr[t]] for t in range(1,len(timesteps_tr))) #If the EV is charging, it should charge at least with the minimum charging power.
       m.addConstrs(p_ch_tr[tr][timesteps_tr[t]]<=p_max*binary[tr][timesteps_tr[t]] for t in range(0,len(timesteps_tr)))#If the EV is charging, it should charge at maximum with the maximum charging power.
       m.addConstrs(binary[tr][timesteps_tr[t]]<=binary[tr][timesteps_tr[t-1]] for t in range(1,len(timesteps_tr))) #The binary variable assures that once the EV has stopped charging, it cannot resume charging. 

    for tr in range(len(session_data.index)): 
       plugintime=session_data['START_rounded_CET'][tr] #arrival time of charging session tr        
       plugouttime=session_data['STOP_rounded_CET_lim'][tr] #departure time of charging session tr           
       timesteps_tr=[x for x in timesteps if x>=plugintime and x<plugouttime] #all timesteps at which the considered charging session is connected to the charging station.        
       volume=session_data['VOL'][tr] #charging volume of charging session tr
       m.addConstr(E_ch_tr[tr][timesteps_tr[-1]]==volume) #the charging demand of charging session tr should be met at its departure from the charging station
       m.addConstrs(E_ch_tr[tr][timesteps_tr[t]]==E_ch_tr[tr][timesteps_tr[t-1]]+(p_ch_tr[tr][timesteps_tr[t]])*(model_resolution/60) for t in range(1,len(timesteps_tr))) #update of the total charged volume during charging session tr
       m.addConstr(E_ch_tr[tr][timesteps_tr[0]]==(p_ch_tr[tr][timesteps_tr[0]])*(model_resolution/60)) ##update of the total charged volume during charging session tr for the first timestep of the charging session 

    for t in timesteps:
        transactionlist=session_data[(t>=session_data['START_rounded_CET']) & (t<session_data['STOP_rounded_CET_lim'])] #all charging sessions connected to a charging station at timestep t
        m.addConstr(p_ch_tot[t]==gp.quicksum(p_ch_tr[tr][t] for tr in transactionlist['TR_NO'])) #the total charging power at timestep t equals the sum of the charging power of all charging sessions charging at this timestep.
    
   
    obj=gp.quicksum((p_ch_tot[t]*DA_prices[t-datetime.timedelta(minutes=t.minute)]/1000*(model_resolution/60)) for t in timesteps) #objective is to minimize charging costs in the day-ahead market

    m.setObjective(obj, gp.GRB.MINIMIZE)  #set objective of the model
    m.update()
    m.optimize() #optimize model
    return m.objVal