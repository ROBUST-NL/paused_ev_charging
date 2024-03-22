# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 16:36:51 2024

@author: 4013425
"""

# -*- coding: utf-8 -*-
"""
Created on Fri May 12 13:47:47 2023

@author: 4013425
"""

# -*- coding: utf-8 -*-
"""
Created on Fri May 12 11:52:49 2023

@author: 4013425
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 16:37:39 2023

@author: 4013425
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

xlabellist=[]
for hour in range(0,24):
    if hour<9:
        time='0'+str(hour)+':00-'+'0'+str(hour+1)+':00'
    elif hour==9:
        time='0'+str(hour)+':00-'+str(hour+1)+':00'
    elif hour==23:
        time=str(hour)+':00-00:00'
    else:
        time=str(hour)+':00-'+str(hour+1)+':00'
    xlabellist+=[time]

resultdf=pd.read_excel('Source Data.xlsx',sheet_name='Figure 6')

fig=plt.figure(figsize=(13,5.5*13/15),dpi=600)
ax1=plt.subplot(111)
plt.subplots_adjust(wspace=0.13, hspace=0.4)
for i in range(1,5):
    plt.plot([-100,100],[i,i],color='lightgrey',linestyle='--',zorder=-100000)
sns.violinplot(data=resultdf, x="timeframe", y="re-dispatchvalue", hue="Type of smart charging",saturation=1,hue_order=['Smart charging without charging pauses','Smart charging with charging pauses'], split=True,bw=0.18,scale='width',palette={"Smart charging without charging pauses": "#F28522","Smart charging with charging pauses": "#00a087"},inner="quart", linewidth=1,zorder=50000)
plt.xticks(rotation=90,fontsize=11.5)
plt.yticks(fontsize=11.5)
plt.ylim(0,4.8)
plt.ylabel('Hourly downward flexibility\n[kW/charging station]',font='DejaVu Sans',fontsize=13)
plt.xlim(-0.8,23.8)
plt.legend(bbox_to_anchor=(0.02,0.997),fontsize=12,loc=2,frameon=False)
plt.xlabel('Flexibility request window',font='DejaVu Sans',fontsize=13)
ax1.set_xticklabels(xlabellist,rotation = 50,ha='right')
