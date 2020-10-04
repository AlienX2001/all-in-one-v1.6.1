import discord
from trio import run as trio_run
from lib.htb import HTBot
import config as cfg

htbot = HTBot(cfg.HTB['email'], cfg.HTB['password'], cfg.HTB['api_token'])

async def send_verif_instructions(ctx):
    embed = discord.Embed(color=0x9acc14)
    embed.add_field(name="Step 1: Log in to your HackTheBox Account", value="Log in to your HackTheBox account and go to the settings page.")
    embed.set_image(url="https://image.noelshack.com/fichiers/2019/48/3/1574858388-unknown.png")
    await ctx.send(embed=embed)
    embed = discord.Embed(color=0x9acc14)
    embed.add_field(name="Step 2: Locate the Identification key", value="In the settings tab, you should be able to identify a field called \"Account Identifier\", click on the green button to copy the string.")
    embed.set_image(url="https://image.noelshack.com/fichiers/2019/48/3/1574858586-capture.png")
    await ctx.send(embed=embed)
    embed = discord.Embed(color=0x9acc14)
    embed.add_field(name="Step 3: Verify", value="Proceed to send your account identification string in the verification channel by:\n`.verify htb <string>`")
    embed.set_image(url="https://i.imgur.com/EHSZQeA.png")
    await ctx.send(embed=embed)


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
