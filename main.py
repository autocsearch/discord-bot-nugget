import discord 
from discord.ext import commands
from discord import app_commands

from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("secrets")
SERVER = os.getenv("ServerId")

class Client(commands.Bot):
    async def on_ready(self):
        print(f'Loged on as {self.user}!')

        try:
            guild = discord.Object(int(SERVER))
            synced = await self.tree.sync(guild=guild)
            print(f'synced {len(synced)} commands to guild {guild.id}')

        except Exception as e:
            print(f'Error syncing commands: {e}')

    async def on_message(self, message):
        if message.author == self.user:
            return
        
        if message.content.startswith('hello'):
            await message.channel.send(f'hi there {message.author}')

        if message.content.lower().startswith('morning'):
            await message.channel.send(f'Good Morning, {message.author}')
        if message.content.lower().startswith('evening'):
            await message.channel.send(f'Good evening, {message.author}')
        if message.content.lower().startswith('afternoon'):
            await message.channel.send(f'Good afternoon, {message.author}')
        if message.content.lower().startswith('night'):
            await message.channel.send(f'Good night, {message.author}')

    async def on_reaction_add(self, reaction, user):
        await reaction.message.channel.send('you reacted')

intents = discord.Intents.default()
intents.message_content = True
client = Client(command_prefix ="/", intents=intents)

GUILD_ID = discord.Object(id=int(SERVER))

@client.tree.command(name="test", description="testing", guild=discord.Object(id=int(SERVER)))
async def greetings(interaction: discord.Interaction):
    await interaction.response.send_message("Good day, fella!" )

@client.tree.command(name="printer", description="i will print whatever you give me!", guild=discord.Object(id=int(SERVER)))
async def greetings(interaction: discord.Interaction, num:int, printer:str):
    await interaction.response.send_message(f"Printer says: `Number {num}`\n{printer}")


client.run(TOKEN)