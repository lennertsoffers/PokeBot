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

    if ctx.channel.name != 'new-players':
        return

    starterPokemonNameList = ["charmander", "bulbasaur", "squirtle"]
    choiceList = ["\U0001F534", "\U0001F7E2", "\U0001F535"]
    starterPokemonList = []
    choiceEmbed = discord.Embed(title="Make a choice:", description='', color=0x45ba36)
    for i in range(len(starterPokemonNameList)):
        starterPokemon = Pokemon(starterPokemonNameList[i], level=5)
        starterPokemonList.append(starterPokemon)
        starterPokemonEmbed = discord.Embed(title=starterPokemon.getName(), description=starterPokemon.getSpecie().getFlavorText(), color=0x45ba36)
        if starterPokemon.isShiny():
            spriteUrl = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/shiny/{starterPokemon.getId()}.png"
        else:
            spriteUrl = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{starterPokemon.getId()}.png"
        starterPokemonEmbed.set_thumbnail(url=spriteUrl)
        choiceEmbed.add_field(name=starterPokemon.getName(), value=choiceList[i], inline=True)
        await ctx.send(embed=starterPokemonEmbed)
    choiceEmbed.set_footer(text="_"*90)
    choiceMessage = await ctx.send(embed=choiceEmbed)
    await choiceMessage.add_reaction(emoji=choiceList[0])
    await choiceMessage.add_reaction(emoji=choiceList[1])
    await choiceMessage.add_reaction(emoji=choiceList[2])
    try:
        await client.wait_for('reaction_add', check=check)
        starterId = None
        print(get(choiceMessage.reactions))
        print(len(choiceMessage.reactions))
        for i in range(len(choiceMessage.reactions)):
            print("in for")
            if choiceMessage.reactions[i].count > 1:
                starterId = i
        print(starterId)
        trainer = Trainer(ctx.message.author.id, ctx.message.author.name)
        trainer.addPokemon(Pokemon(starterPokemonNameList[starterId], level=5))
        trainer.depositCarryPokemon(trainer.getPokemonList()[0])
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

# get reacions on message