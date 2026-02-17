

"""https://discuss.python.org/t/os-walk-and-copying-files/83848
     I’m attempting to create a script to back up all directories and files
    from my linux home folder to a USB drive,
    excepting all which are not hidden and those which are already save on the USB.

    My code successfully copies any new folders and sub-folders from the source (src) directory
     to the destination (dst) directory,
        but it is not copying any files.

         I believe something’s not right with the os.walk in the “for file in files” section,
         but can’t figure what. Likely something simple but this novice doesn’t see it!
         Thanks for any suggested fixes you may have!

        Below is the current code:
"""

"""Check if all subdirectories in a DIST directory exist
    and then copy any new subdirectories and files from a SRC directory
        to usb drive while excluding hidden files and directories
            and those that already exist in the destination.

    DST = destination directory (e.g., USB drive)
    SRC = source directory (e.g., home folder/C drive)

"""
import os
import shutil
import traceback

try:
    def check_and_copy(src, dst):
        # Check if source and destination directories exist
        if not os.path.exists(src):
            raise FileNotFoundError(f"The source directory {src} does not exist.")
        if not os.path.exists(dst):
            #os.makedirs(dst)
            raise FileNotFoundError(f"The Destination USB drive {dst} does not exist.")

        # Walk through the source directory
        for root, dirs, files in os.walk(src):
            # Skip hidden directories
            dirs[:] = [d for d in dirs if not d.startswith('.')]

            # Create corresponding directory in destination
            for d in dirs:
                src_dir = os.path.join(root, d)
                dst_dir = os.path.join(dst, os.path.relpath(src_dir, src))
                if not os.path.exists(dst_dir):
                    os.makedirs(dst_dir)
                    print(f"Creating directory {d}")
                else:
                    print(f"Directory {d} already exists in destination, skipping.")

            # Copy files from source to destination
            for file in files:
                if not file.startswith('.'):
                    # Check if the file does not already exist in the destination
                    if not os.path.exists(dst+"/"+file):
                        src_file = os.path.join(root, file)
                        dst_file = os.path.join(dst, os.path.relpath(src_file, src))
                        shutil.copy2(src_file, dst_file)
                        print(f"Copied file named {file}")
                    else:
                        print(f"File {file} already exists in destination, skipping.")

        print(f"********** END OF BACKUP **********")

    check_and_copy('C:/Users/Ben.Mogotsi/myPyScripts/dir_files', 'C:/Users/Ben.Mogotsi/myPyScripts/dir_files_new')
except Exception as e:
    print("Exception.........", str(e))
    traceback.print_exc()

quit()