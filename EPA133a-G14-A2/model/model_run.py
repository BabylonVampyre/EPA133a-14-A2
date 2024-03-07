import mesa

from model import BangladeshModel
import contextlib
import itertools
import types
from functools import partial

with contextlib.suppress(ImportError):
    import pandas as pd

"""
    Run simulation
    Print output at terminal
"""

# ---------------------------------------------------------------

# run time 5 x 24 hours; 1 tick 1 minute
run_length = 5 * 24 * 60
#run_length = 10
# run time 1000 ticks
#run_length = 1000
#chosen_scenario = 1
#seed = 1234567 #sim 1
#seed = 1234568 #sim 2
#seed = 1234569 #sim 3
#seed = 1234560 #sim 4
#seed = 1234561 #sim 5
#seed = 1234562 #sim 6
#seed = 1234563 #sim 7
#seed = 1234564 #sim 8
#seed = 1234565 #sim 9
#seed = 1234566 #sim 10

chosen_scenario = [0,1,2,3,4,5,6,7,8,9]
seed_list = [1234567,1234568,1234569,1234560,1234561,1234562,1234563,1234564,1234565,1234566]
list_of_driving_times =[]
from statistics import mean
for i in chosen_scenario:
    for seed_index, j in enumerate(seed_list):

        sim_model = BangladeshModel(seed=j)

# Check if the seed is set
#print("SEED " + str(sim_model._seed))

# One run with given steps
        for k in range(run_length):
            sim_model.step()


        df = sim_model.datacollector.get_agent_vars_dataframe()

        #print([i for i in df["Driving time of cars leaving"] if i != None])
        #list_of_driving_times.append(df["Driving time of cars leaving"].loc[2:-1,:].mean(numeric_only=True, axis=0), (i,seed_index))
        df.to_csv(f"../model/experiment/Scenario{i}_sim{seed_index}.csv")

#print(list_of_driving_times)