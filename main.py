import discord, os, time, json, discord.ext
from discord.utils import get
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions,  CheckFailure, check, guild_only
import random

client = discord.Client()

client = commands.Bot(command_prefix = '..')

@client.event
async def on_ready():
    activity = discord.Activity(type=discord.ActivityType.listening, name="..help")
    await client.change_presence(activity=activity)
    print("Bot Online")

@client.event
async def on_guild_channel_create(channel):
    guild = channel.guild
    role = discord.utils.get(guild.roles, name="Muted")
    await channel.set_permissions(role, speak=False, send_messages=False)


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
    await ctx.reply(embed=embed)


@client.command(name="mute")
@commands.has_permissions(manage_messages=True)
async def mute(ctx,member:discord.Member,reason=None):
    try:
        guild = ctx.guild
        role = discord.utils.get(guild.roles, name="Muted")

        if not role:
            role = await guild.create_role(name="Muted")
            for channel in guild.channels:
                await channel.set_permisions(role, speak=False, send_messages=False)

        embed=discord.Embed(title=f"Muted {member.mention}", description=reason)
        await member.add_roles(role, reason=reason)
        await ctx.reply(embed=embed)
    except:
        await ctx.reply("An error ocurred. Try again later")


@client.command(name="unmute")
@commands.has_permissions(manage_messages=True)
async def unmute(ctx,member:discord.Member,reason=None):
    try:
        guild = ctx.guild
        role = discord.utils.get(guild.roles, name="Muted")

        if not role:
            role = await guild.create_role(name="Muted")
            for channel in guild.channels:
                await channel.set_permisions(role, speak=False, send_messages=False)

        embed=discord.Embed(title=f"Unmuted {member.mention}", description=reason)
        await member.remove_roles(role, reason=reason)
        await ctx.reply(embed=embed)
    except:
        await ctx.reply("An error ocurred. Try again later")


@client.command(name="ban")
@commands.has_permissions(ban_members=True)
async def ban(ctx,member:discord.Member,reason=None):
    try:
        embed=discord.Embed(title=f"Banned {member.mention}", description=reason)
        await member.ban(reason=reason)
        await ctx.reply(embed=embed)
    except:
        await ctx.reply("An error ocurred. Try again later")


@client.command(name="unban",aliases=["revokeban"])
@guild_only()
@commands.has_permissions(ban_members=True)
async def unban(ctx,member):
    try:   
        banned_users = await ctx.guild.bans()
	
        member_name, member_discriminator = member.split('#')
        for ban_entry in banned_users:
            user = ban_entry.user
            
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                embed=discord.Embed(title=f"Unbanned {user.mention}")
                await ctx.guild.unban(user)
                await ctx.reply(embed=embed)
    except:
        await ctx.reply("An error ocurred. Try again later")


@client.command(name="kick")
@commands.has_permissions(kick_members=True)
async def kick(ctx,member:discord.Member,reason=None):
    try:
        embed=discord.Embed(title=f"Kicked {member.mention}", description=reason)
        await member.ban(reason=reason)
        await ctx.reply(embed=embed)
    except:
        await ctx.reply("An error occurred. Try again later")


async def openAccount(user):

  bank = json.loads(open("./bank.json","r").read())
  
  if str(user.id) in bank:
    return False
  else:
    bank[str(user.id)] = {}
    bank[str(user.id)]["wallet"] = 1000
    bank[str(user.id)]["bank"] = 0

    with open("./bank.json","w") as bankFile:
      json.dump(bank,bankFile)

@client.command(name="balance",aliases=["bal","money"])
@commands.has_permissions(kick_members=True)
async def balance(ctx,member:discord.Member=None):
  if not member:
    member = ctx.author
  await openAccount(ctx.author)
  bank = json.loads(open("./bank.json","r").read())
  walletAmt = bank[str(member.id)]["wallet"]
  bankAmt = bank[str(member.id)]["bank"]

  embed=discord.Embed(title=f"{member.name}'s Balance")
  embed.add_field(name="Wallet", value=walletAmt, inline=True)
  embed.add_field(name="Bank", value=bankAmt, inline=True)
  await ctx.reply(embed=embed)


@client.command(name="bet")
@commands.has_permissions(kick_members=True)
async def bet(ctx,money:int):
  if money > 2500:
    await ctx.reply("You can't bet more than 2500 dollars")
    return False
  win = random.randrange(2) == 1
  bank = json.loads(open("./bank.json","r").read())
  if win:
    with open("./bank.json","w") as bankW:
      bank[str(ctx.author.id)]["wallet"] += money
      json.dump(bank,bankW)
        
    embed=discord.Embed(title="You Win!",description=f"You won ${money}",color=discord.Colour.green())
  else:
    with open("./bank.json","w") as bankW:
      bank[str(ctx.author.id)]["wallet"] -= money
      json.dump(bank,bankW)
    embed=discord.Embed(title="You Lost",description=f"You lost ${money}",color=discord.Colour.red())
  await ctx.reply(embed=embed)


token = os.environ["token"]
client.run(token)
# invite link - https://discord.com/api/oauth2/authorize?client_id=948069816684642314&permissions=8&scope=bot