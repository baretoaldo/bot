from core.utils import logger
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import threading
import time
import keyboard
import queue
import logging


ascii_art = rf"""
  ___ ___                               ___ ___ ___________________ _________ .__         .__                      
 /   |   \   ___________   ____        /   |   \\_____  \__    ___/ \_   ___ \|  | _____  |__| _____   ___________ 
/    ~    \_/ __ \_  __ \_/ __ \      /    ~    \/   |   \|    |    /    \  \/|  | \__  \ |  |/     \_/ __ \_  __ \
\    Y    /\  ___/|  | \/\  ___/      \    Y    /    |    \    |    \     \___|  |__/ __ \|  |  Y Y  \  ___/|  | \/
 \___|_  /  \___  >__|    \___  > /\   \___|_  /\_______  /____|     \______  /____(____  /__|__|_|  /\___  >__|   
       \/       \/            \/  )/         \/         \/                  \/          \/         \/     \/     
                                     
Authors : MZGALANG

"""
# Disable logging from the browser
logging.getLogger('selenium').setLevel(logging.ERROR)
# Set up logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s | %(levelname)s | %(message)s')
logger = logging.getLogger(__name__)

MAX_CONCURRENT_THREADS = 5  # Set the maximum number of threads


def work_function(private_key, url, thread_index):
    browse(private_key, url, thread_index)


def proccessLoggin(driver, private_key, thread_index):

    logger.info(f"Thread {thread_index} | | Search Login Element")

    searchLoginElement = driver.find_element(
        'xpath', '/html/body/div[1]/div/button/p')
    time.sleep(1)
    searchLoginElement.click()

    time.sleep(3)

    logger.info(f"Thread {thread_index} | | Search Private Key Element")

    searchFormSeed = driver.find_element(
        'xpath', '//*[@id="root"]/div/div[1]/label/textarea')
    logger.info(f"Thread {thread_index} | | Add Private Key")
    time.sleep(1)
    searchFormSeed.send_keys(private_key)

    time.sleep(3)
    searchButton = driver.find_element(
        'xpath', '//*[@id="root"]/div/div[2]/button')
    logger.info(f"Thread {thread_index} | | Click Button Submit")
    time.sleep(1)
    searchButton.click()

    logger.info(
        f"Thread {thread_index} | | Waiting For import Account 10 seconds")
    time.sleep(10)

    searchButton = driver.find_element(
        'xpath', '//*[@id="root"]/div/button')
    logger.info(f"Thread {thread_index} | | Click Button Select Account")
    time.sleep(1)
    searchButton.click()

    logger.info(
        f"Thread {thread_index} | | Waiting For import Account 30 seconds")
    time.sleep(30)


def browse(private_key, url, thread_index):
    logger.info(
        f"Thread {thread_index} | | Started working for private key: {private_key}")

    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--incognito")

    # Set up the web driver (assuming you have chromedriver installed)
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(250, 750)

    # Calculate window position based on the thread index
    # Adjust this value based on your preference
    window_x_position = thread_index * 400
    window_y_position = 0

    driver.set_window_position(window_x_position, window_y_position)

    try:
        # Navigate to the specified URL
        driver.get(url)

        proccessLoggin(driver, private_key, thread_index)

        maxTry = 3

        refresh = False

        attempt = 0

        while attempt < maxTry:
            try:
                # Attempt to find the element

                if refresh == True:
                    searchFormSeed = driver.find_element(
                        'xpath', '//*[@id="root"]/div/div[1]/label/textarea')
                    time.sleep(1)
                    searchFormSeed.send_keys(private_key)
                    time.sleep(3)
                    searchButton = driver.find_element(
                        'xpath', '//*[@id="root"]/div/div[2]/button')
                    time.sleep(1)
                    searchButton.click()
                    logger.info(
                        f"Thread {thread_index} | | Waiting For import Account 10 seconds")
                    time.sleep(10)
                    searchButton = driver.find_element(
                        'xpath', '//*[@id="root"]/div/button')
                    time.sleep(1)
                    searchButton.click()
                    logger.info(
                        f"Thread {thread_index} | | Waiting For import Account 50 seconds (For safety)")
                    time.sleep(50)
                else:
                    searchUsername = driver.find_element(
                        'xpath', '//*[@id="root"]/div/div/div/div[1]/p')
                    # If the searchUsername element is found, perform your actions here
                logger.info(
                    "Thread {thread_index} | | Element 'searchUsername' found. Performing actions.")
                # Add your logic for when the element is found

                # If the element is found, break out of the loop
                break
            except NoSuchElementException:
                # If element not found, refresh the page
                logger.info(
                    f"Thread {thread_index} | | Element Not Found Refreshing Pages Try {attempt}x")
                driver.refresh()

                time.sleep(2)
                refresh = True
                attempt += 1
        else:
            # This block executes if the loop completes without a 'break' statement
            logger.warning(
                "Thread {thread_index} | | Maximum attempts reached. Element not found.")
            exit()

        logger.info(
            f"Thread {thread_index} | | Element Found, Wait 5 second for New Proccess")
        time.sleep(5)
        searchMinningSection = driver.find_element(
            'xpath', '//*[@id="root"]/div/div/div/div[3]/div[2]')
        logger.info(
            f"Thread {thread_index} | | Go to Minning Section")
        time.sleep(1)
        searchMinningSection.click()
        time.sleep(3)

        searchButtonClaim = driver.find_element(
            'xpath', '//*[@id="root"]/div/div[2]/div/div[3]/div/div[2]/div[2]/button')
        time.sleep(3)

        # Check if the button is clickable
        if searchButtonClaim.is_enabled():
            searchButtonClaim.click()
            logger.info(
                f"Thread {thread_index} | | Button Clicked Wait To claim")
            time.sleep(15)
            # You can perform other browser automation tasks here
            # Wait for the user to press 'q' to exit
            logger.info(f"Thread {thread_index} | | Done LFG BROOOO")
            # Perform actions on the clickable button, e.g., button.click()
        else:
            print("Button is not clickable.")
            logger.info(
                f"Thread {thread_index} | | Not Ready To Claim Run next time")
    finally:
        # Close the browser window
        driver.quit()
        logger.info(
            f"Thread {thread_index} | | Finished working for private key: {private_key}")


def main():
    print(ascii_art)

    # List of URLs to open concurrently
    urls = 'https://tgapp.herewallet.app/'

    with open('data/private_keys.txt', 'r') as file:
        private_keys = [line.strip() for line in file]

   # Use ThreadPoolExecutor to limit concurrent threads
    with ThreadPoolExecutor(max_workers=MAX_CONCURRENT_THREADS) as executor:
        # Submit tasks to the thread pool
        futures = {executor.submit(
            work_function, private_key, urls, i+1): private_key for i, private_key in enumerate(private_keys)}

        # Wait for all tasks to complete
        for future in concurrent.futures.as_completed(futures):
            private_key = futures[future]
            try:
                future.result()
            except Exception as e:
                logger.error(
                    f"Error processing private key {private_key}: {e}")


if __name__ == "__main__":
    main()
