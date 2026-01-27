

"""
Script to automate data rescue tasks, like uploading to DataLumos, nominating to EOT/USGWDA, ...

The information that has to be adjusted before starting the script is further below, between the hashtag-lines.
The path of the csv file has to be set before starting the script, the path to the folder with the data files too.
Also, the rows to be processed have to be set (start_row and end_row) - counting starts at 1 and doesn't include the column names row.
You can choose what actions should be executed (uploading, nominating to USGWDA) by setting the corresponding variable to False or True.

There is no error handling (But the browser remains open even if the script crashes).
"""


from selenium import webdriver
from time import sleep
#import traceback
import os

# for chrome:
from selenium.webdriver.chrome.options import Options as ChromeOptions
#from selenium.webdriver.chrome.service import Service as ChromeService
#from webdriver_manager.chrome import ChromeDriverManager

# import own modules (the corresponding files have to be saved in the same directory):
import size_and_extensions
import nominate
from helper_functions import print_red, print_orange, get_paths_uploadfiles, read_csv_line
import upload_to_datalumos


#########################################################

# TODO: VARIABLES TO SET:

csv_file_path = "my_current_inputdata.csv"  # or the complete path, for example: "/home/YNodd/PycharmProjects/datalumos/my_current_inputdata.csv"
folder_path_uploadfiles = "/media/YNodd/32 GB/data rescue project/"  # the folder where the upload files are (there, the subfolders for the single data projects are located)
# example: the files are on a USB flash drive, in a folder named "data rescue project", the example path would be: /media/YNodd/32 GB/data rescue project/
#   in there is the folder "national-transit-map-stops" which contains the zip-files and metadata.xml for uploading
browsertype = "chrome"  # "firefox" or "chrome"

start_row = 9 # WITHOUT COUNTING THE COLUMNS ROW!  (and beginning at 1)
end_row = 9 # (to process only one row, set start_row and end_row to the same number)

do_nominate_to_EOT = False # False or True
do_upload_to_datalumos = True # False if it shouldn't be uploaded automatically (or can't be because the script gets blocked from the website)
datalumos_upload_mode = "normal"  # "normal" for simply uploading files, or "zip" to use the import-from-zip upload (which unpacks files and folders after uploading)
#   Caution: to use the zip upload mode, the title of the project and the name of its folder and the name of the zip file have to be the same!

#########################################################

url_datalumos = "https://www.datalumos.org/datalumos/workspace"

#all_copypaste_rows = []  # todo for later


# todo: (maybe print out, which tasks were selected for execution)
# todo: (maybe check the variables that have to be set be the user right away at the start)

print_orange("\nIf you upload or work from USB device: MAKE SURE THE USB IS PLUGGED IN!")

# prepare the webdrivers for datalumos-upload or EOT-nominating:
if do_upload_to_datalumos == True or do_nominate_to_EOT == True:
    if browsertype.lower() == "firefox":
        browserdriver = webdriver.Firefox()

    elif browsertype.lower() == "chrome":

        # code from mkraley:
        # Set up Chrome options
        chrome_options = ChromeOptions()
        # Uncomment the line below to run in headless mode (no visible browser window)
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        # Initialize Chrome driver using webdriver-manager to automatically handle ChromeDriver
        #service = ChromeService(ChromeDriverManager().install())
        #browserdriver = webdriver.Chrome(service=service, options=chrome_options)
        browserdriver = webdriver.Chrome(options=chrome_options)
        #print(f"✓ Initialized Chrome browser")

    else:
        print_red("You didn't specify correct browser information. The browser variable has to be set either to firefox or to chrome.")


