import traci
from traci import simulation
import json
import os
import time
import csv
import best_scenarios
import get_best_scenarios
import pandas as pd

sumo_binary = "sumo-gui"
# sumo_config_file = r"/Users/ull/Documents/GRA/TRAFFIC-Project/SUMO Files/Bellevue_116th_NE12th_2017-09-11_14-08-35_Full/sumo_config.sumocfg"
# sumo_config_file = r"/Users/ull/Documents/GRA/TRAFFIC-Project/SUMO Files/Bellevue_116th_NE12th__2017-09-11_08-08-50_Full/sumo_config.sumocfg"

file_name = "Bellevue_116th_NE12th__2017-09-11_08-08-50_Full_Video_"

# scenario_groups = [
#     # ("Static", [
#     #     {"duration": 60, "str": "GGGYYYrrrrGGGYYYrrrr"},  # North-South straight go + left turn
#     # ]),

#     ("Static", [
#         {"duration": 60, "str": "GGYYYYrrrrGGYYYYrrrr"}  # 30s Green, 5s Yellow, 25s Red
#     ])

#     # ("Group 2", [
#     #      {"duration": 60, "str": "rrrrGGGGGGrrrrGGGGGG"},  # All directions left + right
#     # ]),

#     # ("Group 3", [
#     #     {"duration": 60, "str": "GGGYYYrrrrGGGYYYrrrr"},  # North-South straight go + left turn
#     # ]),
# ]

