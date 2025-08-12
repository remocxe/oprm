import discord
from discord.ext import commands
import requests
import re

TOKEN = 'TOKEN'

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.dm_messages = True

bot = commands.Bot(command_prefix='-', intents=intents)

WHITELISTED_USERS = [123456789012345678, 1038159009863184396]

@bot.event
async def on_ready():
    print(f'Bot is ready. Logged in as {bot.user}')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s).")
    except Exception as e:
        print(f"Error syncing commands: {e}")

@bot.tree.command(name="sh", description="Search for a gun by its ID")
async def searchgun(interaction: discord.Interaction, id: int):
    user_id = interaction.user.id

    if user_id not in WHITELISTED_USERS:
        await interaction.response.send_message("you cant use this, seems like a skill issue")
        return

    api_url = f"https://restoremonarchy.com/openapi/v1/browser/nordic-armory-3/guns?id={id}"

    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()

        print("API Response:", data)

        if isinstance(data, list) and len(data) > 0:
            gun_data = data[0]
        else:
            await interaction.response.send_message("No data found for the specified gun ID.")
            return

        description = gun_data.get('description', 'N/A')
        description = re.sub(r'<br>', '', description)
        description = re.sub(r'<color=.*?>', '', description)
        description = re.sub(r'</color>', '', description)

        embed = discord.Embed(title=f"{id}", color=discord.Color.blue())
        embed.add_field(name="Name", value=gun_data.get('name', 'N/A'), inline=False)
        embed.add_field(name="Description", value=description, inline=False)
        embed.add_field(name="Range", value=f"{gun_data.get('range', 'N/A')}", inline=True)
        embed.add_field(name="Player Head Damage", value=gun_data.get('playerHeadDamage', 'N/A'), inline=True)
        embed.add_field(name="Player Spine Damage", value=gun_data.get('playerSpineDamage', 'N/A'), inline=True)
        embed.add_field(name="Player Leg Damage", value=gun_data.get('playerLegDamage', 'N/A'), inline=True)
        embed.add_field(name="Player Arm Damage", value=gun_data.get('playerArmDamage', 'N/A'), inline=True)
        embed.add_field(name="Zombie Head Damage", value=gun_data.get('zombieHeadDamage', 'N/A'), inline=True)
        embed.add_field(name="Zombie Spine Damage", value=gun_data.get('zombieSpineDamage', 'N/A'), inline=True)
        embed.add_field(name="Zombie Leg Damage", value=gun_data.get('zombieLegDamage', 'N/A'), inline=True)
        embed.add_field(name="Zombie Arm Damage", value=gun_data.get('zombieArmDamage', 'N/A'), inline=True)
        embed.add_field(name="Animal Head Damage", value=gun_data.get('animalHeadDamage', 'N/A'), inline=True)
        embed.add_field(name="Animal Spine Damage", value=gun_data.get('animalSpineDamage', 'N/A'), inline=True)
        embed.add_field(name="Animal Leg Damage", value=gun_data.get('animalLegDamage', 'N/A'), inline=True)
        embed.add_field(name="Barricade Damage", value=gun_data.get('barricadeDamage', 'N/A'), inline=True)
        embed.add_field(name="Structure Damage", value=gun_data.get('structureDamage', 'N/A'), inline=True)
        embed.add_field(name="Resource Damage", value=gun_data.get('resourceDamage', 'N/A'), inline=True)
        embed.add_field(name="Object Damage", value=gun_data.get('objectDamage', 'N/A'), inline=True)
        embed.set_image(url=gun_data.get('imageUrl', 'https://example.com/default_image.jpg'))


        embed.set_footer(text="Data provided by restoremonarchy.com", icon_url="https://restoremonarchy.com/favicon.ico")


        await interaction.response.send_message(embed=embed)

    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 404:
            await interaction.response.send_message(f"Error: Gun with ID {id} not found.")
        else:
            await interaction.response.send_message(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        await interaction.response.send_message(f"Error fetching gun information: {req_err}")
    except KeyError as key_err:
        await interaction.response.send_message(f"Missing data in the API response: {key_err}")

bot.run(TOKEN)