# Standard imports
import json
import random
import traceback
import os
import re
import difflib
import uuid
import dotenv


# Async
import asyncio
import aiohttp


# Discord
import discord
import discord.interactions as interactions
from discord.ext import commands, tasks


# Misc
from mega import Mega
import datetime

# Accounts utilities
from utilities import (
    save_accounts,
    load_accounts,
    create_deck,
    draw_card,
    calculate_total,
    format_hand,
    handle_win,
    handle_loss,
    handle_tie,
    cleanup,
    find_folder_id,
    get_all_files,
    get_matched_urls,
    download_file_async,
    download_all_urls
)

# Bot Events
from bot_events import message_event, on_error

# Loading system variables like token...etc
dotenv.load_dotenv()

# Initiate Intents
intents = discord.Intents.all()
intents.typing = False

# setting up the prefix to use
bot = commands.Bot(command_prefix='?', intents=intents)

# Removing default command
bot.remove_command('help')
my_secret = os.environ['TOKEN']

mega = Mega()
m = mega.login(os.environ["MEGA_EMAIL"], os.environ["MEGA_PW"])

# 
@tasks.loop(minutes=30)
async def send_json():
    user = await bot.fetch_user(538773310704582666)
    if user:
        try:
            with open("accounts.json", "r") as file:
                ui_data = json.load(file)
                await user.send(
                    f"Data inside accounts.json:\n```json\n{json.dumps(ui_data, indent=4)}\n```"
                )
        except FileNotFoundError:
            await user.send("ui.json not found.")

# LOG in message in the terminal
@bot.event
async def on_ready():
    print('Logged in as', bot.user.name)
    send_json.start()

# Wait for the bot to start and then start the send_json function
send_json.before_loop(bot.wait_until_ready)


@bot.event
async def on_message(message):
    await message_event(bot, message)

start_time = datetime.datetime.now()

@bot.command()
async def uptime(ctx):
    """Displays the bot's uptime."""
    current_time = datetime.datetime.now()
    uptime = current_time - start_time
    days, seconds = divmod(uptime.total_seconds(), 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)

    uptime_str = f"**{int(days)}** days, **{int(hours)}** hours, **{int(minutes)}** minutes, **{int(seconds)}** seconds"

    embed = discord.Embed(title="Uptime",
                          description=uptime_str,
                          color=0x7289DA)
    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)

    await ctx.send(embed=embed)


