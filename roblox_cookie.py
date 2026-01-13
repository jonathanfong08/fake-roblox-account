import random
import discord
from discord_webhook import DiscordWebhook, DiscordEmbed
import json
import requests
from colorama import Fore, Back, Style
from discord.ext import commands
import os

intents = discord.Intents().all()
client = commands.Bot(command_prefix="j.", intents=intents)
upper_ch = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
digits = "0123456789"

api_url = 'https://api.api-ninjas.com/v1/randomuser'
password_url = 'https://api.namefake.com/'

password_data = ""
password = ""
raw_pass = ""

response = ""

json_data = ""
raw_email = ""
raw_password = ""


everything = upper_ch + digits

def clear(): #clears terminal
    os.system('cls')

# Load the webhook URL from the config.json file
with open('config.json') as config_file:
    config = json.load(config_file)
    bot_token = config["bot_token"]
    webhook_url = config["webhook_url"]
    webhook_name = config["webhook_name"]
    api_key = config["api_key"]

cookie_length = ""
cookie = ""


def webhook_send():
    webhook = DiscordWebhook(url=webhook_url, username=webhook_name, content=f"**NOTIFICATION**")
    
    embed = DiscordEmbed(title="LOGS", description="A cookie was generated!", color="03b2f8")
    webhook.add_embed(embed)
    response = webhook.execute()

@client.event
async def on_ready():
    clear()
    print(Fore.LIGHTGREEN_EX + "BOT IS UP AND RUNNING.")
    print("------------------------------------------------------------------------------------")
    print(Style.RESET_ALL) #resets so no more color


@client.command()
async def gen_cookie(ctx):
    global response
    response = requests.get(api_url, headers={'X-Api-Key': f'{api_key}'})
    global json_data
    json_data = response.json()
    global raw_email
    raw_email = json_data["email"]
    global raw_password
    raw_password = json_data["username"] #made this into password cuz it looks similar enough
    global cookie_length
    cookie_length = 744
    global cookie
    cookie = "".join(random.choices(everything, k=cookie_length))
    print(Fore.GREEN + "Cookie has been generated.")
    print(Style.RESET_ALL) #resets so no more color
    
    embed = discord.Embed(title="ACCOUNT", description="Here is your requested Roblox account:")
    embed.add_field(name="Email:", value=raw_email, inline=False)
    embed.add_field(name="Password:", value=raw_password, inline=False)
    embed.add_field(name="Cookie:", value=f"_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_{cookie}", inline=False)
    await ctx.send(embed=embed)
    webhook_send()

client.run(bot_token)

