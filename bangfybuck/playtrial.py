import base64
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from urllib.parse import urljoin
from selenium.webdriver.support.ui import WebDriverWait

import time
from selenium.webdriver.support import expected_conditions as EC

def get_all_images(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    
    # Wait for page to load
    time.sleep(5)

    # Scroll down to load dynamic content
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    # Wait for images to be present
    WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'img')))
    images = driver.find_elements(By.CSS_SELECTOR, ".sc-d13a0e88-1.cindWc")
    for img in images:
        src = img.get_attribute("src")
        print("Image source:", src)

get_all_images("https://www.noon.com/egypt-en/search/?q=shoes")