scenario_groups = [
    # ("Static", [
    #     {"duration": 30, "str": "GGGGGrrrrrGGGGGrrrrr", "traffic_light":"Green", "road":"NS"},  # NS Green (30s), EW Red
    #     {"duration": 5,  "str": "YYYYYrrrrrYYYYYrrrrr", "traffic_light":"Yellow", "road":"NS"},  # NS Yellow (5s), EW Red
    #     {"duration": 25, "str": "rrrrrGGGGGrrrrrGGGGG", "traffic_light":"Red", "road":"NS"},  # EW Green (30s), NS Red
    #     {"duration": 5,  "str": "YYYYYrrrrrYYYYYrrrrr", "traffic_light": "Yellow", "road":"NS"}   # EW Yellow (5s), NS Red
    # ]),
    # ("Group1", [
    #     {"duration": 25, "str": "GGGGGrrrrrGGGGGrrrrr", "traffic_light":"Green", "road":"NS"},  # NS Green (30s), EW Red
    #     {"duration": 5,  "str": "YYYYYrrrrrYYYYYrrrrr", "traffic_light":"Yellow", "road":"NS"},  # NS Yellow (5s), EW Red
    #     {"duration": 30, "str": "rrrrrGGGGGrrrrrGGGGG", "traffic_light":"Red", "road":"NS"},  # EW Green (30s), NS Red
    #     {"duration": 5,  "str": "YYYYYrrrrrYYYYYrrrrr", "traffic_light": "Yellow", "road":"NS"}   # EW Yellow (5s), NS Red
    # ])


# # Standard NS & EW Split Timing

    ("Static", [
        {"duration": 30, "str": "GGGGGrrrrrGGGGGrrrrr", "traffic_light": "Green", "road": "NS"},
        {"duration": 5, "str": "YYYYYrrrrrYYYYYrrrrr", "traffic_light": "Yellow", "road": "NS"},
        {"duration": 25, "str": "rrrrrGGGGGrrrrrGGGGG", "traffic_light": "Green", "road": "EW"},
        {"duration": 5, "str": "rrrrrYYYYYrrrrrYYYYY", "traffic_light": "Yellow", "road": "EW"}
    ]),

# #Separate Phases for North and South
    ("Group1", [
    {"duration": 15, "str": "GGGGGrrrrrrrrrrrrrrr", "traffic_light": "Green", "road": "N"},
    {"duration": 5, "str": "YYYYYrrrrrrrrrrrrrrr", "traffic_light": "Yellow", "road": "N"},
    {"duration": 15, "str": "rrrrrGGGGGrrrrrrrrrr", "traffic_light": "Green", "road": "S"},
    {"duration": 5, "str": "rrrrrYYYYYrrrrrrrrrr", "traffic_light": "Yellow", "road": "S"},
    {"duration": 15, "str": "rrrrrrrrrrGGGGGrrrrr", "traffic_light": "Green", "road": "E"},
    {"duration": 5, "str": "rrrrrrrrrrYYYYYrrrrr", "traffic_light": "Yellow", "road": "E"},
    {"duration": 15, "str": "rrrrrrrrrrrrrrrGGGGG", "traffic_light": "Green", "road": "W"},
    {"duration": 5, "str": "rrrrrrrrrrrrrrrYYYYY", "traffic_light": "Yellow", "road": "W"}
     ]),

# # #Dedicated Left Turns

("Group2", [
    {"duration": 10, "str": "GrrrrrrrrrGrrrrrrrrr", "traffic_light": "Left Turn", "road": "NS"},
    {"duration": 20, "str": "GGGGGrrrrrGGGGGrrrrr", "traffic_light": "Green", "road": "NS"},
    {"duration": 5, "str": "YYYYYrrrrrYYYYYrrrrr", "traffic_light": "Yellow", "road": "NS"},
    {"duration": 10, "str": "rrrrrGrrrrrrrrrGrrrr", "traffic_light": "Left Turn", "road": "EW"},
    {"duration": 20, "str": "rrrrrGGGGGrrrrrGGGGG", "traffic_light": "Green", "road": "EW"},
    {"duration": 5, "str": "rrrrrYYYYYrrrrrYYYYY", "traffic_light": "Yellow", "road": "EW"}
]),

# # #Left Turns + Protected Right Turns

# ("Group3", [
#     {"duration": 10, "str": "GrrrrrrrrrGrrrrrrrrr", "traffic_light": "Left Turn", "road": "NS"},
#     {"duration": 20, "str": "GGGGGrrrrrGGGGGrrrrr", "traffic_light": "Green", "road": "NS"},
#     {"duration": 5, "str": "YYYYYrrrrrYYYYYrrrrr", "traffic_light": "Yellow", "road": "NS"},
#     {"duration": 10, "str": "rrrrrGrrrrrrrrrGrrrr", "traffic_light": "Left Turn", "road": "EW"},
#     {"duration": 20, "str": "rrrrrGGGGGrrrrrGGGGG", "traffic_light": "Green", "road": "EW"},
#     {"duration": 5, "str": "rrrrrYYYYYrrrrrYYYYY", "traffic_light": "Yellow", "road": "EW"},
#     {"duration": 10, "str": "rrGGGrrrrrrrGGGrrrrr", "traffic_light": "Protected Right", "road": "All"}
# ]),

# # #More Frequent Light Changes for High Traffic

# ("Group4", [
#     {"duration": 15, "str": "GGGGGrrrrrGGGGGrrrrr", "traffic_light": "Green", "road": "NS"},
#     {"duration": 5, "str": "YYYYYrrrrrYYYYYrrrrr", "traffic_light": "Yellow", "road": "NS"},
#     {"duration": 15, "str": "rrrrrGGGGGrrrrrGGGGG", "traffic_light": "Green", "road": "EW"},
#     {"duration": 5, "str": "rrrrrYYYYYrrrrrYYYYY", "traffic_light": "Yellow", "road": "EW"},
#     {"duration": 10, "str": "Grrrrrrrrrrrrrrrrrrr", "traffic_light": "Left Turn", "road": "N"},
#     {"duration": 10, "str": "rrrrrGrrrrrrrrrrrrrr", "traffic_light": "Left Turn", "road": "S"},
#     {"duration": 10, "str": "rrrrrrrrrGrrrrrrrrrr", "traffic_light": "Left Turn", "road": "E"},
#     {"duration": 10, "str": "rrrrrrrrrrrrrrrGrrrr", "traffic_light": "Left Turn", "road": "W"}
# ]),

# # #Balanced Timing with Left Turns First
# ("Group5", [
#     {"duration": 10, "str": "GrrrrrrrrrGrrrrrrrrr", "traffic_light": "Left Turn", "road": "NS"},
#     {"duration": 20, "str": "GGGGGrrrrrGGGGGrrrrr", "traffic_light": "Green", "road": "NS"},
#     {"duration": 5, "str": "YYYYYrrrrrYYYYYrrrrr", "traffic_light": "Yellow", "road": "NS"},
#     {"duration": 10, "str": "rrrrrGrrrrrrrrrGrrrr", "traffic_light": "Left Turn", "road": "EW"},
#     {"duration": 20, "str": "rrrrrGGGGGrrrrrGGGGG", "traffic_light": "Green", "road": "EW"},
#     {"duration": 5, "str": "rrrrrYYYYYrrrrrYYYYY", "traffic_light": "Yellow", "road": "EW"}
# ]),

# # #Left Turns First, Starting with East-West
# ("Group6", [
#     {"duration": 10, "str": "rrrrrGrrrrrrrrrGrrrr", "traffic_light": "Left Turn", "road": "EW"},
#     {"duration": 20, "str": "rrrrrGGGGGrrrrrGGGGG", "traffic_light": "Green", "road": "EW"},
#     {"duration": 5, "str": "rrrrrYYYYYrrrrrYYYYY", "traffic_light": "Yellow", "road": "EW"},
#     {"duration": 10, "str": "GrrrrrrrrrGrrrrrrrrr", "traffic_light": "Left Turn", "road": "NS"},
#     {"duration": 20, "str": "GGGGGrrrrrGGGGGrrrrr", "traffic_light": "Green", "road": "NS"},
#     {"duration": 5, "str": "YYYYYrrrrrYYYYYrrrrr", "traffic_light": "Yellow", "road": "NS"}
# ])


]