@bot.command(name="help")
async def help_command(ctx, command_name: str = None):
    if command_name:
        if command_name == "open":
            embed = discord.Embed(title="Command: Open",
                                  description="",
                                  color=0x7289DA)
            embed.add_field(
                name="",
                value=
                "**Description:** Open a new account with a starting balance of 15 coins.",
                inline=False)
            embed.add_field(name="Permissions", value="❌", inline=True)
            embed.add_field(name="Aliases", value="❌", inline=True)
            embed.add_field(name="Usage", value="```?open```", inline=False)
            embed.set_author(name=ctx.author.name,
                             icon_url=ctx.author.avatar.url)
            embed.set_footer(
                text=
                "Type ?help <command> for more information on a specific command"
            )
            await ctx.send(embed=embed)
        elif command_name == "balance":
            embed = discord.Embed(title="Command: balance",
                                  description="",
                                  color=0x7289DA)
            embed.add_field(
                name="",
                value="**Description:** Check your account balance.",
                inline=False)
            embed.add_field(name="Permissions", value="❌", inline=True)
            embed.add_field(name="Aliases", value="`bal`", inline=True)
            embed.add_field(name="Usage", value="```?balance```", inline=False)
            embed.set_author(name=ctx.author.name,
                             icon_url=ctx.author.avatar.url)
            embed.set_footer(
                text=
                "Type ?help <command> for more information on a specific command"
            )
            await ctx.send(embed=embed)
        elif command_name == "leaderboard":
            embed = discord.Embed(title="Command: leaderboard",
                                  description="",
                                  color=0x7289DA)
            embed.add_field(
                name="",
                value="**Description:** View the leaderboard of top users.",
                inline=False)
            embed.add_field(name="Permissions", value="❌", inline=True)
            embed.add_field(name="Aliases", value="`lb`", inline=True)
            embed.add_field(name="Usage",
                            value="```?leaderboard```",
                            inline=False)
            embed.set_author(name=ctx.author.name,
                             icon_url=ctx.author.avatar.url)
            embed.set_footer(
                text=
                "Type ?help <command> for more information on a specific command"
            )
            await ctx.send(embed=embed)
        elif command_name == "cover":
            embed = discord.Embed(title="Command: cover",
                                  description="",
                                  color=0x7289DA)
            embed.add_field(
                name="",
                value=
                "**Description:** Sends cover arts for a specified song to the users DMs",
                inline=False)
            embed.add_field(name="Permissions", value="❌", inline=True)
            embed.add_field(name="Aliases", value="❌", inline=True)
            embed.add_field(name="Usage",
                            value="```?cover revive```",
                            inline=False)
            embed.set_author(name=ctx.author.name,
                             icon_url=ctx.author.avatar.url)
            embed.set_footer(
                text=
                "Type ?help <command> for more information on a specific command"
            )
            await ctx.send(embed=embed)
        elif command_name == "give":
            embed = discord.Embed(title="Command: give",
                                  description="",
                                  color=0x7289DA)
            embed.add_field(name="",
                            value="**Description:** Transfers users money.",
                            inline=False)
            embed.add_field(name="Permissions", value="❌", inline=True)
            embed.add_field(name="Aliases", value="`transfer`", inline=True)
            embed.add_field(name="Usage",
                            value="```?give chaosok 1000```",
                            inline=False)
            embed.set_author(name=ctx.author.name,
                             icon_url=ctx.author.avatar.url)
            embed.set_footer(
                text=
                "Type ?help <command> for more information on a specific command"
            )
            await ctx.send(embed=embed)
        elif command_name == "set":
            embed = discord.Embed(title="Command: set",
                                  description="",
                                  color=0x7289DA)
            embed.add_field(
                name="",
                value="**Description:** Sets a users account balance",
                inline=False)
            embed.add_field(name="Permissions",
                            value="`Bot owner only`",
                            inline=True)
            embed.add_field(name="Aliases", value="❌", inline=True)
            embed.add_field(name="Usage",
                            value="```?set chaosok 1000```",
                            inline=False)
            embed.set_author(name=ctx.author.name,
                             icon_url=ctx.author.avatar.url)
            embed.set_footer(
                text=
                "Type ?help <command> for more information on a specific command"
            )
            await ctx.send(embed=embed)
        elif command_name == "daily":
            embed = discord.Embed(title="Command: daily",
                                  description="",
                                  color=0x7289DA)
            embed.add_field(name="",
                            value="**Description:** Claims your daily coins.",
                            inline=False)
            embed.add_field(name="Permissions", value="❌", inline=True)
            embed.add_field(name="Aliases", value="❌", inline=True)
            embed.add_field(name="Usage", value="```?daily```", inline=False)
            embed.set_author(name=ctx.author.name,
                             icon_url=ctx.author.avatar.url)
            embed.set_footer(
                text=
                "Type ?help <command> for more information on a specific command"
            )
            await ctx.send(embed=embed)
        elif command_name == "blackjack":
            embed = discord.Embed(title="Command: blackjack",
                                  description="",
                                  color=0x7289DA)
            embed.add_field(
                name="",
                value="**Description:** Creates a game of blackjack.",
                inline=False)
            embed.add_field(name="Permissions", value="❌", inline=True)
            embed.add_field(name="Aliases", value="`bj`", inline=True)
            embed.add_field(name="Usage",
                            value="```?blackjack 1000```",
                            inline=False)
            embed.set_author(name=ctx.author.name,
                             icon_url=ctx.author.avatar.url)
            embed.set_footer(
                text=
                "Type ?help <command> for more information on a specific command"
            )
            await ctx.send(embed=embed)
        elif command_name == "uptime":
            embed = discord.Embed(title="Command: uptime",
                                  description="",
                                  color=0x7289DA)
            embed.add_field(name="",
                            value="**Description:** Displays bot uptime",
                            inline=False)
            embed.add_field(name="Permissions", value="❌", inline=True)
            embed.add_field(name="Aliases", value="❌", inline=True)
            embed.add_field(name="Usage", value="```?uptime```", inline=False)
            embed.set_author(name=ctx.author.name,
                             icon_url=ctx.author.avatar.url)
            embed.set_footer(
                text=
                "Type ?help <command> for more information on a specific command"
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send("That command does not exist.")
    else:
        embed = discord.Embed(
            title="Bot Commands",
            description="Here's a list of available commands:",
            color=0x7289DA)
        embed.add_field(
            name="`open`",
            value="Open a new account with a starting balance of 15 coins.",
            inline=False)
        embed.add_field(name="`balance`",
                        value="Check your account balance.",
                        inline=False)
        embed.add_field(name="`leaderboard`",
                        value="View the leaderboard of top users.",
                        inline=False)
        embed.add_field(name="`daily`",
                        value="Claim your daily coins.",
                        inline=False)
        embed.add_field(name="`blackjack`",
                        value="Creates a game of blackjack.",
                        inline=False)
        embed.add_field(name="`give`",
                        value="Transfers users money.",
                        inline=False)
        embed.add_field(name="`set`",
                        value="Sets a users account balance",
                        inline=False)
        embed.add_field(
            name="`cover`",
            value="Sends cover arts for a specified song to the users DMs",
            inline=False)
        embed.add_field(name="`uptime`",
                        value="Displays bot uptime",
                        inline=False)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
        embed.set_footer(
            text=
            "Type ?help <command> for more information on a specific command")

        await ctx.send(embed=embed)


@bot.command(name="open")
async def open_command(ctx):
    author_id = str(ctx.author.id)
    accounts = load_accounts()
    if author_id not in accounts:
        accounts[author_id] = {'balance': 15}
        save_accounts(accounts)
        embed = discord.Embed(title="", color=0xabe86a)
        embed.add_field(
            name="",
            value=
            f"{ctx.author.mention}: Account successfully opened with the starting balance of **15** coins.",
            inline=False)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="", color=0xe69f23)
        embed.add_field(
            name="",
            value=f"{ctx.author.mention}: You already have an account.",
            inline=False)
        await ctx.send(embed=embed)


