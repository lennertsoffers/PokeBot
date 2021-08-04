import random
from classes.Pokemon import Pokemon
from discord.utils import get
import math
import discord
import asyncio


reactionList = ["\U0001F534", "\U0001F7E1", "\U0001F7E2", "\U0001F535", "\U0001F7E0", "\U0001F7E3"]
messages = 0


def check(*reacts):
    if reacts[0].count > 1:
        return True
    return False


def getHpInHearts(pokemon):
    scoreOnTwenty = math.ceil(pokemon.getHp() / pokemon.getStat('hp').getStatValue() * 20)
    hpString = "❤" * scoreOnTwenty
    hpString += "🖤" * (20 - scoreOnTwenty)
    return hpString


async def getDamageEmbed(d, p, ctx):
    embed = discord.Embed(title=f"{p.getName()} got {d} damage", description=f"HP: {getHpInHearts(p)} {p.getHp()}", color=0x45ba36)
    embed.set_thumbnail(url=p.getSprite())
    await ctx.send(embed=embed)
    await asyncio.sleep(2)
    global messages
    messages += 1


async def sendMessageEmbed(message, ctx):
    embed = discord.Embed(title=message, description="\u200b", color=0x45ba36)
    await ctx.send(embed=embed)
    await asyncio.sleep(2)
    global messages
    messages += 1


async def useMoveEmbed(m, p, ctx):
    embed = discord.Embed(title=f"{p.getName()} uses {m.getName()}", description="\u200b", color=0x45ba36)
    await ctx.send(embed=embed)
    await asyncio.sleep(2)
    global messages
    messages += 1


async def sendFaintedEmbed(ctx, pokemon):
    embed = discord.Embed(title=f"{pokemon.getName()} fainted")
    embed.set_thumbnail(url=pokemon.getSprite())
    await ctx.send(embed=embed)


def getPokemonEmbed(textBefore="", *args):
    for pokemon in args:
        embed = discord.Embed(title=textBefore + pokemon.getName(), description=f"HP: {getHpInHearts(pokemon)}", color=0x45ba36)
        embed.add_field(name="Level:", value=pokemon.getLevel(), inline=True)
        embed.add_field(name="Exp:", value=pokemon.getNextLevelExperience(), inline=True)
        # if statusEffect != "":
        #     embed.add_field(name="Status", value=statusEffect)
        embed.set_thumbnail(url=pokemon.getSprite())
        global messages
        messages += 1


async def switchPokemon(trainer, ctx, client):
    switchPokemonEmbed = discord.Embed(title="Your party", description="Choose a pokemon to switch your party leader with", color=0x45ba36)
    choiceSwitchPokemonEmbed = discord.Embed(title="Choose a pokemon to switch", description="\u200b", color=0x45ba36)
    await ctx.send(embed=switchPokemonEmbed)
    global messages
    carryPokemonList = trainer.getCarryPokemonList()

    async def createPartyPokemonEmbeds(pokemon, reaction, infoAfterName=""):
        hpString = getHpInHearts(pokemon)
        partyPokemonEmbed = discord.Embed(title=pokemon.getName() + infoAfterName, description=f"HP: {hpString} {pokemon.getHp()}", color=0x45ba36)
        partyPokemonEmbed.set_thumbnail(url=pokemon.getSprite())
        await ctx.send(embed=partyPokemonEmbed)
        global messages
        messages += 1
        choiceSwitchPokemonEmbed.add_field(name=reaction + " " + pokemon.getName(), value="\u200b", inline=True)

    await createPartyPokemonEmbeds(carryPokemonList[0], reactionList[0], " (party leader)")
    for pokemonIndex in range(1, len(carryPokemonList)):
        await createPartyPokemonEmbeds(carryPokemonList[pokemonIndex], reactionList[pokemonIndex])
    choiceSwitchPokemonEmbed.set_footer(text="_" * 90)
    choiceSwitchMessage = await ctx.send(embed=choiceSwitchPokemonEmbed)
    messages += 2
    for i in range(len(carryPokemonList)):
        await choiceSwitchMessage.add_reaction(emoji=reactionList[i])
    try:
        await client.wait_for('reaction_add', check=check, timeout=120)
        choiceSwitchMessageNew = await ctx.channel.fetch_message(choiceSwitchMessage.id)
        switched = None
        for i in range(len(choiceSwitchMessageNew.reactions)):
            if choiceSwitchMessageNew.reactions[i].count > 1:
                switched = trainer.switchCarryPokemon(i)
                if i == 0:
                    switched = False
        return switched
    except asyncio.TimeoutError:
        trainerCreationFailEmbed = discord.Embed(title="Failed to switch pokemon!", description="You didn't choose a pokemon to switch.", color=0x45ba36)
        trainerCreationFailEmbed.set_footer(text="_"*90)
        await ctx.send(embed=trainerCreationFailEmbed)
        messages += 1
        return False


