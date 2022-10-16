# Pydeas
Pydeas is a [Python](https://www.python.org/) library for dealing in an efficent way with information storage.

# Installation 
Use the package manager [pip](https://pip.pypa.io/en/stable) to install Pydeas
```bash
pip install pydeas
```


## Get Started
This library is based on [pandas](https://github.com/pandas-dev/pandas) and memorize the information in csv files, the database is relational but you can work with multiple folders and files, in this way you can create a dynamic and comprehensible db structure.

```python
from pydeas import PydeasDB

def db() -> None:
    main_folder = PydeasDB.Folder('Database') # create the main folder in the current folder
    password_file = main_folder.create_file('passwords') # create a 'passwords' file in the main folder
    password_file.add_columns(['App', 'Email', 'Username', 'Password']) # add the column to the table of the file
```

Now we created a "passwords.csv" in the database folder, and configured the file adding columns; we can now start working with Pydeas

### Output in ./Database/passwords.csv
```csv
#,App,Email,Username,Password
```


### Add an element to the table
```python
password_file.add_row(['Github', 'myemail@io.com', 'Foo', 'Bar']) # add a row to the table of the file
```

### Output in ./Database/passwords.csv
```csv
#,App,Email,Username,Password
1,Github,myemail@io.com,Foo,Bar
```

### As you can see this library is pretty easy to use and all the methods name are auto-explicative, but you can navigate further in this documentation

## Query
A pydeas database can be queryied in 2 different ways:
one resembles the way of doing things in relational databases
(we recommend using this when queryies are more complex)

```python
def get_config(app_name, email):
    print(password_file.query(f'App == "{app_name}" & Email == "{email}"'))
        
# This function will print the list of objects or None (if nothing is found)
```
for reference you can check the [query method of pandas library](https://sparkbyexamples.com/pandas/pandas-dataframe-query-examples/) which also takes a string and works in the exact same way;

While the other one resembles the non-relational databases (such as [MongoDb](https://www.mongodb.com/) etc.) 
```python
def get_config(app_name, email):
    print(password_file.search({
        "App": app_name,
        'Email': email
    }))
# This function will print the list of objects or None (if nothing is found)
```
## Update
The update function takes 2 arguments: the first one is the query string, the second one the new row 
```python
def update_by_appname(app_name, new_email, new_username, new_password) -> None:
    response = password_file.update(f'App == "{app_name}"', {
        'App': app_name,
        'Email': new_email,
        'Username': new_username,
        'Password': new_password
    })
    print(response)
# This function will print true if the operation is completed succesfully
```

## Delete
The delete function the query string as argument 
```python
def delete_by_appname(app_name) -> None:
    response = password_file.delete(f'App == "{app_name}"')
    print(response)
# This function will print true if the operation is completed succesfully
```
[Pydeas v0.1.7](https://pypi.org/project/pydeas/)
