### vcadoganJobsProject

#### Student: *Victoria Cadogan*

# College Data :mortar_board:
## COMP490 Project 1 Sprint 4

- :bookmark_tabs: Register for an API key to get government data: https://api.data.gov/signup/
- :key: Save the key to a file named secrets.py
- :computer: Open the project (preferably) in PyCharm
- :running: Run window.py
- :mag: It will be gathering over 3K entries
- :hourglass: Wait 1~2 minutes to run (running time may vary)
- Once it finished executing, in the project directory a new database with college data will be created.
- A new window will be uploaded, user can choose their own excel file or visualise the data from the default excel file in the directory.
- If the user chooses to import a new excel file, please wait ~15 seconds to upload the data to the database.
- Once the buttons are clickable/not frozen, then the data imported successfully. (this is still a bare bones project that could use a loading screen)
- Click visualize to view the table data. Please choose one of the two comparison options from the drop down menu. The rightmost column is the key used for sorting.
- The data will be color coded based on the rightmost column. Red: unsatisfactory, Magenta: poor, Yellow: average, Green: satisfactory, Blue: excellent.
- To visualize the map, click Show Map in the Visualize menu. Once clicked, please wait ~15 seconds to load the map with data.
- A browser will open up with the US map. 
- Database layout: three tables (+1 non essential due to auto increment)
- Table for College Data layout: 8 columns, 3203 rows 
    - ID (primary key) that also keeps track of the number of entries 
    - College name 
    - City of that college 
    - State of that college
    - Student size in 2018 
    - Student size in 2017 
    - Number of graduates in 2017 working and not enrolled who earned more than 150% of the single-person household poverty threshold 3 years after completing
    - Number of students in 2016 in the 3-year repayment rate cohort

- Table for Jobs Data layout: 7 columns, 1187 rows
    - jobID: The 6-digit Standard Occupational Classification (SOC) code or OES-specific code for the occupation.
    - State (or territory). This field along with the job ID makes the Primary Key.
    - Occupational group (the aim was to gather ones from "major") aka SOC occupational level.
    - SOC title or OES-specific title for the occupation
    - Estimated total employment rounded to the nearest 10 (excludes self-employed).
    - Hourly 25th percentile wage
    - Annual 25th percentile wage

- Table for State Lookup layout: 3 columns, 54 rows
    - state_id is a primary key (auto-incremented numbers)
    - state_name is the state full name
    - state_abbr is the abbreviation of that state

- The tests will assert: 
    - Whether the college count in the US exceeds 1000 entries;
    - The creation of the database from main as well as a test database
    - The comparison of the entries among the two databases
    - Whether any data is null or doesn't match
    - Whether the jobs_data tables gathered entries from all 50 states (at least)
    - Whether the state_state lookup table returns at least 50 states

