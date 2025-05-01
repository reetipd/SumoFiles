import pandas as pd
import os
import argparse

parser = argparse.ArgumentParser(description='Process throughput data with configurable file parameters')
parser.add_argument('--folder_path', type=str, help='Directory path containing the CSV files')
parser.add_argument('--file_name', type=str, help='Base name of the CSV files (without _X.csv)')
parser.add_argument('--num_files', type=int, help='Number of files to process')
args = parser.parse_args()

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

# Get command line arguments 
folder_path = args.folder_path
file_name = args.file_name 
num_files = args.num_files

print(f"Processing {num_files} intervals with file name {file_name} at path {folder_path}")

# Process throughput
max_throughput, max_group_id, avg_travel_time = 0, None, 0
for i in range(num_files):
    path = os.path.join(folder_path, f"{file_name}_{i}.csv")
    print(f"Processing file: {path}")
    max_throughput, max_group_id, avg_travel_time = process_throughput(
        path, i, max_group_id, max_throughput, avg_travel_time
    )
    print(f"Interval {i}: Max throughput: {max_throughput}, Current group: {max_group_id}")

# Calculate final average travel time
final_avg_time = avg_travel_time / num_files
print(f"Final Results:")
print(f"Maximum Throughput: {max_throughput}")
print(f"Best Group ID: {max_group_id}")
print(f"Average Travel Time: {final_avg_time}")
