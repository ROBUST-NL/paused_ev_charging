# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 16:31:51 2024

@author: 4013425
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21 11:42:37 2022

@author: 4013425
"""

import matplotlib.pyplot as plt
import pandas as pd
import itertools

resultdf=pd.read_excel('Source Data.xlsx',sheet_name='Figure 5',index_col=0)


def flip(items, ncol):
    return itertools.chain(*[items[i::ncol] for i in range(ncol)])

labellist=['Uncontrolled charging','Peak load minimization\nwithout charging pauses','Peak load minimization\nwith charging pauses']
colorlist=['#3c5488','#F28522','#00a087']

fig=plt.figure(figsize=(6,3.2),dpi=500)
ax1=plt.subplot(111)
plt.plot([-100,300],[400,400],color='darkred',linestyle='--',label='Transformer capacity')
for j,col in enumerate(['Uncontrolled charging','No paused charging','Paused charging']):
    ax1.stackplot(resultdf.index, resultdf[col+' - lower bound 95% quantile'], resultdf[col+' - upper bound 95% quantile']-resultdf[col+' - lower bound 95% quantile'], colors=["#ffffff00",colorlist[j]],alpha=0.2,zorder=1000)
    plt.plot(resultdf.index,resultdf[col+' - average value'],label=labellist[j],color=colorlist[j],zorder=1000)
plt.xlabel('Number of charging stations')
plt.ylabel('Transformer peak load [kW]')
plt.ylim(0,598)
plt.xlim(0,130)
plt.grid(axis='both',color='lightgrey',linestyle='--',zorder=-1000)
handles, labels = ax1.get_legend_handles_labels()
plt.legend(flip(handles,2),flip(labels,2),bbox_to_anchor=(0.46, -0.32),loc='center',ncol=2,fontsize=9.5,frameon=False)