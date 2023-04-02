import discord
from discord.ext import commands
from discord import app_commands
from discord.ext.commands import MissingRequiredArgument
import random
from random import randint
from discord import FFmpegPCMAudio
import asyncio
import requests
import json
import aiosqlite
import wavelink
import sans
from sans.api import Api, Dumps
from sans.utils import pretty_string
import datetime
import aiohttp
from typing import Union
from PIL import Image
from io import BytesIO
import urllib.request
from math import factorial

class ShopView(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=120)
        self.bot = bot
        
    @discord.ui.button(
        label="bagel", style=discord.ButtonStyle.blurple, custom_id="bagel"
    )
    async def bagel(self, interaction: discord.Interaction, button: discord.ui.Button):
        async with self.bot.db.cursor() as cursor:
            await cursor.execute("SELECT bagel from inv WHERE user = ?", (interaction.user.id,))
            item = await cursor.fetchone()
            if item is None:
                await cursor.execute("INSERT INTO inv VALUES (?, ?, ?, ?)", (1, 0, 0, interaction.user.id,))
            else:
                await cursor.execute("UPDATE inv SET bagel = ? WHERE user = ?", (item[0] + 1, interaction.user.id,))
        await self.bot.db.commit()
        await interaction.response.send_message("Bagel was bought!")
        
    @discord.ui.button(label="burntrosemary", style=discord.ButtonStyle.success, custom_id="burntrosemary")
    async def burntrosemary(self, interaction: discord.Interaction, button: discord.ui.Button):
        async with self.bot.db.cursor() as cursor:
            await cursor.execute("SELECT burntrosemary from inv WHERE user = ?", (interaction.user.id,))
            item = await cursor.fetchone()
            if item is None:
                await cursor.execute("INSERT INTO inv VALUES (?, ?, ?, ?)", (1, 0, 0, interaction.user.id,))
            else:
                await cursor.execute("UPDATE inv SET burntrosemary = ? WHERE user = ?", (item[0] + 1, interaction.user.id,))
        await self.bot.db.commit()
        await interaction.response.send_message("Burnt Rosemary was bought!")
        
    @discord.ui.button(
        label="governmentid", style=discord.ButtonStyle.danger, custom_id="governmentid"
    )
    async def governmentid(self, interaction: discord.Interaction, button: discord.ui.Button):
        async with self.bot.db.cursor() as cursor:
            await cursor.execute("SELECT governmentid from inv WHERE user = ?", (interaction.user.id,))
            item = await cursor.fetchone()
            if item is None:
                await cursor.execute("INSERT INTO inv VALUES (?, ?, ?, ?)", (1, 0, 0, interaction.user.id,))
            else:
                await cursor.execute("UPDATE inv SET governmentid = ? WHERE user = ?", (item[0] + 1, interaction.user.id,))
        await self.bot.db.commit()
        await interaction.response.send_message("GovernmentID was bought!")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)
