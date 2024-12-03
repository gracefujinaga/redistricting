# redistricting
MSDS 460 Assignment 3

Grace Fujinaga, John Leigh, Timmy Li, Kevin Ou 

## Repo Organization
All of the data, intermediate and used csv and txt files are in the folder titled Data. 

All relevant code is in the folder titled code. Iterations.ipynb showed iterations of our work. Models, examples, and ways we all worked off of one another. MSDS460Assignment5ILCountyDistance.py has all of the relevant code to get the distance between all of the counties. preprocessing_data.ipynb has code to get information about the population, demographics, and handling the adjacency list for the counties. Finally, our problem solution is in MSDS460Assignment3.py. This contains the integer programming problem. 

All relevant maps are in the folder titled maps.

Our write up is titled chicago-group-2-assignment-3.pdf

## Results
The output is in redistricting_output.txt with the results of our code. 


## Maps
Actual Districts: https://districtr.org/plan/261378
Our Solution: https://districtr.org/plan/261382


## TODO (take 2)

redo:
- doing the full problem took over 10 hours and wasnt completing

Cbc0010I After 114700 nodes, 17952 on tree, 64 best solution, best possible 16.483155 (60072.18 seconds)
Cbc0010I After 114800 nodes, 17945 on tree, 64 best solution, best possible 16.483155 (60583.43 seconds)
Cbc0010I After 114900 nodes, 17951 on tree, 64 best solution, best possible 16.483155 (60773.21 seconds)


For regions:
https://www.dhs.state.il.us/page.aspx?item=55223

# Iterations

# Iteration 1:

District breakdown:

{1: [1, 2, 3, 4, 5, 6, 7],
 2: [8, 9, 10, 11, 12, 13],
 3: [14, 15],
 4: [16],
 5: [17, 18]}

0.25 error

With districts 1-7 cook county
District 12 - dupage
District 13 - lake county

Outputs

District 8:
  Total Population: 696826
Connected Component 1: Will County
District 9:
  Total Population: 569524
Connected Component 1: Boone County
Connected Component 2: Kane County
District 10:
  Total Population: 608736
Connected Component 1: Carroll County, Jo Daviess County, Stephenson County, Ogle County, DeKalb County, Lee County, Whiteside County, Winnebago County
District 11:
  Total Population: 602017
Connected Component 1: Grundy County, Kankakee County, Kendall County
Connected Component 2: McHenry County
District 14:
  Total Population: 727538
Connected Component 1: Bureau County, Henry County, Knox County, Fulton County, McDonough County, Henderson County, Mercer County, Warren County, Mason County, Tazewell County, Peoria County, Marshall County, LaSalle County, Putnam County, Woodford County, Stark County
District 15:
  Total Population: 671261
Connected Component 1: Champaign County, Ford County, Iroquois County, Vermilion County, Livingston County, McLean County
Connected Component 2: Rock Island County
District 16:
  Total Population: 853078
Connected Component 1: Adams County, Brown County, Cass County, Menard County, Logan County, De Witt County, Macon County, Christian County, Montgomery County, Macoupin County, Greene County, Calhoun County, Jersey County, Pike County, Morgan County, Sangamon County, Shelby County, Coles County, Clark County, Cumberland County, Effingham County, Edgar County, Douglas County, Moultrie County, Piatt County, Schuyler County, Hancock County
District 17:
  Total Population: 574106
Connected Component 1: Alexander County, Pulaski County, Johnson County, Massac County, Pope County, Hardin County, Gallatin County, Hamilton County, Franklin County, Jackson County, Perry County, Jefferson County, Marion County, Clay County, Fayette County, Clinton County, Washington County, Randolph County, Jasper County, Crawford County, Lawrence County, Richland County, Edwards County, Wabash County, White County, Wayne County, Union County, Williamson County, Saline County
District 18:
  Total Population: 574124
Connected Component 1: Bond County, Madison County, St. Clair County, Monroe County


# Iteration 2:

0.25 error

{1: [1, 2, 3, 4, 5, 6, 7], 2: [8, 9, 10, 11] (12, 13 but not in the dict), 3: [14, 15], 4: [16, 17, 18]}

- combined region 4 and 5, 20% error



