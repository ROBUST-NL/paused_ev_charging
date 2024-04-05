
import pandas as pd
import datetime
import pytz
import warnings
warnings.filterwarnings("ignore")
def uncontrolled_costs(session_data,DA_prices,timesteps):
    """ This function calculates the costs of uncontrolled charging for a given session data and timesteps.
        In uncontrolled charging, the EV is charged with the maximum power available at the charging station until the EV is fully charged.
        Ofcourse, the last non-zero power value is adjusted to the remaining energy to be charged.
        The function returns the total costs of uncontrolled charging.
        param session_data: A dataframe with the session data. It should contain the following columns:
                            - START_rounded_CET: The start time of the session
                            - STOP_rounded_CET_lim: The end time of the session
                            - VOL: The volume of the session
                            - P_MAX: The maximum power available at the charging station
        param DA_prices: A dataframe with the day-ahead prices. It should contain the following columns:
                            - Day-ahead price [EUR/MWh]: The day-ahead prices for each timestep 
        param timesteps: A list of datetime objects representing the timesteps
        return: The total costs of uncontrolled charging
          
    """
    timestep_resolution=0.25 #timestep resolution in hours
    resultdf=pd.DataFrame(0,index=timesteps,columns=['EV_chargingpower']) #create a dataframe with timesteps as columns and the column 'EV_chargingpower'. The intial values of this column equals 0.
    resultdf['DA_price']=DA_prices['Day-ahead price [EUR/MWh]']/1000 #add column with DA-prieces, and convert to EUR/kWh
    resultdf['DA_price']=resultdf['DA_price'].ffill() #Since DA-prices are hourly values, and we consider a 15-min resolution, forward fill is used to set DA-price values for the other timesteps of an hour
    session_data.index=list(range(len(session_data)))
    for tr in range(len(session_data.index)): #loop over all charging sessions
       plugintime=session_data['START_rounded_CET'][tr] #find plug-in time of charging session.          
       plugouttime=session_data['STOP_rounded_CET_lim'][tr] #find plug-out time of charging session.           
       timesteps_tr=[x for x in timesteps if x>=plugintime and x<plugouttime] #identify all timesteps between the plug-in and plug-out time.
       volume=session_data['VOL'][tr] #find charging demand of charging session
       p_max=session_data['P_MAX'][tr] #find charging power of charging session
       required_timesteps=(volume/p_max)/timestep_resolution #find the number of required timesteps to meet the charging demand.
       full_timesteps=timesteps_tr[:int(required_timesteps)] #the number of timestep at which the EV charges at maximum power when using uncontrolled charging
       for t in full_timesteps:
           resultdf.at[t,'EV_chargingpower']+=p_max #for all full timesteps, increase the total charging power by the maximum charging power of the charging session
       remainder=required_timesteps-int(required_timesteps) # Calculate the remainder of the required timesteps after converting to an integer. This essentially captures any fractional part of the number of timesteps needed to meet the charging demand. It is used to handle the last timestep where the charging may not be at full power.
       partial_timesteps=timesteps_tr[int(required_timesteps):int(required_timesteps)+1] #identify the timestep at which partial charging occurs
       for t in partial_timesteps:
           resultdf.at[t,'EV_chargingpower']+=(p_max*remainder) #the average charging power at the partial timestep equals the remainder times the maximum charging power
    resultdf['Costs']=resultdf['EV_chargingpower']*resultdf['DA_price']*timestep_resolution #determine total charging costs at each timestep
    return resultdf['Costs'].sum()
       
    
    