PFuture = ["It is certain", "It is decidedly so", "Without a doubt", "Yes definitely", "You may rely on it", "As I see it, yes", "Most likely", "Outlook good", "Yes", "Signs point to yes", "**E!**", "Reply hazy, try again", "Ask again later", "Better not tell you now", "Cannot predict now", "Concentrate and ask again", "Don’t count on it", "My reply is no", "My sources say no", "Outlook not so good", "Very doubtful"]
ROptions = ["If you were spice, you'd be flour", "There's no one in this world like you. Or at least I hope so", "I'd like to roast you, but it looks like your genetics already did", "I didn't hear you. I'm busy ignoring an annoying person", "You should photoshop your life with better decisions.", "You look like a before picture.", "I'd like to roast you, but i'm too busy judging your choices", "The only way you could get laid is if you crawled up a chicken's ass and waited.", "Your face is so oily that I'm suprised America hasn't invaded yet", "You're not good looking enough to be a model, but you're not smart enough to be anything else", "Did you forget to wipe or is that your natural scent?", "Sorry. I'm on the toilet and I can only deal with one shit at a time", "It's a parent's job to raise their children right. So looking at you, it's no wonder your dad quit after just one day.", "You might just be why the middle finger was invented in the first place", "You do realise we are just tolerating you, right?", "If I had a dollar every time you shut up, I would give it back as a thank you", "It's impossible to underestimate you", "You're the reason gene pools need lifeguards", "You're like the gray sprinkle on a rainbow cupcake", "Have you ever tried not being an idiot", "You're the human version of athlete's foot: annoying and hard to get rid of", "You were so happy about getting negitive for covid... we didn't have the heart to tell you it was actually an IQ test", "We were going to roast you, but burning trash is apparently an environmental hazard", "Everyone has a purpose in life, and your's is to become an organ donor", "You can be anything you want, except good looking", "Don't feel bad, don't feel blue, Frankenstein was ugly too", "I'm the type of person to laugh at mistakes, so sorry if I laughed at your face"]
Robux12 = ["kind", "generous", "compassionate", "gentle", "caring", "noble", "loving", "benevolent", "gracious", "sincere", "beautiful"]
Robux13 = ["soul", "spirit", "nature", "heart", "personality", "character", "essence", "attitude", "demeanor", "disposition"]


@bot.event
async def on_ready():
    game = discord.Game("Outside")
    await bot.change_presence(status=discord.Status.online, activity=game)
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')
    bot.db = await aiosqlite.connect("bank.db")
    await asyncio.sleep(3)
    async with bot.db.cursor() as cursor:
        await cursor.execute("CREATE TABLE IF NOT EXISTS bank(wallet INTEGER, bank INTEGER, maxbank INTEGER, user INTEGER)")
        await cursor.execute("CREATE TABLE IF NOT EXISTS inv (bagel INTEGER, burntrosemary INTEGER, governmentid INTEGER, user INTEGER)")
        await cursor.execute("CREATE TABLE IF NOT EXISTS shop (name TEXT, id TEXT, desc TEXT, cost INTEGER)")
    await bot.db.commit()
    print("Database ready")
    bot.loop.create_task(node_connect())

#defining stuff
async def update_data(users, user):
    if not f"{user.id}" in users:
        users[f'{user.id}'] = {}
        users[f'{user.id}']["experience"] = 0
        users[f'{user.id}']["level"] = 1

async def add_experience(users, user, exp):
    users[f'{user.id}']["experience"] += exp

async def level_up(users, user, message):
    with open("levels.json", "r") as g:
        levels = json.load(g)
    experience = users[f'{user.id}']["experience"]
    lvl_start = users[f'{user.id}']["level"]
    lvl_end = int(experience ** (1/4))
    if lvl_start < lvl_end:
        await message.channel.send(f"{user.mention} has leveled up! **Level - {lvl_end}**")
        users[f'{user.id}']["level"] = lvl_end
    
async def create_balance(user):
    async with bot.db.cursor() as cursor:
        await cursor.execute("INSERT INTO bank VALUES(?, ?, ?, ?)", (0, 100, 500, user.id))
    await bot.db.commit()
    return

async def get_balance(user):
    async with bot.db.cursor() as cursor:
        await cursor.execute("SELECT wallet, bank, maxbank FROM bank WHERE user = ?", (user.id,))
        data = await cursor.fetchone()
        if data is None:
            await create_balance(user)
            return 0, 100, 500
        wallet, bank, maxbank = data[0], data[1], data[2]
        return wallet, bank, maxbank

async def update_wallet(user, amount: int):
    async with bot.db.cursor() as cursor:
        await cursor.execute("SELECT wallet FROM bank WHERE user = ?", (user.id,))
        data = await cursor.fetchone()
        if data is None:
            await create_balance(user)
            return 0
        await cursor.execute("UPDATE bank SET wallet = ? WHERE user = ?", (data[0] + amount, user.id))
    await bot.db.commit()

