import logging
logging.basicConfig(level=logging.INFO)

from db_test import test_oracle_db
test_oracle_db()

import nextcord
from nextcord.ext import commands

# TESTING_GUILD_ID = 123456789  # Replace with your guild ID

# bot = commands.Bot()

# @bot.event
# async def on_ready():
#     print(f'We have logged in as {bot.user}')

# @bot.slash_command(description="My first slash command", guild_ids=[TESTING_GUILD_ID])
# async def hello(interaction: nextcord.Interaction):
#     await interaction.send("Hello!")

# bot.run('your token here')