async def battleMenu(trainer, target, trainerBattle, ctx, client):
    menuOutput = {
        "move": None,
        "run": False,
        "switch": False,
        "useItem": False,
        "displayMenu": False,
        "endBattle": False
    }
    actionList = ["fight", "run", "pokemon", "bag"]
    actionMenuEmbed = discord.Embed(title="Choose your action", description="\u200b", color=0x45ba36)
    for i in range(len(actionList)):
        actionMenuEmbed.add_field(name=reactionList[i] + " " + actionList[i].capitalize(), value="\u200b", inline=True)
    actionMenuEmbed.set_footer(text="_"*90)
    actionMenuEmbedMessage = await ctx.send(embed=actionMenuEmbed)
    global messages
    messages += 2
    for i in range(len(actionList)):
        await actionMenuEmbedMessage.add_reaction(emoji=reactionList[i])
    try:
        await client.wait_for('reaction_add', check=check, timeout=120)
        actionMenuEmbedMessageNew = await ctx.channel.fetch_message(actionMenuEmbedMessage.id)
        actionId = None
        for i in range(len(actionMenuEmbedMessageNew.reactions)):
            if actionMenuEmbedMessageNew.reactions[i].count > 1:
                actionId = i

        if actionList[actionId] == "fight":
            moves = trainer.getCarryPokemonList()[0].getMoves()
            moveMenuEmbed = discord.Embed(title="Choose a move", description="\u200b", color=0x45ba36)
            for moveIndex in range(len(moves)):
                move = moves[f"move{moveIndex + 1}"]
                moveMenuEmbed.add_field(name=reactionList[moveIndex] + " " + move.getName().capitalize(), value=move.getPower(), inline=False)
            moveMenuEmbed.set_footer(text="_" * 90)
            moveMenuEmbedMessage = await ctx.send(embed=moveMenuEmbed)
            for i in range(len(moves)):
                await moveMenuEmbedMessage.add_reaction(emoji=reactionList[i])
            try:
                await client.wait_for('reaction_add', check=check, timeout=120)
                moveMenuEmbedMessageNew = await ctx.channel.fetch_message(moveMenuEmbedMessage.id)
                moveId = None
                for i in range(len(moveMenuEmbedMessageNew.reactions)):
                    if moveMenuEmbedMessageNew.reactions[i].count > 1:
                        moveId = i
                menuOutput["move"] = moves[f"move{moveId + 1}"]
            except asyncio.TimeoutError:
                menuOutput["endBattle"] = True
                trainerCreationFailEmbed = discord.Embed(title="Timeout", description="You didn't choose an move", color=0x45ba36)
                trainerCreationFailEmbed.set_footer(text="_" * 90)
                await ctx.send(embed=trainerCreationFailEmbed)
        elif actionList[actionId] == "run":
            if trainerBattle:
                await ctx.send("Cannot flee a trainer battle")
                menuOutput["displayMenu"] = True
            else:
                if trainer.getCarryPokemonList()[0].getStat("speed").getStatValue() < target.getStat(
                        "speed").getStatValue():
                    await ctx.send("Cannot escape")
                    menuOutput["displayMenu"] = True
                else:
                    menuOutput["run"] = True
        elif actionList[actionId] == "pokemon":
            if await switchPokemon(trainer, ctx, client):
                menuOutput["switch"] = True
            else:
                menuOutput["displayMenu"] = True
        else:
            menuOutput["useItem"] = True

    except asyncio.TimeoutError:
        menuOutput["endBattle"] = True
        trainerCreationFailEmbed = discord.Embed(title="Timeout", description="You didn't choose an action", color=0x45ba36)
        trainerCreationFailEmbed.set_footer(text="_"*90)
        await ctx.send(embed=trainerCreationFailEmbed)
    return menuOutput


