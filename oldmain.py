import traceback
import discord
from discord.ext import commands, tasks
import asyncio
import json
import urllib.parse
import requests
import random
import validators

with open("leaderboard.json", encoding='utf-8') as tmp0:
    leaderboard = json.load(tmp0)
with open("config.json", encoding='utf-8') as tmp1:
    config = json.load(tmp1)
with open("coaching.json", encoding='utf-8') as tmp2:
    coaching = json.load(tmp2)


HOLLI = 222008900025581568
SASHA = 786940025887653928
NINJANA = 905479749617455154


class CommandError(Exception):
    pass


intents = discord.Intents.all()

def command_prefix(bot, message):
    if validators.url(message.content):
        return ''
    else:
        return '!'

bot = commands.Bot(command_prefix='!', intents=intents)
bot.remove_command('help')

roles_id = [
    834851399673315358,
    934601628558954526,
    934601629284565012,
    934601635315978280,
    934601636314239066,
    934601637052416100,
    934601637803200563,
    934601643222270054,
    934601644115656766,
    934601646896472094
]

rank_division = [
    "<:ss:934834425705955368>",
    "<:ironS12:934832930675630111>",
    "<:bronzeS12:934832964351717416>",
    "<:silverS12:934832980793389107>",
    "<:goldS12:934832999499964416>",
    "<:platineS12:934833013844500510>",
    "<:diamantS12:934833028943994890>",
    "<:masterS12:934833052641800232>",
    "<:grandmasterS12:934833074754183198>",
    "<:challengerS12:934833092114399242>"
]
api_tier = [
    "UNRANKED",
    "IRON",
    "BRONZE",
    "SILVER",
    "GOLD",
    "PLATINUM",
    "DIAMOND",
    "MASTER",
    "GRANDMASTER",
    "CHALLENGER"
]
api_rank = [
    "0",
    "I",
    "II",
    "III",
    "IV"
]


class Save:
    def leaderboard():
        with open("leaderboard.json", "w", encoding='utf-8') as leaderboard_file:
            json.dump(leaderboard, leaderboard_file, indent=4)

    def config():
        with open("config.json", "w", encoding='utf-8') as config_file:
            json.dump(config, config_file, indent=4)

    def coaching():
        with open("coaching.json", "w", encoding='utf-8') as coaching_file:
            json.dump(coaching, coaching_file, indent=4)


def check_permission(author):
    if (author.id != HOLLI and author.id != SASHA and author.id != NINJANA and
        not author.guild_permissions.administrator):
        raise CommandError("Permission Denied")


def check_player_exist(tag):
    i = 0

    for i in range(len(leaderboard["user"])):
        if (leaderboard["user"][i][0].replace('!', '') == tag):
            return i
    return -1


async def check_name(user):
    link = f"https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{urllib.parse.quote(user)}?{config['riotkey']}"
    r = requests.get(link)
    res = r.json()
    try:
        leaderboard["tmp_id"] = res["id"]
    except:
        return False
    return True


async def create_player(ctx, tag, user):
    player_exist = check_player_exist(tag)

    if (not await check_name(user)):
        await ctx.reply(f"your summoner_id: *{user}*, wasn't found")
        return
    if (player_exist == -1):
        leaderboard["user"].append([tag, user, None, None, None, leaderboard["tmp_id"]])
    else:
        leaderboard["user"][player_exist] = [tag, user, None, None, None, leaderboard["tmp_id"]]
    leaderboard["tmp_id"] = None
    await ctx.message.channel.send(f"{tag} aka *{user}* has been added to the leaderboard, wait for the next refresh")
    Save.leaderboard()

def get_api_tier(elo):
    i = 0
    while (i < len(api_tier) and api_tier[i] != elo):
        i += 1
    if (i > len(api_tier)):
        return 0
    return i


def get_api_rank(elo):
    i = 0
    while (i < len(api_rank) and api_rank[i] != elo):
        i += 1
    if (i > len(api_rank)):
        return 0
    return i


