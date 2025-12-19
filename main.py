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
        if message.content.lower().startswith("lmao"):
                embed = discord.Embed(title= "i am a Title", description="i am a description", url="https://www.youtube.com/watch?v=wUf1Vgp-2CE", color=discord.Color.gold())
                embed.set_thumbnail(url="https://cdn.pixabay.com/photo/2023/12/07/11/11/girl-8435339_1280.png")
                embed.add_field(name="text 1", value="value 1", inline=False)
                embed.add_field(name="text 2", value="value 2", inline=True)
                embed.add_field(name="text 3", value="value 3", inline=True)
                embed.set_footer(text="this is a footer")
                embed.set_author(name=message.author, url="https://cdn.pixabay.com/photo/2023/12/07/11/11/girl-8435339_1280.png", icon_url="https://cdn.pixabay.com/photo/2023/12/07/11/11/girl-8435339_1280.png")
                await message.channel.send(embed=embed)
            

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
async def saythings(interaction: discord.Interaction, num:int, printer:str):
    await interaction.response.send_message(f"Printer says: `Number {num}`\n{printer}")

@client.tree.command(name="embed", description="Embbed demo!", guild=discord.Object(id=int(SERVER)))
async def embed(interaction: discord.Interaction):
    embed = discord.Embed(title= "i am a Title", description="i am a description", url="https://www.youtube.com/watch?v=wUf1Vgp-2CE", color=discord.Color.gold())
    embed.set_thumbnail(url="https://cdn.pixabay.com/photo/2023/12/07/11/11/girl-8435339_1280.png")
    embed.add_field(name="text 1", value="value 1", inline=False)
    embed.add_field(name="text 2", value="value 2", inline=True)
    embed.add_field(name="text 3", value="value 3", inline=True)
    embed.set_footer(text="this is a footer")
    embed.set_author(name=interaction.user.name, url="https://cdn.pixabay.com/photo/2023/12/07/11/11/girl-8435339_1280.png", icon_url="https://cdn.pixabay.com/photo/2023/12/07/11/11/girl-8435339_1280.png")
    await interaction.response.send_message(embed=embed)


class View(discord.ui.View):
    @discord.ui.button(label="Click me button 1!", style=discord.ButtonStyle.red, emoji="🙍‍♂️")
    async def button_callback(self, button, interaction):
        await button.response.send_message("You have clicked the button 1")

    @discord.ui.button(label="Click me Button 2!", style=discord.ButtonStyle.green, emoji="🧑")
    async def two_button_callback(self, button, interaction):
        await button.response.send_message("You have clicked the button 2")

    @discord.ui.button(label="Click me Button 3!", style=discord.ButtonStyle.grey, emoji="👮‍♂️")
    async def three_button_callback(self, button, interaction):
        await button.response.send_message("You have clicked the button 3")

@client.tree.command(name="button", description="Displaying a button", guild=discord.Object(id=int(SERVER)))
async def myButton(interaction: discord.Interaction):
    await interaction.response.send_message(view=View())


client.run(TOKEN)