async def update_bank(user, amount):
    async with bot.db.cursor() as cursor:
        await cursor.execute("SELECT wallet, bank, maxbank FROM bank WHERE user = ?", (user.id,))
        data = await cursor.fetchone()
        if data is None:
            await create_balance(user)
            return 0
        capacity = int(data[2] - data[1])
        if amount > capacity:
            await update_wallet(user, amount)
            return 1
        await cursor.execute("UPDATE bank SET bank = ? WHERE user = ?", (data[1] + amount, user.id))
    await bot.db.commit()

async def node_connect():
	await bot.wait_until_ready()
	await wavelink.NodePool.create_node(bot=bot, host='lavalink2.botsuniversity.ml', port=443, password='mathiscool', https=True)
    
async def create_inv(user):
    async with bot.db.cursor() as cursor:
        await cursor.execute("INSERT INTO inv VALUES(?, ?, ?, ?)", (0, 0, 0, user.id))
    await bot.db.commit()
    return
    
async def get_inv(user):
    async with bot.db.cursor() as cursor:
        await cursor.execute("SELECT bagel, burntrosemary, governmentid FROM inv WHERE user = ?", (user.id,))
        data = await cursor.fetchone()
        if data is None:
            await create_inv(user)
            return 0, 0, 0
        bagel, burntrosemary, governmentid = data[0], data[1], data[2]
        return bagel, burntrosemary, governmentid

async def update_shop(name: str, id: str, desc: str, cost: int):
    async with bot.db.cursor() as cursor:
        await cursor.execute("INSERT INTO shop VALUES(?, ?, ?, ?)", (name, id, desc, cost))
    await bot.db.commit()
    return

async def update_maxbank(user, amount):
    async with bot.db.cursor() as cursor:
        await cursor.execute("SELECT maxbank FROM bank WHERE user = ?", (user.id,))
        data = await cursor.fetchone()
        if data is None:
            await create_balance(user)
            return 0
        await cursor.execute("UPDATE bank SET maxbank = ? WHERE user = ?", (data[0] + amount, user.id))
    await bot.db.commit()

snipe_message_content = None
snipe_message_author = None

async def get_definition(word):
    url = f"http://api.urbandictionary.com/v0/define?term={word}"
    response = requests.get(url)
    data = response.json()
    if not data['list']:
        return f"No definition found for {word}"
    else:
        return data['list'][0]['definition']

tictac = False
player1 = None
player2 = None
current_player = None
game_over = True
board = [
    [" ", " ", " "],
    [" ", " ", " "],
    [" ", " ", " "]
]

async def print_board(ctx):
    board_string = "-------------\n"
    for row in board:
        board_string += f"| {row[0]} | {row[1]} | {row[2]} |\n"
        board_string += "-------------\n"
    await ctx.send(f"```The board is:\n{board_string}```")

def make_move(player, x, y):
    if board[x][y] != " ":
        return False
    if player == player1:
        board[x][y] = "X"
    else:
        board[x][y] = "O"
    return True

def has_winner():
    for row in board:
        if row[0] == row[1] == row[2] and row[0] != " ":
            return row[0]
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != " ":
            return board[0][col]
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != " ":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != " ":
        return board[0][2]
    return None

#moderation commands
@bot.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    if ctx.author.guild_permissions.kick_members:
        await member.kick(reason=reason)
        await ctx.send(f"{member} has been kicked.")
    else:
        await ctx.send("You  do not have the required permissions to use this command.")

@bot.command()
async def timeout(ctx, member: discord.Member, duration: int, *, reason=None):
    if ctx.author.guild_permissions.manage_messages:
        timeout_role = discord.utils.get(ctx.guild.roles, name="Timeout")
        if not timeout_role:
            timeout_role = await ctx.guild.create_role(name="Timeout")
            for channel in ctx.guild.channels:
                await channel.set_permissions(timeout_role, send_messages=False)
        timeout_seconds = duration * 60
        await member.add_roles(timeout_role)
        await ctx.send(f"{member} has been timed out for {duration} minutes.")
        await asyncio.sleep(timeout_seconds)
        await member.remove_roles(timeout_role)
        await ctx.send(f"{member} has been un-timed out.")
    else:
        await ctx.send("Be a doctor or lawyer not a **failure**")

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=7):
    await ctx.channel.purge(limit=amount)

