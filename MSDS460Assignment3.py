from pulp import LpProblem, LpVariable, lpSum, LpMinimize, LpBinary
import pandas as pd
import csv
import random

#Parse adjacency file to get the adjacency list
def parse_adjacency_file(file_path):
    adjacency_list = {}
    current_county = None
    
    with open(file_path, 'r', encoding='ISO-8859-1') as file:
        for line in file:
            # Check if it's a main county line (no leading whitespace) and contains "IL"
            if line.startswith('"') and "IL" in line:
                # Extract the main county name and ensure it’s from Illinois
                county_name = line.split("\t")[0].strip('"')
                if "IL" in county_name:
                    adjacency_list[county_name] = []
                    current_county = county_name
                else:
                    current_county = None  # Ignore counties not in Illinois
            
            # If we have a current Illinois county, look for Illinois neighbors
            elif current_county and line.startswith('\t') and "IL" in line:
                # Only add neighboring counties in Illinois
                neighbor_county = line.strip().split("\t")[0].strip('"')
                if "IL" in neighbor_county:
                    adjacency_list[current_county].append(neighbor_county)
    
    # Filter out any non-Illinois entries if they accidentally got included
    adjacency_list = {county: neighbors for county, neighbors in adjacency_list.items() if "IL" in county}
    
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

#Constraint 3: adjacency constraint to enforce contiguity
MIN_NEIGHBORS_IN_SAME_DISTRICT = 2  # Increase this to enforce stronger contiguity

for d in districts:
    for county in counties:
        neighbors = adjacency_list.get(county, [])
        #Require that each county assigned to a district has multiple neighbors in the same district
        if neighbors:
            model += lpSum(x[(neighbor, d)] for neighbor in neighbors if neighbor in counties) >= MIN_NEIGHBORS_IN_SAME_DISTRICT * x[(county, d)]



#Solve model
model.solve()

#Collect results and check for any unassigned counties
district_assignments = {}
for county in counties:
    assigned_to_district = False
    for d in districts:
        if x[(county, d)].value() == 1:
            district_assignments[county] = d
            assigned_to_district = True
    if not assigned_to_district:
        print(f"Warning: {county} was not assigned to any district.")

#printing and saving district assignments
print("Optimal County Assignments to Districts:")
for county in counties:
    if county in district_assignments:
        print(f"{county} is assigned to District {district_assignments[county]}")
    else:
        print(f"{county} is not assigned to any district")


#Write output to txt file
with open("redistricting_output.txt", "w") as f:
    f.write("Optimal County Assignments to Districts:\n")
    for county in counties:
        for d in districts:
            if x[(county, d)].value() == 1:
                f.write(f"{county} is assigned to District {d}\n")


#Turn districtr to csv so we can import into districtr
with open("redistricting_districtr.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["County", "District"])
    for county, district in district_assignments.items():
        writer.writerow([county, district])
