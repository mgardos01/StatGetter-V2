import json 
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from io import BytesIO

# True if Good, False if not
async def connection_test(ctx):
    pass
    # await ctx.send("Beginning connection test...")
    # try:
    #     options = webdriver.ChromeOptions()
    #     options.add_argument("--headless")
    #     options.add_argument("--no-sandbox")
    #     driver = webdriver.Remote(
    #         command_executor='http://chrome:4444/wd/hub',
    #         options=options
    #     )
    # except Exception as error:
    #     await ctx.send(f"Driver failed to connect... Error: {error}")
    # await ctx.send("Driver connected!...")

driver = None 
def driver_setup():
    global driver 
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--starts-maximized")
    options.add_argument('window-size=1920x1080');
    driver = webdriver.Remote(
        command_executor='http://chrome:4444/wd/hub',
        options=options
    )

# TODO json config list of services (sites) to fetch from
# services = []
# def fetch(service, **kwargs):
def fetch(ctx, name, tag):
    if driver is None:
        driver_setup()

    # TODO fetches something from the given service and options given by kwargs
    driver.get(f'https://tracker.gg/valorant/profile/riot/{name}%23{tag}/overview')

    # Remove show more buttons
    bad_elements = driver.find_elements(By.CLASS_NAME, "trn-button.view-all")
    print(bad_elements, file=sys.stderr)
    for bad_e in bad_elements:
        driver.execute_script("""
        var bad_e = arguments[0];
        bad_e.parentNode.removeChild(bad_e);;
        """, bad_e)

    # Find the stat box to screenshot
    main_element = driver.find_element(By.CLASS_NAME, "area-main-stats")
    driver.execute_script('arguments[0].scrollIntoView({block: "center"});', main_element)

    print("Returning as png...")
    return BytesIO(main_element.screenshot_as_png)
