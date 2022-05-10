#!/usr/bin/python

import time
import pprint
import json
import types
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os
from datetime import datetime, timedelta
import TVAC_time_constants as TVAC_times
from load_data_files import load_mainhsk_names, load_mapping, load_minigoose, load_NASA_TCs, load_SFC, load_SFC_lists, load_var_names
from plotter_HELIX import make_plot, time_mask
from pip import main

times, df = load_SFC(1)
Xadc_array, magnetflows_array, mainhsk_temps_array, DCT_temps_array, helium_levels_array = load_SFC_lists(times,df)
mainhsk_names = load_mainhsk_names(1)
NASA_TCs = load_NASA_TCs(1)
minigoose = load_minigoose(1)
mapping_df = load_mapping(1)
print(mapping_df.head())
TVAC_times.all_delta_times(1)
var_temp_names = load_var_names(1)
#print(type(times.values[0]))
#print(times.dtypes)
#print(type(TVAC_times.ColdestCase[0]))
#print(type(np.datetime64()))
#print(type(pd.to_datetime(TVAC_times.ColdestCase[0])))
#print(type(pd.to_datetime(TVAC_times.ColdestCase[0]).to_datetime64()))
#print(times.values[(times.values>=pd.to_datetime(TVAC_times.ColdestCase[0]).to_datetime64()) & (times.values<=pd.to_datetime(TVAC_times.ColdestCase[-1]).to_datetime64())])
#print(type(times))

#collect statistics on the types, add as series to DF of var_temp_names
#print(type(df[var_temp_names.NAME.values[0]].values[0]))
#types_list=[]
#for i in var_temp_names.NAME.values:
#      types_list.append(type(df[i].values[0]))
#var_temp_names['datatype']=np.asarray(types_list)
#print(var_temp_names.datatype.values[0])
#var_temp_names.to_csv("datatypes.csv")
#make a new, all variables data types series.
#names_payload=df.columns.values
#print(type(df[names_payload[0]].values))
#all_types_list=[]
#for i in names_payload:
#      all_types_list.append(type(df[i].values[0]))
#all_types=np.asarray(all_types_list)
#df2 = pd.DataFrame(data=np.column_stack((names_payload,np.asarray(all_types_list))),
                  # columns=['NAME', 'datatype'])
#df2.to_csv("all_data_types.csv")

# need timestamps to use here for cold wall begin filling and ending and then hot and cold cases respectively.
# datetime(year, month, day, hour, minute, second, microsecond)
#b = datetime(2017, 11, 28, 23, 55, 59, 342380)

s0=5
print(df.columns)
print(mapping_df.columns)
print(len(mapping_df.columns))
#print(mapping_df.loc[mapping_df['Component Name']=="alicat",mapping_df['Component Name']])
#x,y=time_mask(times, mainhsk_temps_array[:,15],'Coldest')
#make_plot(x,y,'Gas panel-Coldest')
# for the gas panel
#x,y=time_mask(times, mainhsk_temps_array[:,15],'Flip')
#make_plot(x,y,'Gas panel-Flip')
# for the South TOF top 
#x,y=time_mask(times, mainhsk_temps_array[:,7],'Coldest')
#make_plot(x,y,'Top TOF South-Coldest')
# for the Battery rail 
x,y=time_mask(times, mainhsk_temps_array[:,4],'Flip')
make_plot(x,y,'Battery Rail-Flip',[-10,-22.5])



# CHANGE PAYTONS CODE TO FIRST ELIMINATE THE DICT BY GETTING JUST THE TEMPS
test_payton=df['payload.fChargeControlStat.fPVA'].values
temp_list=[]
for i in test_payton: temp_list.append(i)
test_payton_array=np.asarray(temp_list)
print(type(test_payton_array[:,0]))
print("here comes the variables")
for i in test_payton_array[0,:]:
      print(type(i))
print(test_payton_array[0,0]) # this gives me a dictionary
paytons_keys=list(test_payton_array[0,0].keys())
print(paytons_keys)
print(test_payton_array[0,0].get(paytons_keys[-1]))

#
#print the average to see bad channels
#print(DCT_temps_array[:,])
j=10000
while j<len(DCT_temps_array[0,:]):
      print("channel : {} , value : {} ".format(j,np.mean(DCT_temps_array[:,j])))
      j+=1

