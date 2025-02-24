import traci
from traci import simulation
import json
import os
import time
import csv

sumo_binary = "sumo-gui"
# sumo_config_file = r"/Users/ull/Documents/GRA/TRAFFIC-Project/SUMO Files/Bellevue_116th_NE12th__2017-09-11_07-08-32/sumo_files/sumo_config.sumocfg"
sumo_config_file = r"/Users/ull/Documents/GRA/TRAFFIC-Project/SUMO Files/Bellevue_116th_NE12th__2017-09-11_14-08-35_North_South/sumo_config.sumocfg"
file_name = "Bellevue_116th_NE12th__2017-09-11_14-08-32_North_South"

scenario_groups = [
    ("Group 1", [
        {"green": 60, "yellow": 0, "red": 0},
        {"green": 3, "yellow": 5, "red": 53},
        {"green": 40, "yellow": 5, "red": 15},
        {"green": 45, "yellow": 10, "red": 5},
        {"green": 25, "yellow": 15, "red": 20},
        {"green": 50, "yellow": 5, "red": 5},
        {"green": 20, "yellow": 10, "red": 30},
        {"green": 33, "yellow": 12, "red": 15},
        {"green": 28, "yellow": 17, "red": 15},
        {"green": 37, "yellow": 8, "red": 15},
        {"green": 28, "yellow": 17, "red": 15},
        {"green": 30, "yellow": 10, "red": 20},
        {"green": 28, "yellow": 17, "red": 15},
        {"green": 37, "yellow": 8, "red": 15},
        {"green": 28, "yellow": 17, "red": 15},
        {"green": 30, "yellow": 10, "red": 20},
    ])
]

total_vehicle_from_north_to_center = set()
total_vehicle_from_center_to_north = set()

down = {}
up = {}

green_light_vehicle_counts = {}  
current_green_count_NTOS = 0  
current_green_count_STON = 0
previous_phase = -1 
count = 0

vehiclesNorthToSouth = set()
vehiclesSouthToNorth = set()

vehiclesNorthToSouthAll = set()
vehiclesSouthToNorthAll = set()

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
    change = False
    
    while current_step < total_simulation_steps:
        # Check if it's time to change the traffic light phases
        if current_step % change_interval == 0:
            # Get current phase duration for this interval
            current_scenario = phase_durations[interval_index]
         
            # Set the traffic light phases
            junction_ids = traci.trafficlight.getIDList()
            for junction_id in junction_ids:
                print("Current scenario:", current_scenario, interval_index)
                set_traffic_lights(current_scenario)
            
            # Move to the next interval in phase_durations
            interval_index = (interval_index + 1) % total_intervals  # Loop through the phases
            change = True
        else: 
            change = False
            
            
        # Step the simulation
        traci.simulationStep()
        traffic_flow = analyze_traffic(current_step, interval_index - 1, change)


    
        current_step += 1
    
    traci.close()
    return traffic_flow

