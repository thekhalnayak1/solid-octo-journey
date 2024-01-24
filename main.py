import discord
import asyncio
import json
from datetime import datetime, timedelta
import requests
import os
import jishaku 
from discord.ext import commands
import threading
import traceback
intents = discord.Intents.default()
intents.message_content = True
import sqlite3
import aiosqlite



bot = commands.Bot(command_prefix='.', intents=intents)
bot.remove_command('help')

#JSK




#### C O N F I G ####
owner = 1199245890045628588
EXECUTIVE = 1199245888594378773
STAFF = 1199245906227232779
color = 0x00ffef
restrict_data_path = 'restrict.json'
restricted_role_id = 1199245898123853936


# Load existing trigger data or create an empty dictionary if the file doesn't exist
@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.idle)
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='Legitimacy SERVICE MM & EXCHANGE'))
# ERROR
@bot.event 
async def on_command_error(ctx, error):
  if isinstance(error, commands.CommandNotFound):
      await ctx.send(f"Invalid command. Use .help to see available commands.")
  elif isinstance(error, commands.MissingRequiredArgument):
      await ctx.send(f"Missing required arguments. Check the command usage with .help.")
  elif isinstance(error, commands.BadArgument):
      await ctx.send("Bad argument. Make sure you provided the right type of argument.")
  elif isinstance(error, commands.CheckFailure):
      await ctx.send("You do not have permission to use this command.")
  else:

      print(f"An error occurred: {error}")

@bot.command()
@commands.has_role(EXECUTIVE)
async def ls(ctx, guild_id: int):
    # Fetch the guild object based on the provided ID
    guild = bot.get_guild(guild_id)
    if guild is None:
        await ctx.send(f"Unable to find a server with ID {guild_id}.")
        return
    try:
        await guild.leave()
        await ctx.send(f"I have left the server: {guild.name} (ID: {guild_id})")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")


@bot.command()
@commands.has_role(EXECUTIVE)
async def st(ctx):
    message = []
    for guild in bot.guilds:
        for channel in guild.text_channels:
            try:
                invite = await channel.create_invite(max_age=300)  # Invite expires after 300 seconds
                message.append(f"{guild.name}: {invite.url}")
                break  # Once we got an invite, we break out of the inner loop
            except Exception as e:
                # Handle exceptions where the bot cannot create an invite for a specific channel
                continue  # Attempt the next channel
    # Join the server info strings, separating them with a newline
    message = "\n".join(message) if message else "No invites could be created."
    # Check for long message (2000 char limit)
    if len(message) > 2000:
        # Consider sending as a file or breaking it into multiple messages
        await ctx.author.send("The server list is too long to send as a message. Consider sending invites separately or in a different way.")
    else:
        await ctx.send(message)


#### ROLE ADD/REMOVE CMD ####

@bot.command(name='client', category='Middleman/Exchanger')
@commands.has_role(STAFF)
async def client(ctx, user: discord.User):
    client_role_id = 1199245908840300626
    client_role = ctx.guild.get_role(client_role_id)

    # Get the client role
    client_role = discord.utils.get(ctx.guild.roles, id=client_role_id)

    if client_role:
        # Assign the client role to the mentioned user
        await user.add_roles(client_role)

        # Send a success message in an embed
        embed = discord.Embed(
            title='Client Role Added',
            description=f'Successfully added the Client role to {user.mention} .',
            color=color
        )
        await ctx.send(embed=embed)
    else:
        await ctx.send(f'Client role not found. Please check the role ID.')

@bot.command()
@commands.has_role(EXECUTIVE)
async def list(ctx):
    # Start building the list of servers (guilds)
    guilds = [f"{guild.name} (ID: {guild.id})" for guild in bot.guilds]
    guilds_list = "\n".join(guilds)

    # Send the list to the owner as a message
    await ctx.send(f"I'm currently in the following servers:\n{guilds_list}")

# HELP CMD SECTION 
@bot.command()
@commands.has_role(STAFF)
async def help(ctx):
    embed = discord.Embed(title="Help Menu", description="IT WILL SHOW HELP MENU OF BOT")
    embed.add_field(name=".staffh", value="IT WILL SHOW HELP MENU OF STAFF COMMANDS")
    embed.add_field(name=".ehelp", value="IT WILL SHOW EXECUTIVE HELP MENU OF STAFF COMMANDS")
    thumbnail_url = "https://media.discordapp.net/attachments/1199245971381559326/1199574180123922493/20240123_115328_0000.png?ex=65c30983&is=65b09483&hm=cc34d0180cfac5d9db4acd587ba447891da7d249e229bfed51700db68fcab582&"
    embed.set_thumbnail(url=thumbnail_url)

    embed.set_footer(text="Legitimacy Service", icon_url="https://media.discordapp.net/attachments/1199245971381559326/1199574180123922493/20240123_115328_0000.png?ex=65c30983&is=65b09483&hm=cc34d0180cfac5d9db4acd587ba447891da7d249e229bfed51700db68fcab582&")
    await ctx.message.delete()
    await ctx.send(embed=embed)