def get_player_stats(id, i):
    link = f"https://euw1.api.riotgames.com/lol/league/v4/entries/by-summoner/{id}?{config['riotkey']}"
    r = requests.get(link)
    data = r.json()
    filtered_data = None

    try:
        if (isinstance(data, list)):
            for d in data:
                if d['queueType'] ==  "RANKED_SOLO_5x5":
                    filtered_data = d
            if not filtered_data:
                leaderboard["user"][i][2] = 0
                leaderboard["user"][i][3] = "1"
                leaderboard["user"][i][4] = "0"
                return
        leaderboard["user"][i][1] = filtered_data["summonerName"]
        leaderboard["user"][i][2] = get_api_tier(filtered_data["tier"])
        leaderboard["user"][i][3] = get_api_rank(filtered_data["rank"])
        leaderboard["user"][i][4] = filtered_data["leaguePoints"]
    except:
        print(f"error on refreshing {leaderboard['user'][i][1]}")
        return


async def refresh_leaderboard():
    for i in range(len(leaderboard["user"])):
        if ((i + 1) % 10 == 0):
            await asyncio.sleep(1)
        get_player_stats(leaderboard["user"][i][5], i)
    Save.leaderboard()
    print("stats refreshed")


def sort_leaderboard():
    i = 0

    while (i < len(leaderboard["user"]) - 1):
        if (leaderboard["user"][i][2] < leaderboard["user"][i + 1][2] or
                (leaderboard["user"][i][2] == leaderboard["user"][i + 1][2] and
                leaderboard["user"][i][3] > leaderboard["user"][i + 1][3]) or
                    (leaderboard["user"][i][2] == leaderboard["user"][i + 1][2] and
                    leaderboard["user"][i][3] == leaderboard["user"][i + 1][3] and
                    leaderboard["user"][i][4] < leaderboard["user"][i + 1][4])):
            tmp = leaderboard["user"][i]
            leaderboard["user"][i] = leaderboard["user"][i + 1]
            leaderboard["user"][i + 1] = tmp
            i = 0
        else:
            i += 1
    Save.leaderboard()


def get_ranking(i):
    if (i == 1):
        return ":first_place:"
    if (i == 2):
        return ":second_place:"
    if (i == 3):
        return ":third_place:"
    return " {}. ".format(i)



async def print_leaderboard():
    msg = [[]]
    msg_len = 0
    msg_nbr = 0
    user_len = len(leaderboard["user"])
    i = 0

    await refresh_leaderboard()
    sort_leaderboard()
    for user in leaderboard["user"]:
        if user[2] == 0:
            continue
        else:
            new_line =  (f'{get_ranking(i + 1)} '
                        f'{user[0]}, '
                        f'{user[1]} est '
                        f'{rank_division[user[2]]}'
                        f'{(" " + str(user[3])) if user[2] < 7 else ""}, '
                        f'{user[4]} LP')
        i += 1
        msg_len += len(new_line)
        if msg_len > 1850:
            msg.append([])
            msg_nbr += 1
            msg_len = 0
        msg[msg_nbr].append(new_line)
    channel = await bot.fetch_channel(config["channel"])
    i = 0
    for chan_id in config["msgs"]:
        to_edit = await channel.fetch_message(chan_id)
        if i < len(msg):
            await to_edit.edit(content="\n".join(msg[i]))
        else:
            await to_edit.edit(content="ㅤ")
        i += 1
    if i < len(msg):
        new_msg = await channel.send("\n".join(msg[i]))
        config["msgs"].append(new_msg.id)
    print("leaderboard refreshed")
    await refresh_roles()
    Save.config()


async def set_interval(sec = 300, fct = print_leaderboard):
    while True:
        try:
            await fct()
        except:
            traceback.print_exc()
        await asyncio.sleep(sec)


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


@bot.event
async def on_reaction_add(reaction, user):
    if reaction.message.id != coaching["message"] or user.bot:
        return
    coaching["participants"].append(user.mention)
    Save.coaching()


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


@bot.command(name="hello")
async def hello(ctx):
    if (ctx.message.content.startswith(config["prefix"] + 'hello')):
        msg = f'Hello {ctx.message.author.mention}'
        await ctx.message.channel.send(msg)


async def set_auto():
    loop = asyncio.get_event_loop()
    loop.create_task(set_interval())


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


