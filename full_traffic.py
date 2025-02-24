import traci
from traci import simulation
import json
import os
import time
import csv
import best_scenarios
import get_best_scenarios
import pandas as pd

sumo_binary = "sumo"
# sumo_config_file = r"/Users/ull/Documents/GRA/TRAFFIC-Project/SUMO Files/Bellevue_116th_NE12th_2017-09-11_14-08-35_Full/sumo_config.sumocfg"
# sumo_config_file = r"/Users/ull/Documents/GRA/TRAFFIC-Project/SUMO Files/Bellevue_116th_NE12th__2017-09-11_08-08-50_Full/sumo_config.sumocfg"

file_name = "Synthesized_1Min"

# scenario_groups = [
# # ("Static", [
# #     {"duration": 30, "str": "GGGGGrrrrrGGGGGrrrrr", "traffic_light": "Green", "road": "NS"},
# #     {"duration": 5, "str": "YYYYYrrrrrYYYYYrrrrr", "traffic_light": "Yellow", "road": "NS"},
# #     {"duration": 25, "str": "rrrrrGGGGGrrrrrGGGGG", "traffic_light": "Green", "road": "EW"},
# # ]),

# ("Static", [
#        {"duration": 30, "str": "GGGGGrrrrrGGGGGrrrrr", "traffic_light": "Green", "road": "NS"},
#        {"duration": 5, "str": "YYYYYrrrrrYYYYYrrrrr", "traffic_light": "Yellow", "road": "NS"},
#        {"duration": 25, "str": "rrrrrGGGGGrrrrrGGGGG", "traffic_light": "Green", "road": "EW"},
#        {"duration": 5, "str": "rrrrrYYYYYrrrrrYYYYY", "traffic_light": "Yellow", "road": "EW"}
#    ]),

# ("7", [
#     {"duration": 4, "str": "GGGGGrrrrrGGGGGrrrrr", "traffic_light": "Green", "road": "NS"},
#     {"duration": 5, "str": "YYYYYrrrrrYYYYYrrrrr", "traffic_light": "Yellow", "road": "NS"},
#     {"duration": 46, "str": "rrrrrGGGGGrrrrrGGGGG", "traffic_light": "Green", "road": "EW"},
#     {"duration": 5, "str": "rrrrrYYYYYrrrrrYYYYY", "traffic_light": "Yellow", "road": "EW"}
# ]),

# ("6", [
#     {"duration": 7, "str": "GGGGGrrrrrGGGGGrrrrr", "traffic_light": "Green", "road": "NS"},
#     {"duration": 5, "str": "YYYYYrrrrrYYYYYrrrrr", "traffic_light": "Yellow", "road": "NS"},
#     {"duration": 43, "str": "rrrrrGGGGGrrrrrGGGGG", "traffic_light": "Green", "road": "EW"},
#     {"duration": 5, "str": "rrrrrYYYYYrrrrrYYYYY", "traffic_light": "Yellow", "road": "EW"}
# ]),

# ("5", [
#     {"duration": 10, "str": "GGGGGrrrrrGGGGGrrrrr", "traffic_light": "Green", "road": "NS"},
#     {"duration": 5, "str": "YYYYYrrrrrYYYYYrrrrr", "traffic_light": "Yellow", "road": "NS"},
#     {"duration": 40, "str": "rrrrrGGGGGrrrrrGGGGG", "traffic_light": "Green", "road": "EW"},
#     {"duration": 5, "str": "rrrrrYYYYYrrrrrYYYYY", "traffic_light": "Yellow", "road": "EW"}
# ]),

# ("4", [
#     {"duration": 13, "str": "GGGGGrrrrrGGGGGrrrrr", "traffic_light": "Green", "road": "NS"},
#     {"duration": 5, "str": "YYYYYrrrrrYYYYYrrrrr", "traffic_light": "Yellow", "road": "NS"},
#     {"duration": 37, "str": "rrrrrGGGGGrrrrrGGGGG", "traffic_light": "Green", "road": "EW"},
#     {"duration": 5, "str": "rrrrrYYYYYrrrrrYYYYY", "traffic_light": "Yellow", "road": "EW"}
# ]),

# ("3", [
#     {"duration": 16, "str": "GGGGGrrrrrGGGGGrrrrr", "traffic_light": "Green", "road": "NS"},
#     {"duration": 5, "str": "YYYYYrrrrrYYYYYrrrrr", "traffic_light": "Yellow", "road": "NS"},
#     {"duration": 34, "str": "rrrrrGGGGGrrrrrGGGGG", "traffic_light": "Green", "road": "EW"},
#     {"duration": 5, "str": "rrrrrYYYYYrrrrrYYYYY", "traffic_light": "Yellow", "road": "EW"}
# ]),

