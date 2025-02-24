import pandas as pd
import csv

def analyze_traffic_scenarios(file_path, video_index):
    # Read the CSV file
    df = pd.read_csv(file_path)

    final_result_throughput = []
    final_result_time = []

    # Process the data
    for scenario in df['Scenario_ID'].unique():
        scenario_data = df[df['Scenario_ID'] == scenario]

        # Extract the "Static" group data
        static_data = scenario_data[scenario_data['Group_ID'] == "Static"]
        if not static_data.empty:
            static_throughput = static_data.iloc[0]['Throughput']
            static_time = static_data.iloc[0]['Average_Travel_Time']
        else:
            static_throughput = None
            static_time = None

        # Filter out "Static" group to find the best alternative
        non_static_data = scenario_data[scenario_data['Group_ID'] != "Static"]

        # Best throughput excluding "Static"
        if not non_static_data.empty and non_static_data['Throughput'].max() > 0:
            best_throughput_group = non_static_data.loc[non_static_data['Throughput'].idxmax()]
        else:
            best_throughput_group = None

        # Best travel time excluding "Static"
        if not non_static_data.empty and non_static_data['Average_Travel_Time'].min() > 0:
            best_time_group = non_static_data.loc[non_static_data['Average_Travel_Time'].idxmin()]
        else:
            best_time_group = None

        # Store results for throughput
        final_result_throughput.append({
            'Video_Index': video_index,
            'Scenario_ID': scenario,
            'Scenario': static_data.iloc[0]['Scenario_Description'] if not static_data.empty else None,
            'Group_ID': 'Static',
            'Throughput': static_throughput,
            'Average_Travel_time': static_time
            # 'Scenario_Time_Description': static_data.iloc[0]['Scenario_Time_Description'] if not static_data.empty else None
        })

        if best_throughput_group is not None:
            final_result_throughput.append({
                'Video_Index': video_index,
                'Scenario_ID': scenario,
                'Scenario': best_throughput_group['Scenario_Description'],
                'Group_ID': best_throughput_group['Group_ID'],
                'Throughput': best_throughput_group['Throughput'],
                'Average_Travel_time': best_throughput_group['Average_Travel_Time']
                # 'Scenario_Time_Description': static_data.iloc[0]['Scenario_Time_Description'] if not static_data.empty else None
            })

        # Store results for travel time
        final_result_time.append({
            'Video_Index': video_index,
            'Scenario_ID': scenario,
            'Scenario': static_data.iloc[0]['Scenario_Description'] if not static_data.empty else None,
            'Group_ID': 'Static',
            'Throughput': static_throughput,
            'Average_Travel_Time': static_time,
            # 'Scenario_Time_Description': static_data.iloc[0]['Scenario_Time_Description'] if not static_data.empty else None
        })

        if best_time_group is not None:
            final_result_time.append({
                'Video_Index': video_index,
                'Scenario_ID': scenario,
                'Scenario': best_time_group['Scenario_Description'],
                'Group_ID': best_time_group['Group_ID'],
                'Throughput': best_time_group['Throughput'],
                'Average_Travel_Time': best_time_group['Average_Travel_Time'],
                # 'Scenario_Time_Description': static_data.iloc[0]['Scenario_Time_Description'] if not static_data.empty else None
            })

    # Convert the results to DataFrames
    final_df_throughput = pd.DataFrame(final_result_throughput)
    final_df_time = pd.DataFrame(final_result_time)

    # Return the DataFrames
    return final_df_throughput, final_df_time

throughput_final = []
time_final = []


for i in range(2):
    file_name = "Bellevue_150th_Newport__2017-09-11_17-08-32_6Min_Data_Upscaled_New"
    path = f"files/Bellevue_150th_Newport__2017-09-11_17-08-32/new/full_6/{file_name}_{i}.csv"
        

    # Get the best scenario, throughput and time for each cropped video
    best_throughout, best_time = analyze_traffic_scenarios(path, i + 1)

    throughput_final.append(best_throughout)
    time_final.append(best_time)

    final_df_throughput = pd.concat(throughput_final, ignore_index=True)
    final_df_time = pd.concat(time_final, ignore_index=True)

    filtered_throughput = final_df_throughput[final_df_throughput['Group_ID'] != 'Static']
    filtered_time = final_df_time[final_df_time['Group_ID'] != 'Static']

    sum_throughput = filtered_throughput['Throughput'].sum()

    avg_time = filtered_time['Average_Travel_Time'].sum() / 12

    # Print the results
    print("Sum of Throughput (excluding Static):", sum_throughput)
    print("Average Time (excluding Static):", avg_time)

    # Save to a CSV file
    folder_path = 'best_scenarios/Bellevue_150th_Newport__2017-09-11_17-08-32/new/full_6'

    final_df_throughput.to_csv(f'{folder_path}/best_throughput_{file_name}.csv', index=False)
    final_df_time.to_csv(f'{folder_path}/best_time_{file_name}.csv', index=False)

    # Save sum and avg to a separate file
    summary_data = pd.DataFrame({'Metric': ['Sum Throughput', 'Avg Time'], 'Value': [sum_throughput, avg_time]})
    summary_data.to_csv(f'{folder_path}/summary_metrics_{file_name}.csv', index=False)

    print("File saved successfully.")