async def refresh_roles():
    roles = []

    guild = bot.get_guild(832250335631376455)
    for role_id in roles_id:
        roles.append(guild.get_role(role_id))
    for user in leaderboard["user"]:
        is_set = False
        tmp = [int(s) for s in user[0] if s.isdigit()]
        res = ''.join(map(str, tmp))
        try:
            actual_user = await guild.fetch_member(res)
        except:
            print(res)
            continue
        user_roles = actual_user.roles

        for role in roles:
            if role in user_roles:
                is_set = True
                if role != roles[user[2]]:
                    await actual_user.remove_roles(role)
                    continue
                if role == roles[user[2]]:
                    continue
                await actual_user.add_roles(roles[user[2]])
        if not is_set:
            await actual_user.add_roles(roles[user[2]])
        await del_met_ton_opgg_role(guild, actual_user)
    print("roles refreshed")


@bot.command()
async def refresh(ctx):
    check_permission(ctx.message.author)
    await ctx.message.add_reaction("<a:loading:959954330889371709>")
    await print_leaderboard()
    await ctx.message.clear_reactions()
    await ctx.message.add_reaction("✅")


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


@bot.command(name="help")
async def help(ctx):
    embed = discord.Embed(
        colour=discord.Colour.purple()
    )

    embed.set_author(name="Help\n")
    embed.add_field(name=f"{config['prefix']}count_members", value="Send the count of members is this server", inline=False)
    embed.add_field(name=f"{config['prefix']}register *summoner_id*", value="Register/change your League ID on the leaderboard", inline=False)
    embed.add_field(name=f"{config['prefix']}unregister", value="Delete your League ID on the leaderboard", inline=False)
    embed.add_field(name=f"{config['prefix']}hello", value="The bot say hello to you", inline=False)
    embed.add_field(name=f"{config['prefix']}add_player @tag *summoner_id*", value="Register/change a League ID on the leaderboard (admin permission needed)", inline=False)
    embed.add_field(name=f"{config['prefix']}del_player @tag/rank", value="Delete a League ID on the leaderboard (admin permission needed)", inline=False)
    embed.add_field(name=f"{config['prefix']}setchannel *channel_tag*", value="Select the leaderboard channel (admin permission needed)", inline=False)
    embed.add_field(name=f"{config['prefix']}refresh", value="Refresh the leaderboard (admin permission needed)", inline=False)
    embed.add_field(name=f"{config['prefix']}help", value="Display this message", inline=False)

    await ctx.message.reply("Look your DM")
    await ctx.message.author.send(embed=embed)

async def del_met_ton_opgg_role(guild, user):
    role = guild.get_role(864767725339672586)
    if role in user.roles:
        await user.remove_roles(role)

async def addPlayerOpgg(message):
    if message.channel.id not in (832306284593152050, 854497039161229355):
        return
    tag = message.author.mention
    tmp = message.content.split()
    if len(tmp) == 2 and tmp[1].startswith("<@"):
        tag = tmp[1]
    player_exist = check_player_exist(tag)
    opgg = tmp[0].split("/")
    opgg = opgg[-1].split("=")
    user = urllib.parse.unquote(opgg[-1])

    if (not await check_name(user)):
        return
    if (player_exist == -1):
        leaderboard["user"].append([tag, user, None, None, None, leaderboard["tmp_id"]])
    else:
        leaderboard["user"][player_exist] = [tag, user, None, None, None, leaderboard["tmp_id"]]
    leaderboard["tmp_id"] = None
    Save.leaderboard()

def check_link(message):
    if not validators.url(message.content.split()[0]):
        return False
    if message.content.startswith("https://euw.op.gg/summoners/euw/"):
        return True
    if message.content.startswith("https://euw.op.gg/summoner/userName="):
        message.content = message.content[len("https://euw.op.gg/summoner/userName="):]
        return True
    if message.content.startswith("https://www.leagueofgraphs.com/fr/summoner/euw/"):
        return True
    return False

@bot.event
async def on_message(message):
    if message.channel.id in (832306284593152050, 854497039161229355) and not message.author.bot\
        and check_link(message):
        await addPlayerOpgg(message)
    else:
        await bot.process_commands(message)


@bot.event
async def on_member_remove(member):
    tag = member.mention
    pos = check_player_exist(tag)
    if (pos == -1):
        return
    print(leaderboard["user"][pos])
    del(leaderboard["user"][pos])
    print(leaderboard["user"][pos])
    Save.leaderboard()


@bot.event
async def on_ready():
    print('bot is ready !')
    await set_auto()


bot.run(config["token"])