@bot.command(name="balance", aliases=["bal"])
async def balance_command(ctx, user: commands.MemberConverter = None):
    if user is None:
        user = ctx.author

    author_id = str(user.id)
    accounts = load_accounts()

    if author_id in accounts:
        balance = accounts[author_id]['balance']
        formatted_balance = "{:,.0f}".format(balance)
        all_balances = sorted(
            [account['balance'] for account in accounts.values()],
            reverse=True)
        user_rank = all_balances.index(
            balance) + 1 if balance in all_balances else "N/A"

        embed = discord.Embed(title="", color=0xabe86a)
        embed.set_author(name=user.name, icon_url=user.avatar.url)
        embed.add_field(
            name="",
            value=
            f"<:money:1221139949055639695> {user.mention}'s balance is **{formatted_balance}**",
            inline=False)
        embed.set_footer(text=f"Global Rank: #{user_rank}")

        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            title="",
            description=
            "You don't have an account. Use the ?open command to create one.",
            color=0xe69f23)
        await ctx.send(embed=embed)


@bot.command(name="leaderboard", aliases=["lb"])
async def leaderboard_command(ctx):
    accounts = load_accounts()

    top_accounts = sorted(accounts.items(),
                          key=lambda x: x[1]['balance'],
                          reverse=True)[:10]

    leaderboard_text = ""
    for idx, (user_id, data) in enumerate(top_accounts, start=1):
        user = await bot.fetch_user(int(user_id))
        balance_with_commas = "{:,.0f}".format(data['balance'])
        leaderboard_text += f"#{idx} **{user.name}#{user.discriminator}** with **{balance_with_commas}**\n"

    author_id = str(ctx.author.id)
    all_balances = sorted(
        [account['balance'] for account in accounts.values()], reverse=True)
    user_rank = all_balances.index(
        accounts[author_id]['balance']) + 1 if author_id in accounts else "N/A"

    embed = discord.Embed(title="", color=0x7289DA)
    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
    embed.description = leaderboard_text
    embed.set_footer(text=f"Your current ranking: #{user_rank}")

    await ctx.send(embed=embed)