District 8:
  Total Population: 568697
Connected Component 1: Grundy County
Connected Component 2: Kane County
District 9:
  Total Population: 549501
Connected Component 1: Kankakee County
Connected Component 2: Kendall County
Connected Component 3: McHenry County
District 10:
  Total Population: 696826
Connected Component 1: Will County
District 11:
  Total Population: 662079
Connected Component 1: Boone County, DeKalb County, Lee County, Ogle County, Carroll County, Jo Daviess County, Stephenson County, Winnebago County, Whiteside County
District 14:
  Total Population: 858840
Connected Component 1: Bureau County, Henry County, Knox County, Fulton County, McDonough County, Henderson County, Mercer County, Rock Island County, Warren County, Peoria County, Marshall County, LaSalle County, Putnam County, Woodford County, Tazewell County, Stark County
District 15:
  Total Population: 539959
Connected Component 1: Champaign County, Ford County, Iroquois County, Vermilion County, Livingston County, McLean County
Connected Component 2: Mason County
District 16:
  Total Population: 770065
Connected Component 1: Alexander County, Pulaski County, Johnson County, Massac County, Pope County, Hardin County, Gallatin County, Hamilton County, Franklin County, Jackson County, Perry County, Jefferson County, Marion County, Clay County, Effingham County, Cumberland County, Clark County, Coles County, Douglas County, Edgar County, Moultrie County, Shelby County, Fayette County, Bond County, Clinton County, Washington County, Randolph County, Crawford County, Jasper County, Richland County, Edwards County, Wabash County, Lawrence County, White County, Wayne County, Union County, Williamson County, Saline County
District 17:
  Total Population: 557440
Connected Component 1: Madison County, St. Clair County, Monroe County
District 18:
  Total Population: 678744
Connected Component 1: Adams County, Brown County, Cass County, Menard County, Logan County, De Witt County, Macon County, Christian County, Montgomery County, Macoupin County, Greene County, Calhoun County, Jersey County, Pike County, Morgan County, Sangamon County, Scott County, Piatt County, Schuyler County, Hancock County



## Iteration 3:
Notes: District 1 doesnt have a big enough population, pull LaSalle into it
same as above except the named change

move bureau in --> didnt work

move iroguois in

District 8:
  Total Population: 662079
Connected Component 1: Boone County, DeKalb County, Lee County, Ogle County, Carroll County, Jo Daviess County, Stephenson County, Winnebago County, Whiteside County
District 9:
  Total Population: 579072
Connected Component 1: Grundy County, Kankakee County, LaSalle County
Connected Component 2: McHenry County
District 10:
  Total Population: 696826
Connected Component 1: Will County
District 11:
  Total Population: 648536
Connected Component 1: Kane County, Kendall County
District 14:
  Total Population: 724075
Connected Component 1: Bureau County, Henry County, Knox County, Fulton County, McDonough County, Henderson County, Mercer County, Rock Island County, Warren County, Mason County, Tazewell County, Peoria County, Marshall County, Putnam County, Stark County
District 15:
  Total Population: 565314
Connected Component 1: Champaign County, Ford County, Iroquois County, Vermilion County, Livingston County, McLean County, Woodford County
District 16:
  Total Population: 770065
Connected Component 1: Alexander County, Pulaski County, Johnson County, Massac County, Pope County, Hardin County, Gallatin County, Hamilton County, Franklin County, Jackson County, Perry County, Jefferson County, Marion County, Clay County, Effingham County, Cumberland County, Clark County, Coles County, Douglas County, Edgar County, Moultrie County, Shelby County, Fayette County, Bond County, Clinton County, Washington County, Randolph County, Crawford County, Jasper County, Richland County, Edwards County, Wabash County, Lawrence County, White County, Wayne County, Union County, Williamson County, Saline County
District 17:
  Total Population: 557440
Connected Component 1: Madison County, St. Clair County, Monroe County
District 18:
  Total Population: 678744
Connected Component 1: Adams County, Brown County, Cass County, Menard County, Logan County, De Witt County, Macon County, Christian County, Montgomery County, Macoupin County, Greene County, Calhoun County, Jersey County, Pike County, Morgan County, Sangamon County, Scott County, Piatt County, Schuyler County, Hancock County


