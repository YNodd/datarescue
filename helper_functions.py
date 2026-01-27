

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
    uploadfiles_paths = []
    subfolder_list = []  # list for the subfolder names, if there are any
    for foldername, subfolders, filenames in os.walk(combinedpath):
        #print('current folder is ' + foldername)
        for subfolder in subfolders:
            subfolder_list.append(subfolder)
        for filename in filenames:
            # build the paths for the files that should be uploaded, by joining the single parts of the path:
            uploadfiles_paths.append(os.path.join(foldername, filename))
            #if not os.path.exists(os.path.join(foldername, filename)):
                #print_red("DOESNT EXIST")
    if len(subfolder_list) > 0:
        print_orange(f"There are subfolders in the project folder. If the upload-modus for Datalumos isn't 'zip', the files "
                     f"will be uploaded, but not organized into the subfolder structure! Also size and extensions will be false!")  # \n\tThe subfolder names are: {subfolder_list}
    return uploadfiles_paths


def read_csv_line(csv_file, line_to_process):
    # Gets the input from the specified line of the csv file.
    with open(csv_file, "r", newline='') as datafile:
        datareader = csv.DictReader(datafile)
        for i, singlerow in enumerate(datareader):
            if i == (line_to_process - 1):  # -1 because i starts counting at 0
                return singlerow  # is already a dictionary




if __name__ == "__main__":
    testpaths = get_paths_uploadfiles("/media/YNodd/D-LIVE 12_2/sciencebase_downloads_3/", "FiCli Fish and Climate Change Database (ver. 3.0, October 2024)/")
    for singletestp in testpaths:
        print(singletestp)
