import discord
from discord.ext import commands
import lib.manual as man
import lib.moderation as mod
import lib.verification as verification


description = '''An all in one bot'''
client = commands.Bot(command_prefix='.', description=description)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_member_join(member):
    await member.send("Welcome! Please verify using `!verify` in the Verification channel")

warn_list={}

@client.command()
async def verify(ctx, content=""):
    """Verify your HTB account"""
    await verification.verify(ctx,content)


@client.command()
async def ping(ctx):
    """Want to ping pong ?"""
    await ctx.send("Pong ! {}".format(client.latency))

@client.command(aliases=['ar'],pass_context = True)
async def addrole(ctx,role:discord.Role):
    await mod.addrole(ctx,role)

@client.command(aliases=['rr'],pass_context = True)
async def removerole(ctx,role:discord.role.Role):
    await mod.removerole(ctx,role)

@client.command(aliases=['clr'],pass_context = True)
async def clear(ctx, amount=0):
    await mod.clear(ctx,amount)

@client.command(pass_context = True)
async def warn(ctx, member: discord.Member):
     await mod.warn(ctx,member)

@client.command(aliases=['s_w'],pass_context = True)
async def show_warn(ctx, member: discord.Member):
    await mod.show_warn(ctx,member)

@client.command(aliases=['m'],pass_context = True)
async def mute(ctx, member: discord.Member):
    await mod.mute(ctx,member)

@client.command(aliases=['um'],pass_context = True)
async def unmute(ctx, member: discord.Member):
     await mod.unmute(ctx,member)

@client.command(aliases=['ui'],pass_context=True)
async def userinfo(ctx, user: discord.Member):
    await mod.userinfo(ctx,user)

@client.command(aliases=['av'],pass_context=True)
async def avatar(ctx, user: discord.Member):
    await mod.avatar(ctx,user)

@client.command(pass_context = True)
async def kick(ctx, member: discord.Member):
    await mod.kick(ctx,member)

@client.command(pass_context = True)
async def ban(ctx, member: discord.Member):
    await mod.ban(ctx,member)

@client.command(pass_context = True)
async def unban(ctx, user: discord.User):
    await mod.unban(ctx,user)

client.remove_command('help')

@client.command(aliases=['h'])
async def help(ctx,content=""):
    user=ctx.message.author
    if(content=="moderation"):
        if(user.guild_permissions.administrator):
            await man.moderation(user)
            await ctx.send("I have sent you instructions in the dm's")
        else:
            await ctx.send("You are not authorized for this command!!")
    elif(content=="verify"):
        await man.verify(ctx)
    elif(content=="status_check"):
        await man.status_check(ctx)
    else:
        embed = discord.Embed(title="HELP!!.", description="""
        1>ping -> for latency test
        2>help moderation -> for moderation related commands
        3>help verify ->for verification related commands
        4>help status_check ->for getting updates about new upcoming features
        """,color=0x000000)
        await ctx.send(embed=embed)

client.run('NzA1MDg3Mjc2MzU0NjMzOTAw.Xsvz2Q.QHQ4TxgPRtXHN-BEtIfISHWIwCw')