#fig = plt.figure(figsize=(14, 10), dpi=200)
#axs=fig.add_subplot(111)
#axs.scatter(times, DCT_temps_array[:,21], marker='.',s=s0)  # DCTV top
#axs.set_ylim([-20, 39])
#plt.xticks(rotation=45)
#plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %d - %H:%M'))
#plt.gcf().autofmt_xdate()
##axs[0].grid()
#axs.grid()
#plt.show()
i=1000
while(i<len(names_payload)):
      try:
            is_it_float= all_types[i]==all_types[7]
      except Exception:
            is_it_float=False
            pass
      if is_it_float:
            print("its a float")
            print(all_types[i])
            print(i)
            # Now make a plot
            fig = plt.figure(figsize=(14, 10), dpi=200)
            axs=fig.add_subplot(111)
            #gs = fig.add_gridspec(1, 1)
            #axs = gs.subplots(sharex=True, sharey=False)
            #axs = gs.subplots()
            #axs[0].scatter(times, pressure, marker='.')
            #axs[0].set_ylabel("Pressure (Torr)")
            #axs[0].set_ylim([1, 759])
            axs.axvspan(TVAC_times.cold_wall_fill_start, TVAC_times.cold_wall_fill_end, alpha=0.1, color='royalblue',label="cold wall fill")
            axs.axvspan(TVAC_times.cold_case_start, TVAC_times.cold_case_end, alpha=0.1, color='cyan', label="cold case")
            axs.axvspan(TVAC_times.hot_case_start,TVAC_times.hot_case_end , alpha=0.1, color='firebrick', label="hot case")
            axs.axvspan(TVAC_times.kickflip_start,TVAC_times.kickflip_end , alpha=0.3, hatch="XXX", color='darkorange', label="flipped hot case")
            axs.axvspan(TVAC_times.drain_cold_wall_begin,TVAC_times.drain_cold_wall_end , alpha=0.1, color='royalblue', label="draining cold wall")
            axs.axvspan(TVAC_times.slight_warmup_start,TVAC_times.slight_warmup_end , alpha=0.3, color='red', label="slight warm up")
            #axs.scatter(times, df[names_payload[i]], marker='.',s=s0) #this is a temp by the inflections.
            axs.scatter(times[(df[names_payload[i]]>-100) & (df[names_payload[i]]<100)], 
            df.loc[(df[names_payload[i]]>-100) & (df[names_payload[i]]<100),names_payload[i]],
             marker='.',s=s0) #this is a temp by the inflections.
            axs.grid()
            plt.xticks(rotation=45)
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %d - %H:%M'))
            plt.gcf().autofmt_xdate()
            plt.title(names_payload[i])
            
            plt.savefig(os.path.join(data_path,"plots_all\\"+names_payload[i]+".png"), bbox_inches='tight')
            plt.close(fig)
      i+=1


#fig = plt.figure(figsize=(14, 10), dpi=200)
#axs=fig.add_subplot(111)
#axs.scatter(times, magnetflows_array[:,0], marker='.',s=3) #this is a dictionary in each element of the array
#axs.scatter(times, Xadc_array[:,0], marker='.',s=3) #these are xadc for FPGA so array of voltages and temps somewhere
#axs.scatter(times, df['payload.fSFCStatus.fATX_V33'], marker='.',s=3) #this one is always 0
#axs.scatter(times, df['payload.fSFCStatus.fMB_V33SB'], marker='.',s=3) #this one is always 3.2 ish
#axs.scatter(times, df['payload.fSFCStatus.fMB_V33'], marker='.',s=3) #this one is always 2.56

# now in hours
# do conversions...

#Vertical lines
#axs[0].axvline(x=power_on_DAQ,ymin=0, ymax=1, color='red',label="power on DAQ")
#axs[0].text(power_on_DAQ, 10, "Power on DAQ", color='red',rotation=90, fontsize=8)
#axs[0].axvline(x=discharge_magnet,ymin=0, ymax=1, color='Brown',label="discharge magnet")
#axs[0].text(discharge_magnet, 10, "Discharge magnet", color='Brown', rotation=90, fontsize=8)
#axs[1].axvline(x=power_on_DAQ,ymin=0, ymax=1, ls=':', color='red')
#axs[1].axvline(x=discharge_magnet,ymin=0, ymax=1, ls=':',color='Brown')
#axs[1].axvline(x=cold_wall_fill_start,ymin=0, ymax=1, color='black',label="cold wall fill start")
#axs[1].axvline(x=cold_wall_fill_end,ymin=0, ymax=1, color='black',label="cold wall fill start")

