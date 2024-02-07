import json 
import sys
import pandas as pd 
import numpy as np
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from io import BytesIO
import nextcord

# True if Good, False if not
async def connection_test(ctx):
    # await ctx.send("Beginning connection test...")
    # try:
    #     options = webdriver.ChromeOptions()
    #     options.add_argument("--headless")
    #     options.add_argument("--no-sandbox")
    #     driver = webdriver.Remote(
    #         # This name + port comes from the docker-compose config
    #         command_executor='http://chrome:4444/wd/hub',
    #         options=options
    #     )
    # except Exception as error:
    #     await ctx.send(f"Driver failed to connect... Error: {error}")
    # await ctx.send("Driver connected!...")
    pass

driver = None 
def driver_setup():
    global driver 
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--starts-maximized")
    options.add_argument('window-size=1920x1080');
    driver = webdriver.Remote(
        # This name + port comes from the docker-compose config
        command_executor='http://chrome:4444/wd/hub',
        options=options
    )

async def fetch(interaction, opt, name, tag):
    try:
        match opt: 
            case "tracker.gg": 
                # TODO Option embed with different things to pick wait for input 
                # maybe [OVERVIEW]/[AGENTS]
                await agent_performance(interaction, name, tag)
            case _:
                raise Exception("No option :(")
    except:
        raise


async def agent_performance(interaction, name, tag):
    if driver is None:
        driver_setup()

    driver.get(f'https://tracker.gg/valorant/profile/riot/{name}%23{tag}/agents?season=all')

    try:        
        labels = [
            "Agent",
            "Time Played",
            "Matches",
            "Win Percentage",
            "Kill/Death Ratio",
            "Average Damage per Round",
            "Average Combat Score",
            "Average Damage Delta per Round",
            "Headshot Percentage",
            "Killed/Assisted/Survived/Traded Round Ratio",
            "Kills",
            "Deaths",
            "Assists",
            "Attack Win/Loss",
            "Attack Win Percentage",
            "Attack Kill/Death Ratio",
            "Defense Win/Loss",
            "Defense Win Percentage",
            "Defense Kill/Death Ratio"
        ]
        num_cols = len(labels)

        
        values = driver.find_elements(By.CSS_SELECTOR, ".st-content__item .value")
        print(values[0], file=sys.stderr)
        data = [val.get_attribute("textContent") for val in values]
        data = [data[i:i+num_cols] for i in range(0, len(data), num_cols)]
        for row in data: 
            logging.info(f'{row}')
            
        df = pd.DataFrame(data, columns=labels, dtype='string')
        
        print("DF for Agent...", file=sys.stderr)
        df['Agent'] = df['Agent'].astype('string')

        print("DF for Time Played...", file=sys.stderr)
        df['Time Played'] = df['Time Played'].str.rstrip(" hrs").replace(",", "").astype('float').mul(60).astype('int32')

        print("DF for Matches...", file=sys.stderr)
        df['Matches'] = df['Matches'].str.replace(",", "").astype('int32')

        print("DF for Win Percentage...", file=sys.stderr)
        df['Win Percentage'] = df['Win Percentage'].str.rstrip("%").astype('float').div(100)

        print("DF for Kill/Death Ratio...", file=sys.stderr)
        df['Kill/Death Ratio'] = df['Kill/Death Ratio'].astype('float')

        print("DF for Average Damage per Round...", file=sys.stderr)
        df['Average Damage per Round'] = df['Average Damage per Round'].astype('float')

        print("DF for Average Combat Score...", file=sys.stderr)
        df['Average Combat Score'] = df['Average Combat Score'].astype('float')
        
        print("DF for Average Damage Delta per Round...", file=sys.stderr)
        df['Average Damage Delta per Round'] = df['Average Damage Delta per Round'].str.replace(",", "").astype('int16')

        print("DF for Headshot Percentage...", file=sys.stderr)
        df['Headshot Percentage'] = df['Headshot Percentage'].str.rstrip("%").astype('float').div(100)

        print("DF for Killed/Assisted/Survived/Traded Round Ratio...", file=sys.stderr)
        df['Killed/Assisted/Survived/Traded Round Ratio'] = df['Killed/Assisted/Survived/Traded Round Ratio'].str.rstrip("%").astype('float').div(100)
        
        print("DF for Kills...", file=sys.stderr)
        df["Kills"] = df["Kills"].str.replace(",", "").astype('int32')
        
        print("DF for Deaths...", file=sys.stderr)
        df["Deaths"] = df["Deaths"].str.replace(",", "").astype('int32')
        
        print("DF for Assists...", file=sys.stderr)
        df["Assists"] = df["Assists"].str.replace(",", "").astype('int32')
        
        print("DF for Attack Win/Loss...", file=sys.stderr)
        df[["Attack Wins", "Attack Losses"]] = df["Attack Win/Loss"].str.split(" - ", n=1, expand=True).astype("int32")
        
        print("DF for Attack Win Percentage...", file=sys.stderr)
        df["Attack Win Percentage"] = df["Attack Win Percentage"].str.rstrip("%").astype('float').div(100)
        
        print("DF for Attack Kill/Death Ratio...", file=sys.stderr)
        df["Attack Kill/Death Ratio"] = df["Attack Kill/Death Ratio"].astype('float')
        
        print("DF for Defense Win/Loss...", file=sys.stderr)
        df[["Defense Wins", "Defense Losses"]] = df["Defense Win/Loss"].str.replace(",", "").str.split(" - ", n=1, expand=True).astype("int32")
        
        print("DF for Defense Win Percentage...", file=sys.stderr)
        df["Defense Win Percentage"] = df["Defense Win Percentage"].str.rstrip("%").astype('float').div(100)
        
        print("DF for Defense Kill/Death Rati...", file=sys.stderr)
        df["Defense Kill/Death Ratio"] = df["Defense Kill/Death Ratio"].astype('float')

        await interaction.followup.send(f'```\n{df.to_string}```')
        print(df.to_string, sys.stderr)
    except Exception as e: 
        e.add_note("Couldn't find tabular data")
        raise

async def tracker(interaction, name, tag):
    if driver is None:
        driver_setup()

        
    # TODO fetches something from the given service and options given by kwargs
    driver.get(f'https://tracker.gg/valorant/profile/riot/{name}%23{tag}/overview')

    try:
        main_element = driver.find_element(By.CLASS_NAME, "area-main-stats")
    except Exception as e: 
        e.add_note("Couldn't find the main stat display.")
        raise
    
    # Remove show more buttons
    bad_elements = driver.find_elements(By.CLASS_NAME, "trn-button.view-all")

    print(bad_elements, file=sys.stderr)
    for bad_e in bad_elements:
        driver.execute_script("""
        var bad_e = arguments[0];
        bad_e.parentNode.removeChild(bad_e);;
        """, bad_e)

    # Find the stat box to screenshot
    driver.execute_script('arguments[0].scrollIntoView({block: "center"});', main_element)
    png = BytesIO(main_element.screenshot_as_png)

    await interaction.followup.send(file=nextcord.File(png, filename=f'{name}_{tag}.png'))

    