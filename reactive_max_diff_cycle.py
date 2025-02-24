

import pandas as pd

decision= "Static"
def analyze_trend(path, i, interval, past_scenarios=None, past_throughputs_max=None, make_decision_after=3):
    global decision
    """
    Analyzes the trend from the CSV file at the given path and makes a decision on the next scenario.
    
    :param path: Path to the CSV file containing traffic data for the interval.
    :param i: The current interval (used for tracking the scenario group).
    :param interval: The interval unit (e.g., 1-minute, 2-minute).
    :param past_scenarios: List of past scenarios.
    :param past_throughputs_max: List of past throughput values.
    :param decision: Current decision (starting with 'Static').
    :return: A tuple with (chosen_value, decision, past_scenarios, past_throughputs_max).
    """

    chosen_value = ""

    df = pd.read_csv(path)

    if make_decision_after == 3:
        if i % interval == 0 and i != 0:
        # If we have past data, decide based on the best past throughput scenario
            if len(past_scenarios) >= 3:
                if len(past_scenarios) >= 3:
                    if past_scenarios[-1] == past_scenarios[-2] == past_scenarios[-3]:
                        decision = past_scenarios[-1]  # Continue with the same scenario
                    else:
                        max_throughput =  max(past_throughputs_max)
                        index = past_throughputs_max.index(max_throughput)
                        decision = past_scenarios[index]

                    chosed_throughput = df[df['Group_ID'] == str(decision)]['Throughput']
                    if not chosed_throughput.empty:
                        chosen_value = chosed_throughput.iloc[0]  # Get the first value
                    else:
                        print("No matching data found for decision.")

                
                

            # After deciding, we look for the throughput corresponding to the new decision
            chosed_throughput = df[df['Group_ID'] == str(decision)]['Throughput']
            avg_travel_time = df[df['Group_ID'] == str(decision)]['Average_Travel_Time'].mean()
            if not chosed_throughput.empty:
                chosen_value = chosed_throughput.iloc[0]
            else:
                print(f"Interval {i}: No data found for decision {decision}.")

            df_filtered = df[df['Group_ID'] != 'Static']
            group_id = df_filtered.loc[df_filtered['Throughput'].idxmax(), 'Group_ID']

            past_scenarios.clear()
            past_throughputs_max.clear()

            throughput = df_filtered['Throughput'].max()

            past_scenarios.append(group_id)
            past_throughputs_max.append(throughput)


        else:
            chosed_throughput = df[df['Group_ID'] == str(decision)]['Throughput']
            avg_travel_time = df[df['Group_ID'] == str(decision)]['Average_Travel_Time'].mean()
            
            if not chosed_throughput.empty:
                chosen_value = chosed_throughput.iloc[0]
                # avg_travel_time = chosed_avg_time.iloc[0]
            else:
                print(f"Interval {i}: No data found for decision {decision}....")
                chosen_value = 0  # Set to 0 if no matching data is found

            # get maximum througput group_id excluding static group_id
            df_filtered = df[df['Group_ID'] != 'Static']
            group_id = df_filtered.loc[df_filtered['Throughput'].idxmax(), 'Group_ID']
            # print("Group ID: ", group_id, i)   
            throughput = df['Throughput'].max()

            # print("Max throughput at interval", i, "is", throughput, group_id)


        # Track throughput and scenarios for future decision-making
            past_scenarios.append(group_id)
            past_throughputs_max.append(throughput)

        return chosen_value, avg_travel_time

    else:
        if i % interval == 0 and i != 0:
            if len(past_scenarios) >= 2:
                if len(past_scenarios) >= 2:
                    if past_scenarios[-1] == past_scenarios[-2]:
                        decision = past_scenarios[-1]  # Continue with the same scenario
                    else:
                        max_throughput =  max(past_throughputs_max)
                        index = past_throughputs_max.index(max_throughput)
                        decision = past_scenarios[index]

                    chosed_throughput = df[df['Group_ID'] == str(decision)]['Throughput']
                    if not chosed_throughput.empty:
                        chosen_value = chosed_throughput.iloc[0]  # Get the first value
                    else:
                        print("No matching data found for decision.")

                
                

            # After deciding, we look for the throughput corresponding to the new decision
            chosed_throughput = df[df['Group_ID'] == str(decision)]['Throughput']
            avg_travel_time = df[df['Group_ID'] == str(decision)]['Average_Travel_Time'].mean()
            if not chosed_throughput.empty:
                chosen_value = chosed_throughput.iloc[0]
                # avg_travel_time = chosed_avg_time.iloc[0]
                # print(f"Interval {i}: Chosen Group_ID = {decision}, Chosen Throughput: {chosen_value}")
            else:
                print(f"Interval {i}: No data found for decision {decision}.")

            df_filtered = df[df['Group_ID'] != 'Static']
            group_id = df_filtered.loc[df_filtered['Throughput'].idxmax(), 'Group_ID']

            past_scenarios.clear()
            past_throughputs_max.clear()

            throughput = df_filtered['Throughput'].max()

            past_scenarios.append(group_id)
            past_throughputs_max.append(throughput)


        else:
            # For intervals not a multiple of 'interval', use the previous decision
            # print("decision here",decision)
            chosed_throughput = df[df['Group_ID'] == str(decision)]['Throughput']
            avg_travel_time = df[df['Group_ID'] == str(decision)]['Average_Travel_Time'].mean()
            
            if not chosed_throughput.empty:
                chosen_value = chosed_throughput.iloc[0]
                # avg_travel_time = chosed_avg_time.iloc[0]
            else:
                print(f"Interval {i}: No data found for decision {decision}....")
                chosen_value = 0  # Set to 0 if no matching data is found

            # get maximum througput group_id excluding static group_id
            df_filtered = df[df['Group_ID'] != 'Static']
            group_id = df_filtered.loc[df_filtered['Throughput'].idxmax(), 'Group_ID']
            # print("Group ID: ", group_id, i)   
            throughput = df['Throughput'].max()

            # print("Max throughput at interval", i, "is", throughput, group_id)


        # Track throughput and scenarios for future decision-making
            past_scenarios.append(group_id)
            past_throughputs_max.append(throughput)

        return chosen_value, avg_travel_time


# Main loop
max_throughput, max_group_id, avg_travel_time = 0, None, 0
past_scenarios = []  
past_throughputs_max = []  

# Initialize decision as 'Static' for the first interval
decision = 'Static'

total_throughput = 0
total_time = 0

for i in range(4):  # Assuming 12 intervals
    file_name = "Bellevue_116th_NE12th__2017-09-11_14-08-35_3Min_Data_Scaled_2X"
    path = f"files/Bellevue_116th_NE12th__2017-09-11_14-08-35/new/full_3/{file_name}_{i}.csv"
    throughput, time = analyze_trend(
        path, i, 2, past_scenarios, past_throughputs_max, 2
    )

    print("Choesen throughput", throughput)

    total_throughput += throughput
    total_time += time

print("Total Throughput: ", total_throughput)
time = total_time/12
print("Time is", time)