## Iteration 4:


from region 3 to 2:
Henry County, Bureau County, Livingston County, LaSalle County,

from region 4 to 3:
Hancock County, Schuyler County, Cass County, Menard County, 


District 8:
  Total Population: 711160
Connected Component 1: Bureau County, Henry County, Whiteside County, Carroll County, Jo Daviess County, Stephenson County, Ogle County, DeKalb County, LaSalle County, Grundy County, Kankakee County, Livingston County, Lee County
District 9:
  Total Population: 696826
Connected Component 1: Will County
District 10:
  Total Population: 648141
Connected Component 1: Boone County, McHenry County, Winnebago County
District 11:
  Total Population: 648536
Connected Component 1: Kane County, Kendall County
District 14:
  Total Population: 491109
Connected Component 1: Champaign County, Ford County, Iroquois County, Vermilion County, McLean County
District 15:
  Total Population: 565229
Connected Component 1: Cass County, Mason County, Menard County, Schuyler County, Hancock County, Henderson County, McDonough County, Warren County, Knox County, Mercer County, Rock Island County, Peoria County, Marshall County, Putnam County, Stark County, Woodford County
District 16:
  Total Population: 668747
Connected Component 1: Adams County, Brown County, Morgan County, Greene County, Calhoun County, Jersey County, Macoupin County, Madison County, Sangamon County, Pike County, Scott County
District 17:
  Total Population: 645652
Connected Component 1: Bond County, Clinton County, Fayette County, Clay County, Effingham County, Cumberland County, Clark County, Coles County, Douglas County, Edgar County, Moultrie County, Macon County, Christian County, Montgomery County, Shelby County, De Witt County, Logan County, Piatt County, Crawford County, Jasper County, Richland County, Edwards County, Wabash County, Lawrence County, White County, Hamilton County, Wayne County, Marion County
District 18:
  Total Population: 642178
Connected Component 1: Alexander County, Pulaski County, Johnson County, Massac County, Pope County, Hardin County, Gallatin County, Saline County, Franklin County, Jackson County, Perry County, Jefferson County, Washington County, Randolph County, Monroe County, St. Clair County, Union County, Williamson County

## Iteration 5:
give region 2 more districts
define another region to keep mchenry connected 

District 8:
  Total Population: 648141
Connected Component 1: Boone County, McHenry County, Winnebago County
District 9:
  Total Population: 648536
Connected Component 1: Kane County, Kendall County
District 10:
  Total Population: 659948
Connected Component 1: Bureau County, Henry County, Rock Island County, Whiteside County, Carroll County, Jo Daviess County, Stephenson County, Ogle County, DeKalb County, LaSalle County, Lee County
District 11:
  Total Population: 696826
Connected Component 1: Will County
District 12:
  Total Population: 686681
Connected Component 1: Champaign County, Ford County, Iroquois County, Kankakee County, Grundy County, Livingston County, McLean County, Vermilion County
District 14:
  Total Population: 404123
Connected Component 1: Cass County, Mason County, Fulton County, Knox County, Mercer County, Henderson County, Hancock County, McDonough County, Schuyler County, Warren County, Stark County, Marshall County, Putnam County, Woodford County, Tazewell County, Menard County
District 16:
  Total Population: 650177
Connected Component 1: Alexander County, Pulaski County, Johnson County, Massac County, Pope County, Hardin County, Gallatin County, Hamilton County, Franklin County, Jackson County, Perry County, Jefferson County, Washington County, Randolph County, Monroe County, St. Clair County, Union County, Williamson County, Saline County
District 17:
  Total Population: 637653
Connected Component 1: Bond County, Clinton County, Fayette County, Clay County, Effingham County, Cumberland County, Clark County, Coles County, Douglas County, Edgar County, Moultrie County, Macon County, Christian County, Montgomery County, Shelby County, De Witt County, Logan County, Piatt County, Crawford County, Jasper County, Richland County, Edwards County, Wabash County, Lawrence County, White County, Wayne County, Marion County
District 18:
  Total Population: 668747
Connected Component 1: Adams County, Brown County, Morgan County, Greene County, Calhoun County, Jersey County, Macoupin County, Madison County, Sangamon County, Pike County, Scott County