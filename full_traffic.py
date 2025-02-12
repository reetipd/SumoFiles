import traci
from traci import simulation
import json
import os
import time
import csv

sumo_binary = "sumo-gui"
sumo_config_file = r"/Users/ull/Documents/GRA/TRAFFIC-Project/SUMO Files/Bellevue_116th_NE12th_2017-09-11_14-08-35_Full/sumo_config.sumocfg"

file_name = "Bellevue_116th_NE12th_2017-09-11_14-08-35_Full"

# scenario_groups = [
#     ("Group 1", [
#        {"duration":60,"str":"GGGrrrrrrrGGGrrrrrrr"},
#         {"duration":59,"str":"GGGrrrrrrrGGGrrrrrrr"},
#          {"duration":60,"str":"rrrrrGGGrrrrrrrGGGrr"},
#           {"duration":58,"str":"rrrrrGGGrrrrrrrGGGrr"},
          
#     ]),
#     # ("Group 2", [
#     #    {"duration":60,"str":"GGGrrrrrrrGGGrrrrrrr"},
#     #     {"duration":59,"str":"GGGrrrrrrrGGGrrrrrrr"},
#     #      {"duration":60,"str":"rrrrrGGGrrrrrrrGGGrr"},
#     #       {"duration":58,"str":"rrrrrGGGrrrrrrrGGGrr"},
          
#     # ]),
# ]


scenario_groups = [
    ("Group 1", [
        {"duration": 60, "str": "GGGrrrrrrrGGGrrrrrrr"},
        {"duration": 60, "str": "GGGrrrrrrrGGGrrrrrrr"},
        {"duration": 60, "str": "rrrrrGGGrrrrrrrGGGrr"},
        {"duration": 60, "str": "rrrrrGGGrrrrrrrGGGrr"},
        {"duration": 60, "str": "GGGrrrrrrrGGGrrrrrrr"},
        {"duration": 60, "str": "GGGrrrrrrrGGGrrrrrrr"},
        {"duration": 60, "str": "rrrrrGGGrrrrrrrGGGrr"},
        {"duration": 60, "str": "rrrrrGGGrrrrrrrGGGrr"},
    ]),

    ("Group 2", [
        {"duration": 60, "str": "GGGGrrrrrrGGGGrrrrrr"},
        {"duration": 60, "str": "GGGGrrrrrrGGGGrrrrrr"},
        {"duration": 60, "str": "rrrrGGGGrrrrrrGGGGrr"},
        {"duration": 60, "str": "rrrrGGGGrrrrrrGGGGrr"},
        {"duration": 60, "str": "GGGGrrrrrrGGGGrrrrrr"},
        {"duration": 60, "str": "GGGGrrrrrrGGGGrrrrrr"},
        {"duration": 60, "str": "rrrrGGGGrrrrrrGGGGrr"},
        {"duration": 60, "str": "rrrrGGGGrrrrrrGGGGrr"},
    ]),

    # ("Group 3", [
    #     {"duration": 60, "str": "GGGGGrrrrrGGGGGrrrrr"},
    #     {"duration": 60, "str": "GGGGGrrrrrGGGGGrrrrr"},
    #     {"duration": 60, "str": "rrrrGGGGGrrrrrGGGGGrr"},
    #     {"duration": 60, "str": "rrrrGGGGGrrrrrGGGGGrr"},
    #     {"duration": 60, "str": "GGGGGrrrrrGGGGGrrrrr"},
    #     {"duration": 60, "str": "GGGGGrrrrrGGGGGrrrrr"},
    #     {"duration": 60, "str": "rrrrGGGGGrrrrrGGGGGrr"},
    #     {"duration": 60, "str": "rrrrGGGGGrrrrrGGGGGrr"},
    # ]),
]

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



def run_scenario_with_dynamic_lights(junction_id, total_simulation_steps, phase_durations, change_interval):
    """
    Run the simulation with dynamic phase changes at each interval.
    
    :param junction_id: The ID of the traffic light junction.
    :param total_simulation_steps: The total simulation steps to run.
    :param phase_durations: List of tuples [(green_duration, yellow_duration, red_duration), ...]
    :param change_interval: How often to change the traffic light phases (in steps).
    """
    traci.start([sumo_binary, "-c", sumo_config_file])
    change = False
    current_step = 0
    interval_index = 0  # Start with the first phase configuration
    total_intervals = len(phase_durations)

    global vehiclesToWest, vehiclesToEast, vehiclesToNorth, vehiclesToSouth
    set_traffic_lights(phase_durations)
   
    traffic_flow = {}
    veh_time = {}
    idx_count = 0
    while current_step < total_simulation_steps:
        if current_step % change_interval == 0:
            # print("Traffic Flow", traffic_flow )
            current_scenario = phase_durations[interval_index]
            interval_index = (interval_index + 1) % total_intervals
            change = True
            vehiclesToWest = set()
            vehiclesToEast = set()
            vehiclesToNorth = set()
            vehiclesToSouth = set()
            to_east = {}
            to_west = {}
            idx_count += 1


            
        traci.simulationStep()
        traffic_flow = get_veh_count(interval_index-1, current_step, idx_count-1)
        veh_time = get_veh_time(interval_index-1, current_step, idx_count-1)

        
        change = False  
        
        current_step += 1
    
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

