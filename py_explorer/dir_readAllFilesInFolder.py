# read all files in a folder
# 2020-08-27
# Ben Mogotsi

import pathlib
from pathlib import Path
import datetime
from datetime import date
import re


# import date
# path_source = 'C:/Users/Ben.Mogotsi/myPyScripts/'
path_target = 'C:/Users/Ben.Mogotsi/myPyScripts/'
path_source=r'C:\Users\Ben.Mogotsi\OneDrive - Momentum Group\Documents\My Documents\Liscoe\SquirreL_myFiles'

try:
    def search_string_in_file_full_read(file_path, search_string):
        """
        Reads the entire file and checks if the search_string is present.

        Args:
            file_path (str): The path to the text file.
            search_string (str): The string to search for.

        Returns:
            bool: True if the string is found, False otherwise.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                search_string.find(search_string) != -1
                if re.search(search_string, content, re.IGNORECASE):
                        print(f"Found (case-insensitive) '{search_string}' in file '{file_path}' using regex")
                return search_string.casefold() in content.casefold()
                # The casefold() method converts a string into a casefolded form,
                # which is more aggressive than lower() and handles a wider range of Unicode characters for true case-insensitivity.

                if re.search(search_string, main_string, re.IGNORECASE):
                    print("Found (case-insensitive) using regex")

        except FileNotFoundError:
            print(f"Error: File not found at {file_path}")
            return False

    string_to_find = "with "
    for file in Path(path_source).glob('*'):
        if file.is_file():
            print(f"stem:  {file.name} or {file.stem}  or {file.suffix} ")
            file_name = file.name
            if search_string_in_file_full_read(file_name, string_to_find):
                print(f"'{string_to_find}' found in {file_name}")
            else:
                print(f"'{string_to_find}' not found in {file_name}")
        else:
            print(f" path: {file}  st_size: {file.stat().st_size/1000}   suffix: {file.suffix} \
            st_ctime  {datetime.datetime.fromtimestamp(file.stat().st_ctime)} \
             st_atime: {datetime.datetime.fromtimestamp(file.stat().st_atime)}  \
              st_mtime: {datetime.datetime.fromtimestamp(file.stat().st_mtime)}  \
              st_mtime_date: {(datetime.date.fromtimestamp(file.stat().st_mtime))}  \
              n_fields:  {file.stat().n_fields}  \
               stem:  {file.stem}  st_file_attributes: {file.stat().st_file_attributes} \
               st_ctime_ns {datetime.datetime.fromtimestamp(file.stat().st_ctime_ns/1_000_000_000)}")
               # The math.ceil() function from the math module always rounds a number up to the nearest whole number, regardless of the decimal part.
               # To convert a nanosecond timestamp obtained from time.time_ns() to a datetime object in Python, you need to divide the nanosecond value by \(10^{9}\) to get the timestamp in seconds, and then use the datetime.fromtimestamp() method.
               # To convert st_mtime (a Unix timestamp representing the last modification time of a file) to a datetime object in Python, utilize the datetime module.
               # The st_mtime attribute is obtained from the os.stat() function or pathlib.Path().stat() method, and it represents the number of seconds since the Unix epoch (January 1, 1970, 00:00:00 UTC).


except Exception as e:
    print(f"Error: {str(e)}")

# Example usage:




quit()
