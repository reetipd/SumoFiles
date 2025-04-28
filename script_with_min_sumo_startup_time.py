import traci
from traci import simulation
import json
import os
import time
import csv
import best_scenarios
import get_best_scenarios
import pandas as pd
from typing import Dict, List, Set, Tuple, Any, Optional
import xml.etree.ElementTree as ET


class TrafficSimulator:
    def __init__(self, sumo_binary="sumo-gui", file_name="Synthesized_1Min"):
        self.sumo_binary = sumo_binary
        self.file_name = file_name
        self.vehicle_time_tracking = {}
        self.remaining_vehicles = {}
        self.scenario_stats = {}
        self.sumo_running = False
        self.current_video_index = None
        self.reset_vehicle_sets()
        
    def reset_vehicle_sets(self):
        """Reset all vehicle tracking sets"""
        self.vehicles_to_east = set()
        self.vehicles_to_west = set()
        self.vehicles_to_north = set()
        self.vehicles_to_south = set()
        self.vehicles_to_east_all = set()
        self.vehicles_to_west_all = set()
        self.vehicles_to_north_all = set()
        self.vehicles_to_south_all = set()
        self.green_light_vehicle_counts = {}

    def is_route_file_ready(self,file_path):
        """Check if the route file is finished (contains a <done/> element)."""
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            for child in root:
                if child.tag.lower() == 'done':
                    return True
        except ET.ParseError:
            return False
        return False

    def parse_route_file(file_path):
        """
        Parse the route file and return a dictionary of vehicles.
        Each key is a vehicle id, and the value is a dictionary with 'route' and 'depart'.
        """
        vehicles = {}
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            for veh in root.findall("vehicle"):
                veh_id = veh.get("id")
                route_id = veh.get("route")
                depart = veh.get("depart")
                if veh_id and route_id and depart:
                    vehicles[veh_id] = {"route": route_id, "depart": float(depart)}
        except Exception as e:
            print(f"Error parsing route file: {e}")
        return vehicles
        
    def set_traffic_lights(self, scenarios):
        """Configure traffic light patterns based on provided scenarios"""
        junction_ids = traci.trafficlight.getIDList()

        for junction_id in junction_ids:
            phases = []
            for scenario in scenarios:
                phase = traci.trafficlight.Phase(scenario["duration"], scenario["str"])
                phases.append(phase)
            
            program = traci.trafficlight.Logic(f"logic_{junction_id}", 0, 0, phases)
            traci.trafficlight.setProgramLogic(junction_id, program)
            traci.simulationStep()
    
    def start_sumo(self, video_index, cropping_time_in_minutes, max_retries=5, retry_delay=1, scale_factor=3):
        """Start SUMO with retry logic"""
        # If SUMO is already running with the same video index, just return success
        if self.sumo_running and self.current_video_index == video_index:
            return True
        
        # If SUMO is running but with a different video, close it first
        if self.sumo_running:
            self.close_sumo()
            
        base_dir = os.path.dirname(os.path.abspath(__file__))

        sumo_config_file = os.path.join(
            base_dir,
            "sumo_configuration_files",
            "Bellevue_116th_NE12th__2017-09-10_19-08-25",
            f"{cropping_time_in_minutes}Min",
            f"Video_{video_index}",
            "sumo_config.sumocfg"
        )

        print("Using SUMO config:", sumo_config_file)

        # sumo_config_file = fr"/Users/ull/Documents/GRA/TRAFFIC-Project/SUMO Files/sumo_configuration_files/Bellevue_116th_NE12th__2017-09-10_19-08-25/{cropping_time_in_minutes}Min/Video_{video_index}/sumo_config.sumocfg"
        
        def kill_sumo():
            os.system("pkill -f sumo")

        for attempt in range(max_retries):
            try:
                print(f"Starting SUMO, attempt {attempt + 1}/{max_retries}")
                kill_sumo()  # Kill any previous stuck SUMO instance
                time.sleep(1)
                traci.start([self.sumo_binary, "-c", sumo_config_file])
                traci.simulation.setScale(scale_factor)
                self.sumo_running = True
                self.current_video_index = video_index
                return True
            except Exception as e:
                print(f"Error: {e}")
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
        
        print("Failed to start SUMO after multiple attempts.")
        return False

    def run_scenario_with_dynamic_lights(self, junction_id, total_simulation_steps, phase_durations, 
                                      change_interval, group_id, video_index, inject, cropping_time_in_minutes):
        """Run the simulation with dynamic phase changes at each interval"""
        

        # Actual config file loaction to run
        dynamic_value = f"Video_{video_index}"  # Replace with your dynamic value
        # sumo_config_file = fr"/Users/ull/Documents/GRA/TRAFFIC-Project/SUMO Files/sumo_configuration_files/Bellevue_116th_NE12th__2017-09-10_19-08-25/{cropping_time_in_minutes}Min/{dynamic_value}/sumo_config.sumocfg"

        base_dir = os.path.dirname(os.path.abspath(__file__))

        sumo_config_file = os.path.join(
            base_dir,
            "sumo_configuration_files",
            "Bellevue_116th_NE12th__2017-09-10_19-08-25",
            f"{cropping_time_in_minutes}Min",
            f"Video_{video_index}",
            "sumo_config.sumocfg"
        )

        # Load the new config file for simualtion (Resetting the simulation)
        self.reset_simulation(sumo_config_file)
       

        current_step = 0
        interval_index = 0
        change = False
        idx_count = 0

        self.vehicles_to_east = set()
        
        # Apply the traffic light patterns for this scenario
        self.set_traffic_lights(phase_durations)


        # Inject remaining vehicle from previous state
        if inject:
            self.inject_remaining_vehicles(group_id)
    
        traffic_flow = {}
        veh_time = {}
        
        while current_step <= change_interval:
            # Start the simualtion
            traci.simulationStep()

            # Get the vehicle count and travel time
            traffic_flow = self.get_vehicle_count(interval_index-1, current_step, idx_count)
            veh_time = self.get_vehicle_time(interval_index-1, current_step, idx_count, change, group_id)

            change = False  
            current_step += 1

        if current_step == change_interval + 1:
            print(f"Done with {change_interval} seconds ---- Run next scenario ")
            print("Getting the vehicle information: ")

            # Reamining vehicle information
            self.get_vehicle_information(video_index, group_id)
            self.vehicles_to_east_all = set()

        return traffic_flow, veh_time
    
    def get_vehicle_count(self, interval_index, step, idx_count):
        """Count vehicles moving in different directions"""
        junction_ids = traci.trafficlight.getIDList()

        for junction_id in junction_ids:
            vehicle_ids = traci.vehicle.getIDList()

            for vehicle_id in vehicle_ids:
                lane_id = traci.vehicle.getLaneID(vehicle_id)

                # Check if this vehicle hasn't been counted in any direction yet
                if (vehicle_id not in self.vehicles_to_east_all and 
                    vehicle_id not in self.vehicles_to_west_all and 
                    vehicle_id not in self.vehicles_to_north_all and 
                    vehicle_id not in self.vehicles_to_south_all):
                    
                    if lane_id.startswith(":center_") or lane_id.startswith("center_to_"):
                        self.vehicles_to_east_all.add(vehicle_id)
                        self.vehicles_to_east.add(vehicle_id)

            # Get the final vehicle counts after processing the junction
            current_green_count_wtoe = len(self.vehicles_to_east)
            current_green_count_etow = len(self.vehicles_to_west)
            current_green_count_ton = len(self.vehicles_to_north)
            current_green_count_tos = len(self.vehicles_to_south)

            # Store the vehicle counts for this interval
            self.green_light_vehicle_counts[idx_count] = {
                "west_to_east": current_green_count_wtoe,
                "east_to_west": current_green_count_etow,
                "to_north": current_green_count_ton,
                "to_south": current_green_count_tos
            }

        return self.green_light_vehicle_counts
    
    def get_vehicle_time(self, interval_index, step, idx_count, phase_change, group_id):
        """Track vehicle travel times"""
        vehicle_ids = traci.vehicle.getIDList()  

        if phase_change:
            for veh in list(self.vehicle_time_tracking.keys()):  
                if veh in self.vehicle_time_tracking:
                    if "end" not in self.vehicle_time_tracking[veh] and self.vehicle_time_tracking[veh]["traffic_scenario"] == idx_count - 1:
                        self.vehicle_time_tracking[veh]["start"] = step
                        self.vehicle_time_tracking[veh]["traffic_scenario"] = idx_count

        # Check for vehicles that have exited
        for veh in list(self.vehicle_time_tracking.keys()):  
            if veh not in vehicle_ids:
                if "captured" not in self.vehicle_time_tracking[veh]: 
                    self.vehicle_time_tracking[veh]["end"] = step 
                    self.vehicle_time_tracking[veh]["captured"] = True

        # Track new vehicles entering
        for vehicle_id in vehicle_ids:
            lane_id = traci.vehicle.getLaneID(vehicle_id)
            entry_lanes = [
                "west_to_center_0", "west_to_center_1", "west_to_center_2", "west_to_center_3",
                "east_to_center_0", "east_to_center_1", "east_to_center_2",
                "north_to_center_0", "north_to_center_1", "north_to_center_2",
                "south_to_center_0", "south_to_center_1", "south_to_center_2"
            ]
            
            if vehicle_id not in self.vehicle_time_tracking and lane_id in entry_lanes:
                self.vehicle_time_tracking[vehicle_id] = {
                    "start": step,
                    "traffic_scenario": idx_count,
                    "group_id": group_id
                }

        return self.vehicle_time_tracking


    def reset_simulation(self, config_file: str):
        """Completely reloads the network in SUMO (fast) and zeroes everything."""
        traci.load(["-c", config_file])
        # clear Python‐side sets
        # self.reset_vehicle_sets()
    
    def save_avg_and_throughput_to_csv(self, traffic_flow_data, veh_time, scenarios, group_id):
        """Calculate and save scenario statistics"""
        scenario_time_stats = {}

        # Loop through each vehicle's data
        for vehicle_data in veh_time.values():
            if "traffic_scenario" in vehicle_data and "end" in vehicle_data:
                traffic_scenario = vehicle_data['traffic_scenario']  
                
                if traffic_scenario not in scenario_time_stats:
                    scenario_time_stats[traffic_scenario] = {'total_time': 0, 'vehicle_count': 0}

                if vehicle_data["end"] != 0:            
                    scenario_time_stats[traffic_scenario]['total_time'] += vehicle_data['end'] - vehicle_data['start']
                    scenario_time_stats[traffic_scenario]['vehicle_count'] += 1

        # Calculate average time per scenario
        average_time_per_scenario = {
            scenario: stats['total_time'] / stats['vehicle_count'] if stats['vehicle_count'] > 0 else 0
            for scenario, stats in scenario_time_stats.items()
        }

        # Calculate throughput for each scenario
        for x in range(len(traffic_flow_data)):
            scenario_id = x % len(scenarios)
            scenario_description = scenarios

            average_time = average_time_per_scenario.get(x, 0)

            # Calculate throughput for the current row
            throughput = (traffic_flow_data[x]["west_to_east"] + 
                          traffic_flow_data[x]["east_to_west"] + 
                          traffic_flow_data[x]["to_north"] + 
                          traffic_flow_data[x]["to_south"])

            # Store the data in scenario_stats with scenario details
            self.scenario_stats[f"{x}+{group_id}"] = {
                'average_time': average_time,
                'throughput': throughput,
                'scenario_description': scenario_description,
                'group_id': group_id,
                'scenario_id': scenario_id,
                'idx_count': x,
            }
    
    def get_vehicle_information(self, video_index, group_id):
        """Collect information about remaining vehicles"""
        data = {}
        vehicle_ids = traci.vehicle.getIDList()
        
        for vehicle_id in vehicle_ids:
            if vehicle_id not in self.vehicles_to_east_all:
                speed = traci.vehicle.getSpeed(vehicle_id)
                position = traci.vehicle.getPosition(vehicle_id)
                route_id = traci.vehicle.getRouteID(vehicle_id)
                lane_id = traci.vehicle.getLaneID(vehicle_id)
                edge_id = traci.vehicle.getRoadID(vehicle_id)
                lane_index = traci.vehicle.getLaneIndex(vehicle_id)
                pos = traci.vehicle.getLanePosition(vehicle_id)
                
                excluded_lanes = [
                    "center_to_east_0", "center_to_east_1", 
                    "center_to_west_0", "center_to_west_1", 
                    "center_to_north_0", "center_to_north_1", 
                    "center_to_south_0", "center_to_south_1"
                ]
                
                if lane_id not in excluded_lanes:
                    data[vehicle_id] = {
                        "speed": speed,
                        "position": position,
                        "route_id": route_id,
                        "lane_id": lane_id,
                        "edge_id": edge_id,
                        "lane_index": lane_index,
                        "lane_position": pos,
                    }

                    self.remaining_vehicles[group_id] = data

    
    def inject_remaining_vehicles(self, group_id):
        """Inject previously tracked vehicles back into simulation"""
        if group_id in self.remaining_vehicles:
            for vehicle_id, data in self.remaining_vehicles[group_id].items():
                new_vehicle_id = f"old_+{vehicle_id}"
                traci.vehicle.add(
                    vehID=new_vehicle_id, 
                    routeID=data["route_id"], 
                    departPos=str(data["lane_position"]), 
                    departSpeed=str(data["speed"])
                )
                traci.vehicle.moveToXY(
                    vehID=new_vehicle_id, 
                    edgeID=data["edge_id"], 
                    laneIndex=data["lane_index"], 
                    x=data["position"][0], 
                    y=data["position"][1]
                )
            del self.remaining_vehicles[group_id]

    def parse_route_file(self,file_path):
        """
        Parse the route file and return a dictionary of vehicles.
        Each key is a vehicle id, and the value is a dictionary with 'route' and 'depart'.
        """
        vehicles = {}
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            for veh in root.findall("vehicle"):
                veh_id = veh.get("id")
                route_id = veh.get("route")
                depart = veh.get("depart")
                if veh_id and route_id and depart:
                    vehicles[veh_id] = {"route": route_id, "depart": float(depart)}
        except Exception as e:
            print(f"Error parsing route file: {e}")
        return vehicles

    def inject_vehicles_from_route_file(self,route_file):
        """
        Dynamically inject vehicles into the running SUMO simulation by reading the route file.
        Vehicles are added if the current simulation time is greater than or equal to their depart time.
        """
        vehicles = self.parse_route_file(route_file)
        current_time = traci.simulation.getTime()
        injected = []
        for veh_id, data in vehicles.items():
            if current_time >= data["depart"]:
                try:
                    # No departPos provided so SUMO places the vehicle at the beginning of its route.
                    traci.vehicle.add(vehID=veh_id, routeID=data["route"], depart=str(current_time))
                    injected.append(veh_id)
                    # print(f"Injected vehicle {veh_id} at simulation time {current_time}")
                except Exception as e:
                    print(f"Error injecting vehicle {veh_id}: {e}")
        return injected

            
    def run_all_scenarios(self, scenario_groups, video_index, cropping_time_in_minutes, inject):
        """Run all scenario groups in sequence"""
        total_simulation_steps = 5000
        change_interval = 60 # Time to change the traffic scenario

        start_time = time.time()
        print(f"Starting time...")

        for group_name, scenario_group in scenario_groups:
            self.green_light_vehicle_counts = {}

            # Run the simulation with dynamic phase changes
            traffic_flow, veh_time = self.run_scenario_with_dynamic_lights(
                "center", total_simulation_steps, scenario_group, 
                change_interval, group_name, video_index, inject, cropping_time_in_minutes
            )

            self.save_avg_and_throughput_to_csv(traffic_flow, veh_time, scenario_group, group_name)
            
            # Reset tracking sets
            self.vehicles_to_west_all = set()
            self.vehicles_to_east_all = set()
            self.vehicles_to_north_all = set()
            self.vehicles_to_south_all = set()

        print(f"Finished running all scenarios for video index {video_index} in {time.time() - start_time:.2f} seconds.")
        
        
    
    def run_full_simulation(self, scenario_groups, cropping_time_in_minutes=1, inject=False):
        """Run the full simulation across all videos"""
        throughput_final = []
        time_final = []

        no_of_videos = 12
        for i in range(no_of_videos):
            self.run_all_scenarios(scenario_groups, i + 1, cropping_time_in_minutes, inject)

            # Create directory to save results
            directory = f"files/results/{cropping_time_in_minutes}_Min"
            if not os.path.exists(directory):
                os.makedirs(directory)

            # Save results for this iteration
            path = f"{directory}/{self.file_name}_{i}.csv"
            with open(path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Scenario_ID', 'Group_ID', 'Scenario_Description', 
                                'Average_Travel_Time', 'Throughput', 'Idx_Count'])
                
                for scenario, stats in self.scenario_stats.items():
                    writer.writerow([
                        stats['scenario_id'], 
                        stats['group_id'], 
                        stats['scenario_description'],
                        stats['average_time'], 
                        stats['throughput'], 
                        stats['idx_count']
                    ])

            print(f"Saved average time and throughput for iteration {i+1}")

            # Get the best scenario, throughput and time for each cropped video
            best_throughout, best_time = get_best_scenarios.analyze_traffic_scenarios(path, i + 1)

            throughput_final.append(best_throughout)
            time_final.append(best_time)

            inject = True  # Enable injection for subsequent runs

        # Combine results from all iterations
        final_df_throughput = pd.concat(throughput_final, ignore_index=True)
        final_df_time = pd.concat(time_final, ignore_index=True)

        # Save to CSV files
        folder_path = 'best_scenarios/updated'  
        final_df_throughput.to_csv(f'{folder_path}/best_throughput_{self.file_name}.csv', index=False)
        final_df_time.to_csv(f'{folder_path}/best_time_{self.file_name}.csv', index=False)

        print("Final results saved successfully.")

    def close_sumo(self):
        """Close the SUMO simulation"""
        traci.close()

