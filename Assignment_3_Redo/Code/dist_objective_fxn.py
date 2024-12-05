from pulp import LpProblem, LpVariable, lpSum, LpMinimize, LpBinary
import pandas as pd
import csv

# Load data
pop_df = pd.read_csv('/Users/gracefujinaga/Documents/Northwestern/MSDS_460/redistricting/Assignment_3_Redo/Data/pop_data_2020.csv')

# Parse the adjacency data file
def parse_illinois_counties_to_adjacency_list(file_path):
    adjacency_list = {}
    current_county = None
    
    with open(file_path, 'r') as file:
        for line in file:
            # Remove leading/trailing whitespace and split by tab
            parts = line.strip().split("\t")
            
            if len(parts) >= 2 and "IL" in line and line.startswith('"'):
                # Main county is the first part
                county_name = parts[0].strip('"').replace(", IL", "")
                current_county = county_name
                
                # Initialize the adjacency list for the current county
                if county_name not in adjacency_list:
                    adjacency_list[county_name] = []
                
                # Loop through the rest of the parts (neighbor counties)
                neighbor_county = parts[2].strip('"').replace(", IL", "")
                if neighbor_county != current_county:
                    adjacency_list[county_name].append(neighbor_county)

            elif current_county and "IL" in line:
                # Only add neighboring counties in Illinois and remove ", IL"
                neighbor_county = line.strip().split("\t")[0].strip('"').replace(", IL", "")
                # Add the neighbor only if it's not the same as the current county
                if neighbor_county != current_county:
                    adjacency_list[current_county].append(neighbor_county)
    
    return adjacency_list

# Assuming adjacency data file is located in the correct directory
adj_list = parse_illinois_counties_to_adjacency_list('/Users/gracefujinaga/Documents/Northwestern/MSDS_460/redistricting/Assignment_3_Redo/Data/adjacency_data.txt')


'''
districts: list of district numbers that region will use
adj_list: filtered adjacency list of included counties
filtered population_df with population statistics
units: counties for that region
'''
def one_region(districts, adj_list, populations, units ) :
    # Initialize model
    model = LpProblem("Redistricting", LpMinimize)

    # Get target population based on the two counties
    target_population = sum(pop_df['pop2020']) / 18

    lower_bound = target_population - target_population * 0.1 # 15% lower bound
    upper_bound = target_population + target_population * 0.1   # 15% upper bound

    # Decision variables
    x = LpVariable.dicts("Assign", [(i, j) for i in units for j in districts], cat=LpBinary)
    x_cut = LpVariable.dicts("CutEdge", [(a, b) for a in units for b in adj_list.get(a, []) if a < b], cat=LpBinary)

    # Objective: Minimize the number of cut edges
    model += lpSum(x_cut[(a, b)] for a in units for b in adj_list.get(a, []) if a < b), "Minimize_Cut_Edges"

    # Constraint: Each unit must be assigned to exactly one district
    for i in units:
        model += lpSum(x[(i, j)] for j in districts) == 1, f"Assign_Unit_{i}_Once"

    # Constraint: Population bounds for each district
    for j in districts:
        model += (
            lpSum(populations[i] * x[(i, j)] for i in units) >= lower_bound,
            f"District_{j}_Population_Lower_Bound"
        )
        model += (
            lpSum(populations[i] * x[(i, j)] for i in units) <= upper_bound,
            f"District_{j}_Population_Upper_Bound"
        )

    # Constraints for cut edges
    for a in units:
        for b in adj_list.get(a, []):
            if b in units:
                if a < b:  # Ensure unique pairs
                    for j in districts:
                        model += (
                            x_cut[(a, b)] >= x[(a, j)] - x[(b, j)],
                            f"CutEdge_Constraint_1_{a}_{b}_District_{j}"
                        )
                        model += (
                            x_cut[(a, b)] >= x[(b, j)] - x[(a, j)],
                            f"CutEdge_Constraint_2_{a}_{b}_District_{j}"
                        )

    # Solve the model
    model.solve()

    print("\nDecision Variable Assignments (x):")
    for (county, district), var in x.items():
        value = var.value()  # Get the value of the variable
        if value == 1:  # Only print variables that are assigned
            print(f"County {county} is assigned to District {district}")

    
    # Output results
    print("\nOptimized District Assignments:")
    for d in districts:
        assigned_counties = [county for county in units if x[(county, d)].value() == 1]
        district_population = sum(pop_df.loc[pop_df['name'] == county, 'pop2020'].values[0] for county in assigned_counties)

        print(f"District {d}: Population = {district_population}")
        if assigned_counties:
            print(f"Counties assigned: {', '.join(assigned_counties)}")
        else:
            print("Counties assigned: None")


     # Build and return the results dictionary
    district_assignments = {}
    for d in districts:
        assigned_counties = [county for county in units if x[(county, d)].value() == 1]
        total_population = sum(populations[county] for county in assigned_counties)
        district_assignments[d] = {"counties": assigned_counties, "total_population": total_population}

    return district_assignments


def filter_adjacency_list(adj_list, filter_keys):
    # new dict for filtered list
    filtered_adj_list = {}
    
    # Loop through the adjacency list
    for county, neighbors in adj_list.items():
        if county in filter_keys:
            filtered_neighbors = [neighbor for neighbor in neighbors if neighbor in filter_keys]
            filtered_adj_list[county] = filtered_neighbors
    
    return filtered_adj_list

