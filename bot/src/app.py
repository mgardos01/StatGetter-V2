import os
from .logger import logger_setup 
from .fetch import fetch, connection_test

# from db_test import test_oracle_db
# test_oracle_db()

import nextcord
from nextcord.ext import commands

# TESTING_GUILD_ID = 123456789  # Replace with your guild ID

logger_setup()

def run_app():
    bot = commands.Bot()

    intents = nextcord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix="$", intents=intents)

    # TODO remove this, testing 
    @bot.command()
    async def testest(ctx, name, tag):
        print('please print')
        await ctx.send(f'Your val tag: {name}#{tag}')

    @bot.command()
    async def test(ctx, name, tag):
        print("Starting to fetch...")
        png = fetch(ctx, name, tag)
        if png is None:
            await ctx.send('Something went wrong...')
        else:
            await ctx.send(file=nextcord.File(png, filename=f'{name}_{tag}.png'))

    # TODO remove this, it was just for testing
    # @bot.command()
    # async def connect(ctx, please):
    #     if please != "please":
    #         await ctx.send(f'You have to say please or else I will never work')
    #         return 
    #     await connection_test(ctx)

    @bot.event
    async def on_ready():
        print(f'We have logged in as {bot.user}')

    # TODO convert into slash command later
    # @bot.slash_command(description="My first slash command", guild_ids=[TESTING_GUILD_ID])
    # async def hello(interaction: nextcord.Interaction):
    #     await interaction.send("Hello!")
        
    token = os.environ['MY_DISCORD_API_KEY']
    bot.run(token)

run_app()