import pandas as pd

# Your data
data = r"/Users/ull/Documents/GRA/TRAFFIC-Project/SUMO Files/files/east/Bellevue_116th_NE12th_2017-09-11_14-08-35_Full.csv"
filename = "Bellevue_116th_NE12th__2017-09-11_14-08-35_Full"

df = pd.read_csv(data)

final_result_throughput = []
final_result_time = []

for scenario in df['Scenario_ID'].unique():
    scenario_data = df[df['Scenario_ID'] == scenario]
    
    if scenario_data['Throughput'].max() > 0: 
        best_throughput_group = scenario_data.loc[scenario_data['Throughput'].idxmax()]
    else:
        best_throughput_group = scenario_data.iloc[0] 

    if scenario_data['Average_Travel_Time'].min() > 0:  
        best_time_group = scenario_data.loc[scenario_data['Average_Travel_Time'].idxmin()]
    else:
        best_time_group = scenario_data.iloc[0] 
    
    best_group_throughput_data = {
        'Scenario_ID': scenario,
        'Scenario': best_throughput_group['Scenario_Description'],
        'Best_Group_By_Throughput': best_throughput_group['Group_ID'],
        'Best_Throughput': best_throughput_group['Throughput']      
    }

    best_group_time_data = {
        'Scenario_ID': scenario,
        'Scenario': best_throughput_group['Scenario_Description'],
        'Best_Group_By_Time': best_time_group['Group_ID'],
        'Best_Travel_Time': best_time_group['Average_Travel_Time']
    }
    
    final_result_throughput.append(best_group_throughput_data)
    final_result_time.append(best_group_time_data)

# Convert the results to a DataFrame
final_df_throughput = pd.DataFrame(final_result_throughput)
final_df_time = pd.DataFrame(final_result_time)

# Save to a CSV file
folder_path = 'best_scenarios/full'  
final_df_throughput.to_csv(f'{folder_path}/best_throughput_{filename}.csv', index=False)
final_df_time.to_csv(f'{folder_path}/best_time_{filename}.csv', index=False)

print("File saved successfully.")
