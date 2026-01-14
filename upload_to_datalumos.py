

"""
Script to automatically fill in the DataLumos fields from a csv file (exported spreadsheet), and upload the files.
Login, checking and publishing is done manually to avoid errors.

There is no error handling. But the browser remains open even if the script crashes, so the inputs could be checked and/or completed manually.
"""


from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import traceback
from time import sleep

# own modules:
from helper_functions import print_orange
import drag_and_drop_file



waiting_print_was_last = False  # helper variable to ensure the waiting-for-overlay info is just printed once, then represented with dots
datalumos_intro_already_shown = False  # helper variable to print the introduction only one time (at the first iteration)


def print_normal(printtext):
    # helper function to do a normal print and adjusting the variable waiting_print_was_last accordingly
    #   (to track if the last print was a waiting information or not)
    global waiting_print_was_last
    if waiting_print_was_last == False:
        print(printtext)
    else:
        print("\n" + printtext)  # print one more enter to ensure an empty line after the waiting info (which ends with end="")
    waiting_print_was_last = False

def print_red_with_waiting(printtext, colourcode = 160):
    global waiting_print_was_last
    print(f"\033[38;5;{colourcode}m{printtext}\033[0;0m")
    waiting_print_was_last = False


def wait_for_obscuring_elements_in_datalumos(current_driver_obj):

    global waiting_print_was_last

    overlays = current_driver_obj.find_elements(By.ID, "busy")  # caution: find_elements, not find_element
    if len(overlays) != 0:  # there is an overlay
        # The first time the  waiting information is printed out, then it's just printed as dots, until a "normal print" comes in between.
        if waiting_print_was_last == False:
            #print(f"... (Waiting for overlay to disappear. Overlay(s): {overlays})")
            print(f"\n(Waiting for overlay to disappear): .", end = "")
            waiting_print_was_last = True
        else:
            print(".", end = "")
        for overlay in overlays:
            # Wait until the overlay becomes invisible:
            WebDriverWait(current_driver_obj, 360).until(EC.invisibility_of_element_located(overlay))
            sleep(0.5)


