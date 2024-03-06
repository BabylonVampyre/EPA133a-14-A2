import mesa

from model import BangladeshModel
import contextlib
import itertools
import types
from functools import partial
#mini change


with contextlib.suppress(ImportError):
    import pandas as pd

"""
    Run simulation
    Print output at terminal
"""

# ---------------------------------------------------------------

# run time 5 x 24 hours; 1 tick 1 minute
# run_length = 5 * 24 * 60

# run time 1000 ticks
run_length = 1000

seed = 1234567
chosen_scenario = 0

sim_model = BangladeshModel(seed=seed)

# Check if the seed is set
print("SEED " + str(sim_model._seed))

# One run with given step
for i in range(run_length):
    sim_model.step()


df = sim_model.datacollector.get_agent_vars_dataframe()
#subset dataframe to only show the sinks and sourcesinks because we want to collect what vehicles they removed and their driving time

df=df[df['Driving time of cars leaving'].notnull()]
df=df[df['Driving time of cars leaving'].str.len() != 0]
print(df.head())
df.to_csv("../model/OutputModel.csv")
