import pandas as pd
import ast
import numpy as np
import seaborn as sns

#open the csv's and save as dataframes
df={} #collect the trucks and driving time per tick
for i in range (9): #scenario
    df[i] = pd.DataFrame()
    for j in range (10): #run
        df[i]=pd.concat([df[i],pd.read_csv('../model/experiment/Scenario{}_sim{}.csv'.format(i,j))['Driving time of cars leaving']])
    df[i].columns=['Driving time of cars leaving']

#collect per scenario all the driving times of all the runs
df2={}
for framenr in range (9): #iterate the dataframes
    df2[framenr]=np.array([]) #collect all the truck times per scenario
    for tick in df[framenr]['Driving time of cars leaving']: #iterate the entries, where each entry is a list of truck that leave at that tick
        extracted_list = ast.literal_eval(tick) #thx chatgpt
        for truck_time in extracted_list: #iterate over the trucks
            df2[framenr]=np.append(df2[framenr],truck_time[1]) #add the truck's time to the dataframe
    print(df2[framenr][0])

#plot for every scenario a density plot
for scenario in df2:
    sns.kdeplot(scenario, bw=0.5)