@bot.command(pass_context=True)
async def daily(ctx):
    author_id = str(ctx.author.id)
    accounts = load_accounts()

    if author_id not in accounts:
        accounts[author_id] = {'balance': 115}
        save_accounts(accounts)

        formatted_balance = '{:,.0f}'.format(accounts[author_id]['balance'])
        embed = discord.Embed(
            title="",
            description=
            f"You've claimed **115.00** coins. You now have **{formatted_balance}** coins.",
            color=0xabe86a)
        await ctx.send(embed=embed)
    else:
        accounts[author_id]['balance'] += 100
        save_accounts(accounts)

        formatted_balance = '{:,.0f}'.format(accounts[author_id]['balance'])
        embed = discord.Embed(
            title="",
            description=
            f"You've claimed **100.00** coins. You now have **{formatted_balance}** coins.",
            color=0xabe86a)
        await ctx.send(embed=embed)


@bot.event
async def on_command_error(ctx, error):
    await on_error(ctx, error)

class BlackjackView(discord.ui.View):

    def __init__(self, bot, ctx, bet, dealer_hand, dealer_total, player_hand,
                 player_total, message, deck):
        super().__init__()
        self.ctx = ctx
        self.bot = bot
        self.bet = bet
        self.dealer_hand = dealer_hand
        self.dealer_total = dealer_total
        self.player_hand = player_hand
        self.player_total = player_total
        self.message = message
        self.deck = deck
        self.author_id = ctx.author.id
        self.last_stand_time = None
        self.last_double_down_time = None

    async def interaction_check(self, interaction):
        if interaction.user.id != self.author_id:
            embed = discord.Embed(
                title="",
                description="This blackjack game isn't yours.",
                color=discord.Color.red())
            await interaction.response.send_message(embed=embed,
                                                    ephemeral=True)
            return False
        return True

    @discord.ui.button(label="Hit", style=discord.ButtonStyle.green)
    async def hit_button_callback(self, interaction, button):
        await interaction.response.defer()
        self.player_hand.append(draw_card(self.deck))
        self.player_total = calculate_total(self.player_hand)
        embed = self.message.embeds[0]
        embed.set_field_at(0,
                           name=f"Your Cards: {self.player_total}",
                           value=format_hand(self.player_hand),
                           inline=False)
        await self.message.edit(embed=embed)
        if self.player_total > 21:
            await handle_loss(self.bot, self.ctx, self.bet, self.dealer_hand,
                              self.dealer_total, self.player_hand,
                              self.player_total, self.message, self)
            self.stop()

    @discord.ui.button(label="Stand", style=discord.ButtonStyle.red)
    async def stand_button_callback(self, interaction, button):
        if self.last_stand_time and (discord.utils.utcnow() -
                                     self.last_stand_time).total_seconds() < 3:
            await interaction.response.send_message(
                "Please wait a bit before standing again.", ephemeral=True)
            return
        self.last_stand_time = discord.utils.utcnow()
        await interaction.response.defer()
        while self.dealer_total < 17:
            self.dealer_hand.append(draw_card(self.deck))
            self.dealer_total = calculate_total(self.dealer_hand)

        embed = self.message.embeds[0]
        embed.set_field_at(1,
                           name=f"Dealer's Cards: {self.dealer_total}",
                           value=format_hand(self.dealer_hand),
                           inline=False)
        await self.message.edit(embed=embed)
        if self.dealer_total >= 17:
            if not (self.player_total > 21) and (self.dealer_total > 21
                                                 or self.player_total
                                                 > self.dealer_total):
                await handle_win(self.bot, self.ctx, self.bet,
                                 self.dealer_hand, self.dealer_total,
                                 self.player_hand, self.player_total,
                                 self.message, self)
            elif not (self.dealer_total > 21) and (self.player_total > 21
                                                   or self.player_total
                                                   < self.dealer_total):
                await handle_loss(self.bot, self.ctx, self.bet,
                                  self.dealer_hand, self.dealer_total,
                                  self.player_hand, self.player_total,
                                  self.message, self)
            else:
                await handle_tie(self.bot, self.ctx, self.bet,
                                 self.dealer_hand, self.dealer_total,
                                 self.player_hand, self.player_total,
                                 self.message, self)
            for item in self.children:
                item.disabled = True
            await self.message.edit(view=self)
            self.stop()

    @discord.ui.button(label="Double Down", style=discord.ButtonStyle.blurple)
    async def double_down_button_callback(self, interaction, button):
        if self.last_double_down_time and (
                discord.utils.utcnow() -
                self.last_double_down_time).total_seconds() < 3:
            await interaction.response.send_message(
                "Please wait a bit before doubling down again.",
                ephemeral=True)
            return
        self.last_double_down_time = discord.utils.utcnow()
        await interaction.response.defer()
        accounts = load_accounts()
        author_id = str(self.ctx.author.id)
        if author_id in accounts:
            if accounts[author_id]['balance'] < self.bet:
                embed = discord.Embed(
                    description=
                    "You don't have enough balance to place a double down.",
                    color=discord.Color.red())
                await interaction.followup.send(embed=embed, ephemeral=True)
                return
            accounts[author_id]['balance'] -= self.bet
            save_accounts(accounts)

        # Doubling the bet
        self.bet *= 2

        # Drawing one card for the player
        self.player_hand.append(draw_card(self.deck))
        self.player_total = calculate_total(self.player_hand)

        # Drawing cards for the dealer until reaching at least 17
        while self.dealer_total < 17:
            self.dealer_hand.append(draw_card(self.deck))
            self.dealer_total = calculate_total(self.dealer_hand)

        embed = self.message.embeds[0]
        embed.set_field_at(0,
                           name=f"Your Cards: {self.player_total}",
                           value=format_hand(self.player_hand),
                           inline=False)
        embed.set_field_at(1,
                           name=f"Dealer's Cards: {self.dealer_total}",
                           value=format_hand(self.dealer_hand),
                           inline=False)

        # Check the outcome after doubling down
        if (self.player_total > 21
                and self.dealer_total > 21) or (self.player_total
                                                == self.dealer_total):
            await handle_tie(self.bot, self.ctx, self.bet, self.dealer_hand,
                             self.dealer_total, self.player_hand,
                             self.player_total, self.message, self)
        elif self.player_total <= 21 and (self.dealer_total > 21
                                          or self.player_total
                                          > self.dealer_total):
            await handle_win(self.bot, self.ctx, self.bet, self.dealer_hand,
                             self.dealer_total, self.player_hand,
                             self.player_total, self.message, self)
        else:
            await handle_loss(self.bot, self.ctx, self.bet, self.dealer_hand,
                              self.dealer_total, self.player_hand,
                              self.player_total, self.message, self)

        # Disable further interactions and update the message
        for item in self.children:
            item.disabled = True
        await self.message.edit(view=self)
        self.stop()

        #  if self.player_total > 21:

    #     await handle_loss(self.bot, self.ctx, self.bet, self.dealer_hand, self.dealer_total, self.player_hand, self.player_total, self.message, self)
    # elif self.dealer_total > 21 or self.player_total > self.dealer_total:
    #     await handle_win(self.bot, self.ctx, self.bet, self.dealer_hand, self.dealer_total, self.player_hand, self.player_total, self.message, self)
    # else:
    #     await handle_loss(self.bot, self.ctx, self.bet, self.dealer_hand, self.dealer_total, self.player_hand, self.player_total, self.message, self)


