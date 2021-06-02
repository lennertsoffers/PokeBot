import discord
from discord.ext import commands
from discord.utils import get
from classes.Pokemon import Pokemon
from classes.Trainer import Trainer
from battle.battleNew import wildBattle
import asyncio
import random

client = commands.Bot(command_prefix="_")


@client.event
async def on_ready():
    print("Ready to go")


@client.command(aliases=["np", "newPlayer", "newplayer"])
async def new_player(ctx):
    def check(*reacts):
        if reacts[0].count > 1:
            return True
        return False

    starterPokemon = ["charmander", "bulbasaur", "squirtle"]
    if ctx.channel.name != 'new-players':
        return
    await ctx.message.add_reaction(emoji='👍')
    await ctx.message.add_reaction(emoji='👎')
    await ctx.message.add_reaction(emoji='😀')
    try:
        await client.wait_for('reaction_add', check=check)
        starterId = 0
        for i in range(len(ctx.message.reactions)):
            if ctx.message.reactions[i].count > 1:
                starterId = i
        trainer = Trainer(ctx.message.author.id, ctx.message.author.name)
        trainer.addPokemon(Pokemon(starterPokemon[starterId], level=5))
        trainer.depositCarryPokemon(trainer.getPokemonList()[starterPokemon[starterId]])
        print(f'Hello {trainer.getName()}')
        print(f'your starter is {trainer.getCarryPokemonList()[0].getName()}')
    except asyncio.TimeoutError:
        print('timeout')


@client.command(aliases=["Test", "t"])
async def test(ctx):
    channel1 = client.get_channel(831259742352703521)
    new_players = discord.utils.get(ctx.guild.channels, name='new-players')
    await channel1.send('test1')
    await new_players.send('new-players')


client.run("ODMwMTM4Mjg1NjQ0ODQxMDEw.YHCUhg.-3J4fgmva3h_4k1h7fOxGtsxskg")