# loop through the individual rows to process the data:
for current_row in range(start_row, end_row + 1):
    #single_copypaste_row = {} # todo for later
    current_row_data = read_csv_line(csv_file_path, current_row)
    #print(datadict)
    print("\n\n----------------------------")
    print(f"Processing row {current_row}, Title: {current_row_data['4_title']}")
    print("----------------------------")

    # nominate, if required:
    if do_nominate_to_EOT == True:
        try:
            nominate.nominate_to_EOT_USGWDA(current_row_data["7_original_distribution_url"], browserdriver)
        except:
            print_red("\nSomething went wrong while trying to nominate the url!\n")
            #print(traceback.format_exc())

    # get the paths of all the files that are in the project folder
    filepaths = None
    if len(current_row_data["path"]) >= 2:
        filepaths = get_paths_uploadfiles(folder_path_uploadfiles, current_row_data["path"])
        #print("filepaths_:", filepaths)
        if len(filepaths) == 0:
            print_red("There are no file paths found! Are you sure your USB is plugged in and the path correct?\nThe code "
                      "will continue, but no files will be uploaded or processed otherwise!")
    else:
        print_red("You probably forgot to insert a filepath in the csv file.")


    if datalumos_upload_mode == "zip":
        # separate the zip file from the filepaths of the files in the project folder (to ensure for example that the
        #  size and extensions aren't taken from the zipped content too):
        #  the name of the zip file has to be the same as the title and the name of the project folder!

        zipfile_name = current_row_data['4_title'] + ".zip"  # get the path of the zip file
        #print(f"\nzipfile_name: {zipfile_name}")
        operatingsystem = os.name
        slash_char = "/" if operatingsystem == "posix" else "\\"  # assign the right kind of slash depending on the OS
        zipfile_path = folder_path_uploadfiles + current_row_data['4_title'] + slash_char + zipfile_name
        #print(f"zipfile_path: {zipfile_path}")
        if not os.path.exists(zipfile_path) and len(filepaths) != 0:
            print_red("The corresponding zip file wasn't found! Maybe the name of the file isn't identical to the project title and folder name?")
        else:
            #print("zipfile_path in filepaths:", zipfile_path in filepaths)
            try:
                filepaths.remove(zipfile_path)
            except ValueError:
                print_red("zipfile_path wasn't found in the list")
        # todo for later: maybe it would be better to automate the upload_mode selection (check if there are subfolders
        #  in the project folder, zip the content and choose zip as upload-mode) to avoid user error. Or maybe only use
        #  zip mode right away for all uploads and remove the "normal" parts from the script?

    # get the size and the file extensions of the data that should be uploaded:
    if filepaths != None and len(filepaths) != 0:
        datasize, filextensions = size_and_extensions.get_datasize_and_extensions(filepaths)
        print(f"size and file extensions: {datasize}\t{filextensions}")

    # fill in the forms on DataLumos and upload the data:
    if do_upload_to_datalumos == True:
        # if upload mode is "zip", only the file with the zipped project content is given to the upload function, otherwise
        #   the complete list of the files in the project folder (except this zipped content, which was removed from filepaths further above)
        upload_input = [zipfile_path] if datalumos_upload_mode == "zip" else filepaths
        #print(f"\nFile(s) that will be uploaded: {upload_input}")
        upload_to_datalumos.upload_csv_to_datalumos(current_row_data, browserdriver, upload_input, url_datalumos, datalumos_upload_mode)


    #all_copypaste_rows.append(single_copypaste_row)  # todo for later


    if current_row == end_row:
        print("\n\n---------------------------------")

        print("All required tasks should be completed now.\n")
        print_orange("Please check the script output for error messages (in red).\nAnd: If you want some sort of log for later, copy this output and save it in a text file (no logs are being generated at the moment!)\n")

        if do_upload_to_datalumos == True:
            print("\nFor DataLumos: Continue manually (check all the filled in details and publish the project(s))\n")

        #print("In the Inventory spreadsheet: Add the URL in the Download Location field, add 'Y’ to the Data Added field, and change the status field to ‘Done’.\n")
        print("In the Inventory spreadsheet: Add the needed data (for example: add the URL in the Download Location field, add 'Y’ to the Data Added field, ...).\n")
        # todo for later: maybe write function to generate copy-paste output and call it here (after asking the user if he wants it, y/n)




