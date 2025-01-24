import traci
from traci import simulation

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
def start_simulation():
    traci.start([sumo_binary, "-c", sumo_config_file])  

    step = 0
    max_steps = 350  #
    while step < max_steps:
        traci.simulationStep() 

        traffic_flow = analyze_traffic(step)
        print(f"Traffic flow: {traffic_flow}")

        step += 1

    traci.close()  

def analyze_traffic(step):
    global current_green_count_NTOS, current_green_count_STON, previous_phase, vehiclesNorthToSouth, vehiclesSouthToNorth, green_light_vehicle_counts
    junction_ids = traci.trafficlight.getIDList() 
    for junction_id in junction_ids:
        current_phase = traci.trafficlight.getPhase(junction_id)
        if current_phase == 0 and previous_phase != 0:  
            current_green_count_NTOS = 0
            current_green_count_STON = 0
            print(f"Green light started at junction {junction_id} at step {step}")

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
            print(f"Junction {junction_id} - Green light: {current_green_count_NTOS} vehicles passed at step {step} North to South {vehiclesNorthToSouth}")
            print(f"Junction {junction_id} - Green light: {current_green_count_STON} vehicles passed at step {step} South to North {vehiclesSouthToNorth}")

        if current_phase != 0 and previous_phase == 0:  
            count_NTOS = current_green_count_NTOS
            count_STON = current_green_count_STON
            print(f"Total vehicles passed from North to South: {count_NTOS}")
            print(f"Total vehicles passed from South to North: {count_STON}")
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
    start_simulation()
