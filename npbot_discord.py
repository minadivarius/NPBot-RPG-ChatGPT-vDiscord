import discord
from discord import app_commands
from dotenv import load_dotenv
import openai
import requests
import os
from mdtojson import collect_notes
import logging
import mycontext


# initialize memory
chat_history = "Eres El Ordenador"

# initialize log
logging.basicConfig(filename='debug.log', level=logging.INFO)


# initialize bot context
bot_context = mycontext.prompt1
# initialize discord client


class aclient(discord.Client):
    def __init__(self) -> None:
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        self.activity = discord.Activity(
            type=discord.ActivityType.watching, name="Dark.ia")


# pass discord client into a subclass
client = aclient()

# sync discord application commands on bot startup


@client.event
async def on_ready():
    await client.tree.sync()

# wait for use of /chat command


@client.tree.command(name="chat", description="Hablar con El Ordenador")
async def chat(interaction: discord.Interaction, *, message: str):
    global chat_history
    global bot_context
    await interaction.response.send_message("Escribiendo...", ephemeral=True, delete_after=3)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=1.1,
        messages=[
            {"role": "system", "content": f"{bot_context}"},
            {"role": "user", "content": chat_history},
            {"role": "user", "content": message}
        ]
    )
    chat_history += message + "\n"
    response = response['choices'][0]['message']['content']
    # Log a message
    logging.info(response)
    user = interaction.user.mention
    # subtracting 2 for the newline characters
    max_message_length = 2000 - len(user) - len(message) - 2
    chunks = [response[i:i+max_message_length]
              for i in range(0, len(response), max_message_length)]
    for chunk in chunks:
        await interaction.channel.send("\n\n" + user + ": " + message + "\n\n@ORDENADOR: " + response + "\n\n >")

    return

"""
@client.tree.command(name="otro comando", description="Establecer otro comando")
async def chat(interaction: discord.Interaction, *, message: str):
    global chat_history2
    global bot_context2
    notes = collect_notes()
    await interaction.response.send_message("Escribiendo...", ephemeral=True, delete_after=3)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=1.1,
        messages=[
            {"role": "system", "content": f"{bot_context}"},
            {"role": "assistant", "content": f"{notes}"},
            {"role": "user", "content": chat_history},
            {"role": "user", "content": message}
        ]
    )
    chat_history += message + "\n"
    response = response['choices'][0]['message']['content']
    # Log a message
    logging.info(response)
    user = interaction.user.mention
    # subtracting 2 for the newline characters
    max_message_length = 2000 - len(user) - len(message) - 2
    chunks = [response[i:i+max_message_length]
              for i in range(0, len(response), max_message_length)]
    for chunk in chunks:
        await interaction.channel.send("\n\n" + user + ": " + message + "\n\n@ORDENADOR: " + response + "\n\n >")

    return
"""


# run the bot
if __name__ == '__main__':
    load_dotenv()
    path_to_notes = os.getenv("PATH_TO_NOTES")
    discord_token = os.getenv("DISCORD_BOT_TOKEN")
    openai.api_key = os.getenv("OPENAI_API_KEY")
    client.run(discord_token)
