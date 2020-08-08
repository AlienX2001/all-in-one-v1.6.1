import discord
from discord.ext import commands
import lib.manual as man
import lib.moderation as mod
import lib.htb_verification as htb_verification
import lib.cf_verification as cf_verification
import lib.game as game
import json

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
    await member.send("Welcome! Please verify using `.verify` in the Verification channel")

warn_list={}

@client.command()
async def verify(ctx, site="", content=""):
    """Verify your accounts"""
    if(site=="htb" or site=="hackthebox"):
        await htb_verification.verify(ctx,content)
    elif(site=="codeforces"):
        await cf_verification.verify(ctx,content)
    else:
        await ctx.send(f'The Correct Way is `.verify <site> <content>` the <site> can be htb/hackthebox or codeforces')


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

@client.command()
async def quiz(ctx,member:discord.Member,command="",var=""):
    if(command=="start"):
        player1 = ctx.message.author
        player2 = member
        if(player1!=player2):
            if(var==""):
                await ctx.send(f'The correct way is `.quiz <mention user> start <number of rounds>`')
            elif(var=="0"):
                await ctx.send(f'You cant have a quiz of 0 rounds')
            elif(var <="0" or var >="5"):
                await ctx.send(f'Max number of rounds can be 5')
            else:
                with open("lib/rounds.txt","w") as f:#will have to change the file path
                    f.write(str(int(var)*2))
                await ctx.send(f'GAME STARTED !!! {player1.mention} vs {player2.mention}')
                with open("lib/players.json","w") as f:
                    players={"1":player1.id, "2":player2.id}
                    f.write(json.dumps(players))
                await ctx.send(f'You can start playing by `.quiz <user mention> play`')
        else:
            await ctx.send(f'You cant start a game with yourself!!')

    elif(command=="play"):
        #the playing of game
        with open("lib/players.json", "r") as f:
            players=json.loads(f.read())
        for key in players.keys():
            if (key=='1'):
                player1=players['1']
            elif(key=='2'):
                player2=players['2']
        if(ctx.message.author.id in players.values()):
            if(player1!=player2):
                with open("lib/rounds.txt","r") as f:#will have to change the file path
                    rounds=f.read()
                if(int(rounds)>0 and int(rounds)%2==1):
                    targetplayer=player1
                    with open("lib/turn.txt","w") as f: #will have to change the file path
                        f.write(str(targetplayer))
                    #game code
                    await game.play(ctx,targetplayer)
                elif (int(rounds) > 0 and int(rounds) % 2 == 0):
                    targetplayer = player2
                    with open("lib/turn.txt", "w") as f:  # will have to change the file path
                        f.write(str(targetplayer))
                    # game code
                    await game.play(ctx, targetplayer)
                else:
                    await ctx.send(f'No Game in Progress!! Start one to play.')
            else:
                ctx.send(f'You need to mention the other player!!')
        else:
            await ctx.message.delete()
            await ctx.send(f'You are not in the current game {ctx.message.author.mention}')
    elif(command=="answer"):
        #answer command
        with open("lib/players.json", "r") as f:
            players = json.loads(f.read())
        for key in players.keys():
            if (key == '1'):
                player1 = players['1']
            elif (key == '2'):
                player2 = players['2']
        if(ctx.message.author.id in players.values()):
            if(player1!=player2):
                with open("lib/turn.txt", "r") as f:  # will have to change file path
                    targetplayer = f.read()
                if (str(ctx.message.author.id) != targetplayer):
                    await ctx.message.delete()
                    await ctx.send(f'You cant enter the answer')
                else:
                    with open("lib/rounds.txt", "r+") as f:  # will have to change the file path
                        rounds = int(f.read())
                        rounds-=1;
                        f.seek(0,0)
                        f.write(str(rounds))
                    await game.answer(ctx, var, rounds)
            else:
                ctx.send(f'You need to mention the other player!!')
        else:
            await ctx.message.delete()
            await ctx.send(f'You are not in the current game {ctx.message.author.mention}')
    elif(command==""):
        #help options
        embed=discord.Embed(title="Quiz HELP!!!",description='''
        1>.quiz <user mention> start <number of rounds> -> To start a game with the mentioned user\n
        2>.quiz <user mention> play -> To get questions(only if a game is started)\n
        3>.quiz <user mention> answer <answer option(1,2,3)> -> To select the correct option\n
        4>.quiz <user mention> <anything else> -> This help
        ''',color=0xFF0000)
        await ctx.send(embed=embed)

@client.command()
async def quiz_add(ctx,ques="",ans="",anslist=""):
    if(ques==""):
        await ctx.send(f'The format is `.quiz_add <ques> <correct ans> <options list(3) in double quotes with the delimiter as ":">`')
    elif(ans==""):
        await ctx.send(f'Please enter answer')
    elif(anslist==""):
        await ctx.send(f'Please enter 3 options. In double quotes with the delimiter ":"')
    else:
        await game.add(ctx,ques,ans,anslist)

@client.command()
async def show_unverified(ctx):
    if (ctx.message.author.guild_permissions.administrator):
        await game.show(ctx.message.author)
        await ctx.send(f'All unverified questions and answers has been sent to your dms')
    else:
        await ctx.send(f'You are not authourized to view this!!')

@client.command()
async def quiz_verify(ctx,value=""):
    if(ctx.message.author.guild_permissions.administrator):
        await game.verify(ctx,value)
        await ctx.send(f'Question has been verified and is added to the list')
    else:
        await ctx.send(f'You are not authourized to view this!!')

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
    elif(content=="quiz"):
        await man.quiz(ctx)
    else:
        embed = discord.Embed(title="HELP!!.", description="""
        1>ping -> for latency test
        2>help verify -> for verification related commands
        3>help quiz -> for all quiz related commands
        4>help moderation -> for moderation related commands
        5>help status_check -> for getting updates about new upcoming features
        """,color=0x000000)
        await ctx.send(embed=embed)

client.run('YOUR BOT TOKEN HERE')
