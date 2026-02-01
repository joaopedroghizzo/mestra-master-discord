import discord
import os

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Bot conectado como {client.user}')

@client.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content.startswith('!ping'):
        await message.channel.send('Pong! 🟢')

client.run(os.getenv("DISCORD_TOKEN"))

use env var dor discord token
