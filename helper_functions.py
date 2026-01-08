

import os
import csv


def print_red(printtext, colourcode = 160):
    # helper function to print text in red (the colour codes can be found here: https://stackabuse.com/how-to-print-colored-text-in-python/
    #   (in the section "256 Colors in Raw Python")
    print(f"\033[38;5;{colourcode}m{printtext}\033[0;0m")

def print_orange(printtext, colourcode = 208):
    # helper function to print text in orange (the colour codes can be found here: https://stackabuse.com/how-to-print-colored-text-in-python/
    #   (in the section "256 Colors in Raw Python")
    print(f"\033[38;5;{colourcode}m{printtext}\033[0;0m")

def get_paths_uploadfiles(folderpath, projectfolder):
    # Builds a list with all the single file paths to be uploaded. Takes as argument the path to the parent folder,
    #   where all the data folders are located (for example, the path to the external USB drive).
    # todo: maybe include also subfolders?
    mypath = projectfolder
    if mypath[0:2] == ".\\" or mypath[0:2] == "./":
        # eliminate the first two characters, the dot and the slash:
        mypath = mypath[2:]
    operatingsystem = os.name
    if operatingsystem == "posix":  # for linux or mac
        mypath = mypath.replace("\\", "/")
        folderpath = folderpath.replace("\\", "/")
    elif operatingsystem == "nt":  # for windows
        mypath = mypath.replace("/", "\\")
        folderpath = folderpath.replace("\\", "/")
    combinedpath = os.path.join(folderpath, mypath)
    #print("combinedpath:", combinedpath)
    uploadfiles_names = os.listdir(combinedpath)
    # build the complete paths for the files that should be uploaded, by joining the single parts of the path:
    uploadfiles_paths = [os.path.join(combinedpath, filename) for filename in uploadfiles_names]
    # ensure that no paths of directories are taken for upload, if they're in the same folder (only keep the paths of the files):
    uploadfiles_paths = [filepath for filepath in uploadfiles_paths if os.path.isfile(filepath)]
    return uploadfiles_paths


def read_csv_line(csv_file, line_to_process):
    # Gets the input from the specified line of the csv file.
    with open(csv_file, "r", newline='') as datafile:
        datareader = csv.DictReader(datafile)
        for i, singlerow in enumerate(datareader):
            if i == (line_to_process - 1):  # -1 because i starts counting at 0
                return singlerow  # is already a dictionary


