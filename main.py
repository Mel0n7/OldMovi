import discord, os, discord.ext
from discord.ext import commands

client = discord.Client()

client = commands.Bot(command_prefix = '..')

@client.event
async def on_ready():
  activity = discord.Activity(type=discord.ActivityType.listening, name="..help")
  await client.change_presence(activity=activity)
  print("Bot Online")


client.remove_command('help')
@client.command(name="help",aliases=["?"])
async def help(ctx):
  embed=discord.Embed(title="Help")
  embed.add_field(name="..help", value="Open this!", inline=False)
  embed.add_field(name="..mute {member}", value="Mute the member mentioned", inline=False)
  embed.add_field(name="..unmute {member}", value="Umute the member mentioned", inline=False)
  embed.add_field(name="..kick {member} {reason}", value="Kick the member mentioned", inline=False)
  embed.add_field(name="..ban {member} {reason}", value="Ban the member mentioned", inline=False)
  embed.add_field(name="..unban {member}", value="Unban the member mentioned", inline=False)
  embed.add_field(name="..balance {member}", value="Get you or the member specified's balance", inline=False)
  embed.add_field(name="..bal {member}", value="Alieses to ..balance", inline=False)
  embed.add_field(name="..bet {money}", value="Bet the amount of money you specifiy", inline=False)
  embed.add_field(name="..colour {colour}", value="View the hex colour specified", inline=False)
  embed.add_field(name="..color {colour}", value="Alieses to ..colour", inline=False)
  await ctx.reply(embed=embed)


@client.command(name="colour",aliases=["color"])
async def colour(ctx,colour):
  hexColour = hex(int(colour,16))
  rbgColour = tuple(int(hexColour[2:][i:i+2], 16) for i in (0, 2, 4))
  url=f"https://serux.pro/rendercolour?hex={colour}&height=100&width=225"
  embed=discord.Embed(title=hexColour[2:],colour=int(hexColour,16))
  embed.set_thumbnail(url=url)
  embed.add_field(name="Hex", value=hexColour[2:], inline=True)
  embed.add_field(name="RGB", value=rbgColour, inline=True)
  await ctx.send(embed=embed)


client.load_extension("cogs.moderation") # Imports ./cogs/moderation.py
client.load_extension("cogs.economy") # Imports ./cogs/economy.py


token = os.environ["token"]
client.run(token)
# invite link - https://discord.com/api/oauth2/authorize?client_id=948069816684642314&permissions=8&scope=bot