import traci
from traci import simulation

sumo_binary = "sumo-gui" 
# sumo_config_file = r"C:\Users\c00563648\OneDrive - University of Louisiana at Lafayette\Documents\GRA\Traffic\Sumo-Files\SumoFiles\Bellevue_116th_NE12th__2017-09-11_07-08-32\sumo_files\sumo_config.sumocfg"
# sumo_config_file = r"/Users/ull/Documents/GRA/TRAFFIC-Project/SUMO Files/Bellevue_116th_NE12th__2017-09-11_07-08-32/sumo_files/sumo_config.sumocfg"
# sumo_config_file = r"/Users/ull/Documents/GRA/TRAFFIC-Project/SUMO Files/Bellevue_116th_NE12th__2017-09-11_14-08-35_East_West/sumo_config.sumocfg"
sumo_config_file = r"/Users/ull/Documents/GRA/TRAFFIC-Project/SUMO Files/Bellevue_116th_NE12th_2017-09-11_14-08-35_Cropped_Videos/sumo_files/sumo_config.sumocfg"

# Start the simulation
traci.start([sumo_binary, "-c", sumo_config_file])


step = 0
total_vehicle_from_north_to_center = set()
total_vehicle_from_center_to_north = set()
while step < 1000:
    traci.simulationStep()  
    
    vehicle_ids = traci.vehicle.getIDList()
    
    for vehicle_id in vehicle_ids:
        speed = traci.vehicle.getSpeed(vehicle_id)
        position = traci.vehicle.getPosition(vehicle_id)
        lane_id = traci.vehicle.getLaneID(vehicle_id)
        vehicle_type = traci.vehicle.getTypeID(vehicle_id)
        vehicle_route = traci.vehicle.getRouteID(vehicle_id)
        phase = traci.trafficlight.getPhase("center")
        phase_name = traci.trafficlight.getPhaseName("center")
        phase_duration = traci.trafficlight.getPhaseDuration("center")

        # traci.trafficlight.setPhase("center",2)
        # traci.trafficlight.setPhaseDuration("center", 20)
        
        print(f"Step {step}: Vehicle {vehicle_id} info:")
        print(f"Speed: {speed} m/s")
        print(f"Position: {position}")
        print(f"Lane: {lane_id}")
        print(f"Type: {vehicle_type}")
        print(f"Route: {vehicle_route}")
        print()

        print(f"Phase: {phase}")
        print(f"Phase Duration: {phase_duration}")
        print(f"Phase Name: {phase_name}")
        print()

        # if lane_id == "north_to_center_0":
        #     # print(f"Vehicle {vehicle_id} lane {lane_id}")
        #     total_vehicle_from_north_to_center.add(vehicle_id)
        #     print()
        # elif lane_id == "south_to_center_0":
        #     # print(f"Vehicle {vehicle_id} lane {lane_id}")
        #     total_vehicle_from_center_to_north.add(vehicle_id)
    
    step += 1

print(f"Vehicle Count From North to Center: {len(total_vehicle_from_north_to_center)}")
print(f"Vehicle Count To South: {len(total_vehicle_from_center_to_north)}")
traci.close()