# scenario_groups = [
#     ("Static", [
#         # North-South direction phases
#         {"duration": 15, "str": "GGGGGRRRRRRRRRRRR", "traffic_light": "Green", "road": "N"},  # North Green (15s), South Red
#         {"duration": 5,  "str": "YYYYYRRRRRRRRRRRR", "traffic_light": "Yellow", "road": "N"},  # North Yellow (5s), South Red
#         {"duration": 15, "str": "RRRRRRRRRRRRRRRRR", "traffic_light": "Red", "road": "N"},  # North Red (15s), South Green

#         # East-West direction phases
#         {"duration": 15, "str": "RRRRRRRRRRRRRRRGGGGG", "traffic_light": "Green", "road": "E"},  # East Green (15s), West Red
#         {"duration": 5,  "str": "RRRRRRRRRRRRRRRYYYYY", "traffic_light": "Yellow", "road": "E"},  # East Yellow (5s), West Red
#         {"duration": 15, "str": "RRRRRRRRRRRRRRRRR", "traffic_light": "Red", "road": "E"},  # East Red (15s), West Green
#     ])
# ]



total_vehicle_from_west_to_center = set()
total_vehicle_from_center_to_west = set()

to_east = {}
to_west = {}

vehicle_time_tracking = {}
green_light_vehicle_counts = {}  
current_green_count_WTOE = 0  
current_green_count_ETOW = 0
previous_phase = -1 
count = 0

vehiclesToEast = set()
vehiclesToWest = set()
vehiclesToNorth = set()
vehiclesToSouth = set()

vehiclesToEastAll = set()
vehiclesToWestAll = set()
vehiclesToNorthAll = set()
vehiclesToSouthAll = set()

vehicle_entry_times = {}
vehicle_exit_times = {}


vehicle_data = {}
scenario_stats = {}
remaining_vehicles= {}


def set_traffic_lights(scenarios):
    junction_ids = traci.trafficlight.getIDList()

    for junction_id in junction_ids:
        phases = []
        for scenario in scenarios:
            phase = traci.trafficlight.Phase(scenario["duration"], scenario["str"])
            phases.append(phase)
        
        program = traci.trafficlight.Logic(f"logic_{junction_id}", 0, 0, phases)

        traci.trafficlight.setProgramLogic(junction_id, program)

        traci.simulationStep()