def get_veh_time(interval_index, step, idx_count):
    global vehicle_time_tracking
    vehicle_ids = traci.vehicle.getIDList()  

    if vehicle_time_tracking is not None:
        for veh in list(vehicle_time_tracking.keys()):  
            if veh not in vehicle_ids:
                if "captured" not in vehicle_time_tracking[veh]: 
                    vehicle_time_tracking[veh]["end"] = step 
                    vehicle_time_tracking[veh]["captured"] = True
                    vehicle_time_tracking[veh]["traffic_scenario"]= idx_count

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

    return vehicle_time_tracking



def analyze_traffic(step, interval_index, change, change_interval):

    line_1 = 5
    line_2 = 185

    
    # global current_green_count_WTOE, current_green_count_ETOW, previous_phase, vehiclesToEast, vehiclesToWest, green_light_vehicle_counts
    # junction_ids = traci.trafficlight.getIDList() 
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
            to_east[vehicle_id]["traffic_scenario"] = interval_index
        if vehicle_id in to_east:
            if vehicle_position[0] >= line_2 and (lane_id == "center_to_east_0" or lane_id == "center_to_east_1"):
                # if interval_index != to_east[vehicle_id]["traffic_scenario"]:
                #     if step / change_interval >= interval_index:
                #         to_east[vehicle_id]["traffic_scenario"] = interval_index
                to_east[vehicle_id]["end"] = step
                

        if  vehicle_id not in to_west and (lane_id == "east_to_center_0" or lane_id == "east_to_center_1"):
            to_west[vehicle_id] = {"start": step}
            to_west[vehicle_id]["traffic_scenario"] = interval_index

        if vehicle_id in to_west:
            if  vehicle_position[0] <= line_1 and (lane_id == "center_to_west_0" or lane_id == "center_to_west_1"):
                # if interval_index != to_west[vehicle_id]["traffic_scenario"]:
                #     if step / change_interval >= interval_index:
                #         to_west[vehicle_id]["traffic_scenario"] = interval_index
                to_west[vehicle_id]["end"] = step
    
def save_avg_and_throughput_to_csv(traffic_flow_data, veh_time, scenarios, group_id):
    global scenario_stats

    # for scenario_id, scenario in enumerate(scenarios):
    #     vehicles_in_scenario = []

    #     for vehicle_data in veh_time.values():
    #         if "traffic_scenario" in vehicle_data and "end" in vehicle_data: 
    #             if vehicle_data['traffic_scenario'] == scenario_id:
    #                 vehicles_in_scenario.append(vehicle_data)

        
    #     total_time = 0
    #     for vehicle in vehicles_in_scenario:
    #         total_time += vehicle['end'] - vehicle['start']
        
    #     average_time = total_time / len(vehicles_in_scenario) if vehicles_in_scenario else 0

    scenario_time_stats = {}

    # Loop through each vehicle's data
    for vehicle_data in veh_time.values():
        if "traffic_scenario" in vehicle_data and "end" in vehicle_data:
            traffic_scenario = vehicle_data['traffic_scenario']  
            
            if traffic_scenario not in scenario_time_stats:
                scenario_time_stats[traffic_scenario] = {'total_time': 0, 'vehicle_count': 0}
            
            scenario_time_stats[traffic_scenario]['total_time'] += vehicle_data['end'] - vehicle_data['start']
            scenario_time_stats[traffic_scenario]['vehicle_count'] += 1

    average_time_per_scenario = {
        scenario: stats['total_time'] / stats['vehicle_count'] if stats['vehicle_count'] > 0 else 0
        for scenario, stats in scenario_time_stats.items()
    }


    throughput = 0
    for x in range(len(traffic_flow_data)):
        scenario_id = x % len(scenarios)
        scenario_description = scenarios[scenario_id]

        average_time = average_time_per_scenario.get(scenario_id, 0)

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
            'scenario_id': scenario_id
        }

        # print(f"{x}+{group_id}")


def run_all_scenarios(scenario_groups):
    global vehiclesToWestAll, vehiclesToEastAll, vehiclesToSouthAll, vehiclesToNorthAll, green_light_vehicle_counts
    total_simulation_steps = 5000  # e.g., run for 600 steps (10 minutes)
    change_interval = 60 

    for group_id, scenario_group in enumerate(scenario_groups):
        green_light_vehicle_counts = {}
        group_id = scenario_group[0]
        scenario_group =  scenario_group[1]
        # Run the simulation with dynamic phase changes
        traffic_flow, veh_time = run_scenario_with_dynamic_lights("center", total_simulation_steps, scenario_group, change_interval)
        # print("Traffic flow", traffic_flow)

        save_avg_and_throughput_to_csv(traffic_flow, veh_time, scenario_group, group_id)
        vehiclesToWestAll = set()
        vehiclesToEastAll = set()
        vehiclesToNorthAll = set()
        vehiclesToSouthAll = set()


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