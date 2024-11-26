from pulp import LpProblem, LpVariable, lpSum, LpMinimize, LpBinary
import pandas as pd
import csv
import random

# use 2020 data
pop_df = pd.read_csv('/Users/gracefujinaga/Documents/Northwestern/MSDS_460/redistricting/Assignment_3_Redo/Data/pop_data_2020.csv')

def parse_illinois_counties_to_adjacency_list(file_path):
    adjacency_list = {}
    current_county = None
    
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split("\t")
            if len(parts) >= 2 and "IL" in line and line.startswith('"'):
                county_name = parts[0].strip('"').replace(", IL", "")
                current_county = county_name
                
                if county_name not in adjacency_list:
                    adjacency_list[county_name] = []
                
                neighbor_county = parts[2].strip('"').replace(", IL", "")
                if neighbor_county != current_county:
                    adjacency_list[county_name].append(neighbor_county)

            elif current_county and "IL" in line:
                neighbor_county = line.strip().split("\t")[0].strip('"').replace(", IL", "")
                if neighbor_county != current_county:
                    adjacency_list[current_county].append(neighbor_county)
    
    return adjacency_list

# Parse the adjacency data file
adj_list = parse_illinois_counties_to_adjacency_list('/Users/gracefujinaga/Documents/Northwestern/MSDS_460/redistricting/Assignment_3_Redo/Data/adjacency_data.txt')

# Remove specified counties
for county in ['Cook County', 'Lake County', 'DuPage County']:
    adj_list.pop(county)

# Initialize the model
model = LpProblem("Redistricting", LpMinimize)

# Parameters
districts = list(range(1, 9))  # 8 districts after we take out the specified ones

# Get counties
counties = pop_df['name']
remove_counties = ['DuPage County', 'Lake County', 'Cook County']
filtered_counties = counties[~counties.isin(remove_counties)]
county_list = filtered_counties.tolist()

# Get target population
target_population = sum(pop_df['pop2020']) / 17

# Decision variables for assigning counties to districts
x = LpVariable.dicts("Assign", [(county, d) for county in counties for d in districts], cat=LpBinary)

# Deviation variables for population balancing
over_deviation = LpVariable.dicts("OverDev", districts, lowBound=0)
under_deviation = LpVariable.dicts("UnderDev", districts, lowBound=0)

# Objective: Minimize population deviation
model += lpSum(over_deviation[d] + under_deviation[d] for d in districts)

# Constraints: Ensure each county is assigned to exactly one district
for county in county_list:
    model += lpSum(x[(county, d)] for d in districts) == 1

# Population deviation constraints for each district
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

# Connectivity Constraints
y = LpVariable.dicts("Adjacency", [(i, j, d) for i in county_list for j in adj_list.get(i, []) for d in districts], cat=LpBinary)

# Ensure if a county is assigned to a district, its neighbors must be assigned to the same district (and vice versa)
for county in county_list:
    for d in districts:
        for neighbor in adj_list.get(county, []):
            model += (
                y[(county, neighbor, d)] <= x[(county, d)],  # If county is assigned to district, neighbor must also be assigned
                f"Adjacency_1_{county}_{neighbor}_District_{d}"
            )
            model += (
                y[(county, neighbor, d)] <= x[(neighbor, d)],  # If neighbor is assigned to district, county must also be assigned
                f"Adjacency_2_{county}_{neighbor}_District_{d}"
            )
            model += (
                y[(county, neighbor, d)] >= x[(county, d)] + x[(neighbor, d)] - 1,  # If one is assigned, the other must be too
                f"Adjacency_connectivity_{county}_{neighbor}_District_{d}"
            )

# Flow constraints to ensure connectedness
for county in county_list:
    for d in districts:
        flow_constraint_name = f"Flow_{county}_District_{d}"
        model += (
            lpSum(y[(county, neighbor, d)] for neighbor in adj_list.get(county, [])) >= x[(county, d)],  # Propagate flow from county to neighbors
            flow_constraint_name
        )

# Solve the model
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
