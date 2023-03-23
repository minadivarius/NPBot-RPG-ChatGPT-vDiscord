import discord
from discord import app_commands
import openai
import requests
import os
import mycontext
from dotenv import load_dotenv


# initialize memory
memory1 = mycontext.prompt1

"""
memory2 = mycontext.prompt2
"""


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
    global memory1
    await interaction.response.send_message("Escribiendo...", ephemeral=True, delete_after=3)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=1.2,
        messages=[
            {"role": "assistant", "content": memory1},
            {"role": "user", "content": message}
        ]
    )
    response = response['choices'][0]['message']['content']
    memory1 += message + "\n"
    user = interaction.user.mention
    await interaction.channel.send("\n\n" + user + ": " + message + "\n\n@ORDENADOR: " + response + "\n\n >")
    return

"""
@client.tree.command(name="attack", description="Hackear a El Ordenador")
async def chat(interaction: discord.Interaction, *, message: str):
    global memory2
    await interaction.response.send_message("Procesando...", ephemeral=True, delete_after=3)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=1.2,
        messages=[
            {"role": "assistant", "content": memory2},
            {"role": "user", "content": message}
        ]
    )
    response = response['choices'][0]['message']['content']
    memory2 += message + "\n"
    user = interaction.user.mention
    await interaction.channel.send("\n\n" + user + ": " + message + "\n\n@ORDENADOR: " + response + "\n\n >")
    return
"""


# run the bot
if __name__ == '__main__':
    load_dotenv()
    discord_token = os.getenv("DISCORD_BOT_TOKEN")
    openai.api_key = os.getenv("OPENAI_API_KEY")
    client.run(discord_token)