def attackHit(pokemon, target, move):
    nvStatus = pokemon.getNonVolatileStatus()
    vStatus = pokemon.getVolatileStatus()
    mAccuracy = move.getAccuracy()
    pAccuracy = pokemon.getBattleStats()["accuracy"]
    pEvasion = pokemon.getBattleStats()["evasion"]
    canAttackOutput = {"attack": True, "message": "", "before": False}
    for pkmType in target.getTypes():
        if move.getType().getName() == pkmType.getNoDamageFrom():
            canAttackOutput = {"attack": False, "message": "This move doesn't affect the target", "before": False}
    if not mAccuracy:
        mAccuracy = 100
    if pAccuracy >= 0:
        t = mAccuracy * ((3 + pAccuracy) / 3)
    else:
        t = mAccuracy * (3 / (3 + abs(pAccuracy)))
    if pEvasion > 0:
        t *= (3 / (3 + pEvasion))
    else:
        t *= ((3 + abs(pEvasion)) / 3)
    if random.randint(1, 100) > round(t):
        canAttackOutput = {"attack": False, "message": pokemon.getName() + " missed", "before": False}
    if nvStatus["PAR"] and random.randint(1, 100) <= 25:
        canAttackOutput = {"attack": False, "message": pokemon.getName() + " is paralyzed and can't move", "before": True}
    elif nvStatus["SLP"] != -1:
        if nvStatus["SLP"] > 0:
            canAttackOutput = {"attack": False, "message": pokemon.getName() + " is fast asleep", "before": True}
            nvStatus["SLP"] -= 1
        else:
            canAttackOutput = {"attack": True, "message": pokemon.getName() + " woke up!", "before": True}
            nvStatus["SLP"] -= 1
    elif nvStatus["FRZ"]:
        if random.randint(1, 100) > 10:
            canAttackOutput = {"attack": False, "message": pokemon.getName() + " if frozen solid", "before": True}
        else:
            canAttackOutput = {"attack": True, "message": pokemon.getName() + " broke free!", "before": True}
            nvStatus["FRZ"] = False
    elif vStatus["flinch"]:
        canAttackOutput = {"attack": False, "message": pokemon.getName() + " flinched", "before": False}
        vStatus["flinch"] = False

    pokemon.setVolatileStatus(vStatus)
    pokemon.setNonVolatileStatus(nvStatus)
    return canAttackOutput


def calculateAmountOfHits(move):
    if not move.getMultiHitType() == "single":
        if move.getMultiHitType() == "double":
            return 2
        else:
            randHit = random.randint(1, 100)
            if randHit <= 35:
                return 2
            elif randHit <= 70:
                return 3
            elif randHit <= 85:
                return 4
            else:
                return 5
    return 1