#general commands

@bot.command()
async def hitman(ctx):
    await ctx.reply("You hired a hitman...")

@bot.command()
async def say(ctx, *, sussyamogus):
    await ctx.send(sussyamogus)

@bot.command()
async def status(ctx):
    await ctx.send("Fronk is in fact currently online.")

@bot.command()
async def changelog(ctx):
    await ctx.send("Changelog for version 1.0 :")
    await ctx.send('> Added "I will send you to Jesus')
    await ctx.send("> Added zelda command")
    await ctx.send("> Added a status effect")

@bot.command()
async def rick(ctx):
    em = discord.Embed(title="Never gonna give you up")
    em.add_field(name="-", value="We're no strangers to love")
    em.add_field(name="-", value="You know the rules and so do I (do I)")
    em.add_field(name="-", value="A full commitment's what I'm thinking of")
    em.add_field(name="-", value="You wouldn't get this from any other guy")
    em.add_field(name="-", value="I just wanna tell you how I'm feeling")
    em.add_field(name="-", value="Gotta make you understand")
    em.add_field(name="-", value="Mever gonna give you up")
    em.add_field(name="-", value="Never gonna let you down")
    em.add_field(name="-", value="Never gonna run around and desert you")
    em.add_field(name="-", value="Never gonna make you cry")
    em.add_field(name="-", value="Never gonna say goodbye")
    em.add_field(name="-", value="Never gonna tell a lie and hurt you")
    await ctx.send(embed=em)

@bot.command()
async def hello(ctx):
    await ctx.reply("hello?")

@bot.command()
async def add(ctx, num1:int, num2:int):
    await ctx.reply(num1+num2)

@bot.command(name="8ball")
async def ball(ctx):
    def predict1():
        num_picked = randint(0, 20)
        option_picked = PFuture[num_picked]
        return option_picked
    await ctx.reply(predict1())

@bot.command(name="roast")
async def suscrystals(ctx, *, target1):
    await ctx.send("**Fronk bot roasted " + target1 + "**")
    def predict53():
        num_picked = randint(0, 26)
        option_picked = ROptions[num_picked]
        return option_picked
    await ctx.send(predict53())

@bot.command()
async def compliment(ctx, *, target2):
    option1 = Robux12[randint(0, 10)]
    option2 = Robux13[randint(0, 9)]
    await ctx.send(f"**Fronk bot complimented {target2}**")
    await ctx.send(f"You have a {option1} {option2}.")

@bot.command()
async def smite(ctx, target):
    await ctx.send(target + " has been smitten.")

@bot.command()
async def level(ctx, member: discord.Member = None):
    if not member:
        id = ctx.message.author.id
        with open("users.json", "r") as f:
            users = json.load(f)
        lvl = users[str(id)]["level"]
        await ctx.send(f"You are on **level {lvl}**")
    else:
        id = member.id
        with open("users.json", "r") as f:
            users = json.load(f)
        lvl = users[str(id)]["level"]
        await ctx.send(f"{member} is on **level {lvl}**")

@bot.command()
async def balance(ctx, member: discord.Member = None):
    if not member:
        member = ctx.author
    wallet, bank, maxbank = await get_balance(member)
    em = discord.Embed(title=f"{member.name}'s Balance")
    em.add_field(name="Wallet", value=wallet)
    em.add_field(name="Bank", value=f"{bank}/{maxbank}")
    await ctx.send(embed=em)

@bot.command()
@commands.cooldown(1, 30, commands.BucketType.user)
async def pray(ctx):
    chances = random.randint(1, 3)
    if chances == 1:
        return await ctx.send("Fronk withheld his funds.")
    amount = random.randint(1, 321)
    res = await update_wallet(ctx.author, amount)
    if res == 0:
        return await ctx.send("No account was found so I created one for you. Please run this command again.")
    await ctx.send(f"Fronk blessed you with {amount} coins")

