import traci
from traci import simulation
import json
import os
import cv2
import time
import csv


import prepare_csv
sumo_binary = "sumo-gui" 
# sumo_config_file = r"C:\Users\c00563648\OneDrive - University of Louisiana at Lafayette\Documents\GRA\Traffic\Sumo-Files\SumoFiles\Bellevue_116th_NE12th__2017-09-11_07-08-32\sumo_files\sumo_config.sumocfg"
# sumo_config_file = r"/Users/ull/Documents/GRA/TRAFFIC-Project/SUMO Files/sumo_files/sumo_config.sumocfg"
sumo_config_file = r"/Users/ull/Documents/GRA/TRAFFIC-Project/SUMO Files/Bellevue_116th_NE12th__2017-09-11_07-08-32/sumo_files/sumo_config.sumocfg"

green_light_vehicle_counts = {}  
current_green_count_NTOS = 0  
current_green_count_STON = 0
previous_phase = -1 
count = 0

vehiclesNorthToSouth = set()
vehiclesSouthToNorth = set()

vehicle_entry_times = {}
vehicle_exit_times = {}

vehicle_data = {}

def start_simulation():
    traci.start([sumo_binary, "-c", sumo_config_file])  

    if not os.path.exists("sumo_steps"):
        os.makedirs("sumo_steps")

    step = 0
    max_steps = 350  #
    while step < max_steps:
        traci.simulationStep() 
        traffic_flow = analyze_traffic(step)

        # screenshot_path = os.path.join("sumo_steps", f"step_{step:04d}.png")
        step += 1
        # traci.gui.screenshot("View #0", screenshot_path)


    traci.close()  

    return traffic_flow

