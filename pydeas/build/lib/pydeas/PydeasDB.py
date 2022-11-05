import os
from typing import Any
import pandas as pd
import csv
from rich.console import Console
from rich.table import Table
import platform



if platform.system() == 'Windows':
    class File:

        def __init__(self, file_path: str) -> None:
            """Passing the file's path, you can start working with your db file, this function raises an error if the
            file doesn't exist\nReturns the File object referring to the file """
            if os.path.exists(f'{file_path}.csv'):
                self.file = file_path + '.csv'
            else:
                raise FileNotFoundError(file_path)

        def add_column(self, col_name: str) -> None:
            """Add one column to the relational file"""
            df = pd.read_csv(self.file, encoding='utf-8', on_bad_lines='skip')
            if str(col_name) in df.columns:
                return
            df[str(col_name)] = ""
            os.remove(self.file)
            df.to_csv(self.file, index=False)

        def add_columns(self, cols: list) -> None:
            """Add columns to the relational file"""
            for col in cols:
                self.add_column(col)

        def add_row(self, row: list) -> None:
            """Add a row to the file"""
            df = pd.read_csv(self.file, encoding='utf-8', on_bad_lines='skip')

            if len(df.columns) <= len(row):
                raise ValueError(
                    f'It seems like you have passed too many arguments when adding a row \nExpected: {len(df.columns)}, '
                    f'Got: {len(row)} '
                )

            row.insert(0, len(df) + 1)
            with open(self.file, 'a+', newline='') as write_obj:
                csv_writer = csv.writer(write_obj)
                csv_writer.writerow(row)

        def delete_byindex(self, pos: int, failed='Position Not Found') -> Any:
            """Delete a row by index"""
            df = pd.read_csv(self.file, encoding='utf-8', on_bad_lines='skip')

            if isinstance(pos, int):
                try:
                    df.drop(pos - 1, inplace=True)
                except:
                    return failed
                df.loc[pos - 1:, '#'] -= 1
                os.remove(self.file)
                df.to_csv(self.file, index=False)
                return

            for i in pos:
                try:
                    df.drop(i - 1, inplace=True)
                except:
                    return failed

                df.loc[i - 1:, '#'] -= 1
                os.remove(self.file)
                df.to_csv(self.file, index=False)

        def update_byindex(self, pos: int, new_row: dict) -> None:
            """Update a row by index"""
            df = pd.read_csv(self.file, encoding='utf-8', on_bad_lines='skip')

            temp = {'#': pos}
            temp.update(new_row)
            new_row = temp

            df.loc[pos - 1] = new_row

            os.remove(self.file)
            df.to_csv(self.file, index=False)

        def show_table(self) -> None:
            """Show the entire file content"""
            table = Table(show_header=True, header_style='bold blue')
            console = Console()

            df = pd.read_csv(self.file, encoding='utf-8', on_bad_lines='skip')

            [table.add_column(i, style='dim') for i in df.columns]

            for i in range(len(df)):
                t = (list(df.iloc[i]))

                t = tuple([str(i) for i in t])

                table.add_row(*t, style='bold #6be9ff')  # insert finale

            console.print(table)

        def set_column(self, column: str, attribute) -> None:
            """Update a column for all the rows and creates it if it not exists"""
            df = pd.read_csv(self.file, encoding='utf-8', on_bad_lines='skip')
            df[column] = attribute
            os.remove(self.file)
            df.to_csv(self.file, index=False)

        def remove_column(self, column: str) -> None:
            """Remove a column for all the rows"""
            df = pd.read_csv(self.file, encoding='utf-8', on_bad_lines='skip')
            try:
                df.drop(column, axis=1, inplace=True)
            except:
                return None
            os.remove(self.file)
            df.to_csv(self.file, index=False)

        def __repr__(self) -> str:
            self.show_table()
            return ''

        def query(self, query: str) -> list:
            """Returns A list of objects if found\n Query Structure: f 'name == "{name}"'   """
            data = pd.read_csv(self.file, encoding='utf-8', on_bad_lines='skip')
            ris = data.query(query)
            if not ris.empty:
                return ris.to_dict('records')
            return None

        def search(self, filter_dict: dict) -> list:
            """Returns A list of objects if found\n Query Structure: {
                'name': 'Joe',
                'lastname': 'Mama',
                'age': 69
            } """
            data = pd.read_csv(self.file, encoding='utf-8', on_bad_lines='skip')
            ris = data
            for key, value in filter_dict.items():
                ris = data[data[key] == value]
                if ris.empty:
                    return None
                data = ris
            return ris.to_dict('records')

        def delete(self, query: str) -> bool:
            """Delete a row by first querying it, if the rows exists  this function returns True"""
            if ris := self.query(query):
                f = [i['#'] for i in ris]
                self.delete_byindex(f)
                return True
            else:
                return None

        def update(self, query: str, new_row: dict) -> bool:
            """Update a row by first querying it, if the rows exists this function returns True"""
            if ris := self.query(query):
                for i in ris:
                    self.update_byindex(i['#'], new_row)
                return True
            return None


    class Folder:

        def __init__(self, path_to_mother_file: str) -> None:
            """Create a folder if it not exists, returns the Folder object referring to the folder created, or that is
            already created """
            self.mother_folder = path_to_mother_file
            try:
                os.mkdir(path_to_mother_file)
                print("Let's get work done")
            except FileExistsError:
                pass

        def add_folder(self, folder: str):
            """Add a folder to the mother_folder and returns it """
            try:
                os.mkdir(f'{self.mother_folder}\\{folder}')
                return Folder(f'{self.mother_folder}\\{folder}')
            except FileExistsError:
                pass

        def add_folders(self, folders_list: list) -> None:
            """Add the folders that are passed as argument to the mother_folder """
            for folder in folders_list:
                self.add_folder(folder)

        def create_file(self, file_name: str) -> File:
            """Create the File that is passed as argument, and returns the file that is created"""
            if not os.path.exists(f'{self.mother_folder}\\{file_name}.csv'):
                f = open(f'{self.mother_folder}\\{file_name}.csv', 'a')
                f.write('#')
            return File(f'./{self.mother_folder}/{file_name}')

        def create_files(self, files_name: list) -> None:
            """Create the Files that are passed as argument"""
            for file in files_name:
                self.create_file(file)

        @staticmethod
        def remove(path_to_content: str) -> None:
            """Removes the folder"""
            os.remove(path_to_content)

        def view_content(self) -> None:
            """Prints the content of the folder"""
            print(os.listdir(self.mother_folder))

        def __repr__(self) -> str:
            self.view_content()
            return f'\nPath: {self.mother_folder}'

