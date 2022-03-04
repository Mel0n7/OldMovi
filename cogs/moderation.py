from discord.ext import commands
import discord
from discord.ext.commands import guild_only

class Moderation(commands.Cog):
  def __init__(self, client):
    self.client = client

    
  @commands.Cog.listener()
  async def on_guild_channel_create(channel):
    guild = channel.guild
    role = discord.utils.get(guild.roles, name="Muted")
  
    if not role:
      role = await guild.create_role(name="Muted")
      for channel in guild.channels:
        await channel.set_permisions(role, speak=False, send_messages=False)
    else:
      await channel.set_permissions(role, speak=False, send_messages=False)
  
  
  @commands.Cog.listener()
  async def on_guild_join(guild):
    role = discord.utils.get(guild.roles, name="Muted")
  
    if not role:
      role = await guild.create_role(name="Muted")
      for channel in guild.channels:
        await channel.set_permisions(role, speak=False, send_messages=False)

        
  @commands.command(name="mute")
  @commands.has_permissions(manage_messages=True)
  async def mute(self,ctx,member:discord.Member,reason=None):
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
  
  
  @commands.command(name="unmute")
  @commands.has_permissions(manage_messages=True)
  async def unmute(self,ctx,member:discord.Member,reason=None):
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
  
  
  @commands.command(name="ban")
  @commands.has_permissions(ban_members=True)
  async def ban(self,ctx,member:discord.Member,reason=None):
      try:
          embed=discord.Embed(title=f"Banned {member.mention}", description=reason)
          await member.ban(reason=reason)
          await ctx.reply(embed=embed)
      except:
          await ctx.reply("An error ocurred. Try again later")
  
  
  @commands.command(name="unban",aliases=["revokeban"])
  @guild_only()
  @commands.has_permissions(ban_members=True)
  async def unban(self,ctx,member):
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
  
  
  @commands.command(name="kick")
  @commands.has_permissions(kick_members=True)
  async def kick(self,ctx,member:discord.Member,reason=None):
      try:
          embed=discord.Embed(title=f"Kicked {member.mention}", description=reason)
          await member.ban(reason=reason)
          await ctx.reply(embed=embed)
      except:
          await ctx.reply("An error occurred. Try again later")


def setup(client):
    client.add_cog(Moderation(client))