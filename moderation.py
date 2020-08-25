import discord
import json


async def addrole(ctx,role:discord.Role):
    member=ctx.message.author
    if(role.name == 'WannaBe Coder'):
        role=discord.utils.get(member.guild.roles, name = role.name)
        await member.add_roles(role)
        embed = discord.Embed(title="Status",
                              description="Role Added Successfully",
                              color=0x0000ff)
        await ctx.send(embed=embed)
    elif(role.name == 'WannaBe Hacker'):
        role = discord.utils.get(member.guild.roles, name=role.name)
        await member.add_roles(role)
        embed = discord.Embed(title="Status",
                              description="Role Added Successfully",
                              color=0x0000ff)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="Error",
                              description="Cant avail role via this method pls contact admin for details",
                              color=0xff0000)
        await ctx.send(embed=embed)


async def removerole(ctx,role:discord.role.Role):
    member = ctx.message.author
    role = discord.utils.get(member.guild.roles, name=role.name)
    try:
        await member.remove_roles(role)
    except:
        embed = discord.Embed(title="Error",
                              description="An error occured pls contact admin",
                              color=0xff00f6)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="Status",
                              description="Role Removed Successfully",
                              color=0x0000ff)
        await ctx.send(embed=embed)


async def clear(ctx, amount=0):
    if (amount == 0):
        embed = discord.Embed(title="Error",
                              description="Please Enter a Valid amount",
                              color=0xff0000)
        await ctx.send(embed=embed)
    else:
        await ctx.channel.purge(limit=amount + 1)


async def warn(ctx, member: discord.Member):
     if ctx.message.author.guild_permissions.administrator:
        if member.guild_permissions.administrator:
            embed = discord.Embed(title="Error",
                                  description="You cant warn an admin!!",
                                  color=0xff0000)
        else:
            try:
                with open("lib/warning.json", "r") as f:
                    warnlist = json.loads(str(f.read()))
            except:
                ctx.send(f'Error: Warning list not found!!')
            else:
                if(str(str(member.id)) in warnlist.keys()):
                    warnlist[str(str(member.id))]+=1
                else:
                    warnlist[str(str(member.id))]=1
                with open("lib/warning.json", "w") as f:
                    f.write(json.dumps(warnlist))
                if(warnlist[str(member.id)]==1):
                    await ctx.send(f'This is your first warning')
                    embed = discord.Embed(title="Status", description="**{0}** was warned by **{1}**".format(member,
                                                                                                             ctx.message.author),
                                          color=0x0000ff)
                    await ctx.send(embed=embed)
                elif(warnlist[str(member.id)]==2):
                    await ctx.send(f'This is your second warning')
                    embed = discord.Embed(title="Status", description="**{0}** was warned by **{1}**".format(member,
                                                                                                             ctx.message.author),
                                          color=0x0000ff)
                    await ctx.send(embed=embed)
                elif(warnlist[str(member.id)]==1):
                    await ctx.send(f'This is your third warning')
                    embed = discord.Embed(title="Status", description="**{0}** was warned by **{1}**".format(member,
                                                                                                             ctx.message.author),
                                          color=0x0000ff)
                    await ctx.send(embed=embed)
                else:
                    await ctx.guild.kick(member)
                    embed = discord.Embed(title="Status", description="**{0}** was kicked automatically for being warned more than 3 times".format(member),
                                          color=0x0000ff)
                    await ctx.send(embed=embed)
     else:
         embed = discord.Embed(title="Error",
                               description="Permission Denied",
                               color=0xff0000)
         await ctx.send(embed=embed)


async def show_warn(ctx, member: discord.Member):
    if member.name in warn_list.keys():
            await ctx.send(f'{member.name} has {warn_list[member.name]} warnings')
    else:
        await ctx.send(f'{member.name} has no warnings')


async def mute(ctx, member: discord.Member):
    if ctx.message.author.guild_permissions.administrator:
        role = discord.utils.get(member.guild.roles, name='Muted')
        if member.guild_permissions.administrator:
            embed = discord.Embed(title="Error",
                                  description="You cant mute an Admin",
                                  color=0xff0000)
            await ctx.send(embed=embed)
        else:
            await member.add_roles(role)
            embed=discord.Embed(title="Status", description="**{0}** was muted by **{1}**!".format(member, ctx.message.author), color=0x0000ff)
            await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="Error",
                              description="Permission Denied",
                              color=0xff0000)
        await ctx.send(embed=embed)


async def unmute(ctx, member: discord.Member):
     if ctx.message.author.guild_permissions.administrator :
        role = discord.utils.get(member.guild.roles, name='Muted')
        await member.remove_roles(role)
        embed=discord.Embed(title="Status", description="**{0}** was unmuted by **{1}**!".format(member, ctx.message.author), color=0x0000ff)
        await ctx.send(embed=embed)
     else:
         embed = discord.Embed(title="Error",
                               description="Permission Denied",
                               color=0xff0000)
         await ctx.send(embed=embed)


async def userinfo(ctx, user: discord.Member):
    pfp_url=user.avatar_url
    embed=discord.Embed(description=f'The username of the user is `{user.name}`\n'
                   f'The ID of the user is `{user.id}`\n'
                   f'The status of the user is `{user.status}`\n'
                   f'The top role of the user is `{user.top_role}`\n'
                   f'The user joined at `{user.joined_at}`',color=0xffffff)
    embed.set_image(url=pfp_url)
    await ctx.send(embed=embed)


async def avatar(ctx, user: discord.Member):
    pfp_url = user.avatar_url
    embed = discord.Embed(description=f'', color=0xffffff)
    embed.set_image(url=pfp_url)
    await ctx.send(embed=embed)


async def kick(ctx, member: discord.Member):
    if ctx.message.author.guild_permissions.administrator :
        if member.guild_permissions.administrator:
            embed = discord.Embed(title="Error",
                                  description="You cant kick an admin",
                                  color=0xff0000)
            await ctx.send(embed=embed)
        else:
            await ctx.guild.kick(member)
            embed = discord.Embed(title="Status",
                                  description="**{0}** has been kicked by **{1}**!".format(member.name, ctx.message.author),
                                  color=0x0000ff)
            await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="Error",
                                description="Permission Denied",
                                color=0xff0000)
        await ctx.send(embed=embed)


async def ban(ctx, member: discord.Member):
    if ctx.message.author.guild_permissions.administrator:
        if member.guild_permissions.administrator:
            embed = discord.Embed(title="Error",
                                  description="You cant ban an admin",
                                  color=0xff0000)
            await ctx.send(embed=embed)
        else:
            await ctx.guild.ban(member)
            embed = discord.Embed(title="Status",
                                  description="**{0}** has been banned by **{1}**!".format(member.name, ctx.message.author),
                                  color=0x0000ff)
            await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="Error",
                              description="Permission Denied",
                              color=0xff0000)
        await ctx.send(embed=embed)


async def unban(ctx, user: discord.User):
    if ctx.message.author.guild_permissions.administrator:
        try:
            await ctx.guild.unban(user)
        except:
            embed = discord.Embed(title="Status",
                                  description="The user is already unbanned!!",
                                  color=0x0000ff)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="Status",
                                  description="**{0}** has been unbanned by **{1}**!".format(user.name,
                                                                                           ctx.message.author),
                                  color=0x0000ff)
            await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="Error",
                              description="Permission Denied",
                              color=0xff0000)
        await ctx.send(embed=embed)
