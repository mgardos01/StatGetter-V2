import os
from .setup_logger import setup 
from .fetch import fetch

# from db_test import test_oracle_db
# test_oracle_db()

import nextcord
from nextcord.ext import commands

# TESTING_GUILD_ID = 123456789  # Replace with your guild ID

# setup_logger()

def run_app():
    bot = commands.Bot()

    intents = nextcord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix="$", intents=intents)

    @bot.command()
    async def testest(ctx, name, tag):
        ctx.send(f'Your val tag: {name}#{tag}')

    @bot.command()
    async def test(ctx, name, tag):
        png = fetch(name, tag)
        ctx.send(file=nextcord.File(png))

    @bot.event
    async def on_ready():
        print(f'We have logged in as {bot.user}')

    # @bot.slash_command(description="My first slash command", guild_ids=[TESTING_GUILD_ID])
    # async def hello(interaction: nextcord.Interaction):
    #     await interaction.send("Hello!")
    token = os.environ['MY_DISCORD_API_KEY']
    bot.run(token)

run_app()