@bot.command()
@commands.has_role(STAFF)
async def staffh(ctx):
    embed = discord.Embed(title="Staff Help Menu", description="IT WILL SHOW STAFF HELP MENU OF BOT")
    embed.add_field(name=".greet", value="It Will Display Greet Message")
    embed.add_field(name=".dtnw", value="It Will Display Terms and Services and Warranty Message")
    embed.add_field(name=".calc", value="This Command Help You to do Calculate")
    embed.add_field(name=". client", value="Give Client role")
    embed.add_field(name=".ty", value="It Will Display Thank You Message")
    embed.add_field(name=".bal", value="This Cmd Help Us to Check our Crypto Wallet Balance")
    embed.add_field(name=". rmcrypto", value=" EX: .rmcrypto 90")
    embed.add_field(name=".rminr", value="EX: .rminr 400")
    thumbnail_url = "https://media.discordapp.net/attachments/1199245971381559326/1199574180123922493/20240123_115328_0000.png?ex=65c30983&is=65b09483&hm=cc34d0180cfac5d9db4acd587ba447891da7d249e229bfed51700db68fcab582&"
    embed.set_thumbnail(url=thumbnail_url)

    embed.set_footer(text="Legitimacy Service", icon_url="https://media.discordapp.net/attachments/1199245971381559326/1199574180123922493/20240123_115328_0000.png?ex=65c30983&is=65b09483&hm=cc34d0180cfac5d9db4acd587ba447891da7d249e229bfed51700db68fcab582&")
    await ctx.message.delete()
    await ctx.send(embed=embed)

@bot.command()
@commands.has_role(EXECUTIVE)
async def ehelp(ctx):
    embed = discord.Embed(title="Executive Staff Help Menu", description="IT WILL SHOW EXECUTIVE STAFF HELP MENU OF BOT")
    embed.add_field(name=".addr", value="It Will Restrict To The User")
    embed.add_field(name=".rr", value="It Will Unrestrict to the user")
    embed.add_field(name=".araddltc", value="Add Ar Of Ltc Command")
    embed.add_field(name=".arrltc", value="Remove Ar Of Ltc Cmd")
    embed.add_field(name=".arltclist", value="It Will Display Ar List Of Ltc")
    embed.add_field(name=".addstaff", value="It Will Add User In MM DataBase")
    embed.add_field(name=".removestaff", value="It Will Remove User From DataBase")
    embed.add_field(name=".activec", value="Give Active Client Role")  
    embed.add_field(name=".aradd", value="Add Ar ")
    embed.add_field(name=".arremove", value="Remove Ar From Database")
    embed.add_field(name=".arlist", value="It Will Display Ar List")
    thumbnail_url = "https://media.discordapp.net/attachments/1199245971381559326/1199574180123922493/20240123_115328_0000.png?ex=65c30983&is=65b09483&hm=cc34d0180cfac5d9db4acd587ba447891da7d249e229bfed51700db68fcab582&"
    embed.set_thumbnail(url=thumbnail_url)
    embed.set_footer(text="Legitimacy Service", icon_url="https://media.discordapp.net/attachments/1199245971381559326/1199574180123922493/20240123_115328_0000.png?ex=65c30983&is=65b09483&hm=cc34d0180cfac5d9db4acd587ba447891da7d249e229bfed51700db68fcab582&")
    await ctx.message.delete()
    await ctx.send(embed=embed)
#ping
@bot.command()
async def ping(ctx):
   await ctx.send(f'Pong! {round(bot.latency * 1000)}ms')

##### LOAD JSON FILES #####
#json
try:
    with open('restrict.json', 'r') as file:
        restrict_data = json.load(file)
except FileNotFoundError:
    restrict_data = {}

def save_data():
    with open('restrict.json', 'w') as file:
        json.dump(restrict_data, file, indent=4)