def analyze_traffic(step, interval_index, change):
    idx = interval_index
    # print("Interval index", interval_index)
    line_1 = 120
    line_2 = 20

    
    global current_green_count_NTOS, current_green_count_STON, previous_phase, vehiclesNorthToSouth, vehiclesSouthToNorth, green_light_vehicle_counts, vehiclesSouthToNorthAll, vehiclesNorthToSouthAll
    junction_ids = traci.trafficlight.getIDList() 
    global down, up

    vehicle_ids = traci.vehicle.getIDList()

    for vehicle_id in vehicle_ids:
        vehicle_position = traci.vehicle.getPosition(vehicle_id)
        lane_id = traci.vehicle.getLaneID(vehicle_id)
        vehicle_route = traci.vehicle.getRouteID(vehicle_id)
        speed = traci.vehicle.getSpeed(vehicle_id)

        # TODO: Change for other way
        if change:
            idx = interval_index - 1
        if vehicle_id not in down and (lane_id == "north_to_center_0" or lane_id == "north_to_center_1"):
            down[vehicle_id] = {"start": step}
        if vehicle_id in down:
            if vehicle_position[1] <= line_2 and (lane_id == "center_to_south_0" or lane_id == "center_to_south_1"):
                down[vehicle_id]["end"] = step
                down[vehicle_id]["traffic_scenario"] = idx

        if  vehicle_id not in up and (lane_id == "south_to_center_0" or lane_id == "south_to_center_1"):
            up[vehicle_id] = {"start": step}
        if vehicle_id in up:
            if  vehicle_position[1] >= line_1 and (lane_id == "center_to_north_0" or lane_id == "center_to_north_1"):
                up[vehicle_id]["end"] = step
                up[vehicle_id]["traffic_scenario"] = idx


    for junction_id in junction_ids:
        current_phase = traci.trafficlight.getPhase(junction_id)
        if current_phase == 0 and previous_phase != 0:  
            current_green_count_NTOS = 0
            current_green_count_STON = 0

        if current_phase == 0:
            outgoing_edges = traci.junction.getOutgoingEdges(junction_id)
            for edge_id in outgoing_edges:
                # TODO: 
                if edge_id == "center_to_north":
                    # VehicleIds that passed through the south to north 
                    vehicleIds = traci.edge.getLastStepVehicleIDs(edge_id)
                    for i in range(len(vehicleIds)):
                        if vehicleIds[i] not in vehiclesSouthToNorthAll:
                            vehiclesSouthToNorthAll.add(vehicleIds[i])
                            vehiclesSouthToNorth.add(vehicleIds[i])
                # TODO:
                elif edge_id == "center_to_south" or edge_id == ":center_0":
                    # VehicleIds that passed through the south to north 
                    vehicleIds = traci.edge.getLastStepVehicleIDs(edge_id)
                    for i in range(len(vehicleIds)):
                        
                        if vehicleIds[i] not in vehiclesNorthToSouthAll:
                            vehiclesNorthToSouthAll.add(vehicleIds[i])
                            vehiclesNorthToSouth.add(vehicleIds[i])
           
            current_green_count_NTOS = len(vehiclesNorthToSouth)
            current_green_count_STON = len(vehiclesSouthToNorth)
            # print(f"Junction {junction_id} - Green light: {current_green_count_NTOS} vehicles passed at step {step} North to South {vehiclesNorthToSouth}")
            # print(f"Junction {junction_id} - Green light: {current_green_count_STON} vehicles passed at step {step} South to North {vehiclesSouthToNorth}")

        if current_phase != 0 and previous_phase == 0:  
            if change == True:
                interval_index = interval_index - 1
            count_NTOS = current_green_count_NTOS
            count_STON = current_green_count_STON
            print(f"Total vehicles passed from North to South------------: {count_NTOS}, Interval index: {interval_index}")
            print(f"Total vehicles passed from South to North------------: {count_STON}, Interval Index: {interval_index}")

            
            count_NTOS = 0
            count_STON = 0
            vehiclesNorthToSouth = set()
            vehiclesSouthToNorth = set()

            # {["north_to_south": 10, "south_to_north": 20], ["north_to_south": 10, "south_to_north": 20]}
            green_light_vehicle_counts[interval_index] = {"north_to_south": current_green_count_NTOS, "south_to_north": current_green_count_STON}
            

        # Update previous_phase for the next iteration
        previous_phase = current_phase

        return green_light_vehicle_counts
    
def save_avg_and_throughput_to_csv(traffic_flow_data, up, down, scenarios, group_id):
    global scenario_stats
    vehicle_data = {**up, **down}

    for scenario_id, scenario in enumerate(scenarios):
        vehicles_in_scenario = []

        for vehicle_data in up.values():
            if "traffic_scenario" in vehicle_data and "end" in vehicle_data: 
                if vehicle_data['traffic_scenario'] == scenario_id:
                    vehicles_in_scenario.append(vehicle_data)
        for vehicle_data in down.values():
            if "traffic_scenario" in vehicle_data and "end" in vehicle_data: 
                if vehicle_data['traffic_scenario'] == scenario_id:
                    vehicles_in_scenario.append(vehicle_data)

        
        total_time = 0
        for vehicle in vehicles_in_scenario:
            total_time += vehicle['end'] - vehicle['start']
        
        average_time = total_time / len(vehicles_in_scenario) if vehicles_in_scenario else 0
        
        throughput = 0
        for x in traffic_flow_data:
            if x == scenario_id:
                throughput += traffic_flow_data[x]["north_to_south"]
                throughput += traffic_flow_data[x]["south_to_north"]

        # Store the data
        scenario_stats[f"{scenario_id}+{group_id}"] = {
            'average_time': average_time,
            'throughput': throughput,
            'scenario_description': scenario,
            'group_id': group_id,
            'scenario_id': scenario_id
        }


def run_all_scenarios(scenario_groups):
    total_simulation_steps = 600  # e.g., run for 600 steps (10 minutes)
    change_interval = 60 

    global vehiclesSouthToNorthAll, vehiclesNorthToSouthAll, green_light_vehicle_counts

    for group_id, scenario_group in enumerate(scenario_groups):
        group_id = scenario_group[0]
        scenario_group =  scenario_group[1]
        scenario_results = {}
        # Run the simulation with dynamic phase changes
        traffic_flow = run_scenario_with_dynamic_lights("center", total_simulation_steps, scenario_group, change_interval)

        save_avg_and_throughput_to_csv(traffic_flow, up, down, scenario_group, group_id)
        vehiclesNorthToSouthAll = set()
        vehiclesSouthToNorthAll = set()
        green_light_vehicle_counts = {}

if __name__ == "__main__":
    total_simulation_steps = 600  # e.g., run for 600 steps (10 minutes)
    change_interval = 60  # Change the traffic light phases every 50 steps

    run_all_scenarios(scenario_groups)

    with open(f"files/north/{file_name}.csv", mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Scenario_ID', 'Group_ID', 'Scenario_Description', 'Average_Travel_Time', 'Throughput'])
        
        for scenario, stats in scenario_stats.items():
            writer.writerow([stats['scenario_id'], stats['group_id'], stats['scenario_description'], stats['average_time'], stats['throughput']])

    print("Saved average time and throughput to 'scenario_stats.csv'")
