import discord
from trio import run as trio_run
from lib.htb import HTBot
import config as cfg

htbot = HTBot(cfg.HTB['email'], cfg.HTB['password'], cfg.HTB['api_token'])

async def send_verif_instructions(ctx):
    ctx.send("Type `.verify htb <your account identifier>")
    ctx.send("If having trouble kindly refer to this google doc https://docs.google.com/document/d/17GbuhXY1SgCdUjXXbWh1L5XvfofOT7h5DXccBIcqNGo/edit?usp=sharing")


async def verify(ctx, content=""):
    """Verify your HTB account"""
    if content:
        await ctx.message.delete()
        verify_rep = trio_run(htbot.verify_user, ctx.author.id, content)
        if verify_rep == "already_in":
            await ctx.send("You already have verified your HTB account.")
        elif verify_rep == "wrong_id":
            await ctx.send("This Account Identifier does not work.\nAre you sure you followed the instructions correctly ?")
        else:
            member=ctx.message.author
            role = discord.utils.get(member.guild.roles, name='Member')
            await member.add_roles(role)
            embed = discord.Embed(title="Roles added", description='Member', color=0x14ff08)
            await ctx.send(embed=embed)
    else:
        await send_verif_instructions(ctx)
