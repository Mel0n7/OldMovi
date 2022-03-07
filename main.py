import discord, os, discord.ext, json, requests
from discord.ext import commands, tasks
from dotenv import load_dotenv

load_dotenv()
client = discord.Client()

async def getPrefix(client,message):
  with open("./prefix.json","r") as f:
    prefixes = json.loads(f.read())
  try:
    return prefixes[str(message.guild.id)]
  except:
    await setPrefix(message, "..")
    return ".."

client = commands.Bot(command_prefix = getPrefix)

@client.event
async def on_ready():
  activity = discord.Activity(type=discord.ActivityType.listening, name="..help")
  await client.change_presence(activity=activity)
  print("Bot Online")
  checkSubscribed.start()


@client.event
async def on_guild_join(ctx):
  await setPrefix(ctx, "..")


@client.event
async def on_command_error(ctx, error):
  print(error)


client.remove_command('help')
@client.command(name="help",aliases=["?"])
async def help(ctx):
  prefix = await getPrefix(client, ctx)
  embed=discord.Embed(title="Help")
  embed.add_field(name=f"{prefix}help (command)", value="Open this!", inline=False)
  embed.add_field(name=f"{prefix}mute (member) (reason)", value="Mute the member mentioned", inline=False)
  embed.add_field(name=f"{prefix}unmute (member) (reason)", value="Umute the member mentioned", inline=False)
  embed.add_field(name=f"{prefix}kick (member) (reason)", value="Kick the member mentioned", inline=False)
  embed.add_field(name=f"{prefix}ban (member) (reason)", value="Ban the member mentioned", inline=False)
  embed.add_field(name=f"{prefix}unban (member) (reason)", value="Unban the member mentioned", inline=False)
  embed.add_field(name=f"{prefix}deafen (member) (reason)", value="Deafen the member mentioned", inline=False)
  embed.add_field(name=f"{prefix}undeafen (member) (reason)", value="Uneafen the member mentioned", inline=False)
  embed.add_field(name=f"{prefix}balance (member)", value="Get you or the member specified's balance", inline=False)
  embed.add_field(name=f"{prefix}bal (member)", value=f"Alieses to {prefix}balance", inline=False)
  embed.add_field(name=f"{prefix}bet (money)", value="Bet the amount of money you specifiy", inline=False)
  embed.add_field(name=f"{prefix}withdraw (money)", value=f"Withdraw the amount of money specified", inline=False)
  embed.add_field(name=f"{prefix}deposit (money)", value=f"Deposit the amount of money specified", inline=False)
  embed.add_field(name=f"{prefix}colour (colour)", value="View the hex colour specified", inline=False)
  embed.add_field(name=f"{prefix}color (colour)", value=f"Alieses to {prefix}colour", inline=False)
  await ctx.reply(embed=embed)


@client.command(name="colour",aliases=["color"])
async def colour(ctx,colour):
  hexColour = hex(int(colour,16))
  rbgColour = str(tuple(int(hexColour[2:][i:i+2], 16) for i in (0, 2, 4))).strip("(").strip(")")
  url=f"https://serux.pro/rendercolour?hex={colour}&height=100&width=225"
  embed=discord.Embed(title=hexColour[2:],colour=int(hexColour,16))
  embed.set_thumbnail(url=url)
  embed.add_field(name="Hex", value=hexColour[2:], inline=True)
  embed.add_field(name="RGB", value=rbgColour, inline=True)
  await ctx.reply(embed=embed)

async def setPrefix(ctx,prefix):
  with open("./prefix.json","r") as f:
    prefixes = json.loads(f.read())
  prefixes[str(ctx.guild.id)] = prefix
  with open("./prefix.json","w") as f:
    json.dump(prefixes,f)

    
@client.command(name="prefix")
async def prefix(ctx,prefix:str):
  await setPrefix(ctx,prefix)
  await ctx.reply(f"Set prefix to {prefix}")
  

@tasks.loop(minutes=1)
async def checkSubscribed():
  subscribed = json.loads(open("./subscribed.json","r").read())
  ytToken = os.environ["ytKey"]
  for sub in subscribed:
    id = sub["id"]
    url = f"https://www.googleapis.com/youtube/v3/search?key={ytToken}&channelId={id}&part=snippet,id&order=date&maxResults=1"
    channel = requests.get(url).json()
    lastVid = channel["items"][0]
    lastVidID = lastVid["id"]["videoID"]
    lastKnownVid = sub["lastVid"]
    if not lastVidID == lastKnownVid:
      title = lastVid["snippet"]["title"]
      description = lastVid["snippet"]["description"]
      channelName = description = lastVid["snippet"]["channelTitle"]
      channelID = description = lastVid["snippet"]["channelId"]
      channelURL = f"https://www.youtube.com/channel/{channelID}"
      vidURL = f"https://www.youtube.com/watch?v={lastVidID}"
      channelImage = requests.get(f"https://youtube.googleapis.com/youtube/v3/channels?part=snippet%2CcontentDetails&id={channelID}&key={ytToken}").json()["items"]["snippet"]["thumbnails"]["default"]
      embed=discord.Embed(title=title, url=vidURL, description=description)
      embed.set_author(name=channelName, url=channelURL, icon_url=channelImage)
      guild = client.get_guild(sub["guild"])
      channel = guild.text_channels[sub["channel"]]
      await channel.send(embed=embed)    
      subscribed[f"{guild}#{id}"] = {"id":id,"guild":guild.id,"channel":channel.id,"lastVid":lastVidID}
      with open("./subscribed.json","w") as subW:
        json.dump(subscribed,subW)


@client.command(name="subscribe",aliases=["sub"])
async def subscribe(ctx,id:str):
  ytToken = os.environ["ytKey"]
  channel = requests.get(f"https://youtube.googleapis.com/youtube/v3/channels?part=snippet%2CcontentDetails&id={id}&key={ytToken}").json()
  channelName = channel["items"]["snippet"]["title"]
  channelImage = channel["items"]["snippet"]["thumbnails"]["medium"]
  with json.loads(open("./subscribed.json","r").read()) as subs:
    name = f"{ctx.guild.id}#{id}"
    subs[name] = {"id":id,"guild":ctx.guild.id,"channel":ctx.channel.id,"lastVid":""}
    with open("./subscribed.json","w") as subW:
      json.dump(subs,subW)
  embed=discord.Embed(title=f"Subscribed to {channelName}")
  embed.set_thumbnail(url=channelImage)
  await ctx.send(embed=embed)
  

client.load_extension("cogs.moderation") # Imports ./cogs/moderation.py
client.load_extension("cogs.economy") # Imports ./cogs/economy.py


token = os.environ["token"]
client.run(token)
# invite link - https://discord.com/api/oauth2/authorize?client_id=948069816684642314&permissions=8&scope=bot