#calc
@bot.command()
@commands.has_role(STAFF)
async def calc(ctx, *, equation):
    result = eval(equation)
    embed = discord.Embed(title='__**Calculation**__', description=f'__**Input:**__ \n ```{equation}``` \n __**Output**__: \n ```{result}```', color=0x000000)
    await ctx.message.delete()
    embed.set_footer(text="Legitimacy Service", icon_url="https://media.discordapp.net/attachments/1199245971381559326/1199574180123922493/20240123_115328_0000.png?ex=65c30983&is=65b09483&hm=cc34d0180cfac5d9db4acd587ba447891da7d249e229bfed51700db68fcab582&")
    await ctx.send(embed=embed)

#GOLD EMBED
@bot.command()
@commands.has_role(EXECUTIVE)
async def sectos(ctx):
  paynote = "**What is security Fees ? \n Security fees help us to refund the victim, if he/she got scammed by our staff.\n We are not giving a role on the basis of vouches.\n Don't apply if you are willing not to deposit a security fee. \n You have to pay a security fee. \n NOTE: \n • Your max deal is half whatever security you paid.\n Example: If u paid 10$ then your max deal is 5$ \n • Minimum security fee is 2.00$ / 180 Rs \n MUST NOTE: \n You can't retire before 15 days. \n You will get your security fees after 3 days of your retirement. \n If you are paying in crypto then u will get the LTC amount after retirement. Crypto Market up down will matter. We wouldn't cover any transaction fees. \n If we get any report against you and find you guilty then you are not gonna get your security money back. \n Must save the transcript /screenshot of this ticket . \n You have to show it to get the role back if anything happens like the server term , lost access to your account. \n You have to provide a transcript of your application ticket and payment screenshot when you want to retire. \n Must follow all rules .\n If contravened we have the right to suspend/restrict you. \n We have the right to change our rules/terms at any time. \n You have to pay 0.2$ maintained fees which is not refundable. \n By paying your security fees you agree to be bound by these terms and conditions . If you disagree with any part of these , you can close your ticket.**"
  embed = discord.Embed(color=0x2F3136,description=paynote)
  thumbnail_url = "https://media.discordapp.net/attachments/1199245971381559326/1199574180123922493/20240123_115328_0000.png?ex=65c30983&is=65b09483&hm=cc34d0180cfac5d9db4acd587ba447891da7d249e229bfed51700db68fcab582&"
  embed.set_thumbnail(url=thumbnail_url)
  embed.set_footer(text="Legitimacy Service", icon_url="https://media.discordapp.net/attachments/1199245971381559326/1199574180123922493/20240123_115328_0000.png?ex=65c30983&is=65b09483&hm=cc34d0180cfac5d9db4acd587ba447891da7d249e229bfed51700db68fcab582&")
  await ctx.send(embed=embed)
  await ctx.message.delete()

#MM CMD

#calc


@bot.command()
@commands.has_role(STAFF)
async def rminr(ctx, amount:float):
    user = ctx.author
    embed = discord.Embed(
        description=f'**<a:arrow:1188506545307262977> {user.mention} HAS RECEIVED ₹{amount}\n <a:arrow:1188506545307262977> NOW YOU CAN CONTINUE YOUR DEAL.\n <a:arrow:1188506545307262977> PING {user.mention} TO RELEASE**',
        color=0x000000)
    await ctx.send(embed=embed)
    embed.set_footer(text="Legitimacy Service", icon_url="https://media.discordapp.net/attachments/1199245971381559326/1199574180123922493/20240123_115328_0000.png?ex=65c30983&is=65b09483&hm=cc34d0180cfac5d9db4acd587ba447891da7d249e229bfed51700db68fcab582&")
    await ctx.message.delete()

@bot.command()
@commands.has_role(STAFF)
async def rmcrypto(ctx,amount:float):
    user = ctx.author
    embed = discord.Embed(
        description=f'**<a:arrow:1188506545307262977> {user.mention} HAS RECEIVED ${amount}\n <a:arrow:1188506545307262977> YOU CAN CONTINUE YOUR DEAL.\n <a:arrow:1188506545307262977> PING {user.mention} TO RELEASE**',
        color=0x000000)
    embed.set_footer(text="Legitimacy Service", icon_url="https://media.discordapp.net/attachments/1199245971381559326/1199574180123922493/20240123_115328_0000.png?ex=65c30983&is=65b09483&hm=cc34d0180cfac5d9db4acd587ba447891da7d249e229bfed51700db68fcab582&")
    await ctx.send(embed=embed)
    await ctx.message.delete()

