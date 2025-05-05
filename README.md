# DiTAT

## Project Overview

The simulation analyzes various traffic light scenarios to identify optimal timing patterns that maximize throughput and minimize travel time. It processes video of a real intersection and runs different traffic light timing scenarios.

## Prerequisites

- SUMO (version 1.8.0 or higher)
- Python 3.7+
- Required Python packages: traci, pandas

## Installation

### 1. Install SUMO

#### macOS:
```bash
brew install --cask sumo
```

#### Ubuntu/Debian:
```bash
sudo apt-get update
sudo apt-get install sumo sumo-tools sumo-doc
```

#### Windows:
1. Download the installer from the [SUMO website](https://www.eclipse.org/sumo/)
2. Run the installer and follow the instructions
3. Add SUMO_HOME environment variable pointing to your installation directory

### 2. Install Python Dependencies

```bash
pip install traci pandas matplotlib
```

### 3. Clone the Repository

```bash
git clone https://github.com/reetipd/SumoFiles
```

## Project Structure

```
project_root/
├── script_with_min_sumo_startup_time.py   # Main simulation script with SUMO startup time optimization
├── full_traffic.py                        # Main simulation script without SUMO startup time optimization
├── static_sum.py                          # Calculate metrics for static traffic light patterns
├── reactive_max_diff_cycle.py             # Calculate metrics for different cycle times
├── reactive_appraoch_same_cycle.py        # Calculate metrics using same cycle approach
├── get_best_scenarios.py                  # Analysis to identify best scenarios from simulation results
├── get_best_scenarios_final.py            # Final aggregation of best scenarios across all simulations
├── best_scenarios/                        # Directory containing best scenario data
│   └── updated/                           # Latest best scenario results
│       ├── best_throughput_*.csv          # Files with best throughput results
│       └── best_time_*.csv                # Files with best travel time results
├── files/                                 # Directory for simulation results and data
│   ├── results/                         
│   │   ├── 1_Min/                         # Results for 1-minute simulations
│   │   ├── 2_Min/                         # Results for 2-minute simulations
│   │   ├── 3_Min/                         # Results for 3-minute simulations
│   │   └── 4_Min/                         # Results for 4-minute simulations
│   └── [other intersection data / results folders]
└── sumo_configuration_files/              # SUMO configuration files organized by intersection
    └── Bellevue_116th_NE12th__2017-09-10_19-08-25/  # Configuration for specific intersection
        ├── 1Min/                          # 1-minute simulation configurations
        │   ├── Video_1/                   # Configuration for video segment 1
        │   │   ├── sumo_config.sumocfg    # SUMO configuration file
        │   │   └── route.rou.xml          # Traffic route definitions
        │   ├── Video_2/                   # Configuration for video segment 2
        │   
        ├── 2Min/                          # 2-minute simulation configurations
        ├── 3Min/                          # 3-minute simulation configurations
        └── 4Min/                          # 4-minute simulation configurations
```

## Usage

### Main Simulation

Run the main simulation script:

```bash
python script_with_min_sumo_startup_time.py

or 

python full_traffic.py
```

The script will:
1. Initialize SUMO
2. Load route files for each video segment
3. Run multiple traffic light timing scenarios on each video
4. Generate CSV files with results

### Important Notes for Running the Simulation

- **Scenario Settings**: Make sure to adjust the scenario settings for different cycle times. Otherwise, the simulation will repeat the same scenario until the cycle time is reached.

### Analyzing Best Scenarios (Diff Cycle and Setting Time)

P.S. We aren't directly using the `get_best_scenarios.py` or files from best_scenarios becuase we are considerig different cases.

After running the simulation, use the `reactive_max_diff_cycle.py` script to analyze and determine the best traffic light timing patterns having different cycle and setting time:

```bash
python reactive_max_diff_cycle.py
```

Note: You may need to send 3 parameters: 
--folder_path: Directory path containing the CSV files
--file_name: Base name of the CSV files (without _X.csv)
--num_files: Number of intervals to process


### Analyzing Best Scenarios (Same Cycle and Setting Time)

After running the simulation, use the `reactive_appraoch_same_cycle.py` script to analyze and determine the best traffic light timing patterns having same cycle and setting time:

```bash
python reactive_appraoch_same_cycle.py
```

Note: You may need to send 3 parameters: 
--folder_path: Directory path containing the CSV files
--file_name: Base name of the CSV files (without _X.csv)
--num_files: Number of intervals to process


### Static Sum Calculations

To calculate static sum metrics for comparison, run:

```bash
python static_sum.py
```

This script provides aggregate metrics for the static traffic light patterns.

Note: You may need to send 3 parameters: 
--folder_path: Directory path containing the CSV files
--file_name: Base name of the CSV files (without _X.csv)
--num_files: Number of intervals to process

## Traffic Light Scenarios

The code includes 20+1 predefined traffic light timing scenarios, each with different phase durations and patterns. These scenarios include:

- Basic static patterns
- Patterns with left-turn phases
- Patterns prioritizing north-south or east-west traffic
- Various combinations of green, yellow, and left-turn phases

Each scenario is evaluated based on:
- Vehicle throughput (number of vehicles passing through the intersection)
- Average travel time for vehicles to travel from starting of the frame to the end of the frame 

## Output


## Customization

To add or modify traffic light patterns, edit the `scenario_groups` list in the `main()` function with additional timing patterns.

Each scenario requires:
- A unique name ("GroupX")
- A list of phase dictionaries with:
  - "duration": Time in seconds
  - "str": Light pattern (G=green, Y=yellow, r=red)
  - "traffic_light": Phase description
  - "road": Direction (NS, EW, etc.)


To use SUMO GUI, use the `sumo_binary=sumo-gui` else `sumo_binary=sumo`. While using the GUI case, we need to close the SUMO and re-run it ourself all the time. But, using non-GUI version, it works by itself (no manual intervention).

## Troubleshooting

- **SUMO Not Found**: Ensure SUMO is installed and added to your PATH
- **Missing Dependencies**: Install all required Python packages
- **File Permissions**: Ensure write access to output directories
- **Route File Issues**: Verify your route.rou.xml files are correctly formatted
- **Path Issues**: Check that all file paths are correctly specified for your OS
