# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 14:53:03 2024

@author: 4013425
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 10:30:38 2023

@author: 4013425
"""

import matplotlib.pyplot as plt
import pandas as pd
resultdf=pd.read_excel('Source Data.xlsx',sheet_name='Figure 4',index_col=0)
resultdf['cost reduction paused charging']=(resultdf['Costs - paused charging (euro/kWh)']/resultdf['Costs - uncontrolled charging']-1)
resultdf['cost reduction no paused charging']=(resultdf['Costs - no paused charging (euro/kWh)']/resultdf['Costs - uncontrolled charging']-1)


fig=plt.figure(figsize=(8.3,4.8),dpi=500)
barwidth=0.18
plt.subplots_adjust(wspace=0.13, hspace=0.2)

ax1=plt.subplot(2,1,1)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ticks_nochargingpause=[x for x in range(1,14)]
ticks_chargingpause=[x+barwidth for x in range(1,14)]
ticks_uncontrolled=[x-barwidth for x in range(1,14)]
plt.bar(ticks_uncontrolled,resultdf['Costs - uncontrolled charging'][:13],width=barwidth,color='#3c5488',zorder=100)
plt.bar(ticks_nochargingpause,resultdf['Costs - no paused charging (euro/kWh)'][:13],width=barwidth,color='#F28522',zorder=100)
plt.bar(ticks_chargingpause,resultdf['Costs - paused charging (euro/kWh)'][:13],width=barwidth,color='#00a087',zorder=100)
plt.xticks(ticks=ticks_nochargingpause,labels=resultdf.index[:13])
plt.xlim(0.4,13.5)
plt.ylim(0,0.32)
plt.ylabel('Charging costs [€/kWh]')
plt.grid(axis='y',color='lightgrey',linestyle='--',zorder=-1000)

for j,country in enumerate(resultdf.index[:13]):
    plt.arrow(ticks_uncontrolled[j]-0.135,resultdf.loc[country,'Costs - uncontrolled charging']-0.0015,0,-(resultdf.loc[country,'Costs - uncontrolled charging']-resultdf.loc[country,'Costs - no paused charging (euro/kWh)'])+0.005,
              head_width=0.07,head_length=0.005,length_includes_head=True,overhang=0.8,color='#505050',zorder=100)
    plt.text(ticks_uncontrolled[j]-0.255,(resultdf.loc[country,'Costs - no paused charging (euro/kWh)'])+0.002,'–'+str(-int(round(resultdf.loc[country,'cost reduction no paused charging']*100,0)))+'%',fontsize=6.3,rotation=90,va='bottom',ha='center',color='#505050',zorder=100)   

    plt.arrow(ticks_nochargingpause[j]+0.135,resultdf.loc[country,'Costs - uncontrolled charging']-0.0015,0,-(resultdf.loc[country,'Costs - uncontrolled charging']-resultdf.loc[country,'Costs - paused charging (euro/kWh)'])+0.005,
              head_width=0.07,head_length=0.005,length_includes_head=True,overhang=0.8,color='#505050',zorder=100)
    if country in ['ES','CH']:
        plt.text(ticks_nochargingpause[j]+0.275,(resultdf.loc[country,'Costs - paused charging (euro/kWh)'])+0.002,'–'+str(-int(round(resultdf.loc[country,'cost reduction paused charging']*100,0)))+'%',fontsize=6.3,rotation=90,va='bottom',ha='center',color='#505050',zorder=100)   
    else:
        plt.text(ticks_nochargingpause[j]+0.275,(resultdf.loc[country,'Costs - paused charging (euro/kWh)']+resultdf.loc[country,'Costs - uncontrolled charging'])/2,'–'+str(-int(round(resultdf.loc[country,'cost reduction paused charging']*100,0)))+'%',fontsize=6.3,rotation=90,va='center',ha='center',color='#505050',zorder=100)   

ax1=plt.subplot(2,1,2)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
plt.grid(axis='y',color='lightgrey',linestyle='--',zorder=-1000)
plt.bar(ticks_uncontrolled,resultdf['Costs - uncontrolled charging'][13:],width=barwidth,color='#3c5488',label='Uncontrolled charging',zorder=100)
plt.bar(ticks_nochargingpause,resultdf['Costs - no paused charging (euro/kWh)'][13:],width=barwidth,color='#F28522',label='Cost optimization\nwithout charging pauses',zorder=100)
plt.bar(ticks_chargingpause,resultdf['Costs - paused charging (euro/kWh)'][13:],width=barwidth,color='#00a087',label='Cost optimization\nwith charging pauses',zorder=100)
plt.xticks(ticks=ticks_nochargingpause,labels=resultdf.index[13:])
plt.xlim(0.4,13.5)
plt.ylim(0,0.32)
plt.ylabel('Charging costs [€/kWh]')
for j,country in enumerate(resultdf.index[13:]):
    plt.arrow(ticks_uncontrolled[j]-0.135,resultdf.loc[country,'Costs - uncontrolled charging']-0.0015,0,-(resultdf.loc[country,'Costs - uncontrolled charging']-resultdf.loc[country,'Costs - no paused charging (euro/kWh)'])+0.005,
              head_width=0.07,head_length=0.005,length_includes_head=True,overhang=0.8,color='#505050',zorder=100)
    plt.text(ticks_uncontrolled[j]-0.255,(resultdf.loc[country,'Costs - no paused charging (euro/kWh)'])+0.002,'–'+str(-int(round(resultdf.loc[country,'cost reduction no paused charging']*100,0)))+'%',fontsize=6.3,rotation=90,va='bottom',ha='center',color='#505050',zorder=100)   

    plt.arrow(ticks_nochargingpause[j]+0.135,resultdf.loc[country,'Costs - uncontrolled charging']-0.0015,0,-(resultdf.loc[country,'Costs - uncontrolled charging']-resultdf.loc[country,'Costs - paused charging (euro/kWh)'])+0.005,
              head_width=0.07,head_length=0.005,length_includes_head=True,overhang=0.8,color='#505050',zorder=100)
    if country in ['NO','PT','SE','IT','PL']:
        plt.text(ticks_nochargingpause[j]+0.275,(resultdf.loc[country,'Costs - paused charging (euro/kWh)'])+0.002,'–'+str(-int(round(resultdf.loc[country,'cost reduction paused charging']*100,0)))+'%',fontsize=6.3,rotation=90,va='bottom',ha='center',color='#505050',zorder=100)   
    else:
        plt.text(ticks_nochargingpause[j]+0.275,(resultdf.loc[country,'Costs - paused charging (euro/kWh)']+resultdf.loc[country,'Costs - uncontrolled charging'])/2,'–'+str(-int(round(resultdf.loc[country,'cost reduction paused charging']*100,0)))+'%',fontsize=6.3,rotation=90,va='center',ha='center',color='#505050',zorder=100)   
plt.legend(loc=(0,-0.45),ncol=3,frameon=False)    