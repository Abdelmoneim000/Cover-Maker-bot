"""
    This file contains the bot events and the bot commands.
"""
# Discord
import discord
import discord.interactions as interactions
from discord.ext import commands, tasks

# checking messages in channels
async def message_event(bot, message):
    if message.author == bot.user:
        return

    if isinstance(message.channel, discord.DMChannel):
        return

    await bot.process_commands(message)


# Error handling for commands
async def on_error(ctx, error):
    """
    @ctx: context object of the invoked command to provide more info
    @error: error that was raised during the command invocation
    """
    if isinstance(error, commands.CommandNotFound):
        return

    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('You are missing a required argument.')
        return

    if isinstance(error, commands.BadArgument):
        await ctx.send('You passed a bad argument.')
        return

    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f'This command is on cooldown. Try again in {error.retry_after:.2f} seconds.')
        return

    if isinstance(error, commands.CheckFailure):
        await ctx.send('You do not have permission to use this command.')
        return

    if isinstance(error, commands.CommandInvokeError):
        await ctx.send('There was an error while processing the command.')
        return

    await ctx.send('There was an error while processing the command.')
