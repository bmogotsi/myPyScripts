import os
import re

# Pattern to match files starting with "report" followed by digits, ending in ".pdf"
# pattern = re.compile(r"^report\d+\.pdf$")
pattern = re.compile(r"^\w+\.sql$")

#"C:/Users/Ben.Mogotsi/OneDrive - Momentum Group/Documents/My Documents/Liscoe/SquirreL_myFiles_2"
#"C:/Users/Ben.Mogotsi/OneDrive%20-%20Momentum%20Group/Documents/My%20Documents/Liscoe/SquirreL_myFiles_2/"
# files_in_dir = os.listdir("C:/Users/Ben.Mogotsi/OneDrive - Momentum Group/Documents/My Documents/Liscoe/SquirreL_myFiles_2")
files_in_dir = os.listdir(".")
regex_matches = [file for file in files_in_dir if pattern.search(file)]
# print(f"Files matching regex: {regex_matches}")
quit()
