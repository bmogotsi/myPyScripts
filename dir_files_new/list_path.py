from pathlib import Path
import traceback

"""pathlib
    is a powerful library in Python for working with file paths.
    It provides an object-oriented approach to handling file system paths,
        making it easier to manipulate and interact with files and directories.

        In this code snippet, we will use pathlib to
            list all files in a specified folder
            and delete those that end with " - Copy".

"""

# Specify the folder path
folder_path = Path("C:/Users/Ben.Mogotsi/OneDrive - Momentum Group/Documents/My Documents/Liscoe/SquirreL_myFiles_2")
folder_path = Path("C:/Users/Ben.Mogotsi/myPyScripts/dir_files")

try:
    # List all files in the folder
    files = [file.name for file in folder_path.iterdir() if file.is_file() and str(file).endswith(" - Copy")]
    for file in files:
        # ext = file.suffix
        # fstem = file.stem

        delete_fullPath = Path(folder_path._str+"/"+str(file))
        delete_fullPath.unlink()
    # print("Files in the folder:")
    # print("\n".join(files))


except Exception as e:
    print("Exception.........", str(e))
    traceback.print_exc()

quit()

def pathlib_example():
    """
        Here are some common operations you can perform with pathlib:
        methods and attributes/properties of pathlib.Path objects
    """

    folder_path.exists()  # Check if the folder exists
    folder_path.is_dir()  # Check if the path is a directory
    folder_path.iterdir()  # Iterate over the contents of the directory
    folder_path.name  # Get the name of the folder
    folder_path.suffix  # Get the file extension (if it's a file)
    folder_path.stem  # Get the file name without the extension (if it's a file)
    folder_path.parent  # Get the parent directory
    folder_path.joinpath("example.txt")  # Create a new path by joining with another path
    folder_path.glob("*.py")  # Get all Python files in the directory
    folder_path.rglob("*.py")  # Get all Python files in the directory and subdirectories
    folder_path.mkdir(exist_ok=True)  # Create the directory if it doesn't exist
    folder_path.rmdir()  # Remove the directory (only if it's empty)
    folder_path.unlink()  # Remove a file (if it's a file)
    folder_path.rename("new_folder_name")  # Rename the folder
    folder_path.resolve()  # Get the absolute path of the folder
    folder_path.stat()  # Get the status of the folder (e.g., size, permissions)
    folder_path.is_file()  # Check if the path is a file
    folder_path.is_dir()  # Check if the path is a directory
    folder_path.iterdir()  # Iterate over the contents of the directory
    folder_path.glob("*.sql")  # Get all SQL files in the directory

    return