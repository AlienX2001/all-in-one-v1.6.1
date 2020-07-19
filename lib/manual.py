import discord


async def moderation(user):
    embed = discord.Embed(title="Moderation manual", description="""
        1>addrole <role>->adds the role to the user\n
        2>removerole <role>->removes the role of the user\n
        3>userinfo <user mention>->displays info of the mentioned user\n
        4>avatar <user mention>->displays profile picture of user\n
        5>clear <amt of msgs>->clears the number of msgs\n
        6>warn <user mention>->warns the user\n
        7>show_warn <user mention>->shows the number of times the user has been warned\n
        8>mute <user mention>->mutes the user\n
        9>unmute <user mention>->unmutes the user\n
        10>kick <user mention>->kicks the user\n
        11>ban <user mention>->bans the user\n
        12>unban <user mention>->unbans the user\n
        13>user_info <user mention>->displays info of the user
        """,color=0x000000)
    await user.send(embed=embed)
async def verify(ctx):
    embed = discord.Embed(title="Verification manual", description="""
        1>verify -> to get the instructions in dm
        """,color=0x000000)
    await ctx.send(embed=embed)
async def status_check(ctx):
    embed = discord.Embed(title="Status report", description="""
        Currently No new features are been worked on.
        **If You need any feature you can either open an issue in github or enter the support server of the bot**
        """,color=0x000000)
    await ctx.send(embed=embed)