import csv
from pulp import LpProblem, LpVariable, LpMinimize, lpSum, LpBinary

# Parsing functions
def parse_census_population(file_path):
    county_population = {}
    with open(file_path, "r") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for line in reader:
            try:
                population = int(line[0].strip('[]"\''))  # Clean malformed brackets
                county_name = line[1].strip('[]"\'')

                county_population[county_name] = population
            except (ValueError, IndexError) as e:
                print(f"Skipping invalid line: {line}. Error: {e}")
    return county_population


# File paths
population_file = "pop2020data.txt"

# Load data
county_population = parse_census_population(population_file)

# Validate parsed data
print(f"Total counties in population data: {len(county_population)}")

# Initialize model
model = LpProblem("Redistricting", LpMinimize)

# Parameters
districts = list(range(1, 19))  # 18 districts
counties = list(county_population.keys())
target_population = sum(county_population.values()) // len(districts)

# Decision variables
x = LpVariable.dicts("Assign", [(county, d) for county in counties for d in districts], cat=LpBinary)

# Deviation variables
over_deviation = LpVariable.dicts("OverDev", districts, lowBound=0)
under_deviation = LpVariable.dicts("UnderDev", districts, lowBound=0)

# Objective: Minimize population deviation
model += lpSum(over_deviation[d] + under_deviation[d] for d in districts)

# Pre-assign large counties
preassigned_districts = {
    "Cook County, Illinois": list(range(1, 8)),  # 7 districts
    "DuPage County, Illinois": [8],             # 1 district
    "Lake County, Illinois": [9],               # 1 district
}

for county, assigned_districts in preassigned_districts.items():
    for d in districts:
        if d in assigned_districts:
            model += x[(county, d)] == 1
        else:
            model += x[(county, d)] == 0

# Constraints
# 1. Each remaining county assigned to exactly one district
for county in counties:
    if county not in preassigned_districts:
        model += lpSum(x[(county, d)] for d in districts) == 1

# 2. Population deviation constraints
for d in districts:
    model += (
        lpSum(x[(county, d)] * county_population[county] for county in counties) - target_population
        <= over_deviation[d]
    )
    model += (
        target_population
        - lpSum(x[(county, d)] * county_population[county] for county in counties)
        <= under_deviation[d]
    )

# Solve model
model.solve()

# Output results
print("\nPre-assigned Districts:")
for county, assigned_districts in preassigned_districts.items():
    print(f"{county}: Assigned to Districts {assigned_districts}")

print("\nOptimized District Assignments:")
for d in districts:
    district_population = sum(county_population[county] for county in counties if x[(county, d)].value() == 1)
    assigned_counties = [county for county in counties if x[(county, d)].value() == 1]
    print(f"District {d}: Population = {district_population}")
    if assigned_counties:
        print(f"Counties assigned: {', '.join(assigned_counties)}")
    else:
        print("Counties assigned: None")
