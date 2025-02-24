import pandas as pd
import os

def process_throughput(file, i, prev_max_group_id=None, prev_max_throughput=0, prev_avg_travel_time=0):
    df = pd.read_csv(file)
    if 'Throughput' in df.columns and 'Group_ID' in df.columns and 'Average_Travel_Time' in df.columns:
        if i == 0:
            # Take only static throughput
            max_throughput = df[df['Group_ID'] == 'Static']['Throughput'].sum()
            avg_travel_time = df[df['Group_ID'] == 'Static']['Average_Travel_Time'].mean()

            df_filtered = df[df['Group_ID'] != 'Static']
            
            # Max throughput and avg travel time for non-static groups
            max_throughput_row = df_filtered.loc[df_filtered['Throughput'].idxmax()]
            avg_travel_time_row = df_filtered.loc[df_filtered['Average_Travel_Time'].idxmin()]

            max_group_id = max_throughput_row['Group_ID']

            print("Mack group id", max_group_id)

        else:
            # Sum with previous max_group_id throughput and average travel time
            df_filtered = df[df['Group_ID'] != 'Static']
            group_throughput = df_filtered[df_filtered['Group_ID'] == prev_max_group_id]['Throughput'].sum()
            group_avg_travel_time = df_filtered[df_filtered['Group_ID'] == prev_max_group_id]['Average_Travel_Time'].mean()
            
            max_throughput = prev_max_throughput + group_throughput
            avg_travel_time = prev_avg_travel_time + group_avg_travel_time

            # Find new maximum throughput group and minimum average travel time group
            max_throughput_row = df_filtered.loc[df_filtered['Throughput'].idxmax()]
            avg_travel_time_row = df_filtered.loc[df_filtered['Average_Travel_Time'].idxmin()]

            max_group_id = max_throughput_row['Group_ID']
            
    return max_throughput, max_group_id, avg_travel_time

# Example usage
max_throughput, max_group_id, avg_travel_time = 0, None, 0
for i in range(3):
    file_name = "Bellevue_116th_NE12th__2017-09-11_14-08-35_4Min_Data_Scaled_2X"
    path = f"files/Bellevue_116th_NE12th__2017-09-11_14-08-35/new/full_4/{file_name}_{i}.csv"
    max_throughput, max_group_id, avg_travel_time = process_throughput(
        path, i, max_group_id, max_throughput, avg_travel_time
    )
print(f"Maximum Throughput: {max_throughput}, Group ID: {max_group_id}, Average Travel Time: {avg_travel_time/12}")
