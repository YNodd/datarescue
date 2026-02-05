

from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from helper_functions import print_red  # own module

def nominate_to_EOT_USGWDA(url_to_nominate, browser_driver, site_url):
    # Checks if the given url is already nominated to EOT/USGWDA, otherwise nominates it.
    # Returns False if anything went wrong, True if the url is (or was already) nominated
    browser_driver.get(site_url) # start the browser window
    sleep(0.5)
    # <input type="text" class="form-control" name="search-url-value" id="search-url-value" aria-describedby="help-block">
    search_form = WebDriverWait(browser_driver, 30).until(EC.presence_of_element_located((By.ID, "search-url-value")))
    #print("search_form found")
    search_form.send_keys(url_to_nominate)
    sleep(0.5)
    search_form.submit()

    url_already_nominated = None
    try:
        # searching for the text 'The requested URL was not in the system':
        sleep(1)
        browser_driver.find_element(By.XPATH, "//*[contains(text(), 'The requested URL was not in the system')]")
        sleep(1)
        print("The url was not yet nominated. ", end = "")
        url_already_nominated = False
    except NoSuchElementException:
        #print("Didn't find the text 'The requested URL was not in the system' – the url seems to be already nominated")
        try:  # check if the url was already nominated
            sleep(1)  # (this sleep is important))
            # <h4 class="panel-title">URL Information</h4>
            browser_driver.find_element(By.XPATH, "//h4[contains(text(), 'URL Information')]")
            sleep(1)
            print("The url was already nominated.")
            sleep(1)
            url_already_nominated = True
            return True
        except NoSuchElementException:
            print_red("There seems to be a problem with the nominating!")
            return False

    if url_already_nominated == False:
        # <input type="text" name="url_value" value="https://www.sciencebase.gov/catalog/item/5996123ce4b0fe2b9fea7919" id="url-value" class="form-control" required="">
        nominate_form = WebDriverWait(browser_driver, 30).until(EC.presence_of_element_located((By.ID, "url-value")))
        #print("Nominating the url now")
        sleep(0.5)
        nominate_form.clear()
        sleep(0.2)
        nominate_form.send_keys(url_to_nominate)
        sleep(0.5)
        nominate_form.submit()
        sleep(0.5)
        # Thank you for your nomination. View metadata entry for https://www.sciencebase.gov/catalog/item/5996123ce4b0fe2b9fea7919.
        WebDriverWait(browser_driver, 30).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Thank you for your nomination')]")))
        print(f"It should now be nominated to EOT/USGWDA: {url_to_nominate}")
        return True



if __name__ == "__main__":
    from selenium import webdriver
    testbrowser = webdriver.Firefox()
    nominate_to_EOT_USGWDA("https://www.sciencebase.gov/catalog/item/6388f263d34ed907bf78e921", testbrowser)
