import pandas as pd
import os
import argparse

parser = argparse.ArgumentParser(description='Analyze traffic data with configurable file parameters')
parser.add_argument('--folder_path', type=str, help='Directory path containing the CSV files')
parser.add_argument('--file_name', type=str, help='Base name of the CSV files (without _X.csv)')
parser.add_argument('--num_files', type=int, help='Number of intervals to process')
args = parser.parse_args()

def process_throughput(file, prev_max_throughput=0, prev_avg_travel_time=0):
    df = pd.read_csv(file)
    
    if 'Throughput' in df.columns and 'Group_ID' in df.columns and 'Average_Travel_Time' in df.columns:
        static_throughput = df[df['Group_ID'] == 'Static']['Throughput'].sum()
        static_avg_travel_time = df[df['Group_ID'] == 'Static']['Average_Travel_Time'].mean()

        return prev_max_throughput + static_throughput, prev_avg_travel_time + static_avg_travel_time
    return prev_max_throughput, prev_avg_travel_time

# Example usage
max_throughput, avg_travel_time = 0, 0

folder_path = args.folder_path 
file_name = args.file_name 
num_files = args.num_files 

print(f"Processing {num_files} intervals with file name {file_name} at path {folder_path}")

for i in range(num_files):
    path = os.path.join(folder_path, f"{file_name}_{i}.csv")
    max_throughput, avg_travel_time = process_throughput(
        path, max_throughput, avg_travel_time
    )

    print("Max throughput", max_throughput, "Avg travel time", avg_travel_time)

total_files = 12
average_travel_time_across_all_files = avg_travel_time / total_files

print(f"Total Static Throughput: {max_throughput}, Static Average Travel Time: {average_travel_time_across_all_files}")