def main():
    file_name = "Synthesized_1Min"
    
    # Different scenrios to run 
    scenario_groups = [
    ("Static", [
        {"duration": 15, "str": "GGGrrrrrrrGGGrrrrrrr", "traffic_light": "Green", "road": "NS"},
        {"duration": 5, "str": "yyyrrrrrrryyyrrrrrrr", "traffic_light": "Yellow", "road": "NS"},
        {"duration": 5, "str": "rrrGGrrrrrrrrGGrrrrr", "traffic_light": "Green", "road": "EW"},
        {"duration": 15, "str": "rrrrrGGGrrrrrrrGGGrr", "traffic_light": "Green", "road": "NS"},
        {"duration": 5, "str": "rrrrryyyrrrrrrryyyrr", "traffic_light": "Yellow", "road": "NS"},
        {"duration": 5, "str": "rrrrrrrrGGrrrrrrrrGG", "traffic_light": "Green", "road": "EW"},
    ]),

    ("Group1", [
    {"duration": 15, "str": "GGGGGrrrrrrrrrrrrrrr", "traffic_light": "Green", "road": "N"},
    # {"duration": 5, "str": "YYYYYrrrrrrrrrrrrrrr", "traffic_light": "Yellow", "road": "N"},
    # {"duration": 15, "str": "rrrrrGGGGGrrrrrrrrrr", "traffic_light": "Green", "road": "S"},
    # {"duration": 5, "str": "rrrrrYYYYYrrrrrrrrrr", "traffic_light": "Yellow", "road": "S"},
    # {"duration": 15, "str": "rrrrrrrrrrGGGGGrrrrr", "traffic_light": "Green", "road": "E"},
    # {"duration": 5, "str": "rrrrrrrrrrYYYYYrrrrr", "traffic_light": "Yellow", "road": "E"}
        ])
        ,

    ("Group2", [
       {"duration": 10, "str": "GrrrrrrrrrGrrrrrrrrr", "traffic_light": "Left Turn", "road": "NS"},
       {"duration": 20, "str": "GGGGGrrrrrGGGGGrrrrr", "traffic_light": "Green", "road": "NS"},
       {"duration": 5, "str": "YYYYYrrrrrYYYYYrrrrr", "traffic_light": "Yellow", "road": "NS"},
       {"duration": 10, "str": "rrrrrGrrrrrrrrrGrrrr", "traffic_light": "Left Turn", "road": "EW"},
       {"duration": 15, "str": "rrrrrGGGGGrrrrrGGGGG", "traffic_light": "Green", "road": "EW"},
    ]),

    ("Group3", [
       {"duration": 10, "str": "GrrrrrrrrrGrrrrrrrrr", "traffic_light": "Left Turn", "road": "NS"},
       {"duration": 20, "str": "GGGGGrrrrrGGGGGrrrrr", "traffic_light": "Green", "road": "NS"},
       {"duration": 5, "str": "YYYYYrrrrrYYYYYrrrrr", "traffic_light": "Yellow", "road": "NS"},
       {"duration": 10, "str": "rrrrrGrrrrrrrrrGrrrr", "traffic_light": "Left Turn", "road": "EW"},
       {"duration": 15, "str": "rrrrrGGGGGrrrrrGGGGG", "traffic_light": "Green", "road": "EW"},
    ]),


    ("Group4", [
       {"duration": 15, "str": "GGGGGrrrrrGGGGGrrrrr", "traffic_light": "Green", "road": "NS"},
       {"duration": 5, "str": "YYYYYrrrrrYYYYYrrrrr", "traffic_light": "Yellow", "road": "NS"},
       {"duration": 15, "str": "rrrrrGGGGGrrrrrGGGGG", "traffic_light": "Green", "road": "EW"},
       {"duration": 5, "str": "rrrrrYYYYYrrrrrYYYYY", "traffic_light": "Yellow", "road": "EW"},
       {"duration": 10, "str": "Grrrrrrrrrrrrrrrrrrr", "traffic_light": "Left Turn", "road": "N"},
       {"duration": 10, "str": "rrrrrGrrrrrrrrrrrrrr", "traffic_light": "Left Turn", "road": "S"},
    ]),

    ("Group5", [
       {"duration": 10, "str": "GrrrrrrrrrGrrrrrrrrr", "traffic_light": "Left Turn", "road": "NS"},
       {"duration": 20, "str": "GGGGGrrrrrGGGGGrrrrr", "traffic_light": "Green", "road": "NS"},
       {"duration": 5, "str": "YYYYYrrrrrYYYYYrrrrr", "traffic_light": "Yellow", "road": "NS"},
       {"duration": 10, "str": "rrrrrGrrrrrrrrrGrrrr", "traffic_light": "Left Turn", "road": "EW"},
       {"duration": 15, "str": "rrrrrGGGGGrrrrrGGGGG", "traffic_light": "Green", "road": "EW"},
    ]),


    ("Group6", [
       {"duration": 10, "str": "rrrrrGrrrrrrrrrGrrrr", "traffic_light": "Left Turn", "road": "EW"},
       {"duration": 20, "str": "rrrrrGGGGGrrrrrGGGGG", "traffic_light": "Green", "road": "EW"},
       {"duration": 5, "str": "rrrrrYYYYYrrrrrYYYYY", "traffic_light": "Yellow", "road": "EW"},
       {"duration": 10, "str": "GrrrrrrrrrGrrrrrrrrr", "traffic_light": "Left Turn", "road": "NS"},
       {"duration": 15, "str": "GGGGGrrrrrGGGGGrrrrr", "traffic_light": "Green", "road": "NS"},
    ]),

    ("Group7", [
       {"duration": 12, "str": "GGGGGrrrrrGGGGGrrrrr", "traffic_light": "Green", "road": "NS"},
       {"duration": 3,  "str": "YYYYYrrrrrYYYYYrrrrr", "traffic_light": "Yellow", "road": "NS"},
       {"duration": 12, "str": "rrrrrGGGGGrrrrrGGGGG", "traffic_light": "Green", "road": "EW"},
       {"duration": 3,  "str": "rrrrrYYYYYrrrrrYYYYY", "traffic_light": "Yellow", "road": "EW"},
       {"duration": 6,  "str": "Grrrrrrrrrrrrrrrrrrr", "traffic_light": "Left Turn", "road": "N"},
       {"duration": 6,  "str": "rrrrrGrrrrrrrrrrrrrr", "traffic_light": "Left Turn", "road": "S"},
       {"duration": 6,  "str": "rrrrrrrrrGrrrrrrrrrr", "traffic_light": "Left Turn", "road": "E"},
       {"duration": 6,  "str": "rrrrrrrrrrrrrrrGrrrr", "traffic_light": "Left Turn", "road": "W"},
       {"duration": 6, "str": "GGGGGrrrrrGGGGGrrrrr", "traffic_light": "Green", "road": "NS"},
    ]),



    ("Group8", [
       {"duration": 35, "str": "GGGGGrrrrrGGGGGrrrrr", "traffic_light": "Green", "road": "NS"},
       {"duration": 5,  "str": "YYYYYrrrrrYYYYYrrrrr", "traffic_light": "Yellow", "road": "NS"},
       {"duration": 15, "str": "rrrrrGGGGGrrrrrGGGGG", "traffic_light": "Green", "road": "EW"},
       {"duration": 5,  "str": "rrrrrYYYYYrrrrrYYYYY", "traffic_light": "Yellow", "road": "EW"}
    ]),

    ("Group9", [
       {"duration": 7,  "str": "GrrrrrrrrrGrrrrrrrrr", "traffic_light": "Left Turn", "road": "NS"},
       {"duration": 18, "str": "GGGGGrrrrrGGGGGrrrrr", "traffic_light": "Green", "road": "NS"},
       {"duration": 5,  "str": "YYYYYrrrrrYYYYYrrrrr", "traffic_light": "Yellow", "road": "NS"},
       {"duration": 7,  "str": "rrrrrGrrrrrrrrrGrrrr", "traffic_light": "Left Turn", "road": "EW"},
       {"duration": 18, "str": "rrrrrGGGGGrrrrrGGGGG", "traffic_light": "Green", "road": "EW"},
       {"duration": 5,  "str": "rrrrrYYYYYrrrrrYYYYY", "traffic_light": "Yellow", "road": "EW"}
    ]),

    ("Group10", [
       {"duration": 10, "str": "rrrrrGrrrrrrrrrGrrrr", "traffic_light": "Left Turn", "road": "EW"},
       {"duration": 15, "str": "rrrrrGGGGGrrrrrGGGGG", "traffic_light": "Green", "road": "EW"},
       {"duration": 5,  "str": "rrrrrYYYYYrrrrrYYYYY", "traffic_light": "Yellow", "road": "EW"},
       {"duration": 10, "str": "GrrrrrrrrrGrrrrrrrrr", "traffic_light": "Left Turn", "road": "NS"},
       {"duration": 15, "str": "GGGGGrrrrrGGGGGrrrrr", "traffic_light": "Green", "road": "NS"},
       {"duration": 5,  "str": "YYYYYrrrrrYYYYYrrrrr", "traffic_light": "Yellow", "road": "NS"}
    ]),
    ("Group11", [
       {"duration": 10, "str": "rrrrrGrrrrrrrrrGrrrr", "traffic_light": "Left Turn", "road": "EW"},
       {"duration": 20, "str": "rrrrrGGGGGrrrrrGGGGG", "traffic_light": "Green", "road": "EW"},
       {"duration": 5, "str": "rrrrrYYYYYrrrrrYYYYY", "traffic_light": "Yellow", "road": "EW"},
       {"duration": 10, "str": "GrrrrrrrrrGrrrrrrrrr", "traffic_light": "Left Turn", "road": "NS"},
       {"duration": 15, "str": "GGGGGrrrrrGGGGGrrrrr", "traffic_light": "Green", "road": "NS"},
    ]),

    ("Group12", [
       {"duration": 18, "str": "rrrrrGGGGGrrrrrGGGGG", "traffic_light": "Green", "road": "EW"},
       {"duration": 5, "str": "rrrrrYYYYYrrrrrYYYYY", "traffic_light": "Yellow", "road": "EW"},
       {"duration": 18, "str": "GGGGGrrrrrGGGGGrrrrr", "traffic_light": "Green", "road": "NS"},
       {"duration": 5, "str": "YYYYYrrrrrYYYYYrrrrr", "traffic_light": "Yellow", "road": "NS"},
       {"duration": 10, "str": "rrrrrGrrrrrrrrrGrrrr", "traffic_light": "Left Turn", "road": "EW"},
       {"duration": 4, "str": "rrrrrYYYYYrrrrrYYYYY", "traffic_light": "Yellow", "road": "EW"},
    ]),

    ("Group13", [
       {"duration": 10, "str": "rrrrrGrrrrrrrrrGrrrr", "traffic_light": "Left Turn", "road": "EW"},
       {"duration": 10, "str": "GrrrrrrrrrGrrrrrrrrr", "traffic_light": "Left Turn", "road": "NS"},
       {"duration": 20, "str": "GGGGGrrrrrGGGGGrrrrr", "traffic_light": "Green", "road": "NS"},
       {"duration": 5, "str": "YYYYYrrrrrYYYYYrrrrr", "traffic_light": "Yellow", "road": "NS"},
       {"duration": 15, "str": "rrrrrGGGGGrrrrrGGGGG", "traffic_light": "Green", "road": "EW"},
    ]),

    ("Group14", [
       {"duration": 20, "str": "rrrrrGGGGGrrrrrGGGGG", "traffic_light": "Green", "road": "EW"},
       {"duration": 5, "str": "rrrrrYYYYYrrrrrYYYYY", "traffic_light": "Yellow", "road": "EW"},
       {"duration": 20, "str": "GGGGGrrrrrGGGGGrrrrr", "traffic_light": "Green", "road": "NS"},
       {"duration": 5, "str": "YYYYYrrrrrYYYYYrrrrr", "traffic_light": "Yellow", "road": "NS"},
       {"duration": 10, "str": "GrrrrrrrrrGrrrrrrrrr", "traffic_light": "Left Turn", "road": "NS"},
    ]),

    ("Group15", [
       {"duration": 5, "str": "rrrrrGrrrrrrrrrGrrrr", "traffic_light": "Left Turn", "road": "EW"},
       {"duration": 25, "str": "rrrrrGGGGGrrrrrGGGGG", "traffic_light": "Green", "road": "EW"},
       {"duration": 5, "str": "rrrrrYYYYYrrrrrYYYYY", "traffic_light": "Yellow", "road": "EW"},
       {"duration": 25, "str": "GGGGGrrrrrGGGGGrrrrr", "traffic_light": "Green", "road": "NS"},
       {"duration": 5, "str": "YYYYYrrrrrYYYYYrrrrr", "traffic_light": "Yellow", "road": "NS"},
    ]),

    ("Group16", [
       {"duration": 15, "str": "GGGGGrrrrrGGGGGrrrrr", "traffic_light": "Green", "road": "NS"},
       {"duration": 5, "str": "YYYYYrrrrrYYYYYrrrrr", "traffic_light": "Yellow", "road": "NS"},
       {"duration": 15, "str": "rrrrrGGGGGrrrrrGGGGG", "traffic_light": "Green", "road": "EW"},
       {"duration": 5, "str": "rrrrrYYYYYrrrrrYYYYY", "traffic_light": "Yellow", "road": "EW"},
       {"duration": 10, "str": "rrrrrGrrrrrrrrrGrrrr", "traffic_light": "Left Turn", "road": "EW"},
       {"duration": 10, "str": "GrrrrrrrrrGrrrrrrrrr", "traffic_light": "Left Turn", "road": "NS"},
    ]),

    ("Group17", [
       {"duration": 10, "str": "GrrrrrrrrrGrrrrrrrrr", "traffic_light": "Left Turn", "road": "NS"},
       {"duration": 17, "str": "GGGGGrrrrrGGGGGrrrrr", "traffic_light": "Green", "road": "NS"},
       {"duration": 6, "str": "YYYYYrrrrrYYYYYrrrrr", "traffic_light": "Yellow", "road": "NS"},
       {"duration": 10, "str": "rrrrrGrrrrrrrrrGrrrr", "traffic_light": "Left Turn", "road": "EW"},
       {"duration": 17, "str": "rrrrrGGGGGrrrrrGGGGG", "traffic_light": "Green", "road": "EW"},
    ]),

    ("Group18", [
       {"duration": 15, "str": "rrrrrGGGGGrrrrrGGGGG", "traffic_light": "Green", "road": "EW"},
       {"duration": 5, "str": "rrrrrYYYYYrrrrrYYYYY", "traffic_light": "Yellow", "road": "EW"},
       {"duration": 10, "str": "GrrrrrrrrrGrrrrrrrrr", "traffic_light": "Left Turn", "road": "NS"},
       {"duration": 25, "str": "GGGGGrrrrrGGGGGrrrrr", "traffic_light": "Green", "road": "NS"},
       {"duration": 5, "str": "YYYYYrrrrrYYYYYrrrrr", "traffic_light": "Yellow", "road": "NS"}
    ]),

    ("Group19", [
       {"duration": 10, "str": "GrrrrrrrrrGrrrrrrrrr", "traffic_light": "Left Turn", "road": "NS"},
       {"duration": 10, "str": "rrrrrGrrrrrrrrrGrrrr", "traffic_light": "Left Turn", "road": "EW"},
       {"duration": 15, "str": "rrrrrGGGGGrrrrrGGGGG", "traffic_light": "Green", "road": "EW"},
       {"duration": 5, "str": "rrrrrYYYYYrrrrrYYYYY", "traffic_light": "Yellow", "road": "EW"},
       {"duration": 15, "str": "GGGGGrrrrrGGGGGrrrrr", "traffic_light": "Green", "road": "NS"},
       {"duration": 5, "str": "YYYYYrrrrrYYYYYrrrrr", "traffic_light": "Yellow", "road": "NS"}
    ]),

    ("Group20", [
       {"duration": 5, "str": "rrrrrGrrrrrrrrrGrrrr", "traffic_light": "Left Turn", "road": "EW"},
       {"duration": 30, "str": "rrrrrGGGGGrrrrrGGGGG", "traffic_light": "Green", "road": "EW"},
       {"duration": 5, "str": "rrrrrYYYYYrrrrrYYYYY", "traffic_light": "Yellow", "road": "EW"},
       {"duration": 5, "str": "GrrrrrrrrrGrrrrrrrrr", "traffic_light": "Left Turn", "road": "NS"},
       {"duration": 15, "str": "GGGGGrrrrrGGGGGrrrrr", "traffic_light": "Green", "road": "NS"},
    ])

    ]

    # Create simulator and run
    simulator = TrafficSimulator(sumo_binary="sumo", file_name=file_name)  # Use sumo-gui in place of sumo for visualization
    
    try:
        sumo_binary = "sumo"  # or "sumo-gui"

        # For just starting the SUMO (to decrease the overhead time it takes to start SUMO)

        base_dir = os.path.dirname(os.path.abspath(__file__))

        dummy_sumo_config_file = os.path.join(
            base_dir,
            "sumo_configuration_files",
            "Bellevue_116th_NE12th__2017-09-10_19-08-25",
            f"1Min",
            f"Video_1",
            "sumo_config.sumocfg"
        )

        print("Using SUMO config:", dummy_sumo_config_file)
        # dummy_sumo_config_file = "/Users/ull/Documents/GRA/TRAFFIC-Project/SUMO Files/sumo_configuration_files/Bellevue_116th_NE12th__2017-09-10_19-08-25/1Min/Video_1/sumo_config.sumocfg"

        print("Starting SUMO for warm-up...")
        traci.start([sumo_binary, "-c", dummy_sumo_config_file])
        for _ in range(2):  
            traci.simulationStep()
        print("SUMO initialized.")


        base_dir = os.path.dirname(os.path.abspath(__file__))

        route_file = os.path.join(
            base_dir,
            "sumo_configuration_files",
            "Bellevue_116th_NE12th__2017-09-10_19-08-25",
            f"1Min",
            f"Video_1",
            "route.rou.xml"
        )

        print("Using SUMO config:", route_file)
        # # Check if the route file is ready or not (For later, we might need to give list of route files locations and loop to check for each route files after processing the previous route file)
        # route_file = "/Users/ull/Documents/GRA/TRAFFIC-Project/SUMO Files copy/sumo_configuration_files/Bellevue_116th_NE12th__2017-09-10_19-08-25/1Min/Video_1/route.rou.xml"
        print("Waiting for route file to be ready...")
        while not simulator.is_route_file_ready(route_file):
            print("Route file not ready. Waiting...")

        # Once the route file is ready, run the simulation
        simulator.run_full_simulation(scenario_groups)
    finally:
        simulator.close_sumo()
        print("SUMO has been successfully closed.")

if __name__ == "__main__":
    main()