down = {}
up = {}
def analyze_traffic(step):
    global current_green_count_NTOS, current_green_count_STON, previous_phase, vehiclesNorthToSouth, vehiclesSouthToNorth, green_light_vehicle_counts
    junction_ids = traci.trafficlight.getIDList() 
    global down, up

    vehicle_ids = traci.vehicle.getIDList()

    line_1 = 160
    line_2 = 90

    for vehicle_id in vehicle_ids:
        vehicle_position = traci.vehicle.getPosition(vehicle_id)
        lane_id = traci.vehicle.getLaneID(vehicle_id)
        vehicle_route = traci.vehicle.getRouteID(vehicle_id)
        speed = traci.vehicle.getSpeed(vehicle_id)

        vehicle_data.setdefault(vehicle_id, []).append((step, vehicle_position[0], vehicle_position[1], vehicle_route, speed)) 

        # vehicle_data[vehicle_data].append({
        #     "step": step,
        #     "x_position": vehicle_position[0],
        #     "y_position": vehicle_position[1],
        #     "route": vehicle_route,
        # })

        # print(f"Vehicle Data..", vehicle_data)

        if vehicle_position[1] <= line_1 and vehicle_id not in down and (lane_id == "north_to_center_0" or lane_id == "north_to_center_1"):
            down[vehicle_id] = {"start": step}
        if vehicle_id in down:
            if vehicle_position[1] <= line_2 and (lane_id == "center_to_south_0" or lane_id == "center_to_south_1"):
                down[vehicle_id]["end"] = step

        if vehicle_position[1] >= line_2 and vehicle_id not in up and (lane_id == "south_to_center_0" or lane_id == "south_to_center_1"):
            up[vehicle_id] = {"start": step}
        if vehicle_id in up:
            if vehicle_position[1] >= line_1 and (lane_id == "center_to_north_0" or lane_id == "center_to_north_1"):
                up[vehicle_id]["end"] = step


    # Track entry time for new vehicles
    # for vehicle_id in vehicle_ids:
    #     if vehicle_id not in vehicle_entry_times:
    #         # New vehicle, log its entry time
    #         vehicle_entry_times[vehicle_id] = step
    #         # print(f"Vehicle {vehicle_id} entered at time {step}.")

    # vehicles_to_remove = []  

    # for vehicle_id in list(vehicle_entry_times.keys()):  
    #     if vehicle_id not in vehicle_ids:
    #         exit_time = step
    #         entry_time = vehicle_entry_times.pop(vehicle_id)
    #         travel_time = exit_time - entry_time
    #         # print(f"Vehicle {vehicle_id} exited at time {exit_time}. Travel time: {travel_time} seconds.")
    #         vehicles_to_remove.append(vehicle_id)

    # for vehicle_id in vehicles_to_remove:
    #     if vehicle_id in vehicle_entry_times:
    #         del vehicle_entry_times[vehicle_id]

    for junction_id in junction_ids:
        current_phase = traci.trafficlight.getPhase(junction_id)
        if current_phase == 0 and previous_phase != 0:  
            current_green_count_NTOS = 0
            current_green_count_STON = 0

        if current_phase == 0:
            outgoing_edges = traci.junction.getOutgoingEdges(junction_id)
            for edge_id in outgoing_edges:
                if edge_id == "center_to_north":
                    # VehicleIds that passed through the south to north 
                    vehicleIds = traci.edge.getLastStepVehicleIDs(edge_id)
                    for i in range(len(vehicleIds)):
                        vehiclesSouthToNorth.add(vehicleIds[i])
                elif edge_id == "center_to_south" or edge_id == ":center_0":
                    # VehicleIds that passed through the south to north 
                    vehicleIds = traci.edge.getLastStepVehicleIDs(edge_id)
                    for i in range(len(vehicleIds)):
                        vehiclesNorthToSouth.add(vehicleIds[i])
           
            current_green_count_NTOS = len(vehiclesNorthToSouth)
            current_green_count_STON = len(vehiclesSouthToNorth)
            # print(f"Junction {junction_id} - Green light: {current_green_count_NTOS} vehicles passed at step {step} North to South {vehiclesNorthToSouth}")
            # print(f"Junction {junction_id} - Green light: {current_green_count_STON} vehicles passed at step {step} South to North {vehiclesSouthToNorth}")

        if current_phase != 0 and previous_phase == 0:  
            count_NTOS = current_green_count_NTOS
            count_STON = current_green_count_STON
            # print(f"Total vehicles passed from North to South: {count_NTOS}")
            # print(f"Total vehicles passed from South to North: {count_STON}")
            count_NTOS = 0
            count_STON = 0
            vehiclesNorthToSouth = set()
            vehiclesSouthToNorth = set()

            # {["north_to_south": 10, "south_to_north": 20], ["north_to_south": 10, "south_to_north": 20]}
            green_light_vehicle_counts[step] = {"north_to_south": current_green_count_NTOS, "south_to_north": current_green_count_STON}
            

        # Update previous_phase for the next iteration
        previous_phase = current_phase

        return green_light_vehicle_counts, vehicle_data
    

def calculate_average_time(up_data, down_data):
    valid_times = []

    # Calculate valid times for up_data
    for vehicle_id, up_item in up_data.items():
        if "start" in up_item and "end" in up_item and up_item["start"] > 0 and up_item["end"] > 0:
            time_in_sec = up_item["end"] - up_item["start"]
            valid_times.append(time_in_sec)

    # Calculate valid times for down_data
    for vehicle_id, down_item in down_data.items():
        if "start" in down_item and "end" in down_item and down_item["start"] > 0 and down_item["end"] > 0:
            time_in_sec = down_item["end"] - down_item["start"]
            # print(f"Time taken for vehicle {vehicle_id} (Down) is {time_in_sec} seconds.")
            valid_times.append(time_in_sec)

    if valid_times:
        average_time = sum(valid_times) / len(valid_times)
        print(f"Average time: {average_time} seconds for {len(valid_times)} vehicles.")
        return average_time
    else:
        return 0.0    


# Run the simulation
if __name__ == "__main__":
    traffic_flow, vehicle_data = start_simulation()
    # prepare_csv.prepare_llm_dataset(vehicle_data)

    # Save the traffic flow data to a JSON file
    with open("traffic_flow.json", "w") as f:
        json.dump(traffic_flow, f, indent=4)


    calculate_average_time(up, down)

    # Save the vehicle entry and exit times to a JSON file  
    with open("vehicle_entry_exit_times.json", "w") as f:
        json.dump({"up": up, "down": down}, f, indent=4)