@bot.command(name="blackjack", aliases=["bj"])
async def blackjack(ctx, bet: str):
    try:
        deck = create_deck()

        author_id = str(ctx.author.id)
        player_hand = [draw_card(deck), draw_card(deck)]
        dealer_hand = [draw_card(deck), draw_card(deck)]
        player_total = calculate_total(player_hand)
        dealer_total = calculate_total(dealer_hand[1:])

        try:
            with open('accounts.json', 'r') as f:
                accounts = json.load(f)
        except FileNotFoundError:
            accounts = {}

        if author_id not in accounts:
            embed = discord.Embed(
                description=
                "You don't have an account. Use the ?open command to create one.",
                color=0xe69f23)
            await ctx.send(embed=embed)
            return

        try:
            if bet.lower() == 'all':
                bet_amount = accounts[author_id]['balance']
            elif bet.lower() == 'half':
                bet_amount = accounts[author_id]['balance'] // 2
            elif 'e' in bet.lower():
                bet_amount = float(bet)
            else:
                bet_amount = int(bet)
        except ValueError:
            embed = discord.Embed(description="Invalid bet amount.",
                                  color=discord.Color.red())
            await ctx.send(embed=embed)
            return

        if bet_amount <= 0:
            embed = discord.Embed(
                description=
                "Invalid bet amount. Please provide a bet greater than zero.",
                color=discord.Color.red())
            await ctx.send(embed=embed)
            return

        if accounts[author_id]['balance'] < bet_amount:
            embed = discord.Embed(
                description="You don't have enough balance to place this bet.",
                color=discord.Color.red())
            await ctx.send(embed=embed)
            return

        embed = discord.Embed(title="", color=0x232428)
        embed.add_field(name=f"Your Cards: {player_total}",
                        value=format_hand(player_hand),
                        inline=False)
        embed.add_field(
            name=f"Dealer's Cards: {dealer_total}",
            value=
            f"{format_hand(dealer_hand[1:])} <:uncovered:1229222279905415189>",
            inline=False)
        embed.add_field(name="Result", value="In progress", inline=False)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
        embed.set_thumbnail(url="https://i.imgur.com/JBPnaZz.png")

        message = await ctx.send(embed=embed)
        view = BlackjackView(bot, ctx, bet_amount, dealer_hand, dealer_total,
                             player_hand, player_total, message, deck)
        await message.edit(view=view)

        try:
            accounts[author_id]['balance'] -= bet_amount
            with open('accounts.json', 'w') as f:
                json.dump(accounts, f)
        except KeyError:
            await ctx.send("You don't have enough balance to place this bet.")
            return
        except Exception as e:
            await ctx.send(f"An error occurred: {e}")
            return
    except Exception as e:
        traceback_info = traceback.format_exc(
        )  # Gets the traceback information
        await ctx.send(f"An error occurred: {str(e)}\n```{traceback_info}```"
                       )  # Sends the error message with traceback

