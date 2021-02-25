### vcadoganJobsProject

#### Student: *Victoria Cadogan*

# College Data :mortar_board:
## COMP490 Project 1 Sprint 1


- :computer: Open the project (preferably) in PyCharm
- :bookmark_tabs: Register for an API key to get government data: https://api.data.gov/signup/
- :key: Save the key to a file named secrets.py
- :heavy_check_mark: Add requests library to the project
- :running: Run main.py
- :mag: It will be gathering over 3K entries
- :hourglass: Wait 1~2 minutes to run (running time may vary)
- :memo: A new text file will be created containing US College Data
- :pray: For *Sprint 1* nothing I believe is missing


## COMP490 Project 1 Sprint 2

- :bookmark_tabs: Register for an API key to get government data: https://api.data.gov/signup/
- :key: Save the key to a file named secrets.py
- :computer: Open the project (preferably) in PyCharm
- :running: Run main.py
- :mag: It will be gathering over 3K entries
- :hourglass: Wait 1~2 minutes to run (running time may vary)
- Once it finished executing, in the project directory a new database with college data will be created.
- Database layout: one table, 8 columns, 3203 rows
- Table layout: 
    - ID (primary key) that also keeps track of the number of entries 
    - College name 
    - City of that college 
    - State of that college
    - Student size in 2018 
    - Student size in 2017 
    - Number of graduates in 2017 working and not enrolled who earned more than 150% of the single-person household poverty threshold 3 years after completing
    - Number of students in 2016 in the 3-year repayment rate cohort

- :pray: For *Sprint 2* nothing I believe is missing

## COMP490 Project 1 Sprint 3

- :bookmark_tabs: Register for an API key to get government data: https://api.data.gov/signup/
- :key: Save the key to a file named secrets.py
- :computer: Open the project (preferably) in PyCharm
- :running: Run main.py
- :mag: It will be gathering over 3K entries
- :hourglass: Wait 1~2 minutes to run (running time may vary)
- Once it finished executing, in the project directory a new database with college data will be created.
- Database layout: two tables
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
- The tests will assert: 
    - Whether the college count in the US exceeds 1000 entries;
    - The creation of the database from main as well as a test database
    - The comparison of the entries among the two databases
    - Whether any data is null or doesn't match
    - Whether the jobs_data tables gathered entries from all 50 states (at least)