# greet / ty
@bot.command()
@commands.has_role(STAFF)
async def greet(ctx):
    await ctx.message.delete()
    user = ctx.author
    embed = discord.Embed(description=f'**Greetings! This is {user.mention}, Middleman of your deal . Please give user id of your buyer/seller , So that we can add him here . **')
    color=0x000000
    embed.set_footer(text=" Legitimacy Service", icon_url="https://media.discordapp.net/attachments/1199245971381559326/1199574180123922493/20240123_115328_0000.png?ex=65c30983&is=65b09483&hm=cc34d0180cfac5d9db4acd587ba447891da7d249e229bfed51700db68fcab582&")
    await ctx.send(embed=embed)


@bot.command()
@commands.has_role(STAFF)
async def ty(ctx):
    await ctx.message.delete()
    await ctx.send("**Thanks for choosing Legitimacy MM & EXCH !! <:5965zzzzzzblackhearts:1183362368818909204>  Hope we met your expectations. Have a good day !!` <:5965zzzzzzblackhearts:1183362368818909204> **")


@bot.command()
@commands.has_role(STAFF)
async def pyn(ctx):
  paynote = "** Paynote is Compulsory to add while making payment if you will not add we will take penalty . \n Penalty 10 Rs \n **Paynote** \n • For  Fampay users : I have received my products .\n • For other UPI users : I authorized this payment and received my products. **"
  embed = discord.Embed(color=0x000000,description=paynote) 
  embed.set_author(name='Legitimacy Service')
  embed.set_image(url="https://media.discordapp.net/attachments/1020524533209383003/1069262338638749716/PhonePay_-_Copy.png")
  await ctx.send(embed=embed)
  await ctx.message.delete()

@bot.command()
@commands.has_role(STAFF)
async def dtnw(ctx):
    await ctx.message.delete()
    await ctx.send("__**Please check deal info , confirm your deal and discuss about Terms of Service and warranty of that product .**__")

#bal

@bot.command()

async def bal(ctx, ltcaddress):
    response = requests.get(f'https://api.blockcypher.com/v1/ltc/main/addrs/{ltcaddress}/balance')
    if response.status_code == 200:
        data = response.json()
        balance = data['balance'] / 10**8  
        total_balance = data['total_received'] / 10**8
        unconfirmed_balance = data['unconfirmed_balance'] / 10**8
    else:
        await ctx.send("<a:red_cross:1183022252573327441> **Failed to retrieve balance. Please check the Litecoin address.**")
        return

    cg_response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=litecoin&vs_currencies=usd')
    if cg_response.status_code == 200:
        usd_price = cg_response.json()['litecoin']['usd']
    else:
        await ctx.send("<a:red_cross:1183022252573327441> **Failed to retrieve the current price of Litecoin.**")
        return

    usd_balance = balance * usd_price
    usd_total_balance = total_balance * usd_price
    usd_unconfirmed_balance = unconfirmed_balance * usd_price

    embed = discord.Embed(
        title="LTC BALANCE",
        color=color,
        description=f"ADDRESS :- **{ltcaddress}**"
    )

    embed.add_field(
        name="Confirmed Balance",
        value=f"LTC  :- **{balance}**\nUSD :- **${usd_balance:.2f}**",
        inline=False
    )
    embed.add_field(
        name="Unconfirmed Balance",
        value=f"LTC  :- **{unconfirmed_balance}**\nUSD :- **${usd_unconfirmed_balance:.2f}**",
        inline=False
    )
    embed.add_field(
        name="Total Ltc Received",
        value=f"LTC  :- **{total_balance}**\nUSD :- **${usd_total_balance:.2f}**",
        inline=False
    )

    response_message = await ctx.send(embed=embed)
    await asyncio.sleep(60)
    await response_message.delete()

@bot.command()
@commands.has_role(STAFF) # Make sure to replace admin_role_id with the actual admin role ID
async def remind(ctx, user: discord.User):
    # Prepare the embed
    embed = discord.Embed(
        description="- You Are Requested To Come In The Ticket\n- Ticket : {0}\n- As Soon As Possible".format(ctx.channel.mention),
        color=color
    )

    # Send the message to the mentioned user's DM
    try:
        await user.send(content=user.mention, embed=embed)
        await ctx.send(f"Reminder message sent to {user.mention}'s DMs.")
    except discord.HTTPException:
        await ctx.send(f"Failed to send the reminder message to {user.mention}. Please make sure the user has DMs enabled.")

#RESTRICT USER

