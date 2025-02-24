import pandas as pd
import os

def process_throughput(file, prev_max_throughput=0, prev_avg_travel_time=0):
    df = pd.read_csv(file)
    
    if 'Throughput' in df.columns and 'Group_ID' in df.columns and 'Average_Travel_Time' in df.columns:
        static_throughput = df[df['Group_ID'] == 'Static']['Throughput'].sum()
        static_avg_travel_time = df[df['Group_ID'] == 'Static']['Average_Travel_Time'].mean()

        return prev_max_throughput + static_throughput, prev_avg_travel_time + static_avg_travel_time
    return prev_max_throughput, prev_avg_travel_time

# Example usage
max_throughput, avg_travel_time = 0, 0
for i in range(3):
    file_name = "Bellevue_116th_NE12th__2017-09-11_14-08-35_4Min_Data_Scaled_2X"
    path = f"files/Bellevue_116th_NE12th__2017-09-11_14-08-35/new/full_4/{file_name}_{i}.csv"
    max_throughput, avg_travel_time = process_throughput(
        path, max_throughput, avg_travel_time
    )

    print("Max throughput", max_throughput, "Avg travel time", avg_travel_time)

total_files = 12
average_travel_time_across_all_files = avg_travel_time / total_files

print(f"Total Static Throughput: {max_throughput}, Static Average Travel Time: {average_travel_time_across_all_files}")