def run_scenario_with_dynamic_lights(junction_id, total_simulation_steps, phase_durations, change_interval, group_id, video_index, inject):
    """
    Run the simulation with dynamic phase changes at each interval.
    
    :param junction_id: The ID of the traffic light junction.
    :param total_simulation_steps: The total simulation steps to run.
    :param phase_durations: List of tuples [(green_duration, yellow_duration, red_duration), ...]
    :param change_interval: How often to change the traffic light phases (in steps).
    """
    print("Video ------------------------------>>>>>>>>>", video_index)
    dynamic_value = f"Video_{video_index}"  # Replace with your dynamic value
    # sumo_config_file = fr"/Users/ull/Documents/GRA/TRAFFIC-Project/SUMO Files/Bellevue_116th_NE12th_2017-09-11_14-08-35_Cropped_Videos/Bellevue_116th_NE12th_2017-09-11_14-08-35_{dynamic_value}/sumo_config.sumocfg"
    sumo_config_file = fr"/Users/ull/Documents/GRA/TRAFFIC-Project/SUMO Files/Bellevue_116th_NE12th__2017-09-11_14-08-35_Cropped/{dynamic_value}/sumo_config.sumocfg"

    traci.start([sumo_binary, "-c", sumo_config_file])
    change = False
    current_step = 0
    interval_index = 0  # Start with the first phase configuration
    total_intervals = len(phase_durations)

    global vehiclesToWest, vehiclesToEast, vehiclesToNorth, vehiclesToSouth, vehicle_time_tracking, remaining_vehicle, green_light_vehicle_counts, vehiclesToEast, vehiclesToNorth, vehiclesToSouth, vehiclesToWest 
    green_light_vehicle_counts = {}
    vehiclesToWestAll = set()
    vehiclesToEastAll = set()
    vehiclesToNorthAll = set()
    vehiclesToSouthAll = set()
    vehiclesToEast = set()
    vehiclesToWest = set()
    vehiclesToNorth = set()
    vehiclesToSouth = set()

    set_traffic_lights(phase_durations)

    if inject:
        inject_remaining_vehicles()
   
    traffic_flow = {}
    veh_time = {}
    idx_count = 0
    while current_step <= change_interval:
        if current_step == change_interval:
            print("Done with 60 seconds ---- Run next scenario ")
            # print("traffic")
            # print(traffic_flow)
            # print("time")
            # print(veh_time)

            print("Getting the vehicle information: ")
            get_vehicle_information()
            # print("Remaining...", remaining_vehicles)
            print("Len -------->>>", len(remaining_vehicles))



            
        traci.simulationStep()
        traffic_flow = get_veh_count(interval_index-1, current_step, idx_count)
        veh_time = get_veh_time(interval_index-1, current_step, idx_count, change, group_id)

        
        
        change = False  
        
        current_step += 1
    print("Returning..")
    
    traci.close()
    return traffic_flow, veh_time

def get_veh_count(interval_index, step, idx_count):
    junction_ids = traci.trafficlight.getIDList()

    for junction_id in junction_ids:
        vehicle_ids = traci.vehicle.getIDList()

        for vehicle_id in vehicle_ids:
            lane_id = traci.vehicle.getLaneID(vehicle_id)

            if lane_id == "center_to_east_0" or lane_id == "center_to_east_1":
                if vehicle_id not in vehiclesToEastAll:
                    vehiclesToEastAll.add(vehicle_id)
                    vehiclesToEast.add(vehicle_id)

            if lane_id == "center_to_west_0" or lane_id == "center_to_west_1":
                if vehicle_id not in vehiclesToWestAll:
                    vehiclesToWestAll.add(vehicle_id)
                    vehiclesToWest.add(vehicle_id)

            if lane_id == "center_to_north_0" or lane_id == "center_to_north_1":
                if vehicle_id not in vehiclesToNorthAll:
                    vehiclesToNorthAll.add(vehicle_id)
                    vehiclesToNorth.add(vehicle_id)

            if lane_id == "center_to_south_0" or lane_id == "center_to_south_1":
                if vehicle_id not in vehiclesToSouthAll:
                    vehiclesToSouthAll.add(vehicle_id)
                    vehiclesToSouth.add(vehicle_id)

        # Get the final vehicle counts after processing the junction
        current_green_count_WTOE = len(vehiclesToEast)
        current_green_count_ETOW = len(vehiclesToWest)
        current_green_count_TON = len(vehiclesToNorth)
        current_green_count_TOS = len(vehiclesToSouth)

        # Print debug info for vehicle counts
        # print(f"Total vehicles passed from West to East: {current_green_count_WTOE}, Interval index: {interval_index}")
        # print(f"Total vehicles passed from East to West: {current_green_count_ETOW}, Interval Index: {interval_index}")

        # Store the vehicle counts for this interval
        green_light_vehicle_counts[idx_count] = {
            "west_to_east": current_green_count_WTOE,
            "east_to_west": current_green_count_ETOW,
            "to_north":current_green_count_TON,
            "to_south":current_green_count_TOS
        }

    # Return the final vehicle count dictionary

    return green_light_vehicle_counts