# now prep for each region
# now prep for each region
region_1 = "Cook County"

## added everything  efore Jo Daviess
region_2 = "Henry County, Bureau County, Livingston County, LaSalle County, Jo Daviess County, Stephenson County, Winnebago County, Boone County, McHenry County, Carroll County, Ogle County, DeKalb County, Kane County, Whiteside County, Lee County, Kendall County, Grundy County, Will County, Kankakee County" # removed dupage and lake

## added everything before rock island
region_3 = "Hancock County, Schuyler County, Cass County, Menard County, Rock Island County, Mercer County, Iroquois County, Henderson County, Warren County, Knox County, Stark County, Putnam County, Marshall County, Ford County, Vermilion County, Champaign County, McLean County, Woodford County, Tazewell County, Mason County, Peoria County, Fulton County, McDonough County"
# Hancock County, Schuyler County,Cass County, Menard County,
region_4 = "Adams County, Brown County, Logan County, De Witt County, Piatt County, Douglas County, Edgar County, Clark County, Coles County, Cumberland County, Effingham County, Shelby County, Moultrie County, Macon County, Christian County, Montgomery County, Sangamon County, Morgan County, Macoupin County, Greene County, Jersey County, Calhoun County, Scott County, Pike County, Madison County, Bond County, Fayette County, Clay County, Jasper County, Crawford County, Lawrence County, Richland County, Edwards County, Wabash County, Wayne County, Marion County, Clinton County, St. Clair County, Monroe County, Randolph County, Washington County, Jefferson County, Perry County, Jackson County, Franklin County, Hamilton County, White County, Williamson County, Saline County, Union County, Johnson County, Pope County, Hardin County, Alexander County, Pulaski County, Massac County, Gallatin County"

# region_5 = "Madison County, Bond County, Fayette County, Clay County, Jasper County, Crawford County, Lawrence County, Richland County, Edwards County, Wabash County, Wayne County, Marion County, Clinton County, St. Clair County, Monroe County, Randolph County, Washington County, Jefferson County, Perry County, Jackson County, Franklin County, Hamilton County, White County, Williamson County, Saline County, Union County, Johnson County, Pope County, Hardin County, Alexander County, Pulaski County, Massac County, Gallatin County"


'''
From above, we see the following mapping:
- region 1 should be 7 districts
- region 2: 6, 2 of those districts are dupage and lake, 4 for the other counties
- region 3: 2
- region 4: 1 
- region 5: 2
'''

region_district_num_dict = {
    1 : list(range(1, 1 + 7)),
    2 : list(range(8, 1+ 7 + 4)), # also 12, 13
    3: list(range(1+ 7 + 6, 1+ 7 + 6 + 2)),
    4 : list (range(1+ 7 + 6 + 2, 1+ 7 + 6 + 2 +1 + 2))
}

region_county_dict = {
    1: region_1.split(", "),
    2: region_2.split(", "),
    3: region_3.split(", "),
    4: region_4.split(", "),
}

populations = dict(zip(pop_df['name'], pop_df['pop2020']))

#for region in list(range(2, 6)):
dict_list = []
for region in [2, 3, 4]:
#for region in [3]:
    counties = region_county_dict[region]
    print(counties)

    # print(len(counties))
    
    # filter adjacency list
    filtered_adj_list = filter_adjacency_list(adj_list, counties)

    # filter pop list
    dict = one_region(region_district_num_dict[region], filtered_adj_list, populations, counties)
    dict_list.append(dict)
    #dict = one_region([3, 4, 5, 6], filtered_adj_list, populations, counties)




#### testing #####


def filter_adjacency_list(adj_list, filter_keys):
    # new dict for filtered list
    filtered_adj_list = {}
    
    # Loop through the adjacency list
    for county, neighbors in adj_list.items():
        if county in filter_keys:
            filtered_neighbors = [neighbor for neighbor in neighbors if neighbor in filter_keys]
            filtered_adj_list[county] = filtered_neighbors
    
    return filtered_adj_list

# finds all connected components of the solution - we want 1 cc
def find_connected_components(adjacency_list):
    visited = set()  # visited set of counties
    connected_components = []  # list for connected components

    def dfs(county, component):
        visited.add(county)  # Mark the current county as visited
        component.append(county)  # Add the county to the current component
        
        # check all unvisited neighbors
        for neighbor in adjacency_list.get(county, []):
            if neighbor not in visited:
                dfs(neighbor, component)

    # Iterate over all counties in the adjacency list
    for county in adjacency_list:
        if county not in visited:  
            component = []  
            dfs(county, component)  
            connected_components.append(component)  
    
    return connected_components



for dict_elem in dict_list:
    for district_id, details in dict_elem.items():
        # Find connected components
        filter_keys = details['counties']
        filtered_adj_list = filter_adjacency_list(adj_list, filter_keys)
        connected_components = find_connected_components(filtered_adj_list)

        population = details['total_population']  # Get total population
        print(f"District {district_id}:")
        print(f"  Total Population: {population}")

        # Print the connected components
        for i, component in enumerate(connected_components, 1):
            print(f"Connected Component {i}: {', '.join(component)}")


       