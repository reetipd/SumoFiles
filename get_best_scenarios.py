import pandas as pd

def analyze_traffic_scenarios(file_path):
    # Read the CSV file
    df = pd.read_csv(file_path)

    final_result_throughput = []
    final_result_time = []

    # Process the data
    for scenario in df['Scenario_ID'].unique():
        scenario_data = df[df['Scenario_ID'] == scenario]

        # Find the best throughput group
        if scenario_data['Throughput'].max() > 0: 
            best_throughput_group = scenario_data.loc[scenario_data['Throughput'].idxmax()]
        else:
            best_throughput_group = scenario_data.iloc[0]

        # Find the best time group
        if scenario_data['Average_Travel_Time'].min() > 0:  
            best_time_group = scenario_data.loc[scenario_data['Average_Travel_Time'].idxmin()]
        else:
            best_time_group = scenario_data.iloc[0] 

        # Store results for throughput and time
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

    # Convert the results to DataFrames
    final_df_throughput = pd.DataFrame(final_result_throughput)
    final_df_time = pd.DataFrame(final_result_time)

    # Return the DataFrames
    return final_df_throughput, final_df_time
