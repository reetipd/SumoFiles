import traci
from traci import simulation
import json

sumo_binary = "sumo-gui" 
# sumo_config_file = r"C:\Users\c00563648\OneDrive - University of Louisiana at Lafayette\Documents\GRA\Traffic\Sumo-Files\SumoFiles\Bellevue_116th_NE12th__2017-09-11_07-08-32\sumo_files\sumo_config.sumocfg"
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

def start_simulation():
    traci.start([sumo_binary, "-c", sumo_config_file])  

    step = 0
    max_steps = 350  #
    while step < max_steps:
        traci.simulationStep() 

        traffic_flow = analyze_traffic(step)

        step += 1

    traci.close()  

    return traffic_flow

def analyze_traffic(step):
    global current_green_count_NTOS, current_green_count_STON, previous_phase, vehiclesNorthToSouth, vehiclesSouthToNorth, green_light_vehicle_counts
    junction_ids = traci.trafficlight.getIDList() 

    vehicle_ids = traci.vehicle.getIDList()

    # Track entry time for new vehicles
    for vehicle_id in vehicle_ids:
        if vehicle_id not in vehicle_entry_times:
            # New vehicle, log its entry time
            vehicle_entry_times[vehicle_id] = step
            # print(f"Vehicle {vehicle_id} entered at time {step}.")

    vehicles_to_remove = []  

    for vehicle_id in list(vehicle_entry_times.keys()):  
        if vehicle_id not in vehicle_ids:
            exit_time = step
            entry_time = vehicle_entry_times.pop(vehicle_id)
            travel_time = exit_time - entry_time
            # print(f"Vehicle {vehicle_id} exited at time {exit_time}. Travel time: {travel_time} seconds.")
            vehicles_to_remove.append(vehicle_id)

    # Now that the iteration is done, remove the vehicles
    for vehicle_id in vehicles_to_remove:
        if vehicle_id in vehicle_entry_times:
            del vehicle_entry_times[vehicle_id]

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

        return green_light_vehicle_counts

# Run the simulation
if __name__ == "__main__":
    traffic_flow = start_simulation()

    # Save the traffic flow data to a JSON file
    with open("traffic_flow.json", "w") as f:
        json.dump(traffic_flow, f, indent=4)