@bot.command()
@commands.cooldown(1, 86400, commands.BucketType.user)
async def lotto(ctx):
    chances = random.randint(1, 17)
    if chances != 7:
        return await ctx.send("You did not win the lottery. :(")
    amount = random.randint(345, 2650)
    res = await update_wallet(ctx.author, amount)
    if res == 0:
        return await ctx.send("No account was found so I created one for you. Please run this command again.")
    await ctx.send(f"Fronk blessed you with {amount} coins and gave you some flowers for winning the lottery!")

@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def withdraw(ctx, amount):
    wallet, bank, maxbank = await get_balance(ctx.author)
    try:
        amount = int(amount)
    except ValueError:
        pass
    if type(amount) == str:
        if amount.lower() == "max" or amount.lower() == "all":
            amount = int(bank)
    else:
        amount = int(amount)
    bank_res = await update_bank(ctx.author, -amount)
    wallet_res = await update_wallet(ctx.author, amount)
    if bank_res == 0 or wallet_res == 0:
        return await ctx.send("You didn't have an account so I created one for you. Please re-try this command.")
    wallet, bank, maxbank = await get_balance(ctx.author)
    em = discord.Embed(title=f"{amount} coins have been withdrawn")
    em.add_field(name="Updated Wallet", value=wallet)
    em.add_field(name="Updated Bank", value=f"{bank}/{maxbank}")
    await ctx.send(embed=em)
    
@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def deposit(ctx, amount):
    wallet, bank, maxbank = await get_balance(ctx.author)
    try:
        amount = int(amount)
    except ValueError:
        pass
    if type(amount) == str:
        if amount.lower() == "max" or amount.lower() == "all":
            amount = int(wallet)
    else:
        amount = int(amount)
    bank_res = await update_bank(ctx.author, amount)
    wallet_res = await update_wallet(ctx.author, -amount)
    if bank_res == 0 or wallet_res == 0:
        return await ctx.send("You didn't have an account so I created one for you. Please re-try this command.")
    elif bank_res == 1:
        return await ctx.send("You don't have enough storage in your bank :(")
    wallet, bank, maxbank = await get_balance(ctx.author)
    em = discord.Embed(title=f"{amount} coins have been deposited")
    em.add_field(name="Updated Wallet", value=wallet)
    em.add_field(name="Updated Bank", value=f"{bank}/{maxbank}")
    await ctx.send(embed=em)

@bot.command()
async def nstats(ctx, *, nname):
    Api.agent = "<Put the name of your nation as a string here>"
    request = Api(
        "fullname population flag census category founded",
        nation=nname,
        mode="score",
        scale="65 66",
    )
    root = await request
    pretty = pretty_string(root)
    await ctx.send(pretty)

@bot.command()
@commands.is_owner()
async def add_items(ctx, name: str, id: str, desc: str, cost: int):
    await update_shop(name, id, desc, cost)
    await ctx.send("Item added!", delete_after=13)

@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def shop(ctx: commands.Context):
    em = discord.Embed(title="Fronk Shop")
    async with bot.db.cursor() as cursor:
        await cursor.execute("SELECT name, desc, cost FROM shop")
        shop = await cursor.fetchall()
        for item in shop:
            em.add_field(name=item[0], value=f"{item[1]} | Cost: {item[2]}", inline=False)
    await ctx.send(embed=em, view=ShopView(bot))

@bot.command()
async def snipe(ctx):
    if snipe_message_content == None:
        await ctx.send("There is nothing to snipe")
    else:
        em = discord.Embed(colour=(discord.Colour.random()), description=f"{snipe_message_content}")
        em.set_footer(text=f"Requested by {ctx.author}.")
        em.set_author(name=f"Sniped the message by {snipe_message_author}")
        await ctx.send(embed=em)

