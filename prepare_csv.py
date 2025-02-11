import pandas as pd
import numpy as np

def prepare_llm_dataset(track_data, output_csv="llm_dataset.csv"):
    """
    Prepare a CSV dataset from vehicle tracking data YOLO for LSTM training.

    :param track_data: Valid vehicle tracking data.
    :param output_csv: Output file name.
    """

    processed_data = []

    for vehicle_id, records in track_data.items():
        df = pd.DataFrame(records, columns=["step", "x_position", "y_position", "vehicle_route" ,"speed"])
        print(df)
        df = df.sort_values(by="step")
        for _, row in df.iterrows():  
            step = row["step"]
            x_position = row["x_position"]
            y_position = row["y_position"]
            vehicle_route = row["vehicle_route"]
            speed = row["speed"]

            # Append processed data
            processed_data.append([vehicle_id, step, x_position, y_position, vehicle_route, speed])
    # Convert to DataFrame and save as CSV
    columns = ["Vehicle ID", "Step", "X_Position", "Y_Position", "Route", "Speed"]
    df_final = pd.DataFrame(processed_data, columns=columns)
    df_final.to_csv(output_csv, index=False)