else:
    class File:

        def __init__(self, file_path: str) -> None:
            """Passing the file's path, you can start working with your db file, this function raises an error if the
            file doesn't exist\nReturns the File object referring to the file """
            if os.path.exists(f'{file_path}.csv'):
                self.file = file_path + '.csv'
            else:
                raise FileNotFoundError(file_path)

        def add_column(self, col_name: str) -> None:
            """Add one column to the relational file"""
            df = pd.read_csv(self.file, encoding='utf-8', )
            if str(col_name) in df.columns:
                return
            df[str(col_name)] = ""
            os.remove(self.file)
            df.to_csv(self.file, index=False)

        def add_columns(self, cols: list) -> None:
            """Add columns to the relational file"""
            for col in cols:
                self.add_column(col)

        def add_row(self, row: list) -> None:
            """Add a row to the file"""
            df = pd.read_csv(self.file, encoding='utf-8', )

            if len(df.columns) <= len(row):
                raise ValueError(
                    f'It seems like you have passed too many arguments when adding a row \nExpected: {len(df.columns)}, '
                    f'Got: {len(row)} '
                )

            row.insert(0, len(df) + 1)
            with open(self.file, 'a+', newline='') as write_obj:
                csv_writer = csv.writer(write_obj)
                csv_writer.writerow(row)

        def delete_byindex(self, pos: int, failed='Position Not Found') -> Any:
            """Delete a row by index"""
            df = pd.read_csv(self.file, encoding='utf-8', )

            if isinstance(pos, int):
                try:
                    df.drop(pos - 1, inplace=True)
                except:
                    return failed
                df.loc[pos - 1:, '#'] -= 1
                os.remove(self.file)
                df.to_csv(self.file, index=False)
                return

            for i in pos:
                try:
                    df.drop(i - 1, inplace=True)
                except:
                    return failed

                df.loc[i - 1:, '#'] -= 1
                os.remove(self.file)
                df.to_csv(self.file, index=False)

        def update_byindex(self, pos: int, new_row: dict) -> None:
            """Update a row by index"""
            df = pd.read_csv(self.file, encoding='utf-8', )

            temp = {'#': pos}
            temp.update(new_row)
            new_row = temp

            df.loc[pos - 1] = new_row

            os.remove(self.file)
            df.to_csv(self.file, index=False)

        def show_table(self) -> None:
            """Show the entire file content"""
            table = Table(show_header=True, header_style='bold blue')
            console = Console()

            df = pd.read_csv(self.file, encoding='utf-8', )

            [table.add_column(i, style='dim') for i in df.columns]

            for i in range(len(df)):
                t = (list(df.iloc[i]))

                t = tuple([str(i) for i in t])

                table.add_row(*t, style='bold #6be9ff')  # insert finale

            console.print(table)

        def set_column(self, column: str, attribute) -> None:
            """Update a column for all the rows and creates it if it not exists"""
            df = pd.read_csv(self.file, encoding='utf-8', )
            df[column] = attribute
            os.remove(self.file)
            df.to_csv(self.file, index=False)

        def remove_column(self, column: str) -> None:
            """Remove a column for all the rows"""
            df = pd.read_csv(self.file, encoding='utf-8', )
            try:
                df.drop(column, axis=1, inplace=True)
            except:
                return None
            os.remove(self.file)
            df.to_csv(self.file, index=False)

        def __repr__(self) -> str:
            self.show_table()
            return ''

        def query(self, query: str) -> list:
            """Returns A list of objects if found\n Query Structure: f 'name == "{name}"'   """
            data = pd.read_csv(self.file, encoding='utf-8', )
            ris = data.query(query)
            if not ris.empty:
                return ris.to_dict('records')
            return None

        def search(self, filter_dict: dict) -> list:
            """Returns A list of objects if found\n Query Structure: {
                'name': 'Joe',
                'lastname': 'Mama',
                'age': 69
            } """
            data = pd.read_csv(self.file, encoding='utf-8', )
            ris = data
            for key, value in filter_dict.items():
                ris = data[data[key] == value]
                if ris.empty:
                    return None
                data = ris
            return ris.to_dict('records')

        def delete(self, query: str) -> bool:
            """Delete a row by first querying it, if the rows exists  this function returns True"""
            if ris := self.query(query):
                f = [i['#'] for i in ris]
                self.delete_byindex(f)
                return True
            else:
                return None

        def update(self, query: str, new_row: dict) -> bool:
            """Update a row by first querying it, if the rows exists this function returns True"""
            if ris := self.query(query):
                for i in ris:
                    self.update_byindex(i['#'], new_row)
                return True
            return None


    class Folder:

        def __init__(self, path_to_mother_file: str) -> None:
            """Create a folder if it not exists, returns the Folder object referring to the folder created, or that is
            already created """
            self.mother_folder = path_to_mother_file
            try:
                os.mkdir(path_to_mother_file)
                print("Let's get work done")
            except FileExistsError:
                pass

        def add_folder(self, folder: str):
            """Add a folder to the mother_folder and returns it """
            try:
                os.mkdir(f'{self.mother_folder}\\{folder}')
                return Folder(f'{self.mother_folder}\\{folder}')
            except FileExistsError:
                pass

        def add_folders(self, folders_list: list) -> None:
            """Add the folders that are passed as argument to the mother_folder """
            for folder in folders_list:
                self.add_folder(folder)

        def create_file(self, file_name: str) -> File:
            """Create the File that is passed as argument, and returns the file that is created"""
            if not os.path.exists(f'./{self.mother_folder}/{file_name}.csv'):
                f = open(f'./{self.mother_folder}/{file_name}.csv', 'a')
                f.write('#')
            return File(f'./{self.mother_folder}/{file_name}')

        def create_files(self, files_name: list) -> None:
            """Create the Files that are passed as argument"""
            for file in files_name:
                self.create_file(file)

        @staticmethod
        def remove(path_to_content: str) -> None:
            """Removes the folder"""
            os.remove(path_to_content)

        def view_content(self) -> None:
            """Prints the content of the folder"""
            print(os.listdir(self.mother_folder))

        def __repr__(self) -> str:
            self.view_content()
            return f'\nPath: {self.mother_folder}'
    