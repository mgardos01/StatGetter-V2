import json 
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = None

def setup_driver():
    driver = webdriver.Remote(
        command_executor='http://localhost:4444/wd/hub',
        options=webdriver.ChromeOptions()
    )

# TODO json config list of services (sites) to fetch from
# services = []
# def fetch(service, **kwargs):
def fetch(name, tag):
    if driver is None:
        setup_driver()
    # TODO fetches something from the given service and options given by kwargs
    driver.get(f'https://tracker.gg/valorant/profile/riot/{name}%23{tag}/overview')
    element = driver.find_element(By.CLASS_NAME, "area-main-stats")
    return element.screenshot_as_png