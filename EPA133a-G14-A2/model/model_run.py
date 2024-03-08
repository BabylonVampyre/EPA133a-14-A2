from model import BangladeshModel

"""
    Run simulation
    Print output at terminal
"""

# ---------------------------------------------------------------

# run time 5 x 24 hours; 1 tick 1 minute
run_length = 7200

scenario_list = [0,1, 2, 3, 4, 5, 6, 7, 8]

seed_list = [1234567, 1234568, 1234569, 1234560, 1234561,
             1234562, 1234563, 1234564, 1234565, 1234566]

# to print a progress update at each run
number_of_runs = len(scenario_list)*len(seed_list)
counter = 0

for i in scenario_list:
    for seed_index, j in enumerate(seed_list):
        sim_model = BangladeshModel(scenario=i, seed=j)

        # One run with given steps
        for k in range(run_length):
            sim_model.step()

        df = sim_model.datacollector.get_agent_vars_dataframe()
        # subset dataframe to only show the sinks and sourcesinks
        # because we want to collect what vehicles they removed and their driving time
        df = df[df['Driving time of cars leaving'].notnull()]
        df = df[df['Driving time of cars leaving'].str.len() != 0]
        df.to_csv("../model/OutputModel.csv")
        df.to_csv(f"../model/experiment/Scenario{i}_sim{seed_index}.csv")

        counter += 1
        print(counter, '/', number_of_runs, 'Done. Next up: scenario:', i,  'seed: ', j)
