<br>

**PLEASE NOTE: The upload (to DataLumos) part of the script doesn't work anymore, because the it is detected by the webpage / Cloudflare!**

# What it is
It's a script to make it easier to process the projects for rescuing public data. You can use it for nominating the URLs to USGWDA as well as automatically filling in the forms in DataLumos and upload the data (and then check and publish it manually). <br>
What tasks to execute can be chosen by setting the corresponding variables (for more details, see further below).<br>
For now, log in to DataLumos and the publishing step have to be done manually.<br>
It is rather an enhancement for "manually" uploading. If you need full automation, you can use this script as a basis for your own code, or you can find mkraley's complete automation here: https://github.com/mkraley/CDCDataCollector



# How it works
Prepare your metadata by using the template (TEMPLATE_inputdata_for_datalumos.ods), then export it to csv.<br>
Take care that all the needed files of this script are located in the same directory.<br>
Set the variables on top of the main.py file (see below for further information), then run the script.


## the different variables to set before running the script:
- **csv_file_path**: the path where the csv file is located. For example: "/home/YNodd/PycharmProjects/datalumos/my_current_inputdata.csv"
- **folder_path_uploadfiles**: the folder where the upload files are (there, the subfolders for the single data projects are located)<br>
Example: the files are on a USB flash drive, in a folder named "data rescue project", the example path would be: /media/YNodd/32 GB/data rescue project/<br>
In there is the folder "national-transit-map-stops" which contains the zip-files and metadata.xml for uploading.
- **browser_type**: "firefox" or "chrome". (I initially wrote this code for Firefox, but Chrome seems to handle the Cloudflare verification better; it rarely runs into a blocking loop).
- **start_row**: the number of the start row (without counting the columns), begins counting at 1 (not zero)
- **end_row**: the number of the end row. To process only one row, set start_row and end_row to the same number.
- **do_nominate_to_EOT**: if the URLs should be nominated to EOT/USGWDA
- **do_upload_to_datalumos**: if the data should be uploaded to DataLumos (fill in the forms, upload the files)


## about the template spreadsheet:
- The black column names are the ones that are processed by the code (I added the red columns for my own use).
- The names of the columns that are processed in the script cannot be changed (or the code has to be changed too), but they can be left empty if not needed.
Other columns can be added (but will be ignored by the code), and the order of the columns doesn't matter (they can be arranged as you work best).
- The "path" column is the folder name for the folder where the data files are located, and can be in this format: .\epa-facilities, but can also be written without .\ at the beginning. It also doesn't matter if the path is in linux or windows format, both / and \ can be used. 
- the keywords have to be separated by commas in the spreadsheet cell. They can be written with quotation marks or not, and they can optionally be between square brackets.
- the cells in the column "related_resources" have to be the DOI's of the related resources. Multiple entries have to be separated by a comma and a space (example: 10.3133/sir20185001, 10.3133/sir20125088)

(the numbers in the column names have no special meaning; they are only a historic leftover)

## the different functions:
- **main.py**: main part where the different functions get called, if needed.
- **nominate.py**: nominates a given URL to USGWDA (formerly EOT)
- **size_and_extensions.py**: gets the size of all files in a projectfolder, and their file name extensions.
- **upload_to_datalumos.py**: Script to automatically fill in the DataLumos forms from a csv file (exported spreadsheet), and upload the data files. Login, checking and publishing is done manually to avoid errors. It allows adding many data projects to DataLumos in one go. <br>
You can process more than one data project at once with the csv file; the script adds the projects to the workspace. You can check and publish them later.<br>
(BUT NOTE: This part of the script doesn't work any more, because DataLumos blocks automatic scripts).
- **drag_and_drop_file.py**: is needed to drag and drop files into the DataLumos webpage for uploading 
- **helper_functions.py**: here are located some helper functions, like printing in colour or getting the paths of every file in a project folder



# Benefits and drawbacks
benefits:
- the use of the script speeds up "manual" data rescuing and allows batch processing. When the csv file is prepared, putting data and metadata to DataLumos basically does the work by itself; it's easier to fill in the data in a spreadsheet than in the forms of DataLumos (for example the keywords). Additionally you simply can copy-paste the details that stay the same. And when the site is loading slow, you don't need to wait for every single input to be processed while you stare at the "busy" icon ;)
- the code or parts of it can be used for automation, to speed up data rescue tasks.<br>
A csv file in the needed format (as shown in the template) can be created manually. Or you can write your own code to produce the csv automatically, for example while scraping the datasets from the websites.

drawbacks:
- there is no error handling, which is no problem when using the script as intended, because nothing is published automatically - the project can be checked and altered before publishing manually. But take this into consideration when using it as a basis for your own automation code (once published to DataLumos, a project can't be deleted anymore).
- Note: it seems best to not do batches with more than 10 projects, because of how the DataLumos page behaves.


# Installation

[Firefox][] is a requirement. (Chrome works now too.)

Selenium does the heavy lifting for the script. But before installing that, you may
want to create a virtual environment.

```bash
python3 -m venv env
source ./env/bin/activate
```

If you do this, remember to source this virtual environment every time you work
here. Or consider setting up [direnv][] as a convenient way to automatically
source this environment whenever you're in this directory. The provided `.envrc`
assumes your virtual environment is in `env`.

_Now_ you're ready to install your requirements.

```bash
pip3 install -r requirements.txt
```

[Firefox]: https://www.firefox.com/
[direnv]: https://direnv.net/




<br>
<br>

----------------------
**This repository is based on an old one ([https://github.com/YNodd/create-DataLumos-projects-from-csv-file](https://github.com/YNodd/create-DataLumos-projects-from-csv-file)) which I reorganized and integrated here.**<br>

**Thanks to sefk and mkraley for their contributions.**