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