def calculateDamage(pokemon, target, move, basicDamageCalculation):
    calculateDamageOutput = {"damage": 0,
                             "criticalHit": False,
                             "text": ""}

    def calculateStat(value, inBattleStat):
        if inBattleStat >= 0:
            value *= ((2 + inBattleStat) / 2)
        else:
            value *= (2 / (2 + abs(inBattleStat)))
        return value

    def calculateMultiplier(pkm, tar, mov):
        def isCriticalHit(critRate):
            if critRate == 0:
                return random.randint(0, 100) <= 6
            elif critRate == 1:
                return random.randint(0, 100) <= 13
            elif critRate == 2:
                return random.randint(0, 100) <= 25
            elif critRate == 3:
                return random.randint(0, 100) <= 33
            else:
                return random.randint(0, 100) <= 50

        def typeMultiplier(moveType, targetTypes):
            multiplierOutput = {"multiplier": 1, "text": ""}
            for pkmType in targetTypes:
                if moveType in pkmType.getHalfDamageFrom() and multiplierOutput["multiplier"] != 0.5:
                    multiplierOutput["multiplier"] *= 0.5
                    multiplierOutput["text"] = "it was not very effective"
                if moveType in pkmType.getDoubleDamageFrom() and multiplierOutput["multiplier"] != 2:
                    multiplierOutput["multiplier"] *= 2
                    multiplierOutput["text"] = "it was very effective"
            return multiplierOutput

        tMultiplier = typeMultiplier(mov.getType().getName(), tar.getTypes())
        tMultiplierAction = tMultiplier["multiplier"] != 1
        crit = False
        if isCriticalHit(pkm.getBattleStats()["criticalHitRate"]):
            crit = True
            tMultiplier["multiplier"] *= 2
        return {"multiplier": tMultiplier["multiplier"],
                "crit": crit,
                "typeMultiplier": tMultiplierAction,
                "typeMultiplierText": tMultiplier["text"]
                }

    multiplierDict = calculateMultiplier(pokemon, target, move)
    if move.getPower():
        if move.getDamageClass() == "physical":
            a = calculateStat(pokemon.getStat("attack").getStatValue(), pokemon.getBattleStats()["attack"])
            d = calculateStat(target.getStat("defense").getStatValue(), target.getBattleStats()["defense"])
        else:
            a = calculateStat(pokemon.getStat("special-attack").getStatValue(), pokemon.getBattleStats()["special-attack"])
            d = calculateStat(target.getStat("special-defense").getStatValue(), target.getBattleStats()["special-defense"])
        if basicDamageCalculation:
            damage = round(((((2 * pokemon.getLevel()) / 5) + 2) * 40 * (a / d)) / 50)
        else:
            damage = round((((((2 * pokemon.getLevel()) / 5) + 2) * move.getPower() * (a / d)) / 50) * multiplierDict["multiplier"])
    else:
        damage = 0
    if multiplierDict["crit"] and not basicDamageCalculation:
        calculateDamageOutput["criticalHit"] = True
    if multiplierDict["typeMultiplier"] and not basicDamageCalculation and damage != 0:
        calculateDamageOutput["text"] = multiplierDict["typeMultiplierText"]
    if damage != 0:
        calculateDamageOutput["damage"] = damage
    return calculateDamageOutput


