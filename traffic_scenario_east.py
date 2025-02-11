import traci
from traci import simulation
import json
import os
import time
import csv

sumo_binary = "sumo-gui"
sumo_config_file = r"/Users/ull/Documents/GRA/TRAFFIC-Project/SUMO Files/Bellevue_116th_NE12th__2017-09-11_14-08-35_East_West/sumo_config.sumocfg"

file_name = "Bellevue_116th_NE12th__2017-09-11_14-08-35"

# scenarios = [
#     {"green": 60, "yellow": 0, "red": 0},  # Full Green for 1 minute
#     {"green": 50, "yellow": 5, "red": 5},  # Green for 50s, Yellow for 5s, Red for 5s
#     {"green": 40, "yellow": 10, "red": 10},  # Green for 40s, Yellow for 10s, Red for 10s
#     {"green": 45, "yellow": 5, "red": 10},  # Green for 45s, Yellow for 5s, Red for 10s
#     {"green": 30, "yellow": 15, "red": 15},  # Green for 30s, Yellow for 15s, Red for 15s
#     {"green": 35, "yellow": 10, "red": 15},  # Green for 35s, Yellow for 10s, Red for 15s
#     {"green": 25, "yellow": 15, "red": 20},  # Green for 25s, Yellow for 15s, Red for 20s
#     {"green": 40, "yellow": 10, "red": 10},  # Green for 40s, Yellow for 10s, Red for 10s
# ]

# scenario_groups = [
#     ("Group 1", [
#     {"green": 60, "yellow": 0, "red": 0},  # Full Green for 1 minute
#     {"green": 50, "yellow": 5, "red": 5},  # Green for 50s, Yellow for 5s, Red for 5s
#     {"green": 40, "yellow": 10, "red": 10},  # Green for 40s, Yellow for 10s, Red for 10s
#     {"green": 45, "yellow": 5, "red": 10},  # Green for 45s, Yellow for 5s, Red for 10s
#     {"green": 30, "yellow": 15, "red": 15},  # Green for 30s, Yellow for 15s, Red for 15s
#     {"green": 35, "yellow": 10, "red": 15},  # Green for 35s, Yellow for 10s, Red for 15s
#     {"green": 25, "yellow": 15, "red": 20},  # Green for 25s, Yellow for 15s, Red for 20s
#     {"green": 40, "yellow": 10, "red": 10},  # Green for 40s, Yellow for 10s, Red for 10s
#     {"green": 60, "yellow": 0, "red": 0},  # Full Green for 1 minute
#     {"green": 50, "yellow": 5, "red": 5},  # Green for 50s, Yellow for 5s, Red for 5s
#     {"green": 40, "yellow": 10, "red": 10},  # Green for 40s, Yellow for 10s, Red for 10s
#     {"green": 45, "yellow": 5, "red": 10},  # Green for 45s, Yellow for 5s, Red for 10s
#     {"green": 30, "yellow": 15, "red": 15},  # Green for 30s, Yellow for 15s, Red for 15s
#     {"green": 35, "yellow": 10, "red": 15},  # Green for 35s, Yellow for 10s, Red for 15s
#     {"green": 25, "yellow": 15, "red": 20},  # Green for 25s, Yellow for 15s, Red for 20s
#     {"green": 40, "yellow": 10, "red": 10},  # Green for 
# ]),
#     ("Group 2", [
#     {"green": 20, "yellow": 0, "red": 30},  # Full Green for 1 minute
#     {"green": 50, "yellow": 5, "red": 5},  # Green for 50s, Yellow for 5s, Red for 5s
#     {"green": 10, "yellow": 0, "red": 40},  # Full Green for 1 minute
#     {"green": 40, "yellow": 7, "red": 5},  # Green for 50s, Yellow for 5s, Red for 5s
#     {"green": 20, "yellow": 0, "red": 0},  # Full Green for 1 minute
#     {"green": 50, "yellow": 5, "red": 5},  # Green for 50s, Yellow for 5s, Red for 5s
#     {"green": 20, "yellow": 0, "red": 0},  # Full Green for 1 minute
#     {"green": 50, "yellow": 5, "red": 5},  # Green for 50s, Yellow for 5s, Red for 5s
#     {"green": 20, "yellow": 0, "red": 0},  # Full Green for 1 minute
#     {"green": 50, "yellow": 5, "red": 5},  # Green for 50s, Yellow for 5s, Red for 5s
#     {"green": 20, "yellow": 0, "red": 0},  # Full Green for 1 minute
#     {"green": 50, "yellow": 5, "red": 5},  # Green for 50s, Yellow for 5s, Red for 5s
# #     {"green": 40, "yellow": 10, "red": 10},  # Green for 40s, Yellow for 10s, Red for 10s
# #     {"green": 45, "yellow": 5, "red": 10},  # Green for 45s, Yellow for 5s, Red for 10s
# #     {"green": 30, "yellow": 15, "red": 15},  # Green for 30s, Yellow for 15s, Red for 15s
# #     {"green": 35, "yellow": 10, "red": 15},  # Green for 35s, Yellow for 10s, Red for 15s
# #     {"green": 25, "yellow": 15, "red": 20},  # Green for 25s, Yellow for 15s, Red for 20s
# #     {"green": 40, "yellow": 10, "red": 10},  # Green for 40s, Yellow for 10s, Red for 10s
# #     {"green": 60, "yellow": 0, "red": 0},  # Full Green for 1 minute
# #     {"green": 50, "yellow": 5, "red": 5},  # Green for 50s, Yellow for 5s, Red for 5s
# #     {"green": 40, "yellow": 10, "red": 10},  # Green for 40s, Yellow for 10s, Red for 10s
# #     {"green": 45, "yellow": 5, "red": 10},  # Green for 45s, Yellow for 5s, Red for 10s
# #     {"green": 30, "yellow": 15, "red": 15},  # Green for 30s, Yellow for 15s, Red for 15s
# #     {"green": 35, "yellow": 10, "red": 15},  # Green for 35s, Yellow for 10s, Red for 15s
# #     {"green": 25, "yellow": 15, "red": 20},  # Green for 25s, Yellow for 15s, Red for 20s
# #     {"green": 40, "yellow": 10, "red": 10},  # Green for 
# ]
# )
# ]