# hatches for timespans
#axs.axvspan(cold_wall_fill_start, cold_wall_fill_end, alpha=0.1, color='royalblue',label="cold wall fill")
#axs.axvspan(cold_case_start, cold_case_end, alpha=0.1, color='cyan', label="cold case")
#axs.axvspan(hot_case_start,hot_case_end , alpha=0.1, color='firebrick', label="hot case")
#axs.axvspan(kickflip_start,kickflip_end , alpha=0.3, hatch="XXX", color='darkorange', label="flipped hot case")
#axs.axvspan(drain_cold_wall_begin,drain_cold_wall_end , alpha=0.1, color='royalblue', label="draining cold wall")
#axs.axvspan(slight_warmup_start,slight_warmup_end , alpha=0.3, color='red', label="slight warm up")

#minigoose crap
#names_minigoose=minigoose_df.columns
#minigoose_times = pd.to_datetime(minigoose_df['UTC'])

#iter=3
#while iter<len(names_minigoose)-14:
    #print(len(NASA_TCs[iter]['Times'].values))
    #print(len(NASA_TCs[iter]['Value'].values))
    #print(NASA_names[iter]['Times'].values))
    #axs.scatter(minigoose_times,minigoose_df[names_minigoose[iter]], marker='.',s=s0,label=names_minigoose[iter]) # 
    #iter+=1
#axs.set_ylim([-79, 49])
#axs.set_xlim([times.values[0],times.values[-1]])


#size for markers visibility
#temp data goes here

#across foam
#axs.scatter(NASA_TCs[1]['Times'], NASA_TCs[1]['Value'], marker='2',s=s0,label="NASA TC - "+NASA_names.ID.values[1]) # In South is on foam inside gondola
#axs.scatter(NASA_TCs[8]['Times'], NASA_TCs[8]['Value'], marker='2',s=s0,label="NASA TC - "+NASA_names.ID.values[8]) # SoLo is on foam outside gondola
#axs.scatter(NASA_TCs[0]['Times'], NASA_TCs[0]['Value'], marker='2',s=s0,label="NASA TC - "+NASA_names.ID.values[0]) # InEast is on foam inside foam
#axs.scatter(NASA_TCs[6]['Times'], NASA_TCs[6]['Value'], marker='2',s=s0,label="NASA TC - "+NASA_names.ID.values[6]) # EastLo is on foam inside gondola
#axs.set_ylim([-80, 30])
#axs.set_xlim([times.values[0],times.values[-1]])


#NASA TCs
#iter=0
#while iter<len(NASA_TCs):
#    #print(len(NASA_TCs[iter]['Times'].values))
#    #print(len(NASA_TCs[iter]['Value'].values))
#    #print(NASA_names[iter]['Times'].values))
#    axs.scatter(NASA_TCs[iter]['Times'], NASA_TCs[iter]['Value'], marker='.',s=s0,label=NASA_names.ID.values[iter]) # 
#    iter+=1
#
#axs.set_ylim([-79, 49])
#axs.set_xlim([times.values[0],times.values[-1]])

# south here : seq=1
#axs.scatter(times, mainhsk_temps_array[:,7], marker='.',s=s0,label=mainhsk_names.Location.values[7]) # TOF top South
#axs.scatter(times, mainhsk_temps_array[:,5], marker='.',s=s0,label=mainhsk_names.Location.values[5]) # TOF btm south
#axs.scatter(times, mainhsk_temps_array[:,3], marker='.',s=s0,label=mainhsk_names.Location.values[3]) # gondola btm south
#axs.scatter(times, mainhsk_temps_array[:,8], marker='.',s=s0,label=mainhsk_names.Location.values[8]) # gondola mid South
#axs.scatter(NASA_TCs[13]['Times'], NASA_TCs[13]['Value'], marker='2',s=s0,label="NASA TC - "+NASA_names.ID.values[13]) # SoFr is on the gondola I believe
#axs.scatter(NASA_TCs[1]['Times'], NASA_TCs[1]['Value'], marker='2',s=s0,label="NASA TC - "+NASA_names.ID.values[1]) # In South is on foam inside gondola
#axs.scatter(NASA_TCs[7]['Times'], NASA_TCs[7]['Value'], marker='2',s=s0,label="NASA TC - "+NASA_names.ID.values[7]) # SoUp is on foam outside gondola
#axs.scatter(NASA_TCs[8]['Times'], NASA_TCs[8]['Value'], marker='2',s=s0,label="NASA TC - "+NASA_names.ID.values[8]) # SoUp is on foam outside gondola
#axs.set_ylim([-50, 33])
#axs.set_xlim([times.values[0],times.values[-1]])