async def statChanges(move, pokemon, target, damage, ctx):
    pokemonInBattleStats = pokemon.getBattleStats()
    targetBattleStats = target.getBattleStats()
    targetNonVolatileStatus = target.getNonVolatileStatus()
    targetVolatileStatus = target.getVolatileStatus()
    ailment = move.getAilment()
    messageEmbedList = []
    if ailment["name"] != "-1":
        if ailment["name"] == "PAR" and not targetNonVolatileStatus["PAR"]:
            if ailment["chance"] == 0 or random.randint(1, 100) <= ailment["chance"]:
                targetNonVolatileStatus[ailment["name"]] = True
                messageEmbedList.append(discord.Embed(title="PAR", description=f"{target.getName()} is paralyzed and may be unable to move", color=0x45ba36))
        elif ailment["name"] == "BRN" and not targetNonVolatileStatus["BRN"] > 0:
            if ailment["chance"] == 0 or random.randint(1, 100) <= ailment["chance"]:
                targetNonVolatileStatus[ailment["name"]] = calculateBrnPsnDamage(pokemon)
                messageEmbedList.append(discord.Embed(title="BRN", description=f"{target.getName()} is burned", color=0x45ba36))
        elif ailment["name"] == "FRZ" and not targetNonVolatileStatus["FRZ"]:
            if ailment["chance"] == 0 or random.randint(1, 100) <= ailment["chance"]:
                targetNonVolatileStatus[ailment["name"]] = True
                messageEmbedList.append(discord.Embed(title="FRZ", description=f"{target.getName()} is frozen", color=0x45ba36))
        elif ailment["name"] == "PSN" and not targetNonVolatileStatus["PSN"] > 0:
            if ailment["chance"] == 0 or random.randint(1, 100) <= ailment["chance"]:
                targetNonVolatileStatus[ailment["name"]] = calculateBrnPsnDamage(target)
                messageEmbedList.append(discord.Embed(title="PSN", description=f"{target.getName()} was badly poisoned", color=0x45ba36))
        elif ailment["name"] == "SLP" and targetNonVolatileStatus["SLP"] == -1:
            if ailment["chance"] == 0 or random.randint(1, 100) <= ailment["chance"]:
                targetNonVolatileStatus[ailment["name"]] = random.randint(2, 5)
                messageEmbedList.append(discord.Embed(title="SLP", description=f"{target.getName()} is fast asleep", color=0x45ba36))
        elif ailment["name"] == "confusion" and targetVolatileStatus["confusion"] == -1:
            if ailment["chance"] == 0 or random.randint(1, 100) <= ailment["chance"]:
                targetVolatileStatus[ailment["name"]] = random.randint(2, 5)
                messageEmbedList.append(discord.Embed(title="Confusion", description=f"{target.getName()} is confused", color=0x45ba36))
        target.setVolatileStatus(targetVolatileStatus)
        target.setNonVolatileStatus(targetNonVolatileStatus)
    if move.getCriticalRate() > 0:
        pokemonInBattleStats["criticalHitRate"] += 1
        messageEmbedList.append(discord.Embed(title="Crit", description=f"{pokemon.getName()} critical hit ratio rose!", color=0x45ba36))
    healing = move.getHealing()

    def healPokemonHp(pkm, amount):
        maxHeal = pokemon.getStat("hp").getStatValue() - pokemon.getHp()
        if amount > maxHeal:
            pkm.addHp(maxHeal)
            messageEmbedList.append(
                discord.Embed(title="Heal", description=f"{pkm.getName()} healed {maxHeal}hp", color=0x45ba36))
        else:
            pkm.addHp(amount)
            messageEmbedList.append(
                discord.Embed(title="Heal", description=f"{pkm.getName()} healed {amount}hp", color=0x45ba36))

    if healing != 0:
        if healing < 0:
            pokemon.lowerHp(healing)
            messageEmbedList.append(
                discord.Embed(title="Recoil", description=f"{pokemon.getName()} got {healing} recoil", color=0x45ba36))
        else:
            healPokemonHp(pokemon, healing)

    if move.getDrain() != 0:
        healPokemonHp(pokemon, (round(damage * (move.getDrain() / 100))))
    for statChange in move.getStatChanges():
        if statChange["name"] != "hp" and -6 < pokemonInBattleStats[statChange["name"]] < 6 and -6 < targetBattleStats[statChange["name"]] < 6:
            if statChange["change"] == 1:
                pokemonInBattleStats[statChange["name"]] += statChange["change"]
                messageEmbedList.append(discord.Embed(title="Stat change",
                                                      description=f"{pokemon.getName()}'s {statChange['name']} rose!",
                                                      color=0x45ba36))
            elif statChange["change"] == 2:
                pokemonInBattleStats[statChange["name"]] += statChange["change"]
                messageEmbedList.append(discord.Embed(title="Stat change",
                                                      description=f"{pokemon.getName()}'s {statChange['name']} sharply rose!",
                                                      color=0x45ba36))
            elif statChange["change"] == 3:
                pokemonInBattleStats[statChange["name"]] += statChange["change"]
                messageEmbedList.append(discord.Embed(title="Stat change",
                                                      description=f"{pokemon.getName()}'s {statChange['name']} rose drastically!",
                                                      color=0x45ba36))
            elif statChange["change"] == -1:
                targetBattleStats[statChange["name"]] += statChange["change"]
                messageEmbedList.append(discord.Embed(title="Stat change",
                                                      description=f"{target.getName()}'s {statChange['name']} fell!",
                                                      color=0x45ba36))
            elif statChange["change"] == -2:
                targetBattleStats[statChange["name"]] += statChange["change"]
                messageEmbedList.append(discord.Embed(title="Stat change",
                                                      description=f"{target.getName()}'s {statChange['name']} harshly fell!",
                                                      color=0x45ba36))
            elif statChange["change"] == -3:
                targetBattleStats[statChange["name"]] += statChange["change"]
                messageEmbedList.append(discord.Embed(title="Stat change",
                                                      description=f"{target.getName()}'s {statChange['name']} severely fell!",
                                                      color=0x45ba36))
        elif damage > 0:
            messageEmbedList.append(discord.Embed(title="Stat change",
                                                  description="Nothing happened",
                                                  color=0x45ba36))
        pokemon.setBattleStats(pokemonInBattleStats)
        target.setBattleStats(targetBattleStats)
    for embed in messageEmbedList:
        await ctx.send(embed=embed)
        global messages
        messages += 1


