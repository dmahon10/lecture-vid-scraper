## Web Scraper for Downloading Harvard Online Lectures

(Need HUID Login for the course used in this example. Adapt script for your own course.)

This is for keeping notes on what I learn and decisions I make in building this project. Later I will turn this into a more conventional README.

Some references:

- https://www.scrapingbee.com/blog/selenium-python/
- https://www.scrapingbee.com/blog/practical-xpath-for-web-scraping/



### How to Set Up Virtual Environments

<u>Good Resources</u>:

- https://www.youtube.com/watch?v=Kg1Yvry_Ydk
- https://medium.com/@jtpaasch/the-right-way-to-use-virtual-environments-1bc255a0cba7



<u>Steps</u>

- Install python3 & pip3
- Navigate to project directory
- Run:

```bash
python -m venv venv
```

- Do not put anything else in the `venv` directory. Keep all other project files outside of it.
- Put  `venv` in your `.gitignore`

```bash
git init
echo 'venv' > .gitignore
```

- Activate environment:

```bash
source venv/bin/activate
```

- Install something

```bash
pip install selenium
```

- Add dependencies (selenium) to `requirements.txt` . Someone else using this would simply run `pip install -r requirements.txt ` to install all necessary packages. (Maybe run the below command at the end because later we also install `wget`)

```bash
pip freeze > requirements.txt. 
```

- Check into source control

```bash
git add .
```

- To deactivate:

```bash
deactivate
```

The rest of this project will be run from within this virtual environment



### Download chromedriver via Homebrew

(Assuming you already have homebrew installed)

- From command line:

```bash
brew tap homebrew/cask
brew cask install chromedriver
```

- Confirm it was installed

```bash
chromedriver --version
```



### Test selenium and chromedriver

This program will operate in headful mode (with GUI)

```python
import time
from selenium import webdriver

# Chrome driver test code
driver = webdriver.Chrome()
driver.get('https://google.com') # Go to Google
time.sleep(5) # Allow time to see something happen
search_box = driver.find_element_by_name('q') # Get search box
search_box.send_keys('Harvard University') # Type in search
search_box.submit() # Submit search
time.sleep(5)
driver.quit()
```

This program runs headless and prints all `html` for the given page.pi

```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")

driver = webdriver.Chrome(options=options)
driver.get("https://www.google.com/")
print(driver.page_source)
driver.quit()
```



### High Level Steps

- Go to `https://cs61.seas.harvard.edu/site/2019/`
- Click on `Lecture Videos`
- Input username and password
- Click on `Lecture 1`
- Find video `url` in the `HTML`
- Run `wget -O lecture01.mp4 "<videoURLHere>"` to download in current directory
- Run video through `ffmpeg` to compress (this will create a second file)  ==(TODO)==
- Delete original 'mp4' file
- Repeat for each video



The only complication is that for "section" videos there are two each: one of the presenter and one of the screen. I want both. We will have to modify for this case. 



### Getting to page with all video links

As per test code above:

```python
driver = webdriver.Chrome()
driver.get('https://cs61.seas.harvard.edu/site/2019/')
```

To get the link to lecture videos highlight the link and press `cmd`  +  ` shift`  + ` c`.

This is the link:

```html
<a href="https://matterhorn.dce.harvard.edu/engage/ui/index.html#/2020/01/13836">Lecture videos (Harvard ID required)</a>
```

We should just go to this link from the get-go.

Now to iterate through all the videos links, get the video `url`s and download.



### Page navigation with XPath

Good [resource](https://www.scrapingbee.com/blog/practical-xpath-for-web-scraping/)

This will get the link to each page that a lecture video is watchable (not the actual `url` of the video)

```python
# Get all links to individual lectures (sections included for now)
link_elements = driver.find_elements_by_xpath("//a[contains(@class, 'live-event') and contains(@class, 'item-link')]")
video_links = [link.get_attribute('href') for link in link_elements]
```

Added this to navigate to each page for testing purposes:

```python
for link in video_links:
    driver.get(link)
    time.sleep(2)
```

Here I am being prompted to login at each so I will implement an auto login.

```python
def auto_login(driver, usern, passw):
    login = driver.find_element_by_id('username').send_keys(usern)
    password = driver.find_element_by_id('password').send_keys(passw)
    time.sleep(2)
    submit = driver.find_element_by_id('submitLogin').click()
```

Also being asked for DUO dual verification

It is in an `iframe` so will have to use `switch_to()` like so:

```python
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
```

We will only need to do this once.

Lastly we find, download and name the videos:

```python
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
```

And quit

```python
# Quit driver
driver.quit()
```









