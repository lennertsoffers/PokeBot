import discord
from discord.ext import commands
from discord.utils import get
from classes.Pokemon import Pokemon
from classes.Trainer import Trainer
from battle.battleDiscord import wildBattle, playerBattle
import asyncio
import random

client = commands.Bot(command_prefix="_")

# Global variables
trainerDict = {}
battleRooms = []


@client.event
async def on_ready():
    print("Ready to go")


@client.command(aliases=["init", "Initialize", "Init", "I", "i"])
async def initialize(ctx):
    roomIndex = 1
    room = get(ctx.guild.channels, name=("room" + str(roomIndex)))
    while room:
        battleRooms.append({"roomName": "room" + str(roomIndex), "available": True, "roomId": room.id})
        roomIndex += 1
        room = get(ctx.guild.channels, name=("room" + str(roomIndex)))
    await ctx.send("done")


@client.command(aliases=["np", "newPlayer", "newplayer", "n", "NewPlayer", "Newplayer"])
async def new_player(ctx, name=None):
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
        spriteUrl = starterPokemon.getSprite()
        starterPokemonEmbed.set_thumbnail(url=spriteUrl)
        choiceEmbed.add_field(name=starterPokemon.getName(), value=choiceList[i], inline=True)
        await ctx.send(embed=starterPokemonEmbed)
    choiceEmbed.set_footer(text="_"*90)
    choiceMessage = await ctx.send(embed=choiceEmbed)
    for i in range(len(starterPokemonNameList)):
        await choiceMessage.add_reaction(emoji=choiceList[i])
    try:
        await client.wait_for('reaction_add', check=check, timeout=120)
        choiceMessageNew = await ctx.channel.fetch_message(choiceMessage.id)
        starterId = None
        for i in range(len(choiceMessageNew.reactions)):
            if choiceMessageNew.reactions[i].count > 1:
                starterId = i
        trainerName = name
        if trainerName is None:
            trainerName = ctx.message.author.name
        trainer = Trainer(ctx.message.author.id, trainerName, ctx.message.author.avatar_url)
        starter = Pokemon(starterPokemonNameList[starterId], level=5)
        trainer.addPokemon(starter)
        trainerDict.update({ctx.message.author.id: trainer})
        trainerCreationSuccessEmbed = discord.Embed(title=f"Welcome to the world of pokemon {trainer.getName()}",
                                                    description="Congratulations with your first Pokemon. We wish you success on your journey to become a pokemon master",
                                                    color=0x45ba36)
        trainerCreationSuccessEmbed.set_author(name=trainer.getName(), icon_url=trainer.getProfilePicture())
        trainerCreationSuccessEmbed.set_image(url=f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{starter.getId()}.png")
        await ctx.send(embed=trainerCreationSuccessEmbed)
    except asyncio.TimeoutError:
        trainerCreationFailEmbed = discord.Embed(title="Failed to create trainer!", description="You didn't choose a starter pokemon.", color=0x45ba36)
        trainerCreationFailEmbed.set_footer(text="_"*90)
        await ctx.send(embed=trainerCreationFailEmbed)
    return


@client.command(aliases=["wb", "wildBattle", "wildbattle", "w", "Wildbattle", "WildBattle", ""])
async def wild_battle(ctx):
    if ctx.channel.name != 'free-roam':
        return
    trainer = trainerDict[ctx.message.author.id]
    # trainer = Trainer(ctx.message.author.id, 'test')
    # pkm = Pokemon("sandshrew", 40)
    # pkm1 = Pokemon("turtwig", 100)
    # pkm2 = Pokemon(random.randint(1, 600), 100)
    # pkm3 = Pokemon(random.randint(1, 600), 100)
    # pkm4 = Pokemon(random.randint(1, 600), 100)
    # pkm5 = Pokemon(random.randint(1, 600), 100)
    # pkm.lowerHp(450)
    # # pkm1.lowerHp(20)
    # # pkm2.lowerHp(50)
    # # pkm3.lowerHp(120)
    # # pkm4.lowerHp(0)
    # # pkm5.lowerHp(40)
    # trainer.addPokemon(pkm)
    # trainer.addPokemon(pkm1)
    # trainer.addPokemon(pkm2)
    # trainer.addPokemon(pkm3)
    # trainer.addPokemon(pkm4)
    # trainer.addPokemon(pkm5)
    await wildBattle(trainer, ctx, client)


@client.command(aliases=["tb"])
async def trainer_battle(ctx):
    if ctx.channel.name != "battle-requests":
        return
    # trainer = Trainer(ctx.message.author.id, 'test')
    # pkm = Pokemon(random.randint(1, 500), 40)
    # trainer.addPokemon(pkm)
    #
    # trainer2 = Trainer(ctx.message.author.id + 1, 'test2')
    # pkm2 = Pokemon(random.randint(1, 500), 40)
    # trainer2.addPokemon(pkm2)
    # trainer2 = trainerDict[ctx.message.author.id]

    battleRooms[1]["available"] = False
    roomsFound = 0
    selectedRooms = []
    roomIndex = 0
    while roomIndex < len(battleRooms) and roomsFound < 2:
        room = battleRooms[roomIndex]
        if room["available"]:
            selectedRooms.append(room)
            roomsFound += 1
        roomIndex += 1
    print(selectedRooms)

    # await playerBattle([trainer, trainer2], ctx, client, [selectedRooms[0], selectedRooms[1]])


@client.command(aliases=["c", "C", "Clear", "CLEAR"])
async def clear(ctx, number):
    await ctx.channel.purge(limit=int(number))


@client.command(aliases=["Test", "t"])
async def test(ctx):
    print(get(ctx.guild.channels, name="room1").id)


client.run("ODMwMTM4Mjg1NjQ0ODQxMDEw.YHCUhg.-3J4fgmva3h_4k1h7fOxGtsxskg")
