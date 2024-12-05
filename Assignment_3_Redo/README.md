# redistricting
MSDS 460 Assignment 3 - redo assignment
Grace Fujinaga, John Leigh, Timmy Li, Kevin Ou 

# Repo Organization
All of the data, intermediate and used csv and txt files are in the folder titled Data. 

All relevant code is in the folder titled code. Data_preprocesing.ipynb has data preprocessing steps. dist_objective_fxn.py has the code for building a map using min cut edge as the objective function. pop_objective_fxn.py has the code for building a map using even population size as the objective function. 

# Results
The results folder has all of the outputs. 

Our write up is titled chicago-group-2-assignment-3.pdf


# Maps
Actual Districts: https://districtr.org/plan/261378
Our Original Solution: https://districtr.org/plan/261382
Our Second Solution: https://districtr.org/plan/270599


# Notes about using the min cut objective function:

The relevant code for this is in dist_objective_fxn.py

Even after removing Cook, DuPage, and Lake Counties, the problem was still too big to do the min cut objective function for the entire state. It took over 10 hours and still had not come close to reaching a solution. Thus, basing off of Illinois regions, 5 sets were made. These original regions are as follows:

region 1:
 Cook County
region 2:
 JoDaviess County, Stephenson County, Winnebago County, Boone County, McHenry County, Lake County, Carroll County, Ogle County, DeKalb County, Kane County, DuPage County, Whiteside County, Lee County, Kendall County, Grundy County, Will County, Kankakee County
region 3:
 Rock Island County, Mercer County, Henry County, Bureau County, LaSalle County, Henderson County, Warren County, Knox County, Stark County, Putnam County, Marshall County, Livingston County, Ford County, Iroquois County, Vermillion County, Champaign County, McLean County, Woodford County, Tazewell County, Mason County, Peoria County, Fulton County, McDonough County
region 4:
 Hancock County, Adams County, Schuyler County, Brown County, Cass County, Menard County, Logan County, Dewitt County, Piatt County, Douglas County, Edgar County, Clark County, Coles County, Cumberland County, Effingham County, Shelby County, Moultrie County, Macon County, Christian County, Montgomery County, Sangamon County, Morgan County, Macoupin County, Green County, Jersey County, Calhoun County, Scott County, Pike County
region 5:
 Madison County, Bond County, Fayette County, Clay County, Jasper County, Crawford County, Lawerence County, Richland County, Edwards County, Wabash County, Wayne County, Marion County, Clinton County, St. Clair County, Monroe County, Randolph County, Washington County, Jefferson County, Perry County, Jackson County, Franklin County, Hamilton County, White County, Williamson County, Saline County, Union County, Johnson County, Pope County, Hardin County, Alexander County, Pulaski County, Massac County, Gallatin County

Then, DuPage and Lake county were removed from region 2. The first iteration used each region and solved. Based on population, the number of districts per regions is as follows:

target_population:  710575.3888888889
Region 1:
population: 5263608
estimated number of districts: 7.407529281629903
Region 2:
population: 4121701
estimated number of districts: 5.800511901270621
Region 3:
population: 1398799
estimated number of districts: 1.9685441149140717
Region 4:
population: 858019
estimated number of districts: 1.2074988993661397
Region 5:
population: 1148230
estimated number of districts: 1.6159158028192646

Getting a 100% adjacent solution required multiple iterations as follows:

## Iterations

# Iteration 1:

Mapping of regions to districts:
{1: [1, 2, 3, 4, 5, 6, 7],
 2: [8, 9, 10, 11, 12, 13],
 3: [14, 15],
 4: [16],
 5: [17, 18]}

# Iteration 2:

25% constraint on population deviation from total_population, combined region 4 and 5. 

Still had districts that weren't completely connected.

{1: [1, 2, 3, 4, 5, 6, 7], 
 2: [8, 9, 10, 11] (12, 13 but not in the dict), 
 3: [14, 15], 
 4: [16, 17, 18]}


## Iteration 3:

Still had districts that weren't completely connected. Started moving districts one by one into district one to get district populations closer to the necessary range. 

{1: [1, 2, 3, 4, 5, 6, 7], 
 2: [8, 9, 10, 11] (12, 13 but not in the dict), 
 3: [14, 15], 
 4: [16, 17, 18]}

## Iteration 5: Final iteration
15% population deviation constraint
{1: [1, 2, 3, 4, 5, 6, 7], 
 2: [8, 9, 10, 11], 
 3: [14, 15], 
 4: [16, 17, 18]}

- add more districts to region 2
- define another district within region 2 to keep McHenry connected to Boone County, Winnebago county
- Missing Tazewell county, manually assign it to District 15 after the fact