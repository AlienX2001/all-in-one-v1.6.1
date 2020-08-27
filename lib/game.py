import discord
from discord.ext import commands
import random
import json
import os
def show_ans(list):
    temp=""
    for i in range(0,len(list)):
        temp+=("\n"+str(i+1)+"> "+list[i])
    return(temp)

with open("lib/questions.json", "r") as f:
    queslist = json.loads(str(f.read()))
with open("lib/answerlist.json", "r") as f:
    anslist = json.loads(str(f.read()))
with open("lib/answers.json", "r") as f:
    correctans = json.loads(str(f.read()))

index=0

async def add(ctx,ques,ans,anslist):
    with open("lib/unverified_questions.json","r") as f:
        temp_ques=json.loads(str(f.read()))
    qnumber=len(temp_ques.keys())
    with open("lib/unverified_answers.json","r") as f:
        temp_ans = json.loads(str(f.read()))
    anumber=len(temp_ans.keys())
    with open("lib/unverified_anslist.json","r") as f:
        temp_anslist = json.loads(str(f.read()))
    alistnumber=len(temp_anslist.keys())
    temp_ques[qnumber+1]=ques
    temp_ans[anumber+1]=ans
    anslist=anslist.split(':')
    temp_anslist[alistnumber+1]=anslist
    with open("lib/unverified_questions.json","w") as f:
        f.write(json.dumps(temp_ques))
    with open("lib/unverified_answers.json","w") as f:
        f.write(json.dumps(temp_ans))
    with open("lib/unverified_anslist.json","w") as f:
        f.write(json.dumps(temp_anslist))
    await ctx.send(f'Questions has been added to the unverfied list successfully. Kindly wait for an admin to verify the questions')


async def show(user):
    with open("lib/unverified_questions.json","r") as f:
        temp_ques=json.loads(str(f.read()))
    with open("lib/unverified_answers.json","r") as f:
        temp_ans=json.loads(str(f.read()))
    with open("lib/unverified_anslist.json", "r") as f:
        temp_anslist = json.loads(str(f.read()))
    for i,j,k in zip(temp_ques.keys(),temp_ans.keys(),temp_anslist.keys()):
        await user.send(f'Q{int(i)}> {temp_ques[i]}')
        await user.send(f'Ans{int(j)}> {temp_ans[j]}')
        await user.send(f'Options{int(k)}> {temp_anslist[k]}')

async def play(ctx, player):
    await ctx.send(f'This is a question to <@!{player}>')
    numberofques = len(queslist.keys())
    global index
    index = random.randint(1, numberofques)
    with open("index.txt","w") as f:#will have to change file path
        f.write(str(index))
    qembed = discord.Embed(title="Question", description=f'Your question is ***{queslist[str(index)]}***',
                           color=0xff0000)
    await ctx.send(embed=qembed)
    await ctx.send(f'The answers are:-')
    aembed = discord.Embed(title="Answers", description=f'Your choices are ***{show_ans((anslist[str(index)]))}***', color=0xff0000)
    await ctx.send(embed=aembed)
    await ctx.send(f'To answer the question `.quiz <player mention> answer <options(1/2/3)`>')
    with open("correct_ans.txt","w") as f:#will have to change file path
        f.write(str(correctans[str(index)]))
