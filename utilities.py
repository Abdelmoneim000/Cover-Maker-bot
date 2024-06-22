"""
    This file contains utility functions for the accounts app.
"""
import json
import random
import discord
import os
import asyncio
import aiohttp
import re
from mega import Mega


mega = Mega()

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

# Cleanup function after the cover message to clean the images downloaded.
def cleanup():
    all_images = os.listdir("./images")
    for image in all_images:
        print(f"Deleting {image}")
        os.remove(f"./images/{image}")


# Utility functions for to help the cover function

async def find_folder_id(folder_name, parent_id=None):
    loop = asyncio.get_event_loop()
    files = await loop.run_in_executor(None, mega.get_files)
    for file_id, info in files.items():
        if info['t'] == 1 and info['a'] and info['a']['n'] == folder_name and (
                not parent_id or info['p'] == parent_id):
            return file_id
    return None


async def get_all_files():
    loop = asyncio.get_event_loop()
    files = await loop.run_in_executor(None, mega.get_files)
    cover_id = await find_folder_id('cover')

    if not cover_id:
        return

    all_files = {}

    iteration = 0
    async with aiohttp.ClientSession() as session:
        tasks = []
        # All Files
        for file_id, file in files.items():
            print(f"Length of all files: {len(files)}")
            iteration += 1
            print(f"Iteration: {iteration}")

            try:
                if file['t'] == 1:
                    loop = asyncio.get_event_loop()
                    if file_id not in all_files:
                        all_files[file_id] = {}

                    # save the parent file data in the "parent_data" key
                    all_files[file_id]["parent_data"] = file

                    # subfolders for the cover folder
                    subitems = mega.get_files_in_node(file_id)
                    print(f"Cover folder has {len(subitems)} subitems")

                    # Iterate over all the subitems for the cover folder.
                    subfile_count = 0
                    for subitem_id, subitem in subitems.items():
                        subfile_count += 1
                        print(f"Subitem: {subitem_id}, count: {subfile_count}")
                        # If the type is a folder
                        if subitem['t'] == 1:
                            print("- Subitem type is folder")
                            # get all the subsubitems in the subitem in the sub item
                            subsubfiles = mega.get_files_in_node(subitem_id)
                            print(
                                f"- Subitem has {len(subsubfiles)} subsubfiles"
                            )

                            # save the subfiles in the "subfiles" key
                            all_files[file_id]["subitems"][subitem_id][
                                "subitems"] = subsubfiles
                            # subitems: {
                            # 	"item_id": {
                            #  	...item_data,
                            #  	"subitems": {
                            #     	"subitem_id": {},
                            #     	"subitem_id": ...,
                            #     	"subitem_id": ...,
                            # 	}
                            # 	},
                            # 	...
                            # }

                            # iterate over all the sub files
                            new_files = []
                            subsubfile_count = 0
                            for subsubfile_id, subsubfile in subsubfiles.items(
                            ):
                                subsubfile_count += 1
                                print(
                                    f"Subsubfile: {subsubfile_id}, count: {subsubfile_count}"
                                )
                                if subitem['a'] and 'n' in subitem['a']:
                                    simplified_subfile_name = subsubfile['a'][
                                        'n'].lower().replace("_", "")
                                    with open("all_names.txt", "a") as f:
                                        f.write(simplified_subfile_name + "\n")

                                    all_files[file_id]["subitems"][subitem_id][
                                        "subitems"][subsubfile_id][
                                            "simplified_name"] = simplified_subfile_name
                                    url = mega.get_link(
                                        (subsubfile_id, subsubfile))
                                    all_files[file_id]["subitems"][subitem_id][
                                        "subitems"][subsubfile_id]["url"] = url
                                    print(
                                        "Successfully added url and simplified name."
                                    )
                                    print(
                                        f"Simplified name: {simplified_subfile_name}"
                                    )
                                    print(f"Url: {url}")
                        else:
                            # if the type is a file.
                            print("- Subitem type is file")
                            if subitem['a'] and 'n' in subitem[
                                    'a'] and "k" in file and "h" in file:
                                simplified_subfile_name = subitem['a'][
                                    'n'].lower().replace("_", " ")
                                with open("all_names.txt", "a") as f:
                                    f.write(simplified_subfile_name + "\n")
                                all_files[file_id]["subitems"][subitem_id][
                                    "simplified_name"] = simplified_subfile_name
                                url = mega.get_link((subitem_id, subitem))
                                all_files[file_id]["subitems"][subitem_id][
                                    "url"] = url
                                print(
                                    "Successfully added url and simplified name."
                                )
                                print(
                                    f"Simplified name: {simplified_subfile_name}"
                                )
                                print(f"Url: {url}")
                else:
                    # if the type is a file.
                    print("- file is of type file")
                    if file['a'] and 'n' in file[
                            'a'] and "k" in file and "h" in file:
                        simplified_subfile_name = file['a']['n'].lower(
                        ).replace("_", " ")
                        with open("all_names.txt", "a") as f:
                            f.write(simplified_subfile_name + "\n")

                        if file_id not in all_files:
                            all_files[file_id] = {
                            }  # Initialize the dictionary if it not already

                        print(f"File ID: {file_id}")
                        print(f"File: {file}")
                        all_files[file_id][
                            "simplified_name"] = simplified_subfile_name
                        url = await loop.run_in_executor(
                            None, mega.get_link, (file_id, files[file_id]))
                        all_files[file_id]["url"] = url
                        print("Successfully added url and simplified name.")
                        print(f"Simplified name: {simplified_subfile_name}")
                        print(f"Url: {url}")

            except Exception as e:
                print(f"Error: {e}")
                with open("error.txt", "a") as f:
                    f.write(f"Error: {e}\n")
                continue

    file_path = "all_data.json"
    with open(file_path, "w") as f:
        print(f"Dumping json to {file_path}")
        json.dump(all_files, f, indent=2)


