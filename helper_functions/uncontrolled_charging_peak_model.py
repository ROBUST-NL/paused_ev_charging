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
    """ This function calculates the peak grid load with uncontrolled charging for a given session data, non-EV load profile and timesteps.
        In uncontrolled charging, the EV is charged with the maximum power available at the charging station until the EV is fully charged.
        Ofcourse, the last non-zero power value is adjusted to the remaining energy to be charged.
        The function returns the peak grid load with uncontrolled charging.
        param session_data: A dataframe with the session data. It should contain the following columns:
                            - START_rounded_CET: The start time of the session
                            - STOP_rounded_CET_lim: The end time of the session
                            - VOL: The volume of the session
                            - P_MAX: The maximum power available at the charging station
        param timesteps: A list of datetime objects representing the timesteps
        param non_evload: A dataframe with the non-EV load. It should contain the following columns:
                            - Non-EV load: non-EV load in kW
        return: The peak grid load with uncontrolled charging
          
    """ 
    timestep_resolution=0.25 #timestep resolution in hours
    resultdf=pd.DataFrame(0,index=timesteps,columns=['EV_chargingpower']) #create a dataframe with timesteps as columns and the column 'EV_chargingpower'. The intial values of this column equals 0.
    resultdf['non_evload']=non_evload['Non-EV load'].copy() # add a new column to resultdf, portraying the values of the non-EV load.
    session_data.index=list(range(len(session_data)))
    for tr in range(len(session_data.index)): #loop over all charging sessions
       plugintime=session_data['START_rounded_CET'][tr]  #find plug-in time of charging session.     
       plugouttime=session_data['STOP_rounded_CET_lim'][tr] #find plug-out time of charging session.             
       timesteps_tr=[x for x in timesteps if x>=plugintime and x<plugouttime] #identify all timesteps between the plug-in and plug-out time.
       volume=session_data['VOL'][tr] #find charging demand of charging session
       p_max=session_data['P_MAX'][tr] #find charging power of charging session
       required_timesteps=(volume/p_max)/timestep_resolution #find the number of required timesteps to meet the charging demand.
       full_timesteps=timesteps_tr[:int(required_timesteps)] #the number of timestep at which the EV charges at maximum power when using uncontrolled charging
       for t in full_timesteps:
           resultdf.at[t,'EV_chargingpower']+=p_max #for all full timesteps, increase the total charging power by the maximum charging power of the charging session
       remainder=required_timesteps-int(required_timesteps)  # Calculate the remainder of the required timesteps after converting to an integer. This essentially captures any fractional part of the number of timesteps needed to meet the charging demand. It is used to handle the last timestep where the charging may not be at full power.
       partial_timesteps=timesteps_tr[int(required_timesteps):int(required_timesteps)+1] #identify the timestep at which partial charging occurs
       for t in partial_timesteps:
           resultdf.at[t,'EV_chargingpower']+=(p_max*remainder) #the average charging power at the partial timestep equals the remainder times the maximum charging power
    
    resultdf['Total load']=resultdf['EV_chargingpower']+resultdf['non_evload'] #determine total grid load
    return resultdf['Total load'].max()
       
    
    