# scenario_groups = [
#     ("Group_1", [{"green": 60, "yellow": 0, "red": 0}, {"green": 50, "yellow": 5, "red": 5}]),
#     ("Group_2", [{"green": 40, "yellow": 10, "red": 10}, {"green": 45, "yellow": 5, "red": 10}]),
# ]


scenario_groups = [
    ("Group 1", [
        {"green": 30, "yellow": 10, "red": 20},
        {"green": 35, "yellow": 5, "red": 20},
        {"green": 40, "yellow": 5, "red": 15},
        {"green": 45, "yellow": 10, "red": 5},
        {"green": 25, "yellow": 15, "red": 20},
        {"green": 50, "yellow": 5, "red": 5},
        {"green": 20, "yellow": 10, "red": 30},
        {"green": 33, "yellow": 12, "red": 15},
        {"green": 28, "yellow": 17, "red": 15},
        {"green": 37, "yellow": 8, "red": 15}
    ]),
    
    ("Group 2", [
        {"green": 20, "yellow": 15, "red": 25},
        {"green": 25, "yellow": 10, "red": 25},
        {"green": 30, "yellow": 10, "red": 20},
        {"green": 35, "yellow": 8, "red": 17},
        {"green": 40, "yellow": 5, "red": 15},
        {"green": 45, "yellow": 5, "red": 10},
        {"green": 50, "yellow": 5, "red": 5},
        {"green": 22, "yellow": 18, "red": 20},
        {"green": 27, "yellow": 13, "red": 20},
        {"green": 33, "yellow": 7, "red": 20}
    ]),

    ("Group 3", [
        {"green": 15, "yellow": 10, "red": 35},
        {"green": 20, "yellow": 10, "red": 30},
        {"green": 25, "yellow": 15, "red": 20},
        {"green": 30, "yellow": 10, "red": 20},
        {"green": 35, "yellow": 5, "red": 20},
        {"green": 40, "yellow": 5, "red": 15},
        {"green": 45, "yellow": 10, "red": 5},
        {"green": 50, "yellow": 5, "red": 5},
        {"green": 28, "yellow": 17, "red": 15},
        {"green": 32, "yellow": 12, "red": 16}
    ]),

    ("Group 4", [
        {"green": 25, "yellow": 15, "red": 20},
        {"green": 30, "yellow": 10, "red": 20},
        {"green": 35, "yellow": 10, "red": 15},
        {"green": 40, "yellow": 5, "red": 15},
        {"green": 45, "yellow": 5, "red": 10},
        {"green": 50, "yellow": 5, "red": 5},
        {"green": 20, "yellow": 15, "red": 25},
        {"green": 28, "yellow": 10, "red": 22},
        {"green": 32, "yellow": 12, "red": 16},
        {"green": 37, "yellow": 8, "red": 15}
    ]),

    ("Group 5", [
        {"green": 22, "yellow": 18, "red": 20},
        {"green": 25, "yellow": 15, "red": 20},
        {"green": 30, "yellow": 10, "red": 20},
        {"green": 35, "yellow": 10, "red": 15},
        {"green": 40, "yellow": 5, "red": 15},
        {"green": 45, "yellow": 5, "red": 10},
        {"green": 50, "yellow": 5, "red": 5},
        {"green": 28, "yellow": 17, "red": 15},
        {"green": 32, "yellow": 12, "red": 16},
        {"green": 37, "yellow": 8, "red": 15}
    ]),

    ("Group 6", [
        {"green": 20, "yellow": 20, "red": 20},
        {"green": 25, "yellow": 15, "red": 20},
        {"green": 30, "yellow": 10, "red": 20},
        {"green": 35, "yellow": 5, "red": 20},
        {"green": 40, "yellow": 5, "red": 15},
        {"green": 45, "yellow": 5, "red": 10},
        {"green": 50, "yellow": 5, "red": 5},
        {"green": 28, "yellow": 17, "red": 15},
        {"green": 32, "yellow": 12, "red": 16},
        {"green": 37, "yellow": 8, "red": 15}
    ]),

    ("Group 7", [
        {"green": 15, "yellow": 15, "red": 30},
        {"green": 20, "yellow": 10, "red": 30},
        {"green": 25, "yellow": 15, "red": 20},
        {"green": 30, "yellow": 10, "red": 20},
        {"green": 35, "yellow": 10, "red": 15},
        {"green": 40, "yellow": 5, "red": 15},
        {"green": 45, "yellow": 5, "red": 10},
        {"green": 50, "yellow": 5, "red": 5},
        {"green": 28, "yellow": 17, "red": 15},
        {"green": 33, "yellow": 7, "red": 20}
    ])
]




