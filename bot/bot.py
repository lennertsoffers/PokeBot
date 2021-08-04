import discord
from discord.ext import commands
from classes.Pokemon import Pokemon
from classes.Trainer import Trainer
from battle.battleDiscord import wildBattle
from battle.battleDiscord import playerBattle
from classes.PvP import PvP
import random
import asyncio

client = commands.Bot(command_prefix="_")

# Global variables
trainerDict = {}
battles = {}
roomAssignments = {}


def check(*reacts):
    if reacts[0].count > 1:
        return True
    return False


async def createRooms(ctx, challenger, challenged):
    category = discord.utils.get(ctx.guild.categories, name="Battle Rooms")

    roomChallenger = await ctx.guild.create_text_channel(name="room" + str(len(battles) + 1), category=category)
    roomChallenged = await ctx.guild.create_text_channel(name="room" + str(len(battles) + 2), category=category)
    battles.update({
        challenger.id: PvP(challenger.id, challenged.id, "room" + str(len(battles) + 1), roomChallenger.id, True),
        challenged.id: PvP(challenged.id, challenger.id, "room" + str(len(battles) + 2), roomChallenged.id)
    })

    roomAssignmentEmbed = discord.Embed(title="Room assignment:",
                                        description="Type 'ready' in your assigned room to start the battle",
                                        color=0x45ba36)
    roomAssignmentEmbed.add_field(name=f"{challenger.name}:",
                                  value=await roomChallenger.create_invite(max_uses=1, unique=True))
    roomAssignmentEmbed.add_field(name=f"{challenged.name}:",
                                  value=await roomChallenged.create_invite(max_uses=1, unique=True))
    global roomAssignments
    roomAssignments = {
        "challenger": roomChallenger,
        "challenged": roomChallenged
    }
    await ctx.send(embed=roomAssignmentEmbed)
    return


@client.event
async def on_ready():
    print("Ready to go")


@client.command(aliases=["np", "newPlayer", "newplayer", "n", "NewPlayer", "Newplayer"])
async def new_player(ctx, name=None):
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
    print(trainerDict)
    return


@client.command(aliases=["wb", "wildBattle", "wildbattle", "w", "Wildbattle", "WildBattle", ""])
async def wild_battle(ctx):
    if ctx.channel.name != 'free-roam':
        return
    # # trainer = trainerDict[ctx.message.author.id]
    # trainer = Trainer(ctx.message.author.id, 'test')
    # pkm = Pokemon(random.randint(1, 600), 30)
    # pkm1 = Pokemon(random.randint(1, 600), 30)
    # pkm2 = Pokemon(random.randint(1, 600), 30)
    # # pkm3 = Pokemon(random.randint(1, 600), 100)
    # # pkm4 = Pokemon(random.randint(1, 600), 100)
    # # pkm5 = Pokemon(random.randint(1, 600), 100)
    # # pkm.lowerHp(450)
    # # pkm1.lowerHp(20)
    # # pkm2.lowerHp(50)
    # # pkm3.lowerHp(120)
    # # pkm4.lowerHp(0)
    # # pkm5.lowerHp(40)
    # trainer.addPokemon(pkm)
    # trainer.addPokemon(pkm1)
    # trainer.addPokemon(pkm2)
    # # trainer.addPokemon(pkm3)
    # # trainer.addPokemon(pkm4)
    # # trainer.addPokemon(pkm5)
    # await wildBattle(trainer, ctx, client)


@client.command(aliases=["multiplayerRequestPlayer", "mrp", "MultiplayerRequestPlayer"])
async def multiplayer_request_player(ctx, member: discord.Member):
    if ctx.channel.name != "battle-requests":
        return
    requestEmbed = discord.Embed(title=f"{ctx.author.name} has challenged you in a battle!",
                                 description="Go to 'battle-requests' to accept the challenge",
                                 color=0x45ba36)
    challengeEmbed = discord.Embed(title=f"{ctx.author.name} has challenged {member.display_name} in a battle!",
                                   description="Add 👍 to accept and 👎 to decline",
                                   color=0x45ba36)
    await member.send(embed=requestEmbed)
    challengeEmbedMessage = await ctx.send(embed=challengeEmbed)
    await challengeEmbedMessage.add_reaction(emoji="👍")
    await challengeEmbedMessage.add_reaction(emoji="👎")
    try:
        await client.wait_for('reaction_add', check=check, timeout=300)
        challengeEmbedMessageNew = await ctx.channel.fetch_message(challengeEmbedMessage.id)
        if challengeEmbedMessageNew.reactions[0].count > 1:
            await createRooms(ctx, ctx.author, member)
        else:
            await ctx.send(f"{member.display_name} has declined your challenge!")
            await asyncio.sleep(10)
            await ctx.channel.purge(limit=3)
    except asyncio.TimeoutError:
        await ctx.channel.purge(limit=2)
    return


@client.command()
async def setup(ctx):
    trainer1 = Trainer(391962085531189258, "roonie444")
    trainer2 = Trainer(834312962491416626, "te")
    starter1 = Pokemon(1, level=5)
    starter2 = Pokemon(2, level=5)
    trainer1.addPokemon(starter1)
    trainer2.addPokemon(starter2)
    trainerDict.update({391962085531189258: trainer1})
    trainerDict.update({834312962491416626: trainer2})
    print(trainerDict)


@client.command(aliases=["Ready"])
async def ready(ctx):
    if "room" not in ctx.channel.name:
        return
    found = False
    for battle in battles:
        if ctx.author.id == battle:
            PvP_Object = battles[battle]
            PvP_Object.setReady(True)
            if battles[PvP_Object.getOpponentId()].isReady():
                if PvP_Object.isChallenger:
                    print(f"challenger: {PvP_Object.getPlayerId()}/tObject: {trainerDict[PvP_Object.getPlayerId()]}")
                    print(f"challenged: {battles[PvP_Object.getOpponentId()].getPlayerId()}/tObject: {trainerDict[battles[PvP_Object.getOpponentId()].getPlayerId()]}")
                    await playerBattle([trainerDict[PvP_Object.getPlayerId()], trainerDict[battles[PvP_Object.getOpponentId()].getPlayerId()]], ctx, client, roomAssignments)
                else:
                    print(f"challenger: {battles[PvP_Object.getOpponentId()].getPlayerId()}/tObject: {trainerDict[battles[PvP_Object.getOpponentId()].getPlayerId()]}")
                    print(f"challenged: {PvP_Object.getPlayerId()}/tObject: {trainerDict[PvP_Object.getPlayerId()]}")
                    await playerBattle([trainerDict[battles[PvP_Object.getOpponentId()].getPlayerId()], trainerDict[PvP_Object.getPlayerId()]], ctx, client, roomAssignments)
            found = True
            break
    if not found:
        await ctx.send("permission denied")


@client.command(aliases=["c", "C", "Clear", "CLEAR"])
async def clear(ctx, number):
    await ctx.channel.purge(limit=int(number))


@client.command(aliases=["Test", "t"])
async def test(ctx):
    category = discord.utils.get(ctx.guild.categories, name="Battle Rooms")
    room = await ctx.guild.create_text_channel(name='test-channel', category=category)
    await asyncio.sleep(4)
    await room.delete()


client.run("ODMwMTM4Mjg1NjQ0ODQxMDEw.YHCUhg.dPeUoJhCSr5qy946PwHCpHw-SUE")