def upload_csv_to_datalumos(datadict, mydriver, list_of_filepaths, workspace_url):

    global datalumos_intro_already_shown
    global waiting_print_was_last

    waiting_print_was_last = False # reset the variable for every new call/projet row

    mydriver.get(workspace_url) # start the browser window
    if datalumos_intro_already_shown == False:
        print_orange("\nLog in now (manually) in the browser\n")
        datalumos_intro_already_shown = True
    sleep(1)

    new_project_btn = WebDriverWait(mydriver, 360).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".btn > span:nth-child(3)"))) # .btn > span:nth-child(3)
    #print("button found")
    wait_for_obscuring_elements_in_datalumos(mydriver)
    new_project_btn.click()


    # --- Title

    # <input type="text" class="form-control" name="title" id="title" value="" data-reactid=".2.0.0.1.2.0.$0.$0.$0.$displayPropKey2.0.2.0">
    project_title_form = WebDriverWait(mydriver, 10).until(EC.presence_of_element_located((By.ID, "title")))
    # title with pre-title (if existent):
    pojecttitle = datadict["4_title"] if len(datadict["4_pre_title"]) == 0 else datadict["4_pre_title"] + " " + datadict["4_title"]
    project_title_form.send_keys(pojecttitle)
    # .save-project
    project_title_apply = WebDriverWait(mydriver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".save-project")))
    #print("project_title_apply - found")
    project_title_apply.click()
    # <a role="button" class="btn btn-primary" href="workspace?goToPath=/datalumos/239181&amp;goToLevel=project" data-reactid=".2.0.0.1.2.1.0.0.0">Continue To Project Workspace</a>
    #   CSS-selector: a.btn-primary
    project_title_apply2 = WebDriverWait(mydriver, 100).until(EC.presence_of_element_located((By.LINK_TEXT, "Continue To Project Workspace")))
    #print("Continue To Project Workspace - found")
    project_title_apply2.click()


    # --- expand everything

    # collapse all: <span data-reactid=".0.3.1.1.0.1.2.0.1.0.1.1"> Collapse All</span>
    #   css-selector: #expand-init > span:nth-child(2)
    collapse_btn = WebDriverWait(mydriver, 1500).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#expand-init > span:nth-child(2)")))
    wait_for_obscuring_elements_in_datalumos(mydriver)
    collapse_btn.click()
    sleep(2)
    # expand all: <span data-reactid=".0.3.1.1.0.1.2.0.1.0.1.1"> Expand All</span>
    #   CSS-selector:    #expand-init > span:nth-child(2)
    expand_btn = WebDriverWait(mydriver, 50).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#expand-init > span:nth-child(2)")))
    wait_for_obscuring_elements_in_datalumos(mydriver)
    expand_btn.click()
    sleep(2)


    # --- Government agency

    # government add value: <span data-reactid=".0.3.1.1.0.1.2.0.2.1:$0.$0.$0.0.$displayPropKey1.0.2.2"> add value</span>
    #   CSS-selector: #groupAttr0 > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > a:nth-child(3) > span:nth-child(3)
    agency_investigator = [datadict["5_agency"], datadict["5_agency2"]]
    for singleinput in agency_investigator:
        if len(singleinput) != 0 and singleinput != " ":
            add_gvmnt_value = WebDriverWait(mydriver, 100).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#groupAttr0 > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > a:nth-child(3) > span:nth-child(3)")))
            #print("add_gvmnt_value found")
            wait_for_obscuring_elements_in_datalumos(mydriver)
            add_gvmnt_value.click()
            # <a href="#org" aria-controls="org" role="tab" data-toggle="tab" data-reactid=".2.0.0.1.0.1.0">Organization/Agency</a>
            #    css-selector: div.modal:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > ul:nth-child(1) > li:nth-child(2) > a:nth-child(1)
            agency_tab = WebDriverWait(mydriver, 100).until(EC.element_to_be_clickable((By.LINK_TEXT, "Organization/Agency")))
            #print("agency_tab found")
            wait_for_obscuring_elements_in_datalumos(mydriver)
            agency_tab.click()
            # <input type="text" name="orgName" id="orgName" required="" class="form-control ui-autocomplete-input" value="" data-reactid=".2.0.0.1.1.1.0.0.0.1.0.0.0.1.0" autocomplete="off">
            agency_field = WebDriverWait(mydriver, 100).until(EC.presence_of_element_located((By.ID, "orgName")))
            agency_field.send_keys(singleinput)
            # submit: <button type="button" class="btn btn-primary save-org" data-reactid=".2.0.0.1.1.1.0.0.0.1.0.0.1.0.0">Save &amp; Apply</button>
            #   .save-org
            wait_for_obscuring_elements_in_datalumos(mydriver)

            # bits of code taken from mkraley:
            # Wait a moment for the dropdown to appear
            sleep(0.5)
            # Click on the Organization Name label to dismiss the dropdown
            org_label = mydriver.find_element(By.CSS_SELECTOR, "label[for='orgName']")  # (would be better with WebDriverWait() ?)
            org_label.click()

            submit_agency_btn = WebDriverWait(mydriver, 100).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".save-org")))
            submit_agency_btn.click()


    # --- Summary

    summarytext = datadict["6_summary_description"]
    if len(summarytext) != 0 and summarytext != " ":
        # summary edit: <span data-reactid=".0.3.1.1.0.1.2.0.2.1:$0.$0.$0.0.$displayPropKey2.$dcterms_description_0.1.0.0.0.2.1"> edit</span>
        #   CSS-selector: #edit-dcterms_description_0 > span:nth-child(2)
        edit_summary = WebDriverWait(mydriver, 100).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#edit-dcterms_description_0 > span:nth-child(2)")))
        #print("edit_summary found")
        wait_for_obscuring_elements_in_datalumos(mydriver)
        edit_summary.click()
        # summary form: <body contenteditable="true" class="editable-wysihtml5 wysihtml5-editor" spellcheck="true" style="background-color: rgb(255, 255, 255); color: rgb(51, 51, 51); cursor: text; font-family: &quot;Atkinson Hyperlegible&quot;, sans-serif; font-size: 16px; font-style: normal; font-variant: normal; font-weight: 400; line-height: 20px; letter-spacing: normal; text-align: start; text-decoration: rgb(51, 51, 51); text-indent: 0px; text-rendering: optimizelegibility; word-break: normal; overflow-wrap: break-word; word-spacing: 0px;"><span id="_wysihtml5-undo" class="_wysihtml5-temp">﻿</span></body>
        #   css-sel.: body

        # code from mkraley (without this, there seem to be issues if used with Chrome instead of Firefox):
        # summary form: The WYSIWYG editor is inside an iframe with class "wysihtml5-sandbox"
        #   First, find and switch to the iframe
        wysihtml5_iframe = WebDriverWait(mydriver, 100).until(EC.presence_of_element_located((By.CSS_SELECTOR, "iframe.wysihtml5-sandbox")))
        mydriver.switch_to.frame(wysihtml5_iframe)
        # Now find the body element inside the iframe
        summary_form = WebDriverWait(mydriver, 100).until(EC.presence_of_element_located((By.CSS_SELECTOR, "body")))
        # Click to focus the contenteditable element
        summary_form.click()
        sleep(0.3)
        # Clear any existing content
        summary_form.send_keys(Keys.CONTROL + "a")
        sleep(0.2)
        # Use JavaScript to set the text content (more reliable for contenteditable elements)
        # Use the fixed summary text
        mydriver.execute_script("arguments[0].textContent = arguments[1];", summary_form, summarytext)
        # Trigger input event to ensure the editor recognizes the change
        mydriver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", summary_form)
        sleep(0.3)
        # Switch back to default content before clicking save button (which is outside iframe)
        mydriver.switch_to.default_content()
        wait_for_obscuring_elements_in_datalumos(mydriver)

        # save: <i class="glyphicon glyphicon-ok"></i>
        #   .glyphicon-ok
        save_summary_btn = WebDriverWait(mydriver, 100).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".glyphicon-ok")))
    else:
        print_red_with_waiting("The summary is mandatory for the DataLumos project! Please fill it in manually.")


    # --- Original Distribution url

    original_url_text = datadict["7_original_distribution_url"]
    if len(original_url_text) != 0 and original_url_text != " ":
        # edit: <span data-reactid=".0.3.1.1.0.1.2.0.2.1:$0.$0.$0.0.$displayPropKey4.$imeta_sourceURL_0.1.0.0.0.2.0.1"> edit</span>
        #   css-sel: #edit-imeta_sourceURL_0 > span:nth-child(1) > span:nth-child(2)
        orig_distr_edit = WebDriverWait(mydriver, 100).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#edit-imeta_sourceURL_0 > span:nth-child(1) > span:nth-child(2)")))
        wait_for_obscuring_elements_in_datalumos(mydriver)
        orig_distr_edit.click()
        # form: <input type="text" class="form-control input-sm" style="padding-right: 24px;">
        #   css-sel.: .editable-input > input:nth-child(1)
        orig_distr_form = WebDriverWait(mydriver, 100).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".editable-input > input:nth-child(1)")))
        wait_for_obscuring_elements_in_datalumos(mydriver)
        orig_distr_form.send_keys(original_url_text)
        # save: <button type="submit" class="btn btn-primary btn-sm editable-submit"><i class="glyphicon glyphicon-ok"></i> save</button>
        #   css-sel: .editable-submit
        orig_distr_form.submit()


    # --- Subject Terms / keywords

    # form: <input class="select2-search__field" type="search" tabindex="0" autocomplete="off" autocorrect="off" autocapitalize="none" spellcheck="false" role="textbox" aria-autocomplete="list" placeholder="" style="width: 0.75em;">
    #   css-sel: .select2-search__field
    # scroll bar: <li class="select2-results__option select2-results__option--highlighted" role="treeitem" aria-selected="false">HIFLD Open</li>
    #    css-sel: .select2-results__option
    keywordcells = [datadict["8_subject_terms1"], datadict["8_subject_terms2"], datadict["8_keywords"]]
    keywords_to_insert = []
    for single_keywordcell in keywordcells:
        if len(single_keywordcell) != 0 and single_keywordcell != " ":
            more_keywords = single_keywordcell.replace("'", "").replace("[", "").replace("]", "").replace('"', '')  # remove quotes and brackets
            more_keywordslist = more_keywords.split(",")
            keywords_to_insert += more_keywordslist
    print_normal(f"\nkeywords_to_insert: {keywords_to_insert}")
    for single_keyword in keywords_to_insert:
        keyword = single_keyword.strip(" '")
        try:
            wait_for_obscuring_elements_in_datalumos(mydriver)
            keywords_form = WebDriverWait(mydriver, 50).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".select2-search__field")))
            keywords_form.click()
            keywords_form.send_keys(keyword)
            #sleep(2)
            wait_for_obscuring_elements_in_datalumos(mydriver)
            #keyword_sugg = WebDriverWait(mydriver, 50).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".select2-results__option")))
            # find the list element, taking care to match the exact text [suggestion from user sefk]:
            keyword_sugg = WebDriverWait(mydriver, 50).until(EC.element_to_be_clickable((By.XPATH, f"//li[contains(@class, 'select2-results__option') and text()='{keyword}']")))
            wait_for_obscuring_elements_in_datalumos(mydriver)
            keyword_sugg.click()
        except:
            print_red_with_waiting("\nThere was a problem with the keywords! Please check if one ore more are missing in the form and fill them in manually.\n Problem:")
            print_normal(traceback.format_exc())


    # --- Geographic Coverage

    geographic_coverage_text = datadict["9_geographic_coverage"]
    if len(geographic_coverage_text) != 0 and geographic_coverage_text != " ":
        # edit: <span data-reactid=".0.3.1.1.0.1.2.0.2.1:$0.$1.$1.0.$displayPropKey1.0.5:$dcterms_location_0_0.0.0.0.0.2.0.1"> edit</span>
        #   css-sel: #edit-dcterms_location_0 > span:nth-child(1) > span:nth-child(2)
        geogr_cov_edit = WebDriverWait(mydriver, 50).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#edit-dcterms_location_0 > span:nth-child(1) > span:nth-child(2)")))
        #print("edit-button geogr_cov_form found")
        wait_for_obscuring_elements_in_datalumos(mydriver)
        geogr_cov_edit.click()
        # form: <input type="text" class="form-control input-sm" style="padding-right: 24px;">
        #   .editable-input > input:nth-child(1)
        geogr_cov_form = WebDriverWait(mydriver, 50).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".editable-input > input:nth-child(1)")))
        wait_for_obscuring_elements_in_datalumos(mydriver)
        geogr_cov_form.send_keys(geographic_coverage_text)
        geogr_cov_form.submit()


    # --- Time Period

    timeperiod_start_text = datadict["10_time_period1"]
    timeperiod_end_text = datadict["10_time_period2"]
    if len(timeperiod_start_text) != 0 or len(timeperiod_end_text) != 0:
        # edit: <span data-reactid=".0.3.1.1.0.1.2.0.2.1:$0.$1.$1.0.$displayPropKey2.0.2.2"> add value</span>
        #   #groupAttr1 > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > a:nth-child(3) > span:nth-child(3)
        time_period_add_btn = WebDriverWait(mydriver, 50).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#groupAttr1 > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > a:nth-child(3) > span:nth-child(3)")))
        #print("time_period_add_btn found")
        wait_for_obscuring_elements_in_datalumos(mydriver)
        time_period_add_btn.click()
        # start: <input type="text" class="form-control" name="startDate" id="startDate" required="" placeholder="YYYY-MM-DD or YYYY-MM or YYYY" title="Enter as YYYY-MM-DD or YYYY-MM or YYYY" value="" data-reactid=".4.0.0.1.1.0.1.0">
        #   #startDate
        time_period_start = WebDriverWait(mydriver, 50).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#startDate")))
        wait_for_obscuring_elements_in_datalumos(mydriver)
        time_period_start.send_keys(timeperiod_start_text)
        # <input type="text" class="form-control" name="endDate" id="endDate" placeholder="YYYY-MM-DD or YYYY-MM or YYYY" title="Enter as YYYY-MM-DD or YYYY-MM or YYYY" value="" data-reactid=".4.0.0.1.1.1.1.0">
        #   #endDate
        time_period_end = WebDriverWait(mydriver, 50).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#endDate")))
        wait_for_obscuring_elements_in_datalumos(mydriver)
        time_period_end.send_keys(timeperiod_end_text)
        # <button type="button" class="btn btn-primary save-dates" data-reactid=".4.0.0.1.1.3.0.0">Save &amp; Apply</button>
        #    .save-dates
        save_time_btn = WebDriverWait(mydriver, 50).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".save-dates")))
        wait_for_obscuring_elements_in_datalumos(mydriver)
        save_time_btn.click()


    # --- Data types

    datatype_to_select = datadict["11_data_types"]
    if len(datatype_to_select) != 0 and datatype_to_select != " ":
        # <span data-reactid=".0.3.1.1.0.1.2.0.2.1:$0.$1.$1.0.$displayPropKey5.$disco_kindOfData_0.1.0.0.0.2.1"> edit</span>
        #   #disco_kindOfData_0 > span:nth-child(2)
        datatypes_edit_btn = WebDriverWait(mydriver, 50).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#disco_kindOfData_0 > span:nth-child(2)")))
        wait_for_obscuring_elements_in_datalumos(mydriver)
        datatypes_edit_btn.click()
        wait_for_obscuring_elements_in_datalumos(mydriver)
        # <span> geographic information system (GIS) data</span>  # (there is a space character at the beginning of the string!)
        #   .editable-checklist > div:nth-child(8) > label:nth-child(1) > span:nth-child(2)
        datatype_text = WebDriverWait(mydriver, 50).until(EC.presence_of_element_located((By.XPATH, f"//span[contains(text(), '{datatype_to_select}')]")))
        datatype_text.click()
        # <button type="submit" class="btn btn-primary btn-sm editable-submit"><i class="glyphicon glyphicon-ok"></i> save</button>
        #   .editable-submit
        datatypes_save_btn = WebDriverWait(mydriver, 50).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".editable-submit")))
        datatypes_save_btn.click()


    # --- Collection Notes

    if len(datadict["12_collection_notes"]) != 0 or len(datadict["12_download_date_original_source"]) != 0:
        # check if there is data in the date field (otherwise set it to empty string):
        downloaddate = f"(Downloaded {datadict['12_download_date_original_source']})" if len(datadict["12_download_date_original_source"]) != 0 else ""
        # the text for collection notes is the note and the download date, if the note cell in the csv file isn't empty (otherwise it's only the date):
        text_for_collectionnotes = datadict["12_collection_notes"] + " " + downloaddate if len(datadict["12_collection_notes"]) != 0 and datadict["12_collection_notes"] != " " else downloaddate
        # css-sel.: #edit-imeta_collectionNotes_0 > span:nth-child(2)
        coll_notes_edit_btn = WebDriverWait(mydriver, 50).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#edit-imeta_collectionNotes_0 > span:nth-child(2)")))
        wait_for_obscuring_elements_in_datalumos(mydriver)
        coll_notes_edit_btn.click()
        # css-sel: body

        # code from mkraley (without this, there seem to be issues if used with Chrome instead of Firefox), same problem as further above with the summary form:
        # The WYSIWYG editor is inside an iframe with class "wysihtml5-sandbox"
        #   First, find and switch to the iframe
        wysihtml5_iframe = WebDriverWait(mydriver, 50).until(EC.presence_of_element_located((By.CSS_SELECTOR, "iframe.wysihtml5-sandbox")))
        mydriver.switch_to.frame(wysihtml5_iframe)
        # Now find the body element inside the iframe
        coll_notes_form = WebDriverWait(mydriver, 50).until(EC.presence_of_element_located((By.CSS_SELECTOR, "body")))
        # Click to focus the contenteditable element
        coll_notes_form.click()
        sleep(0.3)
        # Clear any existing content
        coll_notes_form.send_keys(Keys.CONTROL + "a")
        sleep(0.2)
        # Use JavaScript to set the text content (more reliable for contenteditable elements)
        mydriver.execute_script("arguments[0].textContent = arguments[1];", coll_notes_form, text_for_collectionnotes)
        # Trigger input event to ensure the editor recognizes the change
        mydriver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", coll_notes_form)
        sleep(0.3)
        # Switch back to default content before clicking save button (which is outside iframe)
        mydriver.switch_to.default_content()
        wait_for_obscuring_elements_in_datalumos(mydriver)

        # css-sel: .editable-submit
        coll_notes_save_btn = WebDriverWait(mydriver, 50).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".editable-submit")))
        coll_notes_save_btn.click()


    # --- Upload files

    if len(datadict["path"]) != 0 and datadict["path"] != " ":
        # upload-button: <span data-reactid=".0.3.1.1.0.0.0.0.0.0.1.2.3">Upload Files</span>
        #   a.btn-primary:nth-child(3) > span:nth-child(4)
        wait_for_obscuring_elements_in_datalumos(mydriver)
        upload_btn = WebDriverWait(mydriver, 50).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.btn-primary:nth-child(3) > span:nth-child(4)")))
        upload_btn.click()
        wait_for_obscuring_elements_in_datalumos(mydriver)
        fileupload_field = WebDriverWait(mydriver, 50).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".col-md-offset-2 > span:nth-child(1)")))

        for singlefile in list_of_filepaths:
            drag_and_drop_file.drag_and_drop_file(fileupload_field, singlefile)

        # when a file is uploaded and its progress bar is complete, a text appears: "File added to queue for upload."
        #   To check that the files are completely uploaded, this text has to be there as often as the number of files:
        filecount = len(list_of_filepaths)
        #print("filecount:", filecount)
        #sleep(10)
        test2 = mydriver.find_elements(By.XPATH, "//span[text()='File added to queue for upload.']")
        # wait until the text has appeared as often as there are files:
        #   (to wait longer for uploads to be completed, change the number in WebDriverWait(mydriver, ...) - it is the waiting time in seconds)
        WebDriverWait(mydriver, 2000).until(lambda x: True if len(mydriver.find_elements(By.XPATH, "//span[text()='File added to queue for upload.']")) == filecount else False)
        print_normal("\nAll files should be uploaded completely now.\n")


        # close-btn: .importFileModal > div:nth-child(3) > button:nth-child(1)
        wait_for_obscuring_elements_in_datalumos(mydriver)
        close_btn = WebDriverWait(mydriver, 50).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".importFileModal > div:nth-child(3) > button:nth-child(1)")))
        close_btn.click()
