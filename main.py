import discord
from discord.ext import commands
import random
import json
import asyncio
import sys

client = commands.Bot(command_prefix = '!')
client.remove_command("help")

@client.event
async def on_ready():
    data = read_json("sings")
    client.sings_channel = data["SingsChannels"]
    await client.change_presence(status=discord.Status.idle)
    print("Bot Ready")

@client.event
async def on_message(message):
    member = message.author
    if message.author.bot:
        return
    if client.user.id != message.author.id:
        if 'l' in message.content:
            if message.channel.id in client.sings_channel:
                async with message.channel.typing():
                    await asyncio.sleep(2)
                responses = ["Lyric Response 1",
                             "Lyric Response 2",]
                await message.channel.send(f'{random.choice(responses)}')
            else:
                return

    await client.process_commands(message)


@client.command()
async def help(ctx):
    embed = discord.Embed(title="BOT COMMANDS", description="Here is my Commands", color=(2621184))
    embed.add_field(name="STANDARD COMMANDS", value=">help - This Message\n>ping - Checks my Ping\n>say - Make me say things\n>esay - Make me say things in a embed", inline=False)
    embed.add_field(name="CONFIG", value=">singtrue - Have me sing christmas songs randomly in your current channel\n>singfalse - Make me no longer sing in your text channel", inline=False)
    embed.add_field(name="SOURCE CODE", value="https://github.com/BoomerangRosalina/DiscordSingsBot.py", inline=False)
    await ctx.send(embed=embed)

@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! My Latency is {round(client.latency * 1000)}ms')

@client.command()
async def say(ctx, *, question: commands.clean_content):
    await ctx.send(f'{question}')
    await ctx.message.delete()

@client.command()
async def esay(ctx, *, question):
    embed = discord.Embed(description=f'{question}', color=(2621184))
    await ctx.send(embed=embed)
    await ctx.message.delete()

@client.command()
@commands.has_permissions(manage_guild=True)
async def singtrue(ctx):
    client.sings_channel.append(ctx.channel.id)
    data = read_json("sings")
    data["SingsChannels"].append(ctx.channel.id)
    write_json(data, "sings")
    await ctx.send("I will now randomly sing in this channel")

@singtrue.error
async def singtrue_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('YOU REQUIRE THE MANAGE_GUILD PERMISSION TO USE THIS COMMAND')
    else:
        raise error

@client.command()
@commands.has_permissions(manage_guild=True)
async def singfalse(ctx):
    client.sings_channel.remove(ctx.channel.id)
    data = read_json("sings")
    data["SingsChannels"].remove(ctx.channel.id)
    write_json(data, "sings")
    await ctx.send("I will no longer randomly sing in this channel")

@singfalse.error
async def singfalse_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('YOU REQUIRE THE MANAGE_GUILD PERMISSION TO USE THIS COMMAND')
    else:
        raise error

def read_json(filename):
    with open(f"./sings.json", "r") as file:
        data = json.load(file)
    return data

def write_json(data, filename):
    with open(f"./sings.json", "w") as file:
        json.dump(data, file, indent=4)

if "__main__" == __name__:
    with open("singtrigger.txt", "r") as f:
        singtrigger = f.read().splitlines()





client.run("INSERTBOTTOKENHERE")