total_vehicle_from_west_to_center = set()
total_vehicle_from_center_to_west = set()

to_east = {}
to_west = {}

green_light_vehicle_counts = {}  
current_green_count_WTOE = 0  
current_green_count_ETOW = 0
previous_phase = -1 
count = 0

vehiclesWestToEast = set()
vehiclesEastToWest = set()

vehiclesWestToEastAll = set()
vehiclesEastToWestAll = set()

vehicle_entry_times = {}
vehicle_exit_times = {}


vehicle_data = {}
scenario_stats = {}

def set_traffic_lights(scenario):
    junction_ids = traci.trafficlight.getIDList()
    for junction_id in junction_ids:
        traci.trafficlight.setPhase(junction_id, 0)  # Set to Green
        traci.trafficlight.setPhaseDuration(junction_id, scenario["green"])
        traci.simulationStep()

        traci.trafficlight.setPhase(junction_id, 1)  # Set to Yellow
        traci.trafficlight.setPhaseDuration(junction_id, scenario["yellow"])
        traci.simulationStep()

        traci.trafficlight.setPhase(junction_id, 2)  # Set to Red
        traci.trafficlight.setPhaseDuration(junction_id, scenario["red"])
        traci.simulationStep()


def run_scenario_with_dynamic_lights(junction_id, total_simulation_steps, phase_durations, change_interval):
    """
    Run the simulation with dynamic phase changes at each interval.
    
    :param junction_id: The ID of the traffic light junction.
    :param total_simulation_steps: The total simulation steps to run.
    :param phase_durations: List of tuples [(green_duration, yellow_duration, red_duration), ...]
    :param change_interval: How often to change the traffic light phases (in steps).
    """
    traci.start([sumo_binary, "-c", sumo_config_file])
    
    current_step = 0
    interval_index = 0  # Start with the first phase configuration
    total_intervals = len(phase_durations)
    
    while current_step < total_simulation_steps:
        # Check if it's time to change the traffic light phases
        if current_step % change_interval == 0:
            # Get current phase duration for this interval
            current_scenario = phase_durations[interval_index]
            # print(f"Current Scenario: {current_scenario}")
            # print(f"Current Index: ", {interval_index})
            
            # Set the traffic light phases
            junction_ids = traci.trafficlight.getIDList()
            for junction_id in junction_ids:
                set_traffic_lights(current_scenario)
            
            # Move to the next interval in phase_durations
            interval_index = (interval_index + 1) % total_intervals  # Loop through the phases
            
            
        # Step the simulation
        traci.simulationStep()
        traffic_flow = analyze_traffic(current_step, interval_index - 1)

    
        current_step += 1
    
    traci.close()
    return traffic_flow