async def calculateBrnPsnDamage(pokemon, previousValue=0):
    newValue = previousValue + (pokemon.getStat('hp').getStatValue() / 8)
    if newValue > 15 * math.floor(pokemon.getStat('hp').getStatValue() / 16):
        newValue = 15 * math.floor(pokemon.getStat('hp').getStatValue() / 16)
    if newValue < 1:
        newValue = 1
    return round(newValue)


async def lowerAfterTurnDamage(pokemon):
    async def lowerNonVolatileStatus(pkm, status, statusLong):
        print(pokemon.getName(), "got hurt by", statusLong)
        pokemon.lowerHp(nonVolatileStatus[status])
        nonVolatileStatus[status] = calculateBrnPsnDamage(pkm, nonVolatileStatus[status])
        pokemon.setNonVolatileStatus(nonVolatileStatus)

    nonVolatileStatus = pokemon.getNonVolatileStatus()
    if nonVolatileStatus["PSN"] > 0:
        await lowerNonVolatileStatus(pokemon, "PSN", "poison")
    if nonVolatileStatus["BRN"] > 0:
        await lowerNonVolatileStatus(pokemon, "BRN", "burn")


async def moveHitLoop(pokemon, target, move, ctx):
    hitCount = calculateAmountOfHits(move)
    effectiveHits = 1
    stopHit = False
    moveHits = attackHit(pokemon, target, move)
    while effectiveHits <= hitCount and not stopHit:
        if moveHits["attack"] and target.getHp() > 0:
            if moveHits["before"] and moveHits["message"] != "":
                await sendMessageEmbed(moveHits["message"], ctx)
            if effectiveHits == 1:
                await useMoveEmbed(move, pokemon, ctx)
            if not moveHits["before"] and moveHits["message"] != "":
                await sendMessageEmbed(moveHits["message"], ctx)
            damageDict = calculateDamage(pokemon, target, move, False)
            target.lowerHp(damageDict["damage"])
            if damageDict["damage"] > 0:
                await getDamageEmbed(damageDict["damage"], target, ctx)
            await statChanges(move, pokemon, target, damageDict["damage"], ctx)
            effectiveHits += 1
            moveHits = attackHit(pokemon, target, move)
        else:
            stopHit = True
            if moveHits["before"] and moveHits["message"] != "":
                await sendMessageEmbed(moveHits["message"], ctx)
            if effectiveHits == 1 and not moveHits["before"]:
                await useMoveEmbed(move, pokemon, ctx)
            if not moveHits["before"] and moveHits["message"] != "":
                await sendMessageEmbed(moveHits["message"], ctx)
    if hitCount > 1:
        await sendMessageEmbed(f"it hit {effectiveHits - 1} times", ctx)


async def moveHit(pokemon, target, move, ctx):
    volatileStatus = pokemon.getVolatileStatus()
    if volatileStatus["confusion"] != -1:
        if volatileStatus["confusion"] == 0:
            await sendMessageEmbed(f"{pokemon.getName()} snapped out of confusion", ctx)
            await moveHitLoop(pokemon, target, move, ctx)
        else:
            pokemon.setVolatileStatus(volatileStatus)
            await sendMessageEmbed(f"{pokemon.getName()} is confused", ctx)
            if random.randint(1, 100) <= 50:
                await moveHitLoop(pokemon, target, move, ctx)
            else:
                await sendMessageEmbed(f"{pokemon.getName()} hurt itself in its confusion", ctx)
                damage = calculateDamage(pokemon, pokemon, move, True)["damage"]
                pokemon.lowerHp(damage)
                if damage > 0:
                    await getDamageEmbed(damage, pokemon, ctx)
        volatileStatus["confusion"] -= 1
    else:
        await moveHitLoop(pokemon, target, move, ctx)
    if pokemon.getHp() > 0:
        await lowerAfterTurnDamage(pokemon)


