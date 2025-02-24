def get_light_durations_from_scenario(scenario_groups):
    for group_name, scenarios in scenario_groups:
        print(f"\nGroup: {group_name}")

        for i, phase in enumerate(scenarios):
            phase_state = phase["str"]  
            phase_duration = phase["duration"] 

            green_count = phase_state.count("G")
            yellow_count = phase_state.count("Y")
            red_count = phase_state.count("r")

            total_lights = len(phase_state)  

            # Calculate actual time for each color
            green_time = (green_count / total_lights) * phase_duration
            yellow_time = (yellow_count / total_lights) * phase_duration
            red_time = (red_count / total_lights) * phase_duration

            print(f"  Phase {i+1}: {phase_state} ({phase_duration}s)")
            print(f"    Green Time: {green_time:.2f}s, Yellow Time: {yellow_time:.2f}s, Red Time: {red_time:.2f}s")

scenario_groups = [
    ("Group 1", [
        {"duration": 60, "str": "GGGYYYrrrrGGGYYYrrrr"},  # North-South straight go + left turn
        {"duration": 60, "str": "rrrrGGGYYYrrrrGGGYYY"},  # East-West straight go + left turn
        {"duration": 60, "str": "GGrrrrrrrrGGrrrrrrrr"},  # North-South right turn only
        {"duration": 60, "str": "rrrrGGrrrrrrrrGGrrrr"},  # East-West right turn only
        {"duration": 60, "str": "GGGYYYYrrrGGGYYYYrrr"},  # North-South left turn only
        {"duration": 60, "str": "rrrGGGYYYYrrrGGGYYYY"},  # East-West left turn only
        {"duration": 60, "str": "GGGrrrrrrrGGGrrrrrrr"},  # All directions straight
        {"duration": 60, "str": "rrrrGGGGGGrrrrGGGGGG"},  # All directions left + right
    ]),
]

get_light_durations_from_scenario(scenario_groups)