#RICH east or west side
#axs.scatter(times, mainhsk_temps_array[:,13], marker='.',s=s0,label=mainhsk_names.Location.values[13]) # Mid east RICH heatsink
#axs.scatter(times, mainhsk_temps_array[:,17], marker='.',s=s0,label=mainhsk_names.Location.values[17]) # RICH cover E
#axs.scatter(NASA_TCs[0]['Times'], NASA_TCs[0]['Value'], marker='2',s=s0,label="NASA TC - "+NASA_names.ID.values[0]) # InEast is on foam inside foam
#axs.scatter(NASA_TCs[5]['Times'], NASA_TCs[5]['Value'], marker='2',s=s0,label="NASA TC - "+NASA_names.ID.values[5]) # EastUp is on foam inside gondola
#axs.scatter(NASA_TCs[6]['Times'], NASA_TCs[6]['Value'], marker='2',s=s0,label="NASA TC - "+NASA_names.ID.values[6]) # EastUp is on foam inside gondola
#axs.scatter(times, mainhsk_temps_array[:,14], marker='.',s=s0,label=mainhsk_names.Location.values[14]) # Mid West RICH heatsink
#axs.scatter(times, mainhsk_temps_array[:,19], marker='.',s=s0,label=mainhsk_names.Location.values[19]) # RICH cover E
#axs.scatter(NASA_TCs[9]['Times'], NASA_TCs[9]['Value'], marker='2',s=s0,label="NASA TC - "+NASA_names.ID.values[9]) # WestUp is on foam inside gondola
#axs.scatter(NASA_TCs[10]['Times'], NASA_TCs[10]['Value'], marker='2',s=s0,label="NASA TC - "+NASA_names.ID.values[10]) # WestLo is on foam inside gondola
#axs.set_ylim([-60, 60])
#axs.set_xlim([times.values[0],times.values[-1]])

#North side across foam
#correct/calibrate the North top TOF sensor
#begin_pumping=datetime(2022,2,7,14,55,0,0)
#times_calibrate=pd.to_datetime(times.values)
#times_range=np.asarray(begin_pumping-times_calibrate).astype('timedelta64[s]')
#times_range = times_range / np.timedelta64(1, 's')
#times_to_consider=np.where(times_range>0)
#TOF_diffs=mainhsk_temps_array[times_to_consider,21]-mainhsk_temps_array[times_to_consider,7]
#average_offset=np.mean(TOF_diffs[0])
#median_offset=np.median(TOF_diffs[0])
#axs.scatter(times, mainhsk_temps_array[:,20], marker='.',s=s0,label=mainhsk_names.Location.values[20]) # Gondola btm north
#axs.scatter(times, mainhsk_temps_array[:,16], marker='.',s=s0,label=mainhsk_names.Location.values[16]) # TOF btm N
#axs.scatter(times, mainhsk_temps_array[:,21]-average_offset, marker='.',s=s0,label=mainhsk_names.Location.values[21]) # TOF top N
#axs.scatter(NASA_TCs[3]['Times'], NASA_TCs[3]['Value'], marker='2',s=s0,label="NASA TC - "+NASA_names.ID.values[3]) # NoUp is on foam inside gondola
#axs.scatter(NASA_TCs[4]['Times'], NASA_TCs[4]['Value'], marker='2',s=s0,label="NASA TC - "+NASA_names.ID.values[4]) # NoLo is on foam inside gondola
#axs.set_ylim([-80, 30])
#axs.set_xlim([times.values[0],times.values[-1]])



#misc 1 interesting areas
#axs[1].scatter(times, mainhsk_temps_array[:,2], marker='.',s=s0,label=mainhsk_names.Location.values[2]) # DCT HV box
#axs[1].scatter(times, mainhsk_temps_array[:,6], marker='.',s=s0,label=mainhsk_names.Location.values[6]) # SFC backplate
#axs[1].scatter(times, mainhsk_temps_array[:,15], marker='.',s=s0,label=mainhsk_names.Location.values[15]) # Gas panel
#axs[1].scatter(times, mainhsk_temps_array[:,3], marker='.',s=s0,label=mainhsk_names.Location.values[3]) # gondola btm South
#axs[1].scatter(times, dctboxtemp, marker='.',s=s0,label="DCT box internal temp") # dctbox temp
#axs[1].set_ylim([-50, 38])


#RICH
#axs.axvline(x=DAQ_Run,ymin=0, ymax=1, color='red',label="DAQ Run")
#axs.axvline(x=DAQ_Run_2,ymin=0, ymax=1, color='black',label="DAQ Run 2 end")
#axs.scatter(times, mainhsk_temps_array[:,23], marker='.',s=s0,label=mainhsk_names.Location.values[23]) # rich focal plane NW
#axs.scatter(times, mainhsk_temps_array[:,0], marker='.',s=s0,label=mainhsk_names.Location.values[0]) # rich focal plane SW
#axs.scatter(times, mainhsk_temps_array[:,18], marker='.',s=s0,label=mainhsk_names.Location.values[18]) # rich cover N
#axs.scatter(times, mainhsk_temps_array[:,9], marker='.',s=s0,label=mainhsk_names.Location.values[9]) # rich cover S
#axs.scatter(times, mainhsk_temps_array[:,19], marker='.',s=s0,label=mainhsk_names.Location.values[19]) # rich cover W
#axs.scatter(times, mainhsk_temps_array[:,17], marker='.',s=s0,label=mainhsk_names.Location.values[17]) # rich cover E
#axs.set_ylim([-20, 39])

