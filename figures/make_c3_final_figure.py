#!/usr/bin/env python3
"""fig_c3_final_bands.png — World Cup final 2026-07-19: the four content-reactive
TVs (REM cloud path, 10 s / 1 W) with Ben's logged event bands (French feed).
Run on GoS1: /srv/data/owl/figures-venv/bin/python figures/make_c3_final_figure.py
Inputs: /srv/data/owl/worldcup-2026-07/grid_2026-07-19.csv (raw stays on GoS1),
runs/worldcup-final-2026-07-19/events.csv. Output: figures/fig_c3_final_bands.png
"""
import pandas as pd, numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
G='/srv/data/owl/worldcup-2026-07/grid_2026-07-19.csv'; EV='runs/worldcup-final-2026-07-19/events.csv'
T0=pd.Timestamp('2026-07-19 18:46:40',tz='UTC'); KO=pd.Timestamp('2026-07-19 19:08:20',tz='UTC')
p=pd.read_csv(G,index_col=0); p.index=T0+pd.to_timedelta(p.index*10,unit='s'); m=(p.index-KO).total_seconds()/60
ev=pd.read_csv(EV); ev['t']=ev.utc.apply(lambda s: pd.Timestamp(('2026-07-20 ' if s.startswith('00') else '2026-07-19 ')+s,tz='UTC'))
ev['m']=(ev.t-KO).dt.total_seconds()/60
COL={'ads':'#d62728','studio':'#ff7f0e','play':None}
DEV=[('BenSamsung55" 4K2015','Ben Samsung 55" 4K (France — the logged feed)'),('STJ Prototype 8K','STJ Prototype 8K (UK feed, lag unknown)'),('TP Sammy','TP Sammy (UK feed, lag unknown)'),('Stan-42”Plasma','Stan plasma 42" (Canada feed, lag unknown)')]
fig,axes=plt.subplots(len(DEV),1,figsize=(12,10),sharex=True)
for ax,(dev,lab) in zip(axes,DEV):
    for i in range(len(ev)-1):
        ph=ev.phase_after.iloc[i]; c=COL.get(ph)
        if c: ax.axvspan(ev.m.iloc[i],ev.m.iloc[i+1],color=c,alpha=0.18,lw=0)
    ax.plot(m,p[dev],lw=0.8,color='C0'); ax.set_ylabel('W'); ax.set_title(lab,fontsize=10); ax.grid(alpha=0.3)
    ax.axvline(0,color='k',lw=0.8,ls=':'); ax.axvline(174.2,color='k',lw=0.8,ls=':')
axes[0].plot([],[],color=COL['ads'],lw=6,alpha=0.3,label='advertising (logged, French feed)'); axes[0].plot([],[],color=COL['studio'],lw=6,alpha=0.3,label='studio / stadium, not play'); axes[0].legend(loc='lower right',fontsize=8)
axes[-1].set_xlabel('minutes from kick-off (19:08:20 UTC); dotted = kick-off / final whistle (extra time)')
fig.suptitle('C3 — World Cup final 2026-07-19, REM cloud path 10 s / 1 W, four content-reactive TVs with the logged event bands',fontsize=11)
fig.tight_layout(rect=(0,0,1,0.97)); fig.savefig('figures/fig_c3_final_bands.png',dpi=160); print('wrote figures/fig_c3_final_bands.png')