@bot.command()
async def jesus(ctx):
    await ctx.send(file=discord.File("jesus.png"))

@bot.command()
async def avatar(ctx, user: discord.Member = None):
    if user == None:
        user = ctx.author
    
    memberAvatar = user.avatar.url
    await ctx.send(memberAvatar)

@bot.command()
async def damage(ctx, user: discord.Member = None):
    if user == None:
        user = ctx.author
    avatar_url = user.avatar.url
    response = requests.get(avatar_url)
    avatar_image = Image.open(BytesIO(response.content))
    avatar_image = avatar_image.resize((55, 55))
    background_image = Image.open('damage.jpg')
    background_image.paste(avatar_image, (117, 17))
    background_image.save("combined.png")
    await ctx.send(file=discord.File('combined.png'))

@bot.command()
async def urban(ctx, word):
    definition = await get_definition(word)
    await ctx.reply(f"The definition of {word} is {definition}")

@bot.command()
async def f(ctx, numv: int):
    if numv < 0:
        return await ctx.send("Too small!")
    if numv > 777:
        return await ctx.send("Too large!")
    numf = factorial(numv)
    await ctx.send(f"The factorial of {numv} is {numf}.")

@bot.command()
async def whoasked(ctx):
    users = []
    messages = []
    async for message in ctx.channel.history(limit=15):
        messages.append(message)
    for message in messages:
        if "?" in message.content:
            users.append(message.author.mention)
    if users:
        await ctx.send(f"These users seem to have asked: {', '.join(users)}")
    else:
        await ctx.send("My complex algorithms sense that *No one asked*")

@bot.command()
async def tictactoe(ctx, opponent: discord.Member = None):
    global player1, player2, current_player, game_over
    for row in range(3):
        for col in range(3):
            board[row][col] = " "
    player1 = ctx.author
    if opponent:
        player2 = opponent
    else:
        await ctx.send("Please provide an opponent")
        return
    current_player = player1
    game_over = False
    await ctx.send(f"Welcome to Tic-Tac-Toe! {player1.mention} will go first. Do $move to make your move!")
    await print_board(ctx)

@bot.command()
async def move(ctx, x: int = None, y: int = None):
    global player1, player2, current_player, game_over
    await asyncio.sleep(0.2)
    if game_over:
        await ctx.send("The game is over. Start a new game with '$tictactoe")
        return
    if ctx.author != current_player:
        await ctx.reply("It is not your turn. It is currently {current_player.mention}'s turn.")
        return
    if x is None or y is None:
        await ctx.send("You must provide both 'x' and 'y' coordinates to make a move. For example: '$move 1 2'.")
        return
    if make_move(current_player, x, y):
        winner = has_winner()
        if winner:
            await ctx.send(f"{winner} wins!")
            await print_board(ctx)
            game_over = True
        else:
            current_player = player1 if current_player == player2 else player2
            await ctx.send(f"It is now {current_player.mention}'s turn.")
            await print_board(ctx)
            try:
                def check(m):
                    return m.author == current_player and m.content.startswith("$move") and m.created_at > ctx.message.created_at
                await asyncio.wait_for(bot.wait_for('message', check=check), timeout=60.0)
            except asyncio.TimeoutError:
                await ctx.send(f"{current_player.mention} took too long to make a move. The game is forfeit.")
                game_over = True
    else:
        await ctx.send("Invalid move. Try again.")


#music commands
@bot.command()
async def vleave(ctx):
    if not (ctx.voice_client):
        await ctx.send("I can't leave a place i'm not in")
        return
    await ctx.guild.voice_client.disconnect()

@bot.command(pass_context = True)
async def zelda(ctx):
    if (ctx.author.voice):
        await ctx.send("Playing *The legend of Zelda theme*")
        channel = ctx.message.author.voice.channel
        voice = await channel.connect()
        source = FFmpegPCMAudio("Zelda.mp3")
        player = voice.play(source)
    else:
        await ctx.send("You have to be in a voice channel to do this.")
    
