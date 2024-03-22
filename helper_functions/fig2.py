# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 14:45:30 2024

@author: 4013425
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 12:10:47 2023

@author: 4013425
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Feb 14 17:29:03 2023

@author: 4013425
"""


# -*- coding: utf-8 -*-
"""
Created on Tue Feb 14 17:29:03 2023

@author: 4013425
"""

import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.ticker as mtick
from matplotlib.lines import Line2D

results=pd.read_excel('Source Data.xlsx',sheet_name='Figure 2',index_col=0)

fig=plt.figure(figsize=(5,2.5),dpi=500)
fmt = '%.0f%%' 
ax1=plt.subplot(111)
font='DejaVu Sans'
xpos=[1,4+1,7+1.9,10+1.6,13+2.4,16+2.1]
plt.bar(xpos,results['Value']*100,color='#3c5488',width=2,zorder=5)
xticklist=['Fluctuating\ncharging',
           'Intermittent\ncharging',
           '',
           '',
           '',
           '']
plt.xticks(ticks=xpos,labels=xticklist,fontsize=8.2)
plt.ylim(0,100)
plt.grid(axis='y',color='lightgrey',linestyle='--',zorder=0)
ax1.yaxis.set_major_formatter(mtick.FormatStrFormatter(fmt))
ax1.tick_params(width=0.001)
plt.ylabel('Success rate of charging tests',font=font,fontsize=8.5)
plt.yticks(font=font,fontsize=8.5)
plt.text(8.9,-5.5,'20 min',fontsize=7.2,font=font,va='center',ha='center')
plt.text(11.6,-5.5,'6 hour',fontsize=7.2,font=font,va='center',ha='center')
plt.text(15.4,-5.5,'20 min',fontsize=7.2,font=font,va='center',ha='center')
plt.text(18.1,-5.5,'6 hour',fontsize=7.2,font=font,va='center',ha='center')
plt.text(10.25,-13.2,'Delayed charging',fontsize=8.2,font=font,va='center',ha='center')
plt.text(16.75,-13.2,'Paused charging',fontsize=8.2,font=font,va='center',ha='center')