#  ("2", [
#     {"duration": 19, "str": "GGGGGrrrrrGGGGGrrrrr", "traffic_light": "Green", "road": "NS"},
#     {"duration": 5, "str": "YYYYYrrrrrYYYYYrrrrr", "traffic_light": "Yellow", "road": "NS"},
#     {"duration": 31, "str": "rrrrrGGGGGrrrrrGGGGG", "traffic_light": "Green", "road": "EW"},
#     {"duration": 5, "str": "rrrrrYYYYYrrrrrYYYYY", "traffic_light": "Yellow", "road": "EW"}
# ]),

# ("1", [
#     {"duration": 22, "str": "GGGGGrrrrrGGGGGrrrrr", "traffic_light": "Green", "road": "NS"},
#     {"duration": 5, "str": "YYYYYrrrrrYYYYYrrrrr", "traffic_light": "Yellow", "road": "NS"},
#     {"duration": 28, "str": "rrrrrGGGGGrrrrrGGGGG", "traffic_light": "Green", "road": "EW"},
#     {"duration": 5, "str": "rrrrrYYYYYrrrrrYYYYY", "traffic_light": "Yellow", "road": "EW"}
# ]),



# ("11", [
#     {"duration": 28, "str": "GGGGGrrrrrGGGGGrrrrr", "traffic_light": "Green", "road": "NS"},
#     {"duration": 5, "str": "YYYYYrrrrrYYYYYrrrrr", "traffic_light": "Yellow", "road": "NS"},
#     {"duration": 22, "str": "rrrrrGGGGGrrrrrGGGGG", "traffic_light": "Green", "road": "EW"},
#     {"duration": 5, "str": "rrrrrYYYYYrrrrrYYYYY", "traffic_light": "Yellow", "road": "EW"}
# ]),

# ("12", [
#     {"duration": 31, "str": "GGGGGrrrrrGGGGGrrrrr", "traffic_light": "Green", "road": "NS"},
#     {"duration": 5, "str": "YYYYYrrrrrYYYYYrrrrr", "traffic_light": "Yellow", "road": "NS"},
#     {"duration": 19, "str": "rrrrrGGGGGrrrrrGGGGG", "traffic_light": "Green", "road": "EW"},
#     {"duration": 5, "str": "rrrrrYYYYYrrrrrYYYYY", "traffic_light": "Yellow", "road": "EW"}
# ]),

# ("13", [
#     {"duration": 34, "str": "GGGGGrrrrrGGGGGrrrrr", "traffic_light": "Green", "road": "NS"},
#     {"duration": 5, "str": "YYYYYrrrrrYYYYYrrrrr", "traffic_light": "Yellow", "road": "NS"},
#     {"duration": 16, "str": "rrrrrGGGGGrrrrrGGGGG", "traffic_light": "Green", "road": "EW"},
#     {"duration": 5, "str": "rrrrrYYYYYrrrrrYYYYY", "traffic_light": "Yellow", "road": "EW"}
# ]),

# ("13", [
#     {"duration": 37, "str": "GGGGGrrrrrGGGGGrrrrr", "traffic_light": "Green", "road": "NS"},
#     {"duration": 5, "str": "YYYYYrrrrrYYYYYrrrrr", "traffic_light": "Yellow", "road": "NS"},
#     {"duration": 13, "str": "rrrrrGGGGGrrrrrGGGGG", "traffic_light": "Green", "road": "EW"},
#     {"duration": 5, "str": "rrrrrYYYYYrrrrrYYYYY", "traffic_light": "Yellow", "road": "EW"}
# ]),

# ("14", [
#     {"duration": 40, "str": "GGGGGrrrrrGGGGGrrrrr", "traffic_light": "Green", "road": "NS"},
#     {"duration": 5, "str": "YYYYYrrrrrYYYYYrrrrr", "traffic_light": "Yellow", "road": "NS"},
#     {"duration": 10, "str": "rrrrrGGGGGrrrrrGGGGG", "traffic_light": "Green", "road": "EW"},
#     {"duration": 5, "str": "rrrrrYYYYYrrrrrYYYYY", "traffic_light": "Yellow", "road": "EW"}
# ]),


# ("15", [
#     {"duration": 43, "str": "GGGGGrrrrrGGGGGrrrrr", "traffic_light": "Green", "road": "NS"},
#     {"duration": 5, "str": "YYYYYrrrrrYYYYYrrrrr", "traffic_light": "Yellow", "road": "NS"},
#     {"duration": 7, "str": "rrrrrGGGGGrrrrrGGGGG", "traffic_light": "Green", "road": "EW"},
#     {"duration": 5, "str": "rrrrrYYYYYrrrrrYYYYY", "traffic_light": "Yellow", "road": "EW"}
# ]),

