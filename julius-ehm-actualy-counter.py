import discord
from discord import app_commands
import json, os

TOKEN = os.getenv("DISCORD_TOKEN")
DATA_FILE = "counter.json"

def load_count():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE) as f:
            return json.load(f).get("count", 0)
    return 0

def save_count(value):
    with open(DATA_FILE, "w") as f:
        json.dump({"count": value}, f)

class MyClient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()

client = MyClient()

@client.tree.command(name="count", description="Show the current count")
async def count(interaction: discord.Interaction):
    await interaction.response.send_message(f"Current count: {load_count()}")

@client.tree.command(name="add", description="Add to the count")
async def add(interaction: discord.Interaction, amount: int = 1):
    new_value = load_count() + amount
    save_count(new_value)
    await interaction.response.send_message(f"Count is now {new_value}")

@client.tree.command(name="remove", description="Subtract from the count")
async def remove(interaction: discord.Interaction, amount: int = 1):
    new_value = load_count() - amount
    save_count(new_value)
    await interaction.response.send_message(f"Count is now {new_value}")

client.run(TOKEN)