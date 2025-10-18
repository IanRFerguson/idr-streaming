from time import sleep

import requests
from selenium import webdriver

#####


def run_driver():
    driver = webdriver.Firefox()
    driver.get("http://localhost:5000")

    while True:
        requests.get("http://localhost:5000/refresh")
        driver.refresh()
        sleep(3)


#####

if __name__ == "__main__":
    run_driver()
