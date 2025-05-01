import traci
from traci import simulation

sumo_binary = "sumo-gui"
# Path to sumo config file 
sumo_config_file = r""

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

    step += 1

print(f"Vehicle Count From North to Center: {len(total_vehicle_from_north_to_center)}")
print(f"Vehicle Count To South: {len(total_vehicle_from_center_to_north)}")
traci.close()
