from discord.ext import commands
import discord, json, random

class Economy(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.Cog.listener()
  async def on_command_error(self, ctx, error):
    if isinstance(error,commands.CommandOnCooldown):
      embed=discord.Embed(title="On Cooldown",description=f"Please wait {int(error.retry_after)} seconds",color=discord.Colour.red())
      await ctx.reply(embed=embed)
      
  async def bankData(self):
    bank = json.loads(open("./bank.json","r").read())
    return bank

  
  async def openAccount(self,user):
    bank = await self.bankData()
    
    if str(user.id) in bank:
      return False
    else:
      bank[str(user.id)] = {}
      bank[str(user.id)]["wallet"] = 1000
      bank[str(user.id)]["bank"] = 0
  
      with open("./bank.json","w") as bankFile:
        json.dump(bank,bankFile)

  
  @commands.command(name="balance",aliases=["bal","money"])
  async def balance(self,ctx,member:discord.Member=None):
    if not member:
      member = ctx.author
    await self.openAccount(ctx.author)
    bank = await self.bankData()
    walletAmt = bank[str(member.id)]["wallet"]
    bankAmt = bank[str(member.id)]["bank"]
  
    embed=discord.Embed(title=f"{member.name}'s Balance")
    embed.add_field(name="Wallet", value=walletAmt, inline=True)
    embed.add_field(name="Bank", value=bankAmt, inline=True)
    await ctx.reply(embed=embed)
  
  
  @commands.command(name="bet")
  async def bet(self,ctx,money:int):
    if money == 0:
      await ctx.reply("You cant bet 0 dollars")
      return False
    if not abs(money) == money:
      await ctx.reply("You cant bet negative money")
      return False
    if money > 2500:
      await ctx.reply("You can't bet more than 2500 dollars")
      return False
    bank = await self.bankData()
    if bank[str(ctx.author.id)]["wallet"] < money:
      await ctx.reply(f"You dont even have {money} dollars")
      return False
    win = random.randrange(2) == 1
    if win:
      with open("./bank.json","w") as bankW:
        try:
          bank[str(ctx.author.id)]["wallet"] += money
        except:
          await ctx.reply("An error occurred. Try again later")
          return False
        else:
          json.dump(bank,bankW)
      newMoney = bank[str(ctx.author.id)]["wallet"]
      d = f"You won ${money}\nYour new balance is ${newMoney}"
      embed=discord.Embed(title="You Win!",description=d,color=discord.Colour.green())
    else:
      with open("./bank.json","w") as bankW:
        try:
          bank[str(ctx.author.id)]["wallet"] -= money
        except:
          await ctx.reply("An error occurred. Try again later")
          return False
        else:
          json.dump(bank,bankW)
      newMoney = bank[str(ctx.author.id)]["wallet"]
      d = f"You lost ${money}\nYour new balance is ${newMoney}"
      embed=discord.Embed(title="You Lost",description=d,color=discord.Colour.red())
    await ctx.reply(embed=embed)


  @commands.command(name="deposit")
  async def deposit(self,ctx,money:int):
    bank = await self.bankData()
    if money == 0:
      await ctx.reply("You cant deposit 0 dollars")
      return False
    if not abs(money) == money:
      await ctx.reply("You cant deposit negative money")
      return False
    if bank[str(ctx.author.id)]["wallet"] < money:
      await ctx.reply(f"You dont even have {money} dollars")
      return False
    with open("./bank.json","w") as bankW:
      try:
        bank[str(ctx.author.id)]["wallet"] -= money
        bank[str(ctx.author.id)]["bank"] += money
      except:
        await ctx.reply("An error occurred. Try again later")
        return False
      else:
        json.dump(bank,bankW)

        
  @commands.command(name="withdraw")
  async def withdraw(self,ctx,money:int):
    bank = await self.bankData()
    if money == 0:
      await ctx.reply("You cant withdraw 0 dollars")
      return False
    if not abs(money) == money:
      await ctx.reply("You cant withdraw negative money")
      return False
    if bank[str(ctx.author.id)]["bank"] < money:
      await ctx.reply(f"You dont even have {money} dollars")
      return False
    with open("./bank.json","w") as bankW:
      try:
        bank[str(ctx.author.id)]["wallet"] += money
        bank[str(ctx.author.id)]["bank"] -= money
      except:
        await ctx.reply("An error occurred. Try again later")
        return False
      else:
        json.dump(bank,bankW)

  @commands.command(name="buy")
  async def buy(self,ctx,item:str):
    items = {"Cool Item":500}
    bank = await self.bankData()
    if item in items:
      if bank[str(ctx.author.id)]["wallet"] < items[item]:
        await ctx.reply(f"You dont even have {items[item]} dollars")
        return False
      with open("./bank.json","w") as bankW:
        try:
          bank[str(ctx.author.id)]["wallet"] -= items[item]
        except:
          await ctx.reply("An error occurred. Try again later")
          return False
        else:
          json.dump(bank,bankW)
          embed=discord.Embed(title=f"Buy {item} for ${items[item]}")
          await ctx.reply(embed=embed)
    else:
      ctx.reply("We dont sell that item")

        
  @commands.command(name="daily")
  @commands.cooldown(1, 86400, commands.BucketType.user)
  async def daily(self,ctx):
    bank = await self.bankData()
    with open("./bank.json","w") as bankW:
      bank[str(ctx.author.id)]["wallet"] += 10000
      json.dump(bank,bankW)
    newMoney = bank[str(ctx.author.id)]["wallet"]
    embed=discord.Embed(title="Daily",description=f"You got $10000\nYour new balance is ${newMoney}",color=discord.Colour.green())
    await ctx.reply(embed=embed)
def setup(client):
    client.add_cog(Economy(client))