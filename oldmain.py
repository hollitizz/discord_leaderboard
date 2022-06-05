import traceback
import discord
from discord.ext import commands, tasks
import asyncio
import json
import urllib.parse
import requests
import random
import validators

@bot.command(name="register")
async def register(ctx):
    await create_player(ctx,
                        ctx.message.author.mention,
                        ctx.message.content.replace(f'{config["prefix"]}register ', ''))


@bot.command()
async def roll(ctx):
    draw_list = ctx.message.content.split()[1:]
    if not draw_list:
        await ctx.reply("'fin tu te fou de ma gueule a roll rien du tout ???????????????")
        await ctx.reply("<:angryarthur:853345559758897172>")
        return
    random.shuffle(draw_list)
    await ctx.reply(draw_list[0])

@bot.command()
async def create_coaching(ctx):
    check_permission(ctx.message.author)
    content = ctx.message.content[len("!create_coaching"):].split(" ")
    day = "demain"
    hour = "21h"
    nbr = "1"
    for i in content:
        if i == "--day":
            day = content[content.index("--day") + 1]
        elif i == "--hour":
            hour = content[content.index("--hour") + 1]
        elif i == "--nbr":
            nbr = content[content.index("--nbr") + 1]
    try:
        coaching["nbr"] = int(nbr)
    except:
        coaching["nbr"] = 1
    coaching["message"] = 0
    coaching["participants"] = []
    msg =   f"Tu as envie de te faire coacher **{day}** à **{hour}** ?\n"\
            f"Réagis avec <:jannapat:847656799590678538>"\
            f" et attends de voir si tu es tiré(e) au sort ! ({nbr} personne(s))"
    channel = await bot.fetch_channel(config["annonce"])
    sended_msg = await channel.send(msg)
    await sended_msg.add_reaction("<:jannapat:847656799590678538>")
    coaching["message"] = sended_msg.id
    Save.coaching()


@bot.command()
async def draw_coaching(ctx):
    check_permission(ctx.message.author)
    content = ctx.message.content[len("!draw_coaching "):]
    if content:
        try:
            coaching["nbr"] = int(content)
        except:
            coaching["nbr"] = 1
    if coaching["nbr"] > len(coaching['participants']):
        coaching["nbr"] = len(coaching['participants'])
    random.shuffle(coaching["participants"])
    msg = "Les personnes sélectionnée(s) pour le coaching sont :\n"
    for i in range(coaching["nbr"]):
        msg += f"{coaching['participants'][i]}\n"
    channel = await bot.fetch_channel(config["annonce"])
    await channel.send(msg)


@bot.command(name="count_members")
async def count_members(ctx):
    guild = bot.get_guild(832250335631376455)

    await ctx.message.channel.send(f"There is actually {guild.member_count} members in this server")


@bot.command(name="add_player")
async def add_player(ctx):
    tag = ctx.message.content.split()[1]
    check_permission(ctx.message.author)
    await create_player(ctx,
                        tag,
                        ctx.message.content.replace(f'{config["prefix"]}add_player {tag} ', ''))


@bot.command(name="unregister")
async def unregister(ctx):
    pos = check_player_exist(ctx.message.author.mention)
    if (pos == -1):
        raise CommandError("You is not registered on the leaderboard")
    await ctx.message.channel.send(f"You has been removed from the leaderboard")
    del(leaderboard["user"][pos])
    Save.leaderboard()


@bot.command()
async def del_player(ctx):
    check_permission(ctx.message.author)
    content = ctx.message.content[12:]
    if (content.isdigit()):
        pos = int(content) - 1
    else:
        pos = check_player_exist(ctx.message.content.split()[1])
    if (pos == -1):
        raise CommandError("This user is not registered on the leaderboard")
    await ctx.channel.send(f"{leaderboard['user'][pos][0]} has been removed from the leaderboard")
    del(leaderboard["user"][pos])
    Save.leaderboard()

@bot.command()
async def get_opgg(ctx, *args):
    for mention in args:
        is_opgg = False
        for user in leaderboard["user"]:
            if mention == user[0].replace('!', ''):
                await ctx.channel.send(f"https://euw.op.gg/summoners/euw/{urllib.parse.quote(user[1])}")
                is_opgg = True
        if not is_opgg:
            await ctx.channel.send(f"opgg of {mention} is not registred")
