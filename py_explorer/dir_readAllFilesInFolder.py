# read all files in a folder
# 2020-08-27
# Ben Mogotsi

import pathlib
from pathlib import Path
import datetime
from datetime import date
import re
import csv


# import date
# path_source = 'C:/Users/Ben.Mogotsi/myPyScripts/'
cwd = cwd = Path.cwd()
path_target = 'C:/Users/Ben.Mogotsi/myPyScripts/'
# path_source=r'C:\Users\Ben.Mogotsi\OneDrive - Momentum Group\Documents\My Documents\Liscoe\SquirreL_myFiles'
path_source = cwd

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
                        return True
                        print(f"Found (case-insensitive) '{search_string}' in file '{file_path}' using regex")
                return search_string.casefold() in content.casefold()
                # The casefold() method converts a string into a casefolded form,
                # which is more aggressive than lower() and handles a wider range of Unicode characters for true case-insensitivity.

                if re.search(search_string, main_string, re.IGNORECASE):
                    print("Found (case-insensitive) using regex")

        except FileNotFoundError:
            print(f"Error: File not found at {file_path}")
            return False
            
    def create_file(fileName, suffix):
        """
            Create an empty file name
                add blank lines before
        """
        if suffix == "":
            suffix = ".txt"
        if suffix[0] != ".":
            suffix = "." + suffix
            
        # create file if it does not exist       
        # if not Path(fileName+suffix).exists():
        if suffix == ".txt":
            file=open(fileName+suffix, mode="w",encoding="utf-8") # clears file if it exists
            file.close
        elif suffix == ".csv":
            new_headings = [["Full Path Name", "Search String", "Found"]]
            with open(fileName+suffix, "w", newline='') as file:
                writer = csv.writer(file, quoting=csv.QUOTE_NONE,
                                    delimiter=',', quotechar='"', escapechar='\\')
                writer.writerows(new_headings)
        
    def open_file(fileName, suffix):
        """
            Open file in append mode
            create file if it does not exist   
                    
        """
        # create file if it does not exist   
        # append file
        
        if suffix == "":
            suffix = ".txt"
        if suffix[0] != ".":
            suffix = "." + suffix
        # Check if the file exists, if not create it
        # return file object
        if suffix == ".txt":
            file_obj = open(fileName+suffix, mode="a",encoding="utf-8")
            return file_obj, fileName+suffix
        elif suffix == ".csv":
            new_headings = ['Full Path Name', 'Search String', 'Found']
            with open(fileName+suffix, 'a', newline='') as file:
                writer = csv.writer(file, quoting=csv.QUOTE_NONE,
                                    delimiter=',', quotechar='"', escapechar='\\')
            return writer, fileName+suffix

        
    def close_file(fileObj):
        """
            Close file 
                        
        """
        if fileObj is not None:
            fileObj.close()
            
    def is_csv_writer(obj):
        """
        Checks if an object behaves like a csv.writer by checking for the 'writerow' method.
        """
        return hasattr(obj, 'writerow') and callable(getattr(obj, 'writerow'))  
        
    def write_to_file(fileobj, filename, new_line, blank_lines=1):
        """
            Write text string to text file
                add blank lines before
                new_line: text to write to file
                blank_lines: number of blank lines to add before writing the new line
                
        """
        
        if fileobj is not None:  
            if is_csv_writer(fileobj):
                # If fileobj is a CSV writer, write a row
                # fileobj.writerow(new_line)  # Write the new line
                with open(filename, 'a', newline='') as file:
                    # writer = csv.writer(file,  
                    #                     delimiter=',', quotechar='"', escapechar='\\') # quoting=csv.QUOTE_NONE "not required for blank lines"
                    #                     #
                    # # Write blank lines before writing the new line
                    # writer.writerow([''] * blank_lines)  # Write blank lines
                    writer = csv.writer(file, quoting=csv.QUOTE_NONE,
                                        delimiter=',', quotechar='"', escapechar='\\')
                    writer.writerow(new_line)  # Write the new line
            else:
                # Otherwise, assume it's a regular file object and write a string
                new_line = str(new_line)
                # Write blank lines before writing the new line
                fileobj.write("\n" * blank_lines)
                fileobj.write(f"{new_line}")
            return True
        else:
            return False
    

    file_name = "search_string_in_file_full_read"
    create_file(file_name, ".txt")
    create_file(file_name, ".csv")
    
    fileobj_txt, file_txt_name = open_file(file_name, ".txt")
    fileobj_csv, file_csv_name = open_file(file_name, ".csv")
    
    string_to_find = "with "    
    for file in Path(path_source).glob('*'):
        if file.is_file():
            print(f" {file.name} ")
            full_path = Path(path_source) / Path(file.name) 
            if search_string_in_file_full_read(full_path, string_to_find):
                write_to_file(fileobj_txt, file_txt_name, f"'{string_to_find}' found in {full_path}")
                write_to_file(fileobj_csv, file_csv_name, [full_path, string_to_find, 'Yes'])
                continue
                print(f"'{string_to_find}' found in {full_path}")
            elif False:
                print(f"'{string_to_find}' not found in {full_path}")
        elif file.is_file == True:
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
    
finally:
    if 'fileobj_txt' in locals() and not fileobj_txt.closed: # Check if file object exists and is open
        close_file(fileobj_txt)
    #  if 'fileobj_csv' in locals() and not fileobj_csv.closed: # Check if file object exists and is open
    #      close_file(fileobj_csv)
    print("File closed successfully.")
    
quit()