@bot.command(name="give", aliases=["transfer"])
async def give_command(ctx, recipient: discord.Member, amount: float):
    sender_id = str(ctx.author.id)
    recipient_username = recipient.name

    if amount <= 0:
        embed = discord.Embed(title="",
                              description="Amount must be above **0.01**",
                              color=0xe69f23)
        await ctx.send(embed=embed)
        return

    accounts = load_accounts()

    if sender_id not in accounts:
        embed = discord.Embed(
            title="",
            description=
            "You don't have an account. Use the ?open command to create one.",
            color=0xe69f23)
        await ctx.send(embed=embed)
        return

    if accounts[sender_id]['balance'] < amount:
        formatted_balance = "{:,.2f}".format(accounts[sender_id]['balance'])
        embed = discord.Embed(
            title="",
            description=
            f"{ctx.author.mention}: You do not have **{amount:,.2f}** coins to transfer!",
            color=0xe69f23)
        await ctx.send(embed=embed)
        return

    accounts[sender_id]['balance'] -= amount
    recipient_id = str(recipient.id)
    accounts[recipient_id] = accounts.get(recipient_id, {'balance': 0})
    accounts[recipient_id]['balance'] += amount

    save_accounts(accounts)

    formatted_amount = "{:,.2f}".format(amount)
    embed = discord.Embed(
        title="",
        description=
        f"{ctx.author.mention}: Transferred **{formatted_amount}** coins to **{recipient_username}**!",
        color=0xabe86a)
    await ctx.send(embed=embed)


@bot.command(name="test")
async def test_command(ctx):
    await ctx.send("hi bro")


