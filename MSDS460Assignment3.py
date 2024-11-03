from pulp import LpProblem, LpVariable, lpSum, LpMinimize, LpBinary
import pandas as pd

#Parsing the adjacency file to get the adjacency list
def parse_adjacency_file(file_path):
    adjacency_list = {}
    with open(file_path, 'r', encoding='ISO-8859-1') as file: #Assisted with ChatGPT, did not know what encoding meant and got an error for this
        current_county = None
        for line in file:
            if line.startswith('"'):
                current_county = line.split("\t")[0].strip('"')
                adjacency_list[current_county] = []
            elif current_county:
                neighbor = line.strip().split("\t")[0].strip('"')
                adjacency_list[current_county].append(neighbor)
    return adjacency_list

#Load pop data
pop_data = pd.read_csv('pop_data.csv')
county_population = pop_data.set_index('county')['pop2024'].to_dict()
total_population = sum(county_population.values())

#Parameters
num_districts = 17
target_population = total_population / num_districts
counties = list(county_population.keys())
districts = range(1, num_districts + 1)

#Adjacency list
adjacency_list = parse_adjacency_file('county_adjacency.txt') 

#Optimization model
model = LpProblem("IL_Congressional_Redistricting", LpMinimize)

#Decision variable: x[(county, district)] = 1 if county is in district
x = LpVariable.dicts("x", [(county, d) for county in counties for d in districts], cat=LpBinary)

#Aux variables for absolute deviation in population
pop_diff = LpVariable.dicts("pop_diff", districts, lowBound=0, cat="Continuous")

#Objective: minimize absolute deviation from target population across districts
model += lpSum(pop_diff[d] for d in districts)

#Constraint 1: population balance within districts
for d in districts:
    district_population = lpSum(x[(county, d)] * county_population[county] for county in counties)
    model += district_population - target_population <= pop_diff[d]
    model += target_population - district_population <= pop_diff[d]

#Constraint 2: each county must be assigned to exactly one district
for county in counties:
    model += lpSum(x[(county, d)] for d in districts) == 1

#Constraint 3: adjacent counties in the same district
for d in districts:
    for county in counties:
        neighbors = adjacency_list.get(county, [])
        #If a county is assigned to a district, at least one of its neighbors must also be in the same district
        if neighbors:
            model += lpSum(x[(neighbor, d)] for neighbor in neighbors if neighbor in counties) >= x[(county, d)]

#Solve model
model.solve()

#Output
print("Optimal County Assignments to Districts:")
for county in counties:
    for d in districts:
        if x[(county, d)].value() == 1:
            print(f"{county} is assigned to District {d}")
