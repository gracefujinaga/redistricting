from pulp import LpProblem, LpVariable, lpSum, LpMinimize, LpBinary
import pandas as pd
import csv
import random


# use 2020 data
pop_df = pd.read_csv('/Users/gracefujinaga/Documents/Northwestern/MSDS_460/redistricting/Assignment_3_Redo/Data/pop_data_2020.csv')

# cook county - 7 districts
# Dupage County - 1 district
# Lake county - 1 district
# thus, 102 -3 = 99 counties
# 17 - 9 = 8 districts

# parse the adjacency list
def parse_illinois_counties_to_adjacency_list(file_path):
    adjacency_list = {}
    current_county = None
    
    with open(file_path, 'r') as file:
        for line in file:
            # Check if it's a main county line (no leading whitespace) and contains "IL"
            if line.startswith('"') and "IL" in line:
                # Extract the main county name and remove ", IL"
                county_name = line.split("\t")[0].strip('"').replace(", IL", "")
                # Initialize an empty list of neighbors for the current county
                adjacency_list[county_name] = []
                current_county = county_name
            elif current_county and "IL" in line:
                # Only add neighboring counties in Illinois and remove ", IL"
                neighbor_county = line.strip().split("\t")[0].strip('"').replace(", IL", "")
                # Add the neighbor only if it's not the same as the current county
                if neighbor_county != current_county:
                    adjacency_list[current_county].append(neighbor_county)
    
    return adjacency_list

# Parse the adjacency data file
adj_list = parse_illinois_counties_to_adjacency_list('/Users/gracefujinaga/Documents/Northwestern/MSDS_460/redistricting/Assignment_3_Redo/Data/adjacency_data.txt')

for county in ['Cook County', 'Lake County', 'DuPage County']:
    adj_list.pop(county)


# Initialize model
model = LpProblem("Redistricting", LpMinimize)

# Parameters
districts = list(range(1, 9))  # 8 districts after we take out those lsited above

# Get counties
counties = pop_df['name']
remove_counties = ['DuPage County', 'Lake County', 'Cook County']
filtered_counties = counties[~counties.isin(remove_counties)]
county_list = filtered_counties.tolist()

# get target population and start with the goal of minimizing the differences here
target_population = sum(pop_df['pop2020'])/ 17  # this should be 17

print(f"target population: {target_population}")

## Kevin's Work

# Decision variables
x = LpVariable.dicts("Assign", [(county, d) for county in counties for d in districts], cat=LpBinary)

# Deviation variables
over_deviation = LpVariable.dicts("OverDev", districts, lowBound=0)
under_deviation = LpVariable.dicts("UnderDev", districts, lowBound=0)

# Objective: Minimize population deviation
model += lpSum(over_deviation[d] + under_deviation[d] for d in districts)

# Constraints
# 1. Each remaining county assigned to exactly one district
for county in county_list:
    model += lpSum(x[(county, d)] for d in districts) == 1

# 2. Population deviation constraints
for d in districts:
    model += (
        lpSum(x[(county, d)] * pop_df.loc[pop_df['name'] == county, 'pop2020'].values[0] for county in county_list) - target_population
        <= over_deviation[d]
    )
    model += (
        target_population
        - lpSum(x[(county, d)] * pop_df.loc[pop_df['name'] == county, 'pop2020'].values[0] for county in county_list)
        <= under_deviation[d]
    )

# 3. compactness
# Adjacency constraint: For each county in the district, at least one other county in the district must be adjacent
for county in county_list:
    for d in districts:
        model += (
            lpSum(x[(neighbor, d)] for neighbor in adj_list.get(county)) >= x[(county, d)],
            f"Adjacency_{county}_District_{d}"
        )

# Solve model
model.solve()

# Output results
print("\nPre-assigned Districts:")
assigned_districts = {
    'Cook County': list(range(9, 16)),
    'DuPage County' : [16],
    'Lake County' : [17]
}

for county in remove_counties:
    preassigned_district = assigned_districts.get(county, "No districts assigned")
    print(f"{county}: Assigned to Districts {preassigned_district}")

print("\nOptimized District Assignments:")
for d in districts:
    district_population = sum(pop_df.loc[pop_df['name'] == county, 'pop2020'].values[0] for county in county_list if x[(county, d)].value() == 1)
    assigned_counties = [county for county in county_list if x[(county, d)].value() == 1]
    print(f"District {d}: Population = {district_population}")
    if assigned_counties:
        print(f"Counties assigned: {', '.join(assigned_counties)}")
    else:
        print("Counties assigned: None")