@bot.command(name="set")
async def set_balance(ctx, target_user: discord.Member, amount: str):
    allowed_users = [538773310704582666, 511009465982779400]
    if ctx.author.id not in allowed_users:
        embed = discord.Embed(
            title="",
            description="You are not allowed to use this command.",
            color=discord.Color.red())
        await ctx.send(embed=embed)
        return

    accounts = load_accounts()

    target_user_id = str(target_user.id)
    if target_user_id not in accounts:
        embed = discord.Embed(title="",
                              description="This user doesn't have an account.",
                              color=discord.Color.red())
        await ctx.send(embed=embed)
        return

    if amount.startswith('+'):
        operation = 'add'
        amount = amount[1:]
    elif amount.startswith('-'):
        operation = 'remove'
        amount = amount[1:]
    else:
        operation = 'set'

    try:
        amount = float(amount)
    except ValueError:
        embed = discord.Embed(title="",
                              description="Please provide a valid number.",
                              color=discord.Color.red())
        await ctx.send(embed=embed)
        return

    if operation == 'add':
        accounts[target_user_id]['balance'] += amount
    elif operation == 'remove':
        accounts[target_user_id]['balance'] -= amount
    else:
        accounts[target_user_id]['balance'] = amount

    save_accounts(accounts)

    formatted_balance = "{:,.0f}".format(accounts[target_user_id]['balance'])

    if operation == 'add':
        operation_desc = "added"
    elif operation == 'remove':
        operation_desc = "removed"
    else:
        operation_desc = "set to"

    embed = discord.Embed(
        title="",
        description=
        f"Successfully set {target_user.mention}'s balance to **{formatted_balance}**",
        color=discord.Color.green())
    await ctx.send(embed=embed)


@bot.command(pass_context=True)
async def cover(ctx, *, song_name: str):
    user = ctx.author
    user_id = user.id

    embed = discord.Embed(
        title="",
        description=
        f"Working on your request for cover arts matching **{song_name}**.",
        color=0xabe86a)
    await user.send(embed=embed)
    try:
        if song_name:
            while True:
                if os.path.exists("all_data.json"):
                    print("all_data.json exists")
                    with open("all_data.json", "r") as f:
                        all_data = json.load(f)

                    if all_data:
                        simplified_file_name = song_name.lower().replace(
                            "_", " ")
                        urls = get_matched_urls(all_data, simplified_file_name)
                        urls = set(urls)
                        print(f"URLs: {urls}")
                        break
                else:
                    print("all_data.json not found. Getting all files...")
                    result = await get_all_files()
            paths_result = await download_all_urls(mega, urls, user_id)

            if len(paths_result) > 0:
                embed = discord.Embed(
                    title="",
                    description=
                    f"Found **{len(paths_result)}** cover arts. Uploading...",
                    color=0xabe86a)
                await ctx.author.send(embed=embed)
                for result in paths_result:
                    path = result["path"]
                    await ctx.author.send(file=discord.File(path))
            else:
                embed = discord.Embed(
                    title="",
                    description=
                    f"No cover arts found with the name **{song_name}**.",
                    color=0xe69f23)
                await user.send(embed=embed)
            # Clean up the user's directory
            cleanup_dir = f"./images/{user_id}"
            for file in os.listdir(cleanup_dir):
                os.remove(os.path.join(cleanup_dir, file))
            os.rmdir(cleanup_dir)
    except Exception as e:
        traceback_info = traceback.format_exc()
        await ctx.author.send(
            f"An error occurred: {str(e)}\n```{traceback_info}```")


@bot.command(pass_context=True)
async def pot(ctx):
    with open('lottery.txt', 'r+') as f:
        try:
            pot = int(f.readline())
        except ValueError:
            traceback_info = traceback.format_exc()
            embed = discord.Embed(title=f"An error occurred",
                                  color=discord.Color.red())
            await interactions.send_message(embed=embed)
            return

        if not pot:
            f.write("10000")
            pot = 10000

    fpot = "{:,.0f}".format(pot)
    embed = discord.Embed(
        title=f"",
        description=
        f"<:moneybag:1234932901125292032> The pot in the lottery is: **${fpot}**",
        color=discord.Color.green())
    await ctx.send(embed=embed)


class TicketSelectView(discord.ui.View):

    def __init__(self, bot, user, tickets):
        super().__init__(timeout=60)
        self.bot = bot
        self.user = user
        self.tickets = tickets
        # Creating the options for the select menu
        options = [
            discord.SelectOption(label=ticket['name'],
                                 description=f"Price: ${ticket['price']}",
                                 value=str(idx))
            for idx, ticket in enumerate(tickets, start=1)
        ]
        # Adding the select menu to the view
        self.add_item(
            TicketSelect(bot=bot, user=user, tickets=tickets, options=options))

    async def interaction_check(self, interaction):
        if interaction.user != self.user:
            await interaction.response.send_message("This is not for you!",
                                                    ephemeral=True)
            return False
        return True