def analyze_traffic(step, interval_index):

    line_1 = 5
    line_2 = 185

    
    global current_green_count_WTOE, current_green_count_ETOW, previous_phase, vehiclesWestToEast, vehiclesEastToWest, green_light_vehicle_counts
    junction_ids = traci.trafficlight.getIDList() 
    global to_east, to_west

    vehicle_ids = traci.vehicle.getIDList()

    for vehicle_id in vehicle_ids:
        vehicle_position = traci.vehicle.getPosition(vehicle_id)
        lane_id = traci.vehicle.getLaneID(vehicle_id)
        vehicle_route = traci.vehicle.getRouteID(vehicle_id)
        speed = traci.vehicle.getSpeed(vehicle_id)

        # TODO: Change for other way
        if vehicle_id not in to_east and (lane_id == "west_to_center_0" or lane_id == "west_to_center_1"):
            to_east[vehicle_id] = {"start": step}
        if vehicle_id in to_east:
            if vehicle_position[0] >= line_2 and (lane_id == "center_to_east_0" or lane_id == "center_to_east_1"):
                to_east[vehicle_id]["end"] = step
                to_east[vehicle_id]["traffic_scenario"] = interval_index

        if  vehicle_id not in to_west and (lane_id == "east_to_center_0" or lane_id == "east_to_center_1"):
            to_west[vehicle_id] = {"start": step}
        if vehicle_id in to_west:
            if  vehicle_position[0] <= line_1 and (lane_id == "center_to_west_0" or lane_id == "center_to_west_1"):
                to_west[vehicle_id]["end"] = step
                to_west[vehicle_id]["traffic_scenario"] = interval_index


        # if lane_id == "west_to_center_0":
        #     print(f"Vehicle {vehicle_id} lane {lane_id}")
        #     total_vehicle_from_west_to_center.add(vehicle_id)
        #     print()
        # elif lane_id == "east_to_center_0":
        #     print(f"Vehicle {vehicle_id} lane {lane_id}")
        #     total_vehicle_from_center_to_west.add(vehicle_id)

    # print("To east: ", to_east)

    for junction_id in junction_ids:
        current_phase = traci.trafficlight.getPhase(junction_id)
        if current_phase == 0 and previous_phase != 0:  
            current_green_count_WTOE = 0
            current_green_count_ETOW = 0

        if current_phase == 0:
            # outgoing_edges = traci.junction.getOutgoingEdges(junction_id)
            # for edge_id in outgoing_edges:
            #     # TODO: 
            #     if edge_id == "center_to_west":
            #         # VehicleIds that passed through the south to north 
            #         vehicleIds = traci.edge.getLastStepVehicleIDs(edge_id)
            #         for i in range(len(vehicleIds)):
            #             if vehicle_ids[i] not in vehiclesEastToWestAll:
            #                 vehiclesEastToWest.add(vehicleIds[i])
            #     # TODO:
            #     elif edge_id == "center_to_east":
            #         # VehicleIds that passed through the south to north 
            #         vehicleIds = traci.edge.getLastStepVehicleIDs(edge_id)
            #         print(f"Veh ids..", vehicle_ids)

            #         for i in range(len(vehicleIds)):
            #             if vehicle_ids[i] not in vehiclesWestToEastAll:
            #                 vehiclesWestToEast.add(vehicleIds[i])
            #         print("All", vehiclesWestToEast)
           
            vehicle_ids = traci.vehicle.getIDList()
            for vehicle_id in vehicle_ids:
                lane_id = traci.vehicle.getLaneID(vehicle_id)
                if lane_id == "center_to_east_0" or lane_id == "center_to_east_1":
                    if vehicle_id not in vehiclesWestToEastAll:
                        vehiclesWestToEastAll.add(vehicle_id)
                        vehiclesWestToEast.add(vehicle_id)
                if lane_id == "center_to_west_0" or lane_id == "center_to_west_1":
                    if vehicle_id not in vehiclesEastToWestAll:
                        vehiclesEastToWestAll.add(vehicle_id)
                        vehiclesEastToWest.add(vehicle_id)

            current_green_count_WTOE = len(vehiclesWestToEast)
            current_green_count_ETOW = len(vehiclesEastToWest)
            # print(f"Junction {junction_id} - Green light: {current_green_count_WTOE} vehicles passed at step {step} North to South {vehiclesWestToEast}")
            # print(f"Junction {junction_id} - Green light: {current_green_count_ETOW} vehicles passed at step {step} South to North {vehiclesEastToWest}")

        if current_phase != 0 and previous_phase == 0:  
            count_WTOE = current_green_count_WTOE
            count_ETOW = current_green_count_ETOW
            print(f"Total vehicles passed from West to East: {count_WTOE}, Interval index: {interval_index}")
            print(f"Total vehicles passed from East to West: {count_ETOW}, Interval Index: {interval_index}")

            
            count_WTOE = 0
            count_ETOW = 0
            vehiclesWestToEast = set()
            vehiclesEastToWest = set()

            # {["west_to_east": 10, "east_to_west": 20], ["west_to_east": 10, "east_to_west": 20]}
            green_light_vehicle_counts[interval_index] = {"west_to_east": current_green_count_WTOE, "east_to_west": current_green_count_ETOW}
            

        # Update previous_phase for the next iteration
        previous_phase = current_phase

        return green_light_vehicle_counts
    
