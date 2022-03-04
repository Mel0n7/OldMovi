from discord.ext import commands
import discord, json, random

class Economy(commands.Cog):
  def __init__(self, client):
    self.client = client

  async def bankData(self):
    bank = json.loads(open("./../bank.json","r").read())
    return bank
  
  async def openAccount(self,user):

    bank = self.bankData()
    
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
    bank = self.bankData()
    walletAmt = bank[str(member.id)]["wallet"]
    bankAmt = bank[str(member.id)]["bank"]
  
    embed=discord.Embed(title=f"{member.name}'s Balance")
    embed.add_field(name="Wallet", value=walletAmt, inline=True)
    embed.add_field(name="Bank", value=bankAmt, inline=True)
    await ctx.reply(embed=embed)
  
  
  @commands.command(name="bet")
  async def bet(self,ctx,money:int):
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

def setup(client):
    client.add_cog(Economy(client))