@bot.command()
async def vjoin(ctx):
    voicetrue = ctx.author.voice
    if voicetrue is None:
        return await ctx.send("You need to be in a voice channel first")
    await ctx.author.voice.channel.connect()
    
@bot.command()
async def play(ctx: commands.Context, *, search: wavelink.YouTubeTrack):
    if not (ctx.author.voice):
        return await ctx.send("Join a voice channel first")
    elif not ctx.voice_client:
        vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
    else:
        vc: wavelink.Player = ctx.voice_client
    await vc.play(search)
    await ctx.send(f"*Now Playing {search.title}*")
    vc.ctx = ctx
        
@bot.command()
async def pause(ctx: commands.Context):
    if not ctx.voice_client:
        return await ctx.send("Ur not playing any music :bruh:")
    elif not getattr(ctx.author.voice, "channel", None):
        return await ctx.send("Join a voice channel first")
    else:
        vc: wavelink.Player = ctx.voice_client
    await vc.pause()
    await ctx.send("The music was paused")

@bot.command()
async def resume(ctx: commands.Context):
    if not ctx.voice_client:
        return await ctx.send("Ur not playing any music :bruh:")
    elif not getattr(ctx.author.voice, "channel", None):
        return await ctx.send("Join a voice channel first")
    else:
        vc: wavelink.Player = ctx.voice_client
    await vc.resume()
    await ctx.send("**Fronk killed the silence")

@bot.command()
async def stop(ctx: commands.Context):
    if not ctx.voice_client:
        return await ctx.send("Ur not playing any music :bruh:")
    elif not getattr(ctx.author.voice, "channel", None):
        return await ctx.send("Join a voice channel first")
    else:
        vc: wavelink.Player = ctx.voice_client
    await vc.stop()
    await ctx.send("Stopped the song")

@bot.command()
async def loop(ctx: commands.Context):
    if not ctx.voice_client:
        return await ctx.send("Ur not playing any music :bruh:")
    elif not getattr(ctx.author.voice, "channel", None):
        return await ctx.send("Join a voice channel first")
    else:
        vc: wavelink.Player = ctx.voice_client
    try:
        vc.loop ^= True
    except Exception:
        setattr(vc, "loop", False)
    if vc.loop:
        return await ctx.send("Loop is now enabled")
    else:
        return await ctx.send("Loop is now disabled")

@bot.command()
async def queue(ctx: commands.Context):
    if not ctx.voice_client:
        return await ctx.send("Ur not playing any music :bruh:")
    elif not getattr(ctx.author.voice, "channel", None):
        return await ctx.send("Join a voice channel first")
    else:
        vc: wavelink.Player = ctx.voice_client
    if vc.queue.is_empty:
        return await ctx.send("Queue is empty")
    em = discord.Embed(title="Song Queue")
    queue = vc.queue.copy()
    song_count = 0
    for song in queue:
        song_count += 1
        em.add_field(name=f"Songs: {queue}")
    return await ctx.send(embed=em)

@bot.command()
async def volume(ctx, volume: int):
    if not ctx.voice_client:
        return await ctx.send("Ur not playing any music :bruh:")
    elif not getattr(ctx.author.voice, "channel", None):
        return await ctx.send("Join a voice channel first")
    else:
        vc: wavelink.Player = ctx.voice_client
    
    if volume > 100:
        return await ctx.send("Thats too high")
    if volume < 0:
        return await ctx.send("That's way too low")
    await ctx.send(f"The volume was set to *{volume}%*")
    return await vc.set_volume(volume)