async def answer(ctx,ans,rounds):
        try:
            with open("index.txt","r") as f:#will have to change file path
                global index
                index=f.read()
            with open("correct_ans.txt","r") as f:#will have to change file path
                correctanswer=f.read()
        except exception as e:
            await ctx.send(f'{e}')
        else:
            if(anslist[index][int(ans)-1]==correctanswer):
                await ctx.send(f'NICE')
                score={
                    str(ctx.message.author):1
                }
            else:
                await ctx.send(f'FAILED')
                score = {
                    str(ctx.message.author): 0
                }
            with open("lib/scoreboard.json","r") as f: #will have to change file path
                tempvar=json.loads(str(f.read()))
            if(len(tempvar.keys())==0):
                list_main={}
            else:
                list_main=tempvar
            if(str(ctx.message.author.id) in str(list_main.keys())):
                with open("lib/scoreboard.json", "r") as f:  # will have to change file path
                    tempvar = json.loads(str(f.read()))
                list1 = tempvar
                for key in list1.keys():
                    key ='"'+key+'"'
                list1[str(ctx.message.author.id)] += score[str(ctx.message.author)]
                with open("lib/scoreboard.json","w") as f:#will have to change file path
                    f.write(json.dumps(list1))
            else:
                with open("lib/scoreboard.json","r") as f: #will have to change file path
                    tempvar = json.loads(str(f.read()))
                if(tempvar==""):
                    list2={}
                else:
                    list2=tempvar
                list2[str(ctx.message.author.id)] = 0
                list2[str(ctx.message.author.id)] += score[str(ctx.message.author)]
                for key in list2.keys():
                    key = '"' + key + '"'
                with open("lib/scoreboard.json","w") as f:#will have to change file path
                    f.write(json.dumps(list2))
            if(rounds==0):
                with open("lib/scoreboard.json", "r") as f:  # will have to change file path
                    tempvar = json.loads(str(f.read()))
                scores=tempvar.values()
                if(list(scores)[0]>list(scores)[1]):
                    for val in tempvar.values():
                        if(list(scores)[0]==val):
                            await ctx.send(f'<@!{list(tempvar.keys())[list(tempvar.values()).index(val)]}> wins 🥳🥳')
                            with open("lib/scoreboard.json",
                                      "r") as f:  # will have to change file path
                                tempvar = json.loads(str(f.read()))
                            for key in tempvar.keys():
                                key = '"' + key + '"'
                            for key in tempvar.keys():
                                tempvar[key]=0
                            with open("lib/scoreboard.json","w") as f:
                                f.write(json.dumps(tempvar))

                elif(list(scores)[1]>list(scores)[0]):
                    for val in tempvar.values():
                        if(list(scores)[1]==val):
                            await ctx.send(f'<@!{list(tempvar.keys())[list(tempvar.values()).index(val)]}> wins 🥳🥳')
                            with open("lib/scoreboard.json","r") as f:  # will have to change file path
                                tempvar = json.loads(str(f.read()))
                            for key in tempvar.keys():
                                key = '"' + key + '"'
                            for key in tempvar.keys():
                                tempvar[key]=0
                            with open("lib/scoreboard.json","w") as f:  # will have to change file path
                                f.write(json.dumps(tempvar))
                else:
                    await ctx.send(f'Its a Draw!!...Well Played both of You')
                    with open("lib/scoreboard.json","r") as f:  # will have to change file path
                        tempvar = json.loads(str(f.read()))
                    for key in tempvar.keys():
                        key = '"' + key + '"'
                    for key in tempvar.keys():
                        tempvar[key] = 0
                    with open("lib/scoreboard.json","w") as f:  # will have to change file path
                        f.write(json.dumps(tempvar))


async def verify(ctx,val):
    with open("lib/unverified_questions.json","r") as f:
        temp_ques=json.loads(str(f.read()))
    with open("lib/unverified_answers.json","r") as f:
        temp_ans=json.loads(str(f.read()))
    with open("lib/unverified_anslist.json","r") as f:
        temp_anslist=json.loads(str(f.read()))
    with open("lib/questions.json","r") as f:
        ques=json.loads(str(f.read()))
    with open("lib/answers.json","r") as f:
        ans=json.loads(str(f.read()))
    with open("lib/answerlist.json","r") as f:
        anslist=json.loads(str(f.read()))
    temp_temp_ques={1:""}
    temp_temp_ans={1:""}
    temp_temp_anslist={1:[]}
    for key in temp_ques.keys():
        if(int(val)==int(key)):
            temp_temp_ques[1]=temp_ques[key]
    del temp_ques[val]
    with open("lib/unverified_questions.json", "w") as f:
        f.write(json.dumps(temp_ques))
    for key in temp_ans.keys():
        if(int(val)==int(key)):
            temp_temp_ans[1]=temp_ans[key]
    del temp_ans[val]
    with open("lib/unverified_answers.json", "w") as f:
        f.write(json.dumps(temp_ans))
    for key in temp_anslist.keys():
        if(int(val)==int(key)):
            temp_temp_anslist[1]=temp_anslist[key]
    del temp_anslist[val]
    with open("lib/unverified_anslist.json", "w") as f:
        f.write(json.dumps(temp_anslist))
    if(len(ques.keys())==0):
        ques[1]=temp_temp_ques[1]
        ans[1]=temp_temp_ans[1]
        anslist[1]=temp_temp_anslist[1]
    else:
        ques[len(ques.keys())+1]=temp_temp_ques[1]
        ans[len(ans.keys())+1]=temp_temp_ans[1]
        anslist[len(ans.keys()+1)]=temp_temp_anslist[1]
    with open("lib/questions.json","w") as f:
        f.write(json.dumps(ques))
    with open("lib/answers.json","w") as f:
        f.write(json.dumps(ans))
    with open("lib/answerlist.json","w") as f:
        f.write(json.dumps(anslist))
    await ctx.send(f'Question has been verified successfully')

#add feature to display who won via the scoreboard(current) and then do +1 in the scoreboard(final) and then delete thre records of current scorboard for the next match