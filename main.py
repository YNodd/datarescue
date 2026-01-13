

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

start_row = 8 # WITHOUT COUNTING THE COLUMNS ROW!  (and beginning at 1)
end_row = 9 # (to process only one row, set start_row and end_row to the same number)

do_nominate_to_EOT = False # False or True
do_upload_to_datalumos = True # False if it shouldn't be uploaded automatically (or can't be because the script gets blocked from the website)

#########################################################

url_datalumos = "https://www.datalumos.org/datalumos/workspace"

#all_copypaste_rows = []  # todo for later

# todo: (maybe print out, which tasks were selected for execution)

# prepare the webdrivers for datalumos-upload or EOT-nominating:
if do_upload_to_datalumos == True or do_nominate_to_EOT == True:
    browserdriver = webdriver.Firefox() # firefox must be installed on the computer, or the code should be changed for another browser


# loop through the individual rows to process the data:
for current_row in range(start_row, end_row + 1):
    #single_copypaste_row = {} # todo for later
    current_row_data = read_csv_line(csv_file_path, current_row)
    #print(datadict)
    print("\n----------------------------")
    print(f"Processing row {current_row}, Title: {current_row_data['4_title']}")
    print("----------------------------")

    # nominate, if required:
    if do_nominate_to_EOT == True:
        try:
            nominate.nominate_to_EOT_USGWDA(current_row_data["7_original_distribution_url"], browserdriver)
        except:
            print_red("\nSomething went wrong while trying to nominate the url!\n")
            #print(traceback.format_exc())

    # get the paths of the files that should be uploaded
    filepaths_to_upload = None
    if len(current_row_data["path"]) >= 2:
        try:
            filepaths_to_upload = get_paths_uploadfiles(folder_path_uploadfiles, current_row_data["path"])
            #print("filepaths_to_upload:", filepaths_to_upload)
        except FileNotFoundError:
            print_red("\nFile not found. Are you sure your USB is plugged in and the path correct?")
    else:
        print_red("You probably forgot to insert a filepath in the csv file.")

    # get the size and the file extensions of the data that should be uploaded:
    if filepaths_to_upload != None and len(filepaths_to_upload) != 0:
        datasize, filextensions = size_and_extensions.get_datasize_and_extensions(filepaths_to_upload)
        #print(f"size and file extensions: {datasize}\t{filextensions}")

    # fill in the forms on DataLumos and upload the data:
    if do_upload_to_datalumos == True:
        print(f"\nFiles that will be uploaded: {filepaths_to_upload}\n")
        upload_to_datalumos.upload_csv_to_datalumos(current_row_data, browserdriver, filepaths_to_upload, url_datalumos)

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




