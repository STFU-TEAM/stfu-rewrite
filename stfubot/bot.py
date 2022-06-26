import os

from stfubot.globals.variables import LOOP
from stfubot.models.bot.stfubot import StfuBot
from disnake.ext import commands

TOKEN = os.environ["TOKEN_DISCORD"]

textart = " ____  ____  ____  _  _    ____  ____  __   _  _  __  ____  _  _ \n/ ___)(_  _)(  __)/ )( \  (  _ \(  __)/  \ / )( \(  )(  __)( \/ )\n\___ \  )(   ) _) ) \/ (   )   / ) _)(  O )) \/ ( )(  ) _) / \/ \ \n(____/ (__) (__)  \____/  (__\_)(____)\__\)\____/(__)(____)\_)(_/"


Client = StfuBot(LOOP)

print("All the databases ,emojis and apis have been initialized")

main_extension = {
    "extensions.daily",
    "extensions.management",
    "extensions.fight",
    "extensions.social",
    "extensions.crusade",
    "extensions.tower",
    "extensions.items",
    "extensions.gangs",
    "extensions.shop",
    "extensions.admincommand",
    "extensions.errors",
    "extensions.statcord",
    "extensions.topgg",
}

# loads file and stuff
for file in main_extension:
    try:
        Client.load_extension(file)
    except commands.ExtensionAlreadyLoaded:
        # print(f'{file} already loaded , ignoring')
        pass
    else:
        print(f"loaded {file}")
print(textart)

if __name__ == "__main__":
    # run the bot
    Client.run(TOKEN)