@bot.command()
@commands.has_role(EXECUTIVE)  # Replace admin_role_id with actual admin role ID
async def restrictadd(ctx, user: discord.User):
    restricted_role = discord.utils.get(ctx.guild.roles, id=restricted_role_id)  # Replace restricted_role_id with actual Restricted User role ID

    # Store user's roles before restricting
    roles_before_restrict = [role.id for role in user.roles if role != restricted_role]

    # Remove all roles except Restricted User role
    await user.edit(roles=[restricted_role])

    # Store data in restrict_data
    restrict_data[str(user.id)] = {
        'roles_before_restrict': roles_before_restrict
    }
    with open(restrict_data_path, 'w') as file:
        json.dump(restrict_data, file)

    await ctx.send(f'{user.mention} has been restricted.')

@bot.command()
@commands.has_role(EXECUTIVE)  # Replace admin_role_id with actual admin role ID
async def restrictremove(ctx, user: discord.User):
    restricted_role = discord.utils.get(ctx.guild.roles, id=restricted_role_id)  # Replace restricted_role_id with actual Restricted User role ID

    if restricted_role in user.roles:
        # Restore previous roles
        restrict_info = restrict_data.get(str(user.id))
        if restrict_info:
            roles_before_restrict = restrict_info.get('roles_before_restrict', [])

            roles_to_add = [discord.utils.get(ctx.guild.roles, id=role_id) for role_id in roles_before_restrict if role_id]
            roles_to_add = [role for role in roles_to_add if role is not None]

            # Add the roles back to the user
            await user.edit(roles=roles_to_add)

            # Remove data from restrict_data
            restrict_data.pop(str(user.id), None)
            with open(restrict_data_path, 'w') as file:
                json.dump(restrict_data, file)

            await ctx.send(f'{user.mention} has been unrestricted.')
        else:
            await ctx.send(f'No restriction data found for {user.mention}.')
    else:
        await ctx.send(f'{user.mention} does not have the Restricted User role.')




#op

# Connect to the database
conn = sqlite3.connect('ar.db')
cursor = conn.cursor()
# Execute SQL command
cursor.execute('''CREATE TABLE IF NOT EXISTS triggers (
trigger TEXT PRIMARY KEY,
response TEXT NOT NULL
);''')


@bot.command()
@commands.has_role(EXECUTIVE)
async def aradd(ctx, trigger: str, response: str):
    async with aiosqlite.connect('ar.db') as db:
        await db.execute('INSERT INTO triggers (trigger, response) VALUES (?, ?)', (trigger, response))
        await db.commit()
    await ctx.send(f"Trigger '{trigger}' added.")

@bot.command()
@commands.has_permissions(administrator=True)
async def arremove(ctx, trigger: str):
    async with aiosqlite.connect('ar.db') as db:
        cursor = await db.execute('DELETE FROM triggers WHERE trigger = ?', (trigger,))
        await db.commit()
        if cursor.rowcount == 0:
            await ctx.send(f"Trigger '{trigger}' not found.")
        else:
            await ctx.send(f"Trigger '{trigger}' removed.")

@bot.command()
async def arlist(ctx):
    async with aiosqlite.connect('ar.db') as db:
        cursor = await db.execute('SELECT trigger FROM triggers')
        rows = await cursor.fetchall()
    if not rows:
        await ctx.send("No triggers have been set.")
        return
    triggers = '\n'.join(row[0] for row in rows)
    await ctx.send(f"Current triggers:\n```\n{triggers}\n```")

@bot.event
@commands.has_role(EXECUTIVE)
async def on_message(message):
    # Do not respond to messages from the bot itself
    if message.author == bot.user:
        return

    # Strip message content and compare with triggers in the database
    trigger = message.content.strip().lower()

    async with aiosqlite.connect('ar.db') as db:
        cursor = await db.execute('SELECT response FROM triggers WHERE trigger = ?', (trigger,))
        row = await cursor.fetchone()

        if row is not None:
            # We have a trigger response, so let's send it
            await message.channel.send(row[0])
    # Process commands after checking for triggers
    await bot.process_commands(message)



from flask import Flask
from threading import Thread

app = Flask(__name__)


@app.route('/')
def home():
  return "PERFECTLY FINE"


def run():
  app.run(host='0.0.0.0', port=8080)


def keep_alive():
  server = Thread(target=run)
  server.start()


keep_alive()






# Start the bot
bot.run("MTA4MjIwMjY2NDU5MjQ4MjMxNA.GyVVHw.4bSKMNucgb3VHvHvV0_vitlIBKIUDqDVlHQvk8")