async def wildPokemonFainted(trainer, pokemon, ctx, client):
    currentPokemon = trainer.getCarryPokemonList()[0]
    if currentPokemon.getHp() == 0:
        await sendFaintedEmbed(ctx, currentPokemon)
        if 0 < any(pkm.getHp() for pkm in trainer.getCarryPokemonList()):
            await switchPokemon(trainer, ctx, client)
    if pokemon.getHp() == 0:
        await sendFaintedEmbed(ctx, pokemon)


async def playerPokemonFainted(trainers, ctx, client):
    for trainer in trainers:
        currentPokemon = trainer.getCarryPokemonList()[0]
        if currentPokemon.getHp() == 0:
            await sendFaintedEmbed(ctx, currentPokemon)
            if 0 < any(pkm.getHp() for pkm in trainer.getCarryPokemonList()):
                await switchPokemon(trainer, ctx, client)


async def wildAttackTurn(trainer, wildPokemon, ctx, client):
    trainerAction = await battleMenu(trainer, wildPokemon, False, ctx, client)
    while trainerAction["displayMenu"]:
        trainerAction = await battleMenu(trainer, wildPokemon, False, ctx, client)
    print(trainerAction)
    global messages
    if trainerAction["run"]:
        runEmbed = discord.Embed(title="Run", description="Got away safely", color=0x45ba36)
        runEmbed.set_footer(text="_" * 90)
        await ctx.send(embed=runEmbed)
        messages += 1
        return False
    elif trainerAction["useItem"]:
        useItemEmbed = discord.Embed(title="Use Item", description=f"{trainer.getName()} used <item-name>", color=0x45ba36)
        useItemEmbed.set_footer(text="_" * 90)
        await ctx.send(embed=useItemEmbed)
        messages += 1
        await moveHit(wildPokemon, trainer.getCarryPokemonList()[0], wildPokemon.getMoves()["move" + str(random.randint(1, len(wildPokemon.getMoves())))], ctx)
        await wildPokemonFainted(trainer, wildPokemon, ctx, client)
        return True
    elif trainerAction["switch"]:
        await moveHit(wildPokemon, trainer.getCarryPokemonList()[0], wildPokemon.getMoves()["move" + str(random.randint(1, len(wildPokemon.getMoves())))], ctx)
        await wildPokemonFainted(trainer, wildPokemon, ctx, client)
        return True
    elif trainerAction["move"]:
        trainerPokemon = trainer.getCarryPokemonList()[0]
        if trainerPokemon.getStat("speed").getStatValue() > wildPokemon.getStat("speed").getStatValue():
            await moveHit(trainerPokemon, wildPokemon, trainerAction["move"], ctx)
            await wildPokemonFainted(trainer, wildPokemon, ctx, client)
            if all(pkm.getHp() for pkm in [trainerPokemon, wildPokemon]) > 0:
                await moveHit(wildPokemon, trainerPokemon, wildPokemon.getMoves()["move" + str(random.randint(1, len(wildPokemon.getMoves())))], ctx)
                await wildPokemonFainted(trainer, wildPokemon, ctx, client)
        else:
            await moveHit(wildPokemon, trainerPokemon, wildPokemon.getMoves()["move" + str(random.randint(1, len(wildPokemon.getMoves())))], ctx)
            await wildPokemonFainted(trainer, wildPokemon, ctx, client)
            if all(pkm.getHp() for pkm in [trainerPokemon, wildPokemon]) > 0:
                await moveHit(trainerPokemon, wildPokemon, trainerAction["move"], ctx)
                await wildPokemonFainted(trainer, wildPokemon, ctx, client)
        return True


