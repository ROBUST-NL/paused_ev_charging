# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 11:26:58 2024

@author: 4013425
"""

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
def uncontrolled_profile(session_data,timesteps):
    """ This function creates a uncontrolled charging profile for a given session data and timesteps.
        In uncontrolled charging, the EV is charged with the maximum power available at the charging station until the EV is fully charged.
        Ofcourse, the last non-zero power value is adjusted to the remaining energy to be charged.
        The function returns a dataframe with the charging power values for each timestep.
        param session_data: A dataframe with the session data. It should contain the following columns:
                            - START_rounded_CET: The start time of the session
                            - STOP_rounded_CET_lim: The end time of the session
                            - VOL: The volume of the session
                            - P_MAX: The maximum power available at the charging station
        param timesteps: A list of datetime objects representing the timesteps
        return: A dataframe with the charging power values for each timestep
    """
    resultdf=pd.DataFrame(index=timesteps)
    resultdf['EV_chargingpower']=[0]*len(resultdf)
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
    
    return resultdf
       
    
    