class TicketSelect(discord.ui.Select):

    def __init__(self, bot, user, tickets, options: list):
        super().__init__(placeholder='Choose your ticket...',
                         min_values=1,
                         max_values=1,
                         options=options)
        self.bot = bot
        self.user = user
        self.tickets = tickets

    async def callback(self, interaction: discord.Interaction):
        selected_index = int(self.values[0]) - 1
        ticket = self.tickets[selected_index]
        if load_accounts()[str(self.user.id)]["balance"] < ticket['price']:
            await interaction.response.send_message(
                f"You do not have enough balance to buy this ticket. Please try a cheaper ticket or accumulate more balance.",
                ephemeral=True)

        else:
            accounts = load_accounts()
            with open('lottery.txt', 'r+') as f:
                try:
                    pot = int(f.readline())
                except ValueError:
                    traceback_info = traceback.format_exc()
                    embed = discord.Embed(title=f"An error occurred",
                                          color=discord.Color.red())
                    await interaction.response.send_message(embed=embed)
                    return

                if not pot:
                    f.write("10000")
                    pot = 10000
            if random.random() < ticket["chance"]:
                formatted_amount = "{:,.0f}".format(ticket['price'] + pot)
                embed = discord.Embed(
                    title="You won the lottery!",
                    description=f"Amount won: **${formatted_amount}**!",
                    color=discord.Color.green())
                await interaction.response.send_message(embed=embed)
                accounts[str(self.user.id)]["balance"] += ticket["price"] + pot
                save_accounts(accounts)
                with open('lottery.txt', 'w') as f:
                    try:
                        f.write(str(10000))
                    except Exception as e:
                        traceback_info = traceback.format_exc()
                        embed = discord.Embed(title=f"An error occurred",
                                              color=discord.Color.red())
                        await interaction.response.send_message(embed=embed)
            else:
                accounts[str(self.user.id)]["balance"] -= ticket["price"]
                save_accounts(accounts)
                formatted_amount = "{:,.0f}".format(ticket['price'])
                embed = discord.Embed(
                    title="You lost the lottery.",
                    description=f"Amount lost: **${formatted_amount}**",
                    color=discord.Color.red())
                await interaction.response.send_message(embed=embed)

                with open('lottery.txt', 'w') as f:
                    try:
                        f.write(str(pot + ticket["price"]))
                    except Exception as e:
                        traceback_info = traceback.format_exc()
                        embed = discord.Embed(title=f"An error occurred",
                                              color=discord.Color.red())
                        await interaction.response.send_message(embed=embed)


@bot.command(pass_context=True)
async def lottery(ctx):
    try:
        author = ctx.author
        tickets = [{
            "price": 5,
            "chance": 0.00001,
            "name": "Ticket 1"
        }, {
            "price": 500,
            "chance": 0.0001,
            "name": "Ticket 2"
        }, {
            "price": 50000,
            "chance": 0.001,
            "name": "Ticket 3"
        }, {
            "price": 5000000,
            "chance": 0.01,
            "name": "Ticket 4"
        }]

        try:
            with open('accounts.json', 'r') as f:
                accounts = json.load(f)
        except FileNotFoundError:
            accounts = {}

        if str(author.id) not in accounts:
            embed = discord.Embed(
                description=
                "You don't have an account. Use the ?open command to create one.",
                color=0xe69f23)
            await ctx.send(embed=embed)
            return

        embed = discord.Embed(title="Lottery Tickets",
                              description="Choose your ticket:",
                              color=0x7289DA)
        for idx, ticket in enumerate(tickets, start=1):
            formatted_chance = ticket["chance"] * 100
            if formatted_chance == 1.0:
                formatted_chance = int(formatted_chance)
            embed.add_field(
                name=f"{ticket['name']}",
                value=f"Price: ${ticket['price']}\nChance: {formatted_chance}%",
                inline=False)
        view = TicketSelectView(bot, author, tickets)
        await ctx.send(embed=embed, view=view)

    except Exception as e:
        traceback_info = traceback.format_exc()
        await ctx.send(f"An error occurred")


bot.run(my_secret)