def get_matched_urls(all_data, simplified_file_name):
    print("Getting matched urls...")
    
    file_format_pattern = r'\.\w+$'
    # Open the log file in append mode
    with open('log.txt', 'a') as log_file:
        # Check if the simplified file name contains a file format
        if re.search(file_format_pattern, simplified_file_name):
            # Log an error message if a file format is found
            log_file.write("Error: wrong song name, please use a valid song name\n")
            return []
        else:
            # Log the simplified file name if no file format is found
            log_file.write(simplified_file_name + '\n')
    urls = []
    subfile_names = []

    file_count = 0
    for file_id, file in all_data.items():
        file_count += 1
        if not "subitems" in file:
            if simplified_file_name.lower() in file["simplified_name"].lower(
            ) or simplified_file_name.lower().replace(
                    " ", "") in file["simplified_name"].lower():
                if "png" in file["simplified_name"].lower(
                ) or "jpg" in file["simplified_name"].lower():
                    print(
                        f"Found file with simplified name: {simplified_file_name}"
                    )
                    urls.append(file["url"])
                    subfile_names.append(file["simplified_name"].lower())
            continue

        subitems = file.get("subitems")
        print(
            f"({file_count}: File {file_id} has a total of {len(subitems)} subitems"
        )

        subitem_count = 0
        for subitem_id, subitem in subitems.items():
            subitem_count += 1
            if subitem['a'] and 'n' in subitem['a']:

                simplified_subfile_name = subitem['a']['n'].lower()
                print(f"Simplified name: {simplified_subfile_name}")

                if simplified_file_name.lower(
                ) in simplified_subfile_name or simplified_file_name.lower(
                ).replace(" ", "") in simplified_subfile_name:
                    if "png" in simplified_subfile_name or "jpg" in simplified_subfile_name:
                        print(subitem)
                        try:
                            url = subitem["url"]
                            urls.append(url)
                            subfile_names.append(simplified_subfile_name)
                            print(f"Successfully appended url: {url}")
                        except Exception as e:
                            print(f"Error: {e}")
                            continue

    with open("./simplified-subfile-name.json", "w") as f:
        json.dump(subfile_names, f, indent=2)
    return urls


async def download_file_async(session, subfile_id, subfile, dest_filename):
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, lambda: mega.download(
        (subfile_id, subfile), dest_filename=dest_filename)
                               )  # <-- Added this too


async def download_all_urls(mega, urls, user_id):
    # Create a unique directory for the user's request
    user_dir = f"./images/{user_id}"
    os.makedirs(user_dir, exist_ok=True)

    return_array = []
    for i, url in enumerate(urls):
        print(f"{(i+1)} Downloading {url.replace('#!', 'file/')}")
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, mega.download_url, url,
                                            user_dir, f"image_{i+1}.png")
        return_array.append({
            "result": result,
            "path": f"{user_dir}/image_{i+1}.png"
        })
    return return_array
