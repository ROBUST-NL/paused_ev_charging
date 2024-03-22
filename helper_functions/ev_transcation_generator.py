
import numpy as np
import datetime as dt
import tqdm.notebook as tq
import pandas as pd

def generate_dummy_transactions(number_of_days = 100,
                                start_date = dt.datetime(year=2022, month=1, day=1)
                                ):
    """ This function generates dummy transactions for a given number of days, from a given start date
    param number_of_days: number of days for which the transactions are to be generated
    param start_date: start date of the transactions
    return: pandas dataframe containing the transactions
            The columns are 'START', 'STOP', 'P_MAX', 'VOL'
    """
    def return_random_transaction(mean_dur = 13.7,
                                    std_dur = 14.8,
                                    mean_start = 13.75,
                                    std_start = 4.58,
                                    year_ = 2022,
                                    p_min =4,
                                    p_max = 22,
                                    vol_min = 1,
                                    vol_max = 60,
                                    month_ = 1,
                                    day_ = 1):
        """ This function returns a random transaction based on the input parameters
        param mean_dur: mean duration of the transaction
        param std_dur: standard deviation of the duration of the transaction
        param mean_start: mean start time of the transaction
        param std_start: standard deviation of the start time of the transaction
        param year_: year of the transaction
        param p_min: minimum power
        param p_max: maximum power
        param vol_min: minimum volume
        param vol_max: maximum volume
        param month_: month of the transaction
        param day_: day of the transaction
        return: dictionary containing the start time, stop time, maximum power and volume of the transaction
                The keys are 'START', 'STOP', 'P_MAX', 'VOL'
        """

        # Based on the month fix a max value of days
       
        
        start_time = dt.datetime(year=year_, month=month_, day=day_, hour=int(abs(min(np.random.normal(loc=mean_start,scale=std_start),23))),minute=np.random.randint(0,60),second=np.random.randint(0,60))
        # Sample onlypositive values
        dur_ = np.round(np.random.normal(loc=mean_dur, scale=std_dur))
        end_time = start_time + dt.timedelta(hours=int(max(2,dur_)))
        p_max = np.random.uniform(low=p_min, high=p_max)
        vol = min(p_max*dur_, np.random.uniform(low=vol_min, high=vol_max))
        return {'START':start_time, 'STOP':end_time, 'P_MAX':p_max, 'VOL':vol}




    transactions_per_date = np.random.randint(0,1000, number_of_days)
    date_day_list= [start_date + dt.timedelta(days=i) for i in range(number_of_days)]
    transactions = []
    c = 0
    for i in tq.tqdm(date_day_list, desc='Generating transactions'):
        for j in range(transactions_per_date[c]):
            transactions.append(return_random_transaction(year_=i.year, month_=i.month, day_=i.day))
        c = c+1
    df_ = pd.DataFrame(transactions)
    df_['START']= df_['START'].dt.tz_localize('UTC')
    df_['STOP']= df_['STOP'].dt.tz_localize('UTC')

    return df_