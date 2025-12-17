import discord 
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("secrets")

class Client(discord.Client):
    async def on_ready(self):
        print(f'Loged on as {self.user}!')
    async def on_message(self, message):
        if message.author == self.user:
            return 
        
        if message.content.startswith('hello'):
            await message.channel.send(f'hi there {message.author}')
    async def on_reaction_add(self, reaction, user):
        await reaction.message.channel.send('you reacted')

intents = discord.Intents.default()
intents.message_content = True


client = Client(intents=intents)
client.run(TOKEN)