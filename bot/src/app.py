import os
from .logger import logger_setup 
from .fetch import fetch, connection_test

# from db_test import test_oracle_db
# test_oracle_db()

import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands

def run_app():
    logger_setup()

    bot = commands.Bot()

    intents = nextcord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix="$", intents=intents)

    @bot.slash_command(description="Main command to get stats", guild_ids=[int(os.environ["TESTING_GUILD_ID"])])
    async def statget(interaction: Interaction):
        pass

    @statget.subcommand(name="fetch", description="Fetches stat data from the web")
    async def statfetch(interaction: Interaction, 
        opt = SlashOption(
            choices=["tracker.gg"]
        ), 
        username:str = SlashOption(required=True),
        tag:str = SlashOption(name="tag", required=True)
    ):
        await interaction.response.defer()
        try:
            await fetch(interaction, opt, username, tag)
        except Exception as error: 
            await interaction.followup.send(
                'Something went wrong...\n'
                '```\n'
                f'{error}\n'
                f'```'
            )
        
    @bot.event
    async def on_ready():
        print(f'We have logged in as {bot.user}')

    token = os.environ['DISCORD_API_KEY']
    bot.run(token)