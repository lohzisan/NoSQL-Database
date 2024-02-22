Files in Google Drive: 
1. readme.md [Documentation you are currently reading.]
2. requirements.txt [packages required to run the code]
3. script.py [Main Script of Database]
4. IMDB.json [IMDB Table with data from Kaggle]
5. Directors.json [Dummy Directors data used for join function]

Please note that each new "table" created will be stored as their individual JSON files. 

Setup: 
1. Install requirements.txt; Command: pip or pip3 install -r requirements.txt
2. Run script.py; Command: python or python3 script.py 
3. Make sure that the JSON files & script.py are in the same folder at the time of running 
4. Load the table that you want to manipulate into the database; Command: load <table_name> 
5. Run queries with syntax below. More specific example of queries are also given below. 

Query Syntax: 
1. Create; Command Syntax: create <table_name>
2. Load; Command Syntax: load <table_name>
3. Insert; Command Syntax: insert {key: value, key: value, etc...}
4. Update; Command Syntax: update <key> = <new_value> WHERE <key> = <current_value>
5. Delete; Command Syntax: delete <key> = <value>
6. Find; Command Syntax: find record whose <key> is <value>
7. Pick; Command Syntax: pick <key>, <key> WHERE <key> at least/is/greater than/less than <value>
8. Sort; Command Syntax: sortby <key> ASC/DESC
9. Group/Aggregate; Command Syntax: organizeby <key> <key> SUM/AVG/COUNT
10. Join; Command Syntax: join <table_name> <table_name> <common_key>
11. Exit; Command Syntax: exit()

Specific Query Examples: 
[Make sure to load the relevant tables when running these queries. E.g., for movies, load IMDB, for directors, load Directors, for employee data load Employees]
1. Create: - create employees
           - create movies
2. Load: - load IMDB    
         - load Directors
3. Insert: - insert {"EmployeeID": 5, "FirstName": "Tyler", "LastName": "Le", "Department": "HR", "Salary": 50000}
           - insert {"EmployeeID": 6, "FirstName": "Megan", "LastName": "Pham", "Department": "Sales", "Salary": 80000}
4. Update: - update Salary = 60000 WHERE EmployeeID = 5
           - update FirstName = Meghan WHERE LastName = Pham
5. Delete: - delete EmployeeID = 5
           - delete Movie = Mission: Impossible - Dead Reckoning Part One
6. Find: - find movies whose Genre is Action
         - find movies whose Stars is Tom Cruise
7. Pick: - pick Director, Age WHERE Country is USA 
         - pick FirstName, LastName WHERE Department = Sales
8. Sort: - sortby Age DESC
9. Join: - join IMDB Directors Director
10. Aggregate: - groupby Movie Rating AVG
