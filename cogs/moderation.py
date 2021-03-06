from discord.ext import commands
import discord
from discord.ext.commands import guild_only

class Moderation(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.Cog.listener()
  async def on_command_error(self, ctx, error):
    if isinstance(error,commands.BotMissingPermissions):
      textPerms = "I need these permissions:"
      for perm in error.missing_perms:
        textPerms = f"{textPerms}\n{perm}"
      embed=discord.Embed(title="I dont have permission to do that",description=textPerms,color=discord.Colour.red())
      await ctx.reply(embed=embed)
    
  @commands.Cog.listener()
  async def on_guild_channel_create(self,channel):
    guild = channel.guild
    role = discord.utils.get(guild.roles, name="Muted")
  
    if not role:
      role = await guild.create_role(name="Muted")
      for channel in guild.channels:
        await channel.set_permisions(role, speak=False, send_messages=False)
    else:
      await channel.set_permissions(role, speak=False, send_messages=False)
  
  
  @commands.Cog.listener()
  async def on_guild_join(self,guild):
    role = discord.utils.get(guild.roles, name="Muted")
  
    if not role:
      role = await guild.create_role(name="Muted")
      for channel in guild.channels:
        await channel.set_permisions(role, speak=False, send_messages=False)

        
  @commands.command(name="mute")
  @commands.has_permissions(manage_messages=True)
  async def mute(self,ctx,member:commands.MemberConverter,*,reason=None):
      try:
          guild = ctx.guild
          role = discord.utils.get(guild.roles, name="Muted")
  
          if not role:
              role = await guild.create_role(name="Muted")
              for channel in guild.channels:
                  await channel.set_permisions(role, speak=False, send_messages=False)
  
          embed=discord.Embed(title=f"Muted {member}", description=reason, color=discord.Colour.gold())
          await member.add_roles(role, reason=reason)
          await ctx.reply(embed=embed)
      except:
          await ctx.reply("An error ocurred. Try again later")
  
  
  @commands.command(name="unmute")
  @commands.has_permissions(manage_messages=True)
  async def unmute(self,ctx,member:commands.MemberConverter,*,reason=None):
      try:
          guild = ctx.guild
          role = discord.utils.get(guild.roles, name="Muted")
  
          if not role:
              role = await guild.create_role(name="Muted")
              for channel in guild.channels:
                  await channel.set_permisions(role, speak=False, send_messages=False)
  
          embed=discord.Embed(title=f"Unmuted {member}", description=reason, color=discord.Colour.gold())
          await member.remove_roles(role, reason=reason)
          await ctx.reply(embed=embed)
      except:
          await ctx.reply("An error ocurred. Try again later")
  
  
  @commands.command(name="ban")
  @commands.has_permissions(ban_members=True)
  async def ban(self,ctx,member:commands.MemberConverter,*,reason=None):
      try:
          embed=discord.Embed(title=f"Banned {member}", description=reason, color=discord.Colour.red())
          await member.ban(reason=reason)
          await ctx.reply(embed=embed)
      except:
          await ctx.reply("An error ocurred. Try again later")
  
  
  @commands.command(name="unban",aliases=["revokeban"])
  @guild_only()
  @commands.has_permissions(ban_members=True)
  async def unban(self,ctx,member,*,reason=None):
      try:   
          banned_users = await ctx.guild.bans()
  	
          member_name, member_discriminator = member.split('#')
          for ban_entry in banned_users:
              user = ban_entry.user
              
              if (user.name, user.discriminator) == (member_name, member_discriminator):
                  embed=discord.Embed(title=f"Unbanned {member}", description=reason, color=discord.Colour.red())
                  await ctx.guild.unban(user)
                  await ctx.reply(embed=embed)
      except:
          await ctx.reply("An error ocurred. Try again later")
  
  
  @commands.command(name="kick")
  @commands.has_permissions(kick_members=True)
  async def kick(self,ctx,member:commands.MemberConverter,*,reason=None):
      try:
          embed=discord.Embed(title=f"Kicked {member}", description=reason, color=discord.Colour.gold())
          await member.ban(reason=reason)
          await ctx.reply(embed=embed)
      except:
          await ctx.reply("An error occurred. Try again later")

  
  @commands.command(name="deafen")
  @commands.has_permissions(administrator=True)
  async def deafen(self,ctx,member:commands.MemberConverter,*,reason=None):
      try:
          embed=discord.Embed(title=f"Deafened {member}", description=reason, color=discord.Colour.gold())
          await member.edit(deafen=True)
          await ctx.reply(embed=embed)
      except:
          await ctx.reply("An error occurred. Try again later")


  @commands.command(name="undeafen")
  @commands.has_permissions(administrator=True)
  async def undeafen(self,ctx,member:commands.MemberConverter,*,reason=None):
      try:
          embed=discord.Embed(title=f"Undeafened {member}", description=reason, color=discord.Colour.gold())
          await member.edit(deafen=False)
          await ctx.reply(embed=embed)
      except:
          await ctx.reply("An error occurred. Try again later")

  
  @commands.command(name="slowmode",aliases=["sm","chatdelay"])
  @commands.has_permissions(administrator=True)
  async def slowmode(self,ctx,time:int,channel:commands.TextChannelConverter=None):
      try:
          if not channel:
            channel = ctx.channel
          embed=discord.Embed(title=f"Set slowmode to {time}s", description=f"Set slowmode for #{channel.name} to {time}s", color=discord.Colour.green())
          await channel.edit(slowmode_delay=time)
          await ctx.reply(embed=embed)
      except:
          await ctx.reply("An error occurred. Try again later")

  
  @commands.command(name="nickname",aliases=["nn","nick"])
  @commands.has_permissions(administrator=True)
  async def nickname(self,ctx,member:commands.MemberConverter,*,name:str):
      try:
          embed=discord.Embed(title=f"Set {member}'s name to {name}", color=discord.Colour.green())
          await member.edit(nick=name)
          await ctx.reply(embed=embed)
      except:
          await ctx.reply("An error occurred. Try again later")

def setup(client):
    client.add_cog(Moderation(client))