# ("16", [
#     {"duration": 46, "str": "GGGGGrrrrrGGGGGrrrrr", "traffic_light": "Green", "road": "NS"},
#     {"duration": 5, "str": "YYYYYrrrrrYYYYYrrrrr", "traffic_light": "Yellow", "road": "NS"},
#     {"duration": 4, "str": "rrrrrGGGGGrrrrrGGGGG", "traffic_light": "Green", "road": "EW"},
#     {"duration": 5, "str": "rrrrrYYYYYrrrrrYYYYY", "traffic_light": "Yellow", "road": "EW"}
# ]),


# ]

# # # For 1 Min
scenario_groups = [
# # Standard NS & EW Split Timing
#    ("Static", [
#        {"duration": 30, "str": "GGGGGrrrrrGGGGGrrrrr", "traffic_light": "Green", "road": "NS"},
#        {"duration": 5, "str": "YYYYYrrrrrYYYYYrrrrr", "traffic_light": "Yellow", "road": "NS"},
#        {"duration": 25, "str": "rrrrrGGGGGrrrrrGGGGG", "traffic_light": "Green", "road": "EW"},
#        {"duration": 5, "str": "rrrrrYYYYYrrrrrYYYYY", "traffic_light": "Yellow", "road": "EW"}
#    ]),

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
   {"duration": 5, "str": "YYYYYrrrrrrrrrrrrrrr", "traffic_light": "Yellow", "road": "N"},
   {"duration": 15, "str": "rrrrrGGGGGrrrrrrrrrr", "traffic_light": "Green", "road": "S"},
   {"duration": 5, "str": "rrrrrYYYYYrrrrrrrrrr", "traffic_light": "Yellow", "road": "S"},
   {"duration": 15, "str": "rrrrrrrrrrGGGGGrrrrr", "traffic_light": "Green", "road": "E"},
   {"duration": 5, "str": "rrrrrrrrrrYYYYYrrrrr", "traffic_light": "Yellow", "road": "E"}
    ]),

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
remaining_vehicles= {}


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



