import os
import traceback

all_files = list()
all_dirs = list()

path1 = "C:/Users/Ben.Mogotsi/OneDrive - Momentum Group/Documents/My Documents/Liscoe/SquirreL_myFiles_2"
path2 = "C:/Users/Ben.Mogotsi/myPyScripts/dir_files"
path2 = "C:/Users/Ben.Mogotsi/myPyScripts"

"""
    works well:
        deletes files that ENDs with " - Copy" in the name
        the sql files were selected by OS without extension.

        The os.walk() function in Python
            is a powerful and efficient way to traverse a directory tree recursively,
            either from top to bottom (default) or bottom to top.
"""

try:
    # Iterate for each dict object in os.walk()
    for root, dirs, files in os.walk(path2):
        # Add the files list to the all_files list
        all_files.extend(files)
        # Add the dirs list to the all_dirs list
        all_dirs.extend(dirs)

    for file in all_files:
        if str(file).endswith(".py"):
            print("Skip", {file})
        elif str(file).endswith(" - Copy"):
            os.remove(path2+"/"+str(file) )
            print("file removed", {file})
        else:
            print("leave alone", {file})

    # os.remove(file)
    # print(all_files)
except Exception as e:
    print("Exception.........", str(e))
    traceback.print_exc()

quit()