def get_veh_time(interval_index, step, idx_count, phase_change, group_id):
    global vehicle_time_tracking
    vehicle_ids = traci.vehicle.getIDList()  

    if phase_change:
        if vehicle_time_tracking is not None:
            for veh in list(vehicle_time_tracking.keys()):  
                if veh in vehicle_time_tracking:
                    if "end" not in vehicle_time_tracking[veh] and vehicle_time_tracking[veh]["traffic_scenario"] == idx_count - 1:
                        vehicle_time_tracking[veh]["start"] = step
                        vehicle_time_tracking[veh]["traffic_scenario"] = idx_count


    if vehicle_time_tracking is not None:
        for veh in list(vehicle_time_tracking.keys()):  
            if veh not in vehicle_ids:
                if "captured" not in vehicle_time_tracking[veh]: 
                    vehicle_time_tracking[veh]["end"] = step 
                    vehicle_time_tracking[veh]["captured"] = True
                    # vehicle_time_tracking[veh]["traffic_scenario"]= idx_count

                    # print(f"Vehicle {veh} left at step {step}")

    for vehicle_id in vehicle_ids:
        vehicle_position = traci.vehicle.getPosition(vehicle_id)
        lane_id = traci.vehicle.getLaneID(vehicle_id)

        if vehicle_id not in vehicle_time_tracking:
            if lane_id in ["west_to_center_0", "west_to_center_1", "west_to_center_2", "west_to_center_3",
                            "east_to_center_0", "east_to_center_1", "east_to_center_2",
                            "north_to_center_0", "north_to_center_1", "north_to_center_2",
                            "south_to_center_0", "south_to_center_1", "south_to_center_2"]:
                vehicle_time_tracking[vehicle_id] = {"start": step}
                vehicle_time_tracking[vehicle_id]["traffic_scenario"] = idx_count
                vehicle_time_tracking[vehicle_id]["group_id"] = group_id

                

    return vehicle_time_tracking

def save_avg_and_throughput_to_csv(traffic_flow_data, veh_time, scenarios, group_id):
    # print("Savving data..?")
    global scenario_stats
    scenario_time_stats = {}

    # Loop through each vehicle's data
    for vehicle_data in veh_time.values():
        if "traffic_scenario" in vehicle_data and "end" in vehicle_data:
            traffic_scenario = vehicle_data['traffic_scenario']  
            # print("Traffic Scenario: ", traffic_scenario)
            
            if traffic_scenario not in scenario_time_stats:
                scenario_time_stats[traffic_scenario] = {'total_time': 0, 'vehicle_count': 0}

            if vehicle_data["end"] != 0:            
                scenario_time_stats[traffic_scenario]['total_time'] += vehicle_data['end'] - vehicle_data['start']
                scenario_time_stats[traffic_scenario]['vehicle_count'] += 1

    average_time_per_scenario = {
        scenario: stats['total_time'] / stats['vehicle_count'] if stats['vehicle_count'] > 0 else 0
        for scenario, stats in scenario_time_stats.items()
    }

    throughput = 0
    for x in range(len(traffic_flow_data)):
        scenario_id = x % len(scenarios)
        scenario_description = scenarios

        average_time = average_time_per_scenario.get(x, 0)

        # print("Traffic flow Data", traffic_flow_data)

        # Calculate throughput for the current row
        throughput = traffic_flow_data[x]["west_to_east"]
        throughput += traffic_flow_data[x]["east_to_west"]
        throughput += traffic_flow_data[x]["to_north"]
        throughput += traffic_flow_data[x]["to_south"]

        # Store the data in scenario_stats with scenario details
        scenario_stats[f"{x}+{group_id}"] = {
            'average_time': average_time,  # assuming average_time is available in the flow data
            'throughput': throughput,
            'scenario_description': scenario_description,
            'group_id': group_id,
            'scenario_id': scenario_id,
            'idx_count':x,
            # "scenario_time_description": get_light_durations_from_scenario(scenario_description)
        }


        print("stats", scenario_stats)

        # print(f"{x}+{group_id}")

def get_light_durations_from_scenario(phase):
        
        print("scenario desc", phase)
    
        phase_state = phase["str"]  # Example: "GGGrrrrrrrGGGrrrrrrr"
        phase_duration = phase["duration"]  # Duration of this phase

        # Count occurrences of each light state
        green_count = phase_state.count("G")
        yellow_count = phase_state.count("Y")
        red_count = phase_state.count("r")

        total_lights = len(phase_state)  # Total traffic lights controlled

        # Calculate actual time for each color
        green_time = (green_count / total_lights) * phase_duration
        yellow_time = (yellow_count / total_lights) * phase_duration
        red_time = (red_count / total_lights) * phase_duration

        scenario_desc = f"Green: {green_time:.2f}, Yellow: {yellow_time:.2f}, Red: {red_time:.2f}"

        return scenario_desc