@bot.command()
async def songinfo(ctx):
    if not ctx.voice_client:
        return await ctx.send("Ur not playing any music :bruh:")
    elif not getattr(ctx.author.voice, "channel", None):
        return await ctx.send("Join a voice channel first")
    else:
        vc: wavelink.Player = ctx.voice_client
    
    if not vc.is_playing():
        return await ctx.send("Theres nothing playing at the moment")
    
    em = discord.Embed(title=f"Now playing: {vc.track.title}", description=f"Artist: {vc.track.author}")
    em.add_field(name="Duration", value=f"{str(datetime.timedelta(seconds=vc.track.length))}")
    em.add_field(name="Extra Info", value=f"Song URL: [click me]({str(vc.track.uri)})")
    return await ctx.send(embed=em)

@bot.command()
async def poll(ctx, *, question):
    options = question.split("|")
    question = options[0]
    del options[0]
    if len(options) <= 1:
        await ctx.send('You need more than one option to make a poll!')
        return
    if len(options) > 10:
        await ctx.send('You cannot make a poll for more than 10 things!')
        return
    if len(options) == 2 and options[0] == 'yes' and options[1] == 'no':
        reactions = ['👍', '👎']
    else:
        reactions = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']
    description = []
    for i, option in enumerate(options):
        description += '\n {} {}'.format(reactions[i], option)
    embed = discord.Embed(title=question, description=''.join(description))
    react_message = await ctx.send(embed=embed)
    for reaction in reactions[:len(options)]:
        await react_message.add_reaction(reaction)
    await ctx.message.delete()

#events
@bot.event
async def on_wavelink_node_ready(node: wavelink.Node):
	print(f"Node {node.identifier} is ready!")
    
@bot.event
async def on_member_join(member):
    with open("users.json", "r") as f:
        users = json.load(f)
    await update_data(users, member)
    with open("users.json", "w") as f:
        json.dump(users, f, indent=4)

@bot.event
async def on_message(message):
    if "uwu" in message.content.lower():
        response = f"<@516128226708553738> the user {message.author.mention} said the u word. Punish them"
        await message.channel.send(response)
    if message.author.bot == False:
        with open("users.json",  "r") as f:
            users = json.load(f)
        await update_data(users, message.author)
        await add_experience(users, message.author, 5)
        await level_up(users, message.author, message)
        with open("users.json", "w") as f:
            json.dump(users, f, indent=4)
    await bot.process_commands(message)

@bot.event
async def on_wavelink_track_end(player: wavelink.Player, track: wavelink.Track, reason):
    ctx = player.ctx
    vc: player = ctx.voice_client
    if not vc.queue.is_empty:
        next_song = vc.queue.get()
        await vc.play(next_song)
        await ctx.send(f"*Now playing: {next_song.title}*")

@bot.event
async def on_message_delete(message):
    global snipe_message_content
    global snipe_message_author
    snipe_message_content = message.content
    snipe_message_author = message.author.name

@bot.event
async def on_member_join(member):
    for channel in member.guild.channels:
        if channel.name == 'general':
            await channel.send(f"Welcome to the gulag, {member.mention}!")
            return
        if channel.name == 'general-communism':
            await channel.send(f"Welcome to the gulag, {member.mention}!")
            return

#errors
@pray.error
async def pray_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=f"Command is on Cooldown", description=f"Try again in {error.retry_after:.2f}s.")
        await ctx.send(embed=em)

@withdraw.error
async def withdraw_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=f"Command is on Cooldown", description=f"Try again in {error.retry_after:.2f}s.")
        await ctx.send(embed=em)

@deposit.error
async def deposit_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=f"Command is on Cooldown", description=f"Try again in {error.retry_after:.2f}s.")
        await ctx.send(embed=em)

@shop.error
async def shop_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=f"Command is on Cooldown", description=f"Try again in {error.retry_after:.2f}s.")
        await ctx.send(embed=em)

@lotto.error
async def lotto_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=f"Command is on Cooldown", description=f"Try again in {error.retry_after:.2f}s.")
        await ctx.send(embed=em)

@urban.error
async def urban_error(ctx, error):
    if isinstance(error, MissingRequiredArgument):
        await ctx.send("You are missing a required argument, please provide one.")

@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have the required permissions to do this")

#token
token = "<You put your token here>"
bot.run(token)

