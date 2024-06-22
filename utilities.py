"""
    This file contains utility functions for the accounts app.
"""
import json
import random
import discord


def load_accounts():
    """Load the accounts from the accounts.json file and return them as a dictionary.
        If the file does not exist, return an empty dictionary.
    """
    try:
        with open('accounts.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_accounts(accounts):
    """
    Save the accounts to the accounts.json file.
    """
    with open('accounts.json', 'w') as f:
        json.dump(accounts, f, indent=4)

def create_deck():
    cards = [(1, '<:ACE:1222736603525546104>'),
             (2, '<:TWO:1222736601461821550>'),
             (3, '<:THREE:1222736640955650048>'),
             (4, '<:FOUR:1222736598161166357>'),
             (5, '<:FIVE:1222736597028573285>'),
             (6, '<:SIX:1222736581467705455>'),
             (7, '<:SEVEN:1222736595434737696>'),
             (8, '<:EIGHT:1222736594424041573>'),
             (9, '<:NINE:1222736593329328189>'),
             (10, '<:TEN:1222736592158855218>'),
             (10, '<:JACK:1222736587935322242>'),
             (10, '<:QUEEN:1222736589575295100>'),
             (10, '<:KING:1222736590510493851>')]
    list = []
    for i in range(4):
        list.extend(cards)

    return list


def draw_card(deck):
    if len(deck) == 0:
        deck.extend(create_deck())
    card = random.choice(deck)
    deck.remove(card)
    return card


def calculate_total(hand):
    total = sum(card[0] for card in hand)
    num_aces = len([card for card in hand if card[0] == 1])
    while total <= 11 and num_aces > 0:
        total += 10
        num_aces -= 1
    return total


def format_hand(hand):
    return " ".join(card[1] for card in hand)

async def handle_win(bot,
                     ctx,
                     bet,
                     dealer_hand,
                     dealer_total,
                     player_hand,
                     player_total,
                     message,
                     view=None):
    author_id = str(ctx.author.id)
    with open('accounts.json', 'r') as f:
        accounts = json.load(f)

    if player_total == 21:
        accounts[author_id]['balance'] += bet * 2.5
    else:
        accounts[author_id]['balance'] += bet * 2
    new_balance = "{:,.0f}".format(accounts[author_id]['balance'])

    with open('accounts.json', 'w') as f:
        json.dump(accounts, f)

    embed = discord.Embed(title="", color=0x232428)
    embed.add_field(name=f"Your Cards: {player_total}",
                    value=f"{format_hand(player_hand)}",
                    inline=False)
    embed.add_field(name=f"Dealer's Cards: {dealer_total}",
                    value=format_hand(dealer_hand),
                    inline=False)
    embed.add_field(name="Result",
                    value=f"You won! Your new balance is: **{new_balance}**",
                    inline=False)
    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
    embed.set_thumbnail(url="https://i.imgur.com/JBPnaZz.png")
    await message.edit(embed=embed)
    for item in view.children:
        item.disabled = True
    await message.edit(view=view)

async def handle_loss(bot,
                      ctx,
                      bet,
                      dealer_hand,
                      dealer_total,
                      player_hand,
                      player_total,
                      message,
                      view=None):
    author_id = str(ctx.author.id)
    with open('accounts.json', 'r') as f:
        accounts = json.load(f)

    new_balance = "{:,.0f}".format(accounts[author_id]['balance'])

    with open('accounts.json', 'w') as f:
        json.dump(accounts, f)

    embed = discord.Embed(title="", color=0x232428)
    embed.add_field(name=f"Your Cards: {player_total}",
                    value=f"{format_hand(player_hand)}",
                    inline=False)
    embed.add_field(name=f"Dealer's Cards: {dealer_total}",
                    value=format_hand(dealer_hand),
                    inline=False)
    embed.add_field(name="Result",
                    value=f"You lost. Your new balance is: **{new_balance}**",
                    inline=False)
    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
    embed.set_thumbnail(url="https://i.imgur.com/JBPnaZz.png")
    await message.edit(embed=embed)
    for item in view.children:
        item.disabled = True
    await message.edit(view=view)


async def handle_tie(bot,
                     ctx,
                     bet,
                     dealer_hand,
                     dealer_total,
                     player_hand,
                     player_total,
                     message,
                     view=None):
    author_id = str(ctx.author.id)
    with open('accounts.json', 'r') as f:
        accounts = json.load(f)

    accounts[author_id]['balance'] += bet
    save_accounts(accounts)

    new_balance = "{:,.0f}".format(accounts[author_id]['balance'])

    embed = discord.Embed(title="", color=0x232428)
    embed.add_field(name=f"Your Cards: {player_total}",
                    value=f"{format_hand(player_hand)}",
                    inline=False)
    embed.add_field(name=f"Dealer's Cards: {dealer_total}",
                    value=format_hand(dealer_hand),
                    inline=False)
    embed.add_field(
        name="Result",
        value=f"The hand is a push. Your balance remains: **{new_balance}**",
        inline=False)
    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
    embed.set_thumbnail(url="https://i.imgur.com/JBPnaZz.png")
    await message.edit(embed=embed)
    for item in view.children:
        item.disabled = True
    await message.edit(view=view)