async def playerAttackTurn(trainer1, trainer2, ctx, client):
    async def activeTrainerAction(activeTrainer, inactiveTrainer):
        action = await battleMenu(activeTrainer, inactiveTrainer.getCarryPokemonList()[0], True, ctx, client)
        while action["displayMenu"]:
            action = await battleMenu(activeTrainer, inactiveTrainer.getCarryPokemonList()[0], True, ctx, client)
        print(action)
        global messages
        if action["useItem"]:
            useItemEmbed = discord.Embed(title="Use Item", description=f"{activeTrainer.getName()} used <item-name>",
                                         color=0x45ba36)
            useItemEmbed.set_footer(text="_" * 90)
            await ctx.send(embed=useItemEmbed)
            messages += 1
            return False
        elif action["move"]:
            return action["move"]

    trainerTurns = {"trainer1": await activeTrainerAction(trainer1, trainer2),
                    "trainer2": await activeTrainerAction(trainer2, trainer1)}
    trainerPokemons = {"trainer1": trainer1.getCarryPokemonList()[0],
                       "trainer2": trainer2.getCarryPokemonList()[0]}

    if trainerTurns["trainer1"] and trainerTurns["trainer2"]:
        if trainerPokemons["trainer1"].getStat("speed").getStatValue() > trainerPokemons["trainer2"].getStat("speed").getStatValue():
            await moveHit(trainerPokemons["trainer1"], trainerPokemons["trainer2"], trainerTurns["trainer1"], ctx)
            await playerPokemonFainted([trainer1, trainer2], ctx, client)
            if all(trainerPokemons[trainerPokemon].getHp() for trainerPokemon in trainerPokemons) > 0:
                await moveHit(trainerPokemons["trainer2"], trainerPokemons["trainer1"], trainerTurns["trainer2"], ctx)
                await playerPokemonFainted([trainer1, trainer2], ctx, client)
        else:
            await moveHit(trainerPokemons["trainer2"], trainerPokemons["trainer1"], trainerTurns["trainer2"], ctx)
            await playerPokemonFainted([trainer1, trainer2], ctx, client)
            if all(trainerPokemons[trainerPokemon].getHp() for trainerPokemon in trainerPokemons) > 0:
                await moveHit(trainerPokemons["trainer1"], trainerPokemons["trainer2"], trainerTurns["trainer1"], ctx)
                await playerPokemonFainted([trainer1, trainer2], ctx, client)
    else:
        for trainerTurn in trainerTurns:
            if trainerTurn == "trainer1":
                active = "trainer1"
                inactive = "trainer2"
            else:
                active = "trainer2"
                inactive = "trainer1"
            if trainerTurns[active]:
                await moveHit(trainerPokemons[active], trainerPokemons[inactive], trainerTurns[active], ctx)
                if active == "trainer1":
                    await playerPokemonFainted([trainer1, trainer2], ctx, client)
                else:
                    await playerPokemonFainted([trainer1, trainer2], ctx, client)


async def wildBattle(trainer, ctx, client):
    wildPokemon = Pokemon(random.randint(1, 500), trainer.getCarryPokemonList()[0].getLevel())
    await ctx.send(embed=getPokemonEmbed(f"{trainer.getName()} uses ", trainer.getCarryPokemonList()[0]))
    await ctx.send(embed=getPokemonEmbed("Wild pokemon: ", wildPokemon))
    continueTurns = True
    await asyncio.sleep(5)
    while wildPokemon.getHp() > 0 and 0 < any(pkm.getHp() for pkm in trainer.getCarryPokemonList()) and continueTurns:
        global messages
        await ctx.channel.purge(limit=int(messages))
        messages = 0
        await ctx.send(embed=getPokemonEmbed(ctx, "", trainer.getCarryPokemonList()[0], wildPokemon))
        continueTurns = await wildAttackTurn(trainer, wildPokemon, ctx, client)
        await asyncio.sleep(3)


async def playerBattle(players, ctx, client, roomAssignments):
    await roomAssignments["challenger"].send(embed=getPokemonEmbed(ctx, f"{players[0].getName()} uses ", players[0].getCarryPokemonList()[0]))
    await roomAssignments["challenged"].send(embed=getPokemonEmbed(ctx, f"{players[1].getName()} uses ", players[1].getCarryPokemonList()[0]))
    while 0 < any(pkm.getHp() for pkm in players[0].getCarryPokemonList()) and 0 < any(pkm.getHp() for pkm in players[1].getCarryPokemonList()):
        await playerAttackTurn(players[0], players[1], ctx, client)


# fainted in multi hit loops doesn't end loop
# pokemon embed with status effect
# recoil healed -... damage