def run_scenario_with_dynamic_lights(junction_id, total_simulation_steps, phase_durations, change_interval, group_id, video_index, inject, cropping_time_in_minutes):
    """
    Run the simulation with dynamic phase changes at each interval.
    
    :param junction_id: The ID of the traffic light junction.
    :param total_simulation_steps: The total simulation steps to run.
    :param phase_durations: List of tuples [(green_duration, yellow_duration, red_duration), ...]
    :param change_interval: How often to change the traffic light phases (in steps).
    """
    dynamic_value = f"Video_{video_index}"  # Replace with your dynamic value
    sumo_config_file = fr"/Users/ull/Documents/GRA/TRAFFIC-Project/SUMO Files/sumo_configuration_files/Synthesized-1/{cropping_time_in_minutes}Min/{dynamic_value}/sumo_config.sumocfg"

    max_retries = 5
    retry_delay = 1  # seconds
    scale_factor = 3

    def kill_sumo():
        os.system("pkill -f sumo")

    for attempt in range(max_retries):
        try:
            print(f"Starting SUMO, attempt {attempt + 1}/{max_retries}")
            kill_sumo()  # Kill any previous stuck SUMO instance
            time.sleep(1)
            traci.start([sumo_binary, "-c", sumo_config_file])
            traci.simulation.setScale(scale_factor)
            
            break  # Exit loop if successful
        except Exception as e:
            print(f"Error: {e}")
            print(f"Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
    else:
        print("Failed to start SUMO after multiple attempts.")

    change = False
    current_step = 0
    interval_index = 0  # Start with the first phase configuration
    total_intervals = len(phase_durations)

    global vehiclesToWest, vehiclesToEast, vehiclesToNorth, vehiclesToSouth, vehicle_time_tracking, remaining_vehicle, green_light_vehicle_counts, vehiclesToEast, vehiclesToNorth, vehiclesToSouth, vehiclesToWest 
    green_light_vehicle_counts = {}
    vehiclesToWestAll = set()
    # vehiclesToEastAll = set()
    vehiclesToNorthAll = set()
    vehiclesToSouthAll = set()
    vehiclesToEast = set()
    vehiclesToWest = set()
    vehiclesToNorth = set()
    vehiclesToSouth = set()

    set_traffic_lights(phase_durations)

    if inject:
        inject_remaining_vehicles(video_index, group_id)
   
    traffic_flow = {}
    veh_time = {}
    idx_count = 0
    
    while current_step <= change_interval:
        traci.simulationStep()
        traffic_flow = get_veh_count(interval_index-1, current_step, idx_count)
        veh_time = get_veh_time(interval_index-1, current_step, idx_count, change, group_id)

        change = False  
        
        current_step += 1

    if current_step == change_interval + 1:
        print(f"Done with {change_interval} seconds ---- Run next scenario ")
        print("Getting the vehicle information: ")
        get_vehicle_information(video_index, group_id)
        vehiclesToEastAll = set()

    traci.close()
    return traffic_flow, veh_time

def get_veh_count(interval_index, step, idx_count):
    junction_ids = traci.trafficlight.getIDList()

    for junction_id in junction_ids:
        vehicle_ids = traci.vehicle.getIDList()

        for vehicle_id in vehicle_ids:
            lane_id = traci.vehicle.getLaneID(vehicle_id)

            if vehicle_id not in vehiclesToEastAll and vehicle_id not in vehiclesToWestAll and vehicle_id not in vehiclesToNorthAll and vehicle_id not in vehiclesToSouthAll:
                if lane_id.startswith(":center_") or lane_id.startswith("center_to_"):
                    vehiclesToEastAll.add(vehicle_id)
                    vehiclesToEast.add(vehicle_id)  

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

def get_veh_time(interval_index, step, idx_count, phase_change, group_id):
    global vehicle_time_tracking
    vehicle_ids = traci.vehicle.getIDList()  

    if phase_change:
        if vehicle_time_tracking is not None:
            for veh in list(vehicle_time_tracking.keys()):  
                if veh in vehicle_time_tracking:
                    if "end" not in vehicle_time_tracking[veh] and vehicle_time_tracking[veh]["traffic_scenario"] == idx_count - 1:
                        vehicle_time_tracking[veh]["start"] = step
                        vehicle_time_tracking[veh]["traffic_scenario"] = idx_count


    if vehicle_time_tracking is not None:
        for veh in list(vehicle_time_tracking.keys()):  
            if veh not in vehicle_ids:
                if "captured" not in vehicle_time_tracking[veh]: 
                    vehicle_time_tracking[veh]["end"] = step 
                    vehicle_time_tracking[veh]["captured"] = True


    for vehicle_id in vehicle_ids:
        vehicle_position = traci.vehicle.getPosition(vehicle_id)
        lane_id = traci.vehicle.getLaneID(vehicle_id)

        if vehicle_id not in vehicle_time_tracking:
            if lane_id in ["west_to_center_0", "west_to_center_1", "west_to_center_2", "west_to_center_3",
                            "east_to_center_0", "east_to_center_1", "east_to_center_2",
                            "north_to_center_0", "north_to_center_1", "north_to_center_2",
                            "south_to_center_0", "south_to_center_1", "south_to_center_2"]:
                vehicle_time_tracking[vehicle_id] = {"start": step}
                vehicle_time_tracking[vehicle_id]["traffic_scenario"] = idx_count
                vehicle_time_tracking[vehicle_id]["group_id"] = group_id

                

    return vehicle_time_tracking

def save_avg_and_throughput_to_csv(traffic_flow_data, veh_time, scenarios, group_id):
    global scenario_stats
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

    average_time_per_scenario = {
        scenario: stats['total_time'] / stats['vehicle_count'] if stats['vehicle_count'] > 0 else 0
        for scenario, stats in scenario_time_stats.items()
    }

    throughput = 0
    for x in range(len(traffic_flow_data)):
        scenario_id = x % len(scenarios)
        scenario_description = scenarios

        average_time = average_time_per_scenario.get(x, 0)

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
            'scenario_id': scenario_id,
            'idx_count':x,
        }


def get_light_durations_from_scenario(phase):
        
        phase_state = phase["str"]
        phase_duration = phase["duration"]  

        # Count occurrences of each light state
        green_count = phase_state.count("G")
        yellow_count = phase_state.count("Y")
        red_count = phase_state.count("r")

        total_lights = len(phase_state)  

        # Calculate actual time for each color
        green_time = (green_count / total_lights) * phase_duration
        yellow_time = (yellow_count / total_lights) * phase_duration
        red_time = (red_count / total_lights) * phase_duration

        scenario_desc = f"Green: {green_time:.2f}, Yellow: {yellow_time:.2f}, Red: {red_time:.2f}"

        return scenario_desc