#TOF Fees only
#axs.scatter(times, mainhsk_temps_array[:,12], marker='.',s=s0,label=mainhsk_names.Location.values[12]) 
#axs.scatter(times, mainhsk_temps_array[:,22], marker='.',s=s0,label=mainhsk_names.Location.values[22]) 
#axs.scatter(times, mainhsk_temps_array[:,24], marker='.',s=s0,label=mainhsk_names.Location.values[24]) 
#axs.scatter(times, mainhsk_temps_array[:,25], marker='.',s=s0,label=mainhsk_names.Location.values[25]) 

#Gondola Bottom
#axs.scatter(times, mainhsk_temps_array[:,3], marker='.',s=s0,label=mainhsk_names.Location.values[3]) 
#axs.scatter(times, mainhsk_temps_array[:,4], marker='.',s=s0,label=mainhsk_names.Location.values[4]) 
#axs.scatter(times, mainhsk_temps_array[:,20], marker='.',s=s0,label=mainhsk_names.Location.values[20]) 
#axs.scatter(times, mainhsk_temps_array[:,2], marker='.',s=s0,label=mainhsk_names.Location.values[2])

#bore paddle stuff
#axs.scatter(times, mainhsk_temps_array[:,10], marker='.',s=s0,label=mainhsk_names.Location.values[10]) 
#axs.scatter(times, mainhsk_temps_array[:,11], marker='.',s=s0,label=mainhsk_names.Location.values[11]) 

#DCT
#axs.axvline(x=heater_start,ymin=0, ymax=1,ls='-', color='red',label="heaters start")
#axs.axvline(x=heater_max,ymin=0, ymax=1,ls=':', color='black',label="heaters highest")
#axs.scatter(times, mainhsk_temps_array[:,15], marker='.',s=s0,label=mainhsk_names.Location.values[15]) #gas panel
#axs.scatter(times, mainhsk_temps_array[:,1], marker='.',s=s0,label=mainhsk_names.Location.values[1])  # DCTV top
#dct box temp
#axs.scatter(times,df['payload.dctBoxTemp'], marker='2',s=s0,label="DCT HSK box uC") # In South is on foam inside gondola
#axs.set_ylim([-30, 50])
# for DCT thermistors
#iter=0
#while iter<len(DCT_temps[0]): #,label=mainhsk_names.Location.values[1]
#    axs[1].scatter(times, DCT_temps_array[:,iter], marker='.',s=s0)  # DCTV top
#    iter+=1
#
#axs[1].set_ylim([-20, 39])

#axs.set_ylabel("Temps (C)",fontsize=12)

#plt.xticks(rotation=45)
#plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %d - %H:%M'))
#plt.gcf().autofmt_xdate()
#axs[0].grid()
#axs.grid()
#handles, labels = axs.get_legend_handles_labels()
#lgd = axs[1].legend(handles, labels)
#for legend_handle in lgd.legendHandles:
#    legend_handle.set_sizes([20])
#labels[6]._legmarker.set_markersize(6)
#lgd=fig.legend(handles, labels, loc='upper center', ncol=5, fontsize=12)
# as many of these as axs[1].scatter above

#lgd.legendHandles[-14].set_sizes([60])
#lgd.legendHandles[-13].set_sizes([60])
#lgd.legendHandles[-12].set_sizes([60])
#lgd.legendHandles[-11].set_sizes([60])
#lgd.legendHandles[-10].set_sizes([60])
#lgd.legendHandles[-9].set_sizes([60])
#lgd.legendHandles[-8].set_sizes([60])
#lgd.legendHandles[-7].set_sizes([60])
#lgd.legendHandles[-6].set_sizes([60])
#lgd.legendHandles[-5].set_sizes([60])
#lgd.legendHandles[-4].set_sizes([60])
#lgd.legendHandles[-3].set_sizes([60])
#lgd.legendHandles[-2].set_sizes([60])
#lgd.legendHandles[-1].set_sizes([60])#

#plt.savefig("plot_timeline_south.pdf", bbox_inches='tight')

#plt.savefig("minigeese.png")

#plt.show()
