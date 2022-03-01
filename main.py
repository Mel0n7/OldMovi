import discord, os, time, requests, json, discord.ext
from discord.utils import get
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions,  CheckFailure, check, guild_only

client = discord.Client()

client = commands.Bot(command_prefix = '..')

@client.event
async def on_ready():
    activity = discord.Activity(type=discord.ActivityType.listening, name="..help")
    await client.change_presence(activity=activity) # Set Activity to "Listening to /status"
    print("Bot Online")

client.remove_command('help')
@client.command(name="help")
async def help(ctx):
    embed=discord.Embed(title="Help")
    embed.add_field(name="..help", value="Open this!", inline=False)
    embed.add_field(name="..mute {member} {reason}", value="Kick the member mentioned", inline=False)
    embed.add_field(name="..kick {member} {reason}", value="Kick the member mentioned", inline=False)
    embed.add_field(name="..ban {member} {reason}", value="Ban the member mentioned", inline=False)
    embed.add_field(name="..unban {member}", value="Unban the member mentioned", inline=False)
    await ctx.reply(embed=embed)
@client.command(name="mute")
@commands.has_permissions(mute_members=True)
async def mute(ctx,member:discord.Member):
    try:
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        embed=discord.Embed(title=f"Muted {member}")
        await member.add_roles(role)
        await ctx.reply(embed=embed)
    except:
        await ctx.reply("An error ocurred. Try again later")
@client.command(name="unmute")
@commands.has_permissions(mute_members=True)
async def unmute(ctx,member:discord.Member):
    try:
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        embed=discord.Embed(title=f"Muted {member}")
        await member.remove_roles(role)
        await ctx.reply(embed=embed)
    except:
        await ctx.reply("An error ocurred. Try again later")
@client.command(name="ban")
@commands.has_permissions(ban_members=True)
async def ban(ctx,member:discord.Member,reason=None):
    try:
        embed=discord.Embed(title=f"Banned {member}", description=reason)
        await member.ban(reason=reason)
        await ctx.reply(embed=embed)
    except:
        await ctx.reply("An error ocurred. Try again later")
@client.command(name="unban")
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
        embed=discord.Embed(title=f"Kicked {member}", description=reason)
        await member.ban(reason=reason)
        await ctx.reply(embed=embed)
    except:
        await ctx.reply("An error ocurred. Try again later")
client.run("OTQ4MDY5ODE2Njg0NjQyMzE0.Yh2c0g.ZkgmyGC8lNg_AODMctL86rTJJsc")
# invite link - https://discord.com/api/oauth2/authorize?client_id=948069816684642314&permissions=8&scope=bot