def run_all_scenarios(scenario_groups, video_index):
    inject = False
    global vehiclesToWestAll, vehiclesToEastAll, vehiclesToSouthAll, vehiclesToNorthAll, green_light_vehicle_counts
    total_simulation_steps = 5000  # e.g., run for 600 steps (10 minutes)
    change_interval = 60 

    for group_id, scenario_group in enumerate(scenario_groups):
        green_light_vehicle_counts = {}
        group_id = scenario_group[0]
        scenario_group =  scenario_group[1]
        # Run the simulation with dynamic phase changes
        traffic_flow, veh_time = run_scenario_with_dynamic_lights("center", total_simulation_steps, scenario_group, change_interval, group_id, video_index, inject)
        # print("Vehicle time: ", veh_time)

        save_avg_and_throughput_to_csv(traffic_flow, veh_time, scenario_group, group_id)
        vehiclesToWestAll = set()
        vehiclesToEastAll = set()
        vehiclesToNorthAll = set()
        vehiclesToSouthAll = set()

        inject = True


def get_vehicle_information():
    global remaining_vehicles
    vehicle_ids = traci.vehicle.getIDList()
    for vehicle_id in vehicle_ids:
        speed = traci.vehicle.getSpeed(vehicle_id)
        position = traci.vehicle.getPosition(vehicle_id)
        route_id = traci.vehicle.getRouteID(vehicle_id)
        lane_id = traci.vehicle.getLaneID(vehicle_id)
        edge_id = traci.vehicle.getRoadID(vehicle_id)
        lane_index = traci.vehicle.getLaneIndex(vehicle_id)
        pos = traci.vehicle.getLanePosition(vehicle_id)

        remaining_vehicles[vehicle_id] = {
            "speed": speed,
            "position": position,
            "route_id": route_id,
            "lane_id": lane_id,
            "edge_id": edge_id,
            "lane_index":lane_index,
            "lane_position": pos,
        }

    # return remaining_vehicles


def inject_remaining_vehicles():
    global remaining_vehicles
    for vehicle_id, data in remaining_vehicles.items():
        vehicle_id = f"old_+{vehicle_id}"
        # edge_id, lane, pos = traci.simulation.convertRoadPosition(data["position"][0], data["position"][1])
        # print("vehicle and route", vehicle_id, data["route_id"])
        traci.vehicle.add(vehID=vehicle_id, routeID=data["route_id"], departPos=str(data["lane_position"]), departSpeed=str(data["speed"]))
        traci.vehicle.moveToXY(vehID=vehicle_id, edgeID=data["edge_id"], laneIndex=data["lane_index"], x=data["position"][0], y=data["position"][1])
        # traci.vehicle.setSpeed(vehID=vehicle_id, speed=data["speed"])
    
    remaining_vehicles = {}

if __name__ == "__main__":
    throughput_final = []
    time_final = []
    total_simulation_steps = 600  # e.g., run for 600 steps (10 minutes)
    change_interval = 60  # Change the traffic light phases every 50 steps

    for i in range(1):
        run_all_scenarios(scenario_groups, i + 1)

        path = f"files/full/{file_name}_{i}.csv"
        with open(path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Scenario_ID', 'Group_ID', 'Scenario_Description' ,'Average_Travel_Time', 'Throughput', 'Idx_Count'])
            
            for scenario, stats in scenario_stats.items():
                writer.writerow([stats['scenario_id'], stats['group_id'], stats['scenario_description'],stats['average_time'], stats['throughput'], stats['idx_count']])

        print("Saved average time and throughput to 'scenario_stats.csv'")

        # Get the best scenario
        print("Need to get best scenario here....")

        # Get the best scenario, throughput and time for each cropped video
        best_throughout, best_time = get_best_scenarios.analyze_traffic_scenarios(path, i + 1)

        throughput_final.append(best_throughout)
        time_final.append(best_time)

        # print("Video index..", i)
        # print("Best dataframe:")
        # print(best_throughout)
        # print(best_time)

        # TODO: Append the best throughput and time -> Get the final one with best throughput and time for each time interval video
        # OR can just save different files for diff cropped videos

    final_df_throughput = pd.concat(throughput_final, ignore_index=True)
    final_df_time = pd.concat(time_final, ignore_index=True)

    # Print the properly merged DataFrames
    print(final_df_throughput)
    print(final_df_time)

    # Save to a CSV file
    folder_path = 'best_scenarios/full'  
    final_df_throughput.to_csv(f'{folder_path}/best_throughput_{file_name}.csv', index=False)
    final_df_time.to_csv(f'{folder_path}/best_time_{file_name}.csv', index=False)

    print("File saved successfully.")
        
        

