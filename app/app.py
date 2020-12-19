import time, wget, os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

USERNAME = "yourUsernameHere"
PASSWORD = "yourPasswordHere"
PATH = "pathToWhereYouWantToSave"
LECTURE_LIST_URL = "https://matterhorn.dce.harvard.edu/engage/ui/index.html#/2020/01/13836" # CS61 lecture videos page

def auto_login(driver, usern, passw):
    # Username
    driver.find_element_by_id('username').send_keys(usern)
    # Password
    driver.find_element_by_id('password').send_keys(passw)
    # Submit
    driver.find_element_by_id('submitLogin').click()


if __name__ == "__main__":

    # Chrome driver (headful)
    driver = webdriver.Chrome()
    driver.get(LECTURE_LIST_URL) # Go to lecture video site
    time.sleep(2) # Allow time to see something happen

    # Get all links to individual videos
    link_elements = driver.find_elements_by_xpath("//a[contains(@class, 'live-event') and contains(@class, 'item-link')]")
    video_links = [link.get_attribute('href') for link in link_elements]
    video_links.reverse()

    # Counters for naming
    lec_count = 1
    sec_count = 1

    # Iterate through all videos
    for i, link in enumerate(video_links):
        driver.get(link)
        time.sleep(1)

        # Login and dual verification first time only
        if i == 0:

            # Will be redirected to login page
            auto_login(driver, USERNAME, PASSWORD)

            # Switch to control embeded duo iframe
            iframe = driver.find_element_by_xpath("//iframe[@id='duo_iframe']")
            driver.switch_to.frame(iframe)

            # Remember me
            driver.find_element_by_xpath(".//*[contains(text(), 'Remember me for 30 days')]").click()
            time.sleep(1)

            # Send push to iPhone
            driver.find_element_by_xpath(".//*[contains(text(), 'Send Me a Push')]").click()
            time.sleep(10)
        
        # Find videos
        mp4_elements = driver.find_elements_by_tag_name("source")
        mp4_urls = [mp4_element.get_attribute("src") for mp4_element in mp4_elements]

        # Download and name video files
        for j, mp4 in enumerate(mp4_urls):

            if len(mp4_urls) < 2:
                name = "lecture"
                count = str(lec_count)
                lec_count += 1
            
            else:
                name = "section"
                count = str((sec_count + 1) // 2) + "screen" + str(j + 1)
                sec_count += 1

            path_name = PATH + name + count + ".mp4"

            # Download
            wget.download(mp4, path_name)
    
    # Quit driver
    driver.quit()
            

    # Switch back
    # driver.switch_to.default_content()

    # Headless
    # options = Options()
    # options.headless = True
    # options.add_argument("--window-size=1920,1200")
    # driver = webdriver.Chrome(options=options)
    # driver.get("insertURLhere")
    # print(driver.page_source)
    # driver.quit()

