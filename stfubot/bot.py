import os
import asyncio

from globals.variables import LOOP
from models.bot.stfubot import StfuBot
from disnake.ext import commands

TOKEN = os.environ["TOKEN_DISCORD"]


Client = StfuBot(LOOP)

print("All the databases ,emojis and apis have been initialized")

main_extension = {"extensions.daily", "extensions.management", "extensions.fight"}

# loads file and stuff
for file in main_extension:
    try:
        Client.load_extension(file)
    except commands.ExtensionAlreadyLoaded:
        # print(f'{file} already loaded , ignoring')
        pass
    else:
        print(f"loaded {file}")

if __name__ == "__main__":
    # run the bot
    Client.run(TOKEN)