prev_video_index = 1
def run_all_scenarios(scenario_groups, video_index, cropping_time_in_minutes, inject):
    

    global vehiclesToWestAll, vehiclesToEastAll, vehiclesToSouthAll, vehiclesToNorthAll, green_light_vehicle_counts
    total_simulation_steps = 5000  # e.g., run for 600 steps (10 minutes)
    change_interval = 60 

    for group_id, scenario_group in enumerate(scenario_groups):
        green_light_vehicle_counts = {}
        group_id = scenario_group[0]
        scenario_group =  scenario_group[1]

        # Run the simulation with dynamic phase changes
        traffic_flow, veh_time = run_scenario_with_dynamic_lights("center", total_simulation_steps, scenario_group, change_interval, group_id, video_index, inject, cropping_time_in_minutes)

        save_avg_and_throughput_to_csv(traffic_flow, veh_time, scenario_group, group_id)
        vehiclesToWestAll = set()
        vehiclesToEastAll = set()
        vehiclesToNorthAll = set()
        vehiclesToSouthAll = set()



def get_vehicle_information(video_index, group_id):
    global vehiclesToEastAll
    data = {}
    global remaining_vehicles
    vehicle_ids = traci.vehicle.getIDList()
    
    
    for vehicle_id in vehicle_ids:
        if vehicle_id not in vehiclesToEastAll:
            speed = traci.vehicle.getSpeed(vehicle_id)
            position = traci.vehicle.getPosition(vehicle_id)
            route_id = traci.vehicle.getRouteID(vehicle_id)
            lane_id = traci.vehicle.getLaneID(vehicle_id)
            edge_id = traci.vehicle.getRoadID(vehicle_id)
            lane_index = traci.vehicle.getLaneIndex(vehicle_id)
            pos = traci.vehicle.getLanePosition(vehicle_id)
            if lane_id != "center_to_east_0" and lane_id != "center_to_east_1" and lane_id != "center_to_west_0" and lane_id != "center_to_west_1" and lane_id != "center_to_north_0" and lane_id != "center_to_north_1" and lane_id != "center_to_south_0" and lane_id != "center_to_south_1":
                data[vehicle_id] = {
                    "speed": speed,
                    "position": position,
                    "route_id": route_id,
                    "lane_id": lane_id,
                    "edge_id": edge_id,
                    "lane_index":lane_index,
                    "lane_position": pos,
                }

                remaining_vehicles[group_id] = data


def inject_remaining_vehicles(video_index, group_id):
    global remaining_vehicles
    if group_id in remaining_vehicles:
        for vehicle_id, data in remaining_vehicles[group_id].items():
            vehicle_id = f"old_+{vehicle_id}"
            traci.vehicle.add(vehID=vehicle_id, routeID=data["route_id"], departPos=str(data["lane_position"]), departSpeed=str(data["speed"]))
            traci.vehicle.moveToXY(vehID=vehicle_id, edgeID=data["edge_id"], laneIndex=data["lane_index"], x=data["position"][0], y=data["position"][1])
        del remaining_vehicles[group_id]


if __name__ == "__main__":
    throughput_final = []
    time_final = []
    total_simulation_steps = 600  
    change_interval = 60  
    cropping_time_in_minutes = 1
    inject = False


    for i in range(60):
        run_all_scenarios(scenario_groups, i + 1, cropping_time_in_minutes, inject)

        path = f"files/Synthesized-1/new/full_{cropping_time_in_minutes}/{file_name}_{i}.csv"
        with open(path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Scenario_ID', 'Group_ID', 'Scenario_Description' ,'Average_Travel_Time', 'Throughput', 'Idx_Count'])
            
            for scenario, stats in scenario_stats.items():
                writer.writerow([stats['scenario_id'], stats['group_id'], stats['scenario_description'],stats['average_time'], stats['throughput'], stats['idx_count']])

        print("Saved average time and throughput to 'scenario_stats.csv'")

        # Get the best scenario
        print("Need to get best scenario here....")

        # Get the best scenario, throughput and time for each cropped video
        best_throughout, best_time = get_best_scenarios.analyze_traffic_scenarios(path, i + 1)

        throughput_final.append(best_throughout)
        time_final.append(best_time)

        inject = True

    final_df_throughput = pd.concat(throughput_final, ignore_index=True)
    final_df_time = pd.concat(time_final, ignore_index=True)

    # Save to a CSV file
    folder_path = 'best_scenarios/updated'  
    final_df_throughput.to_csv(f'{folder_path}/best_throughput_{file_name}.csv', index=False)
    final_df_time.to_csv(f'{folder_path}/best_time_{file_name}.csv', index=False)

    print("File saved successfully.")
        
        

