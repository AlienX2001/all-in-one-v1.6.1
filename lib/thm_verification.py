import discord
import lib.thm as thm

async def verify(ctx, content=""):
    """Verify your codeforces account"""
    if content:
        await ctx.message.delete()
        verify_rep = thm.verify_user(str(ctx.message.author.id),content)
        if verify_rep == "already_in":
            await ctx.send("You already have verified your codeforces account.")
        elif verify_rep == "wrong_id":
            await ctx.send("This Account Handle does not work.\nAre you sure you followed the instructions correctly ?")
        else:
            member=ctx.message.author
            role = discord.utils.get(member.guild.roles, name='Member')
            await member.add_roles(role)
            embed = discord.Embed(title="Roles added", description='Member', color=0x14ff08)
            await ctx.send(embed=embed)
    else:
            await ctx.send(f'Please send your discord token via the following ``.verify thm/tryhackme <token>``')