def save_avg_and_throughput_to_csv(traffic_flow_data, to_west, to_east, scenarios, group_id):
    global scenario_stats
    vehicle_data = {**to_west, **to_east}

    for scenario_id, scenario in enumerate(scenarios):
        # print(f"Scenario ID:", scenario_id)
        vehicles_in_scenario = []

        for vehicle_data in to_west.values():
            if "traffic_scenario" in vehicle_data and "end" in vehicle_data: 
                if vehicle_data['traffic_scenario'] == scenario_id:
                    vehicles_in_scenario.append(vehicle_data)
        for vehicle_data in to_east.values():
            if "traffic_scenario" in vehicle_data and "end" in vehicle_data: 
                if vehicle_data['traffic_scenario'] == scenario_id:
                    vehicles_in_scenario.append(vehicle_data)

        
        total_time = 0
        for vehicle in vehicles_in_scenario:
            total_time += vehicle['end'] - vehicle['start']
        
        average_time = total_time / len(vehicles_in_scenario) if vehicles_in_scenario else 0
        
        # print("Traffic Flow Data: ", traffic_flow_data)
        throughput = 0
        for x in traffic_flow_data:
            if x == scenario_id:
                throughput += traffic_flow_data[x]["west_to_east"]
                throughput += traffic_flow_data[x]["east_to_west"]
        
        # print("Throughpout", throughput)
        # print("Avg time", average_time)
        # Store the data
        scenario_stats[f"{scenario_id}+{group_id}"] = {
            'average_time': average_time,
            'throughput': throughput,
            'scenario_description': scenario,
            'group_id': group_id,
            'scenario_id': scenario_id
        }

        # print(f"Scenarios", scenario_stats)
#  with open('scenario_stats.csv', mode='w', newline='') as file:
#         writer = csv.writer(file)
#         writer.writerow(['Scenario_ID', 'Scenario_Description', 'Average_Travel_Time', 'Throughput'])
        
#         for scenario, stats in scenario_stats.items():
#             writer.writerow([scenario, stats['scenario_description'], stats['average_time'], stats['throughput']])

#     print("Saved average time and throughput to 'scenario_stats.csv'")


def run_all_scenarios(scenario_groups):
    global vehiclesEastToWestAll, vehiclesWestToEastAll
    total_simulation_steps = 600  # e.g., run for 600 steps (10 minutes)
    change_interval = 60 

    for group_id, scenario_group in enumerate(scenario_groups):
        group_id = scenario_group[0]
        scenario_group =  scenario_group[1]
        scenario_results = {}
        # Run the simulation with dynamic phase changes
        traffic_flow = run_scenario_with_dynamic_lights("center", total_simulation_steps, scenario_group, change_interval)

        save_avg_and_throughput_to_csv(traffic_flow, to_west, to_east, scenario_group, group_id)
        vehiclesEastToWestAll = set()
        vehiclesWestToEastAll = set()
        # print(scenario_group)

if __name__ == "__main__":
    total_simulation_steps = 600  # e.g., run for 600 steps (10 minutes)
    change_interval = 60  # Change the traffic light phases every 50 steps

    run_all_scenarios(scenario_groups)

    with open(f"files/east/{file_name}.csv", mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Scenario_ID', 'Group_ID', 'Scenario_Description', 'Average_Travel_Time', 'Throughput'])
        
        for scenario, stats in scenario_stats.items():
            writer.writerow([stats['scenario_id'], stats['group_id'], stats['scenario_description'], stats['average_time'], stats['throughput']])

    print("Saved average time and throughput to 'scenario_stats.csv'")
    
    # Run the simulation with dynamic phase changes
    # traffic_flow = run_scenario_with_dynamic_lights("center", total_simulation_steps, scenarios, change_interval)

    # save_avg_and_throughput_to_csv(traffic_flow, up, to_east)