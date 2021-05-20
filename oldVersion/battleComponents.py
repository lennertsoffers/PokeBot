import random


def calculateExperience(winner, loser, wild=True):
    a = 1
    if not wild:
        a = 1.5
    xp = ((a * loser.getBaseExperience() * loser.getLevel()) / 5) * \
         (((2 * loser.getLevel() + 10) / (loser.getLevel() + winner.getLevel() + 10)) ** 2.5) + 1
    return round(xp)


def calculateDamage(pkm, move, target):
    def calculateStat(value, inBattleStat):
        if inBattleStat >= 0:
            value *= ((2 + inBattleStat) / 2)
        else:
            value *= (2 / (2 + abs(inBattleStat)))
        return value

    def attackMiss(pAccuracy, evasion, mAccuracy):
        if not mAccuracy:
            mAccuracy = 100
        if pAccuracy >= 0:
            t = mAccuracy * ((3 + pAccuracy) / 3)
        else:
            t = mAccuracy * (3 / (3 + abs(pAccuracy)))
        if evasion > 0:
            t *= (3 / (3 + evasion))
        else:
            t *= ((3 + abs(evasion)) / 3)
        if random.randint(1, 100) <= round(t):
            return False
        return True

    def nextPokemonFlinch(flinchChance):
        if flinchChance > 0 and random.randint(1, 100) <= flinchChance:
            return True
        return False

    def isCriticalHit(critRate):
        if critRate == 0:
            if random.randint(0, 100) <= 6:
                return True
        elif critRate == 1:
            if random.randint(0, 100) <= 13:
                return True
        elif critRate == 2:
            if random.randint(0, 100) <= 25:
                return True
        elif critRate == 3:
            if random.randint(0, 100) <= 33:
                return True
        else:
            if random.randint(0, 100) <= 50:
                return True
        return False

    multiplier = 1
    moveType = move.getType().getName()
    print()
    print(pkm.getName(), "uses", move.getName())
    if move.getPower():
        if move.getDamageClass() == "physical":
            a = calculateStat(pkm.getStat("attack").getStatValue(), pkm.getBattleStats()["attack"])
            d = calculateStat(target.getStat("defense").getStatValue(), target.getBattleStats()["defense"])
        else:
            a = calculateStat(pkm.getStat("special-attack").getStatValue(), pkm.getBattleStats()["special-attack"])
            d = calculateStat(target.getStat("special-defense").getStatValue(),
                              target.getBattleStats()["special-defense"])
        if attackMiss(pkm.getBattleStats()["accuracy"], target.getBattleStats()["evasion"], move.getAccuracy()):
            damage = 0
            hit = 0
        else:
            for pkmType in target.getTypes():
                if moveType in pkmType.getNoDamageFrom():
                    multiplier *= 0
                    print("this move doesn't affect this type")
                else:
                    if moveType in pkmType.getHalfDamageFrom() and multiplier != 0.5:
                        multiplier *= 0.5
                        print("it was not very effective")
                    if moveType in pkmType.getDoubleDamageFrom() and multiplier != 2:
                        multiplier *= 2
                        print("it was very effective")
            damage = (((((2 * pkm.getLevel()) / 5) + 2) * move.getPower() * (a / d)) / 50) * multiplier
            if isCriticalHit(pkm.getBattleStats()["criticalHitRate"]):
                damage *= 2
                print("a critical hit!")
            hit = 1
    else:
        hit = 1
        damage = 0
    return round(damage), hit, nextPokemonFlinch(move.getFlinchChance())


def calculateStatChanges(move, pokemon, target, damage):
    pokemonInBattleStats = pokemon.getBattleStats()
    targetBattleStats = target.getBattleStats()
    if move.getAilment()["name"] != "-1":
        print(move.getAilment()["name"])
    if move.getCriticalRate() > 0:
        pokemonInBattleStats["criticalHitRate"] += 1
        print(f"{pokemon.getName()} critical hit ratio rose!")
    if move.getHealing() != 0:
        pokemon.addHp(move.getHealing())
    if move.getDrain() != 0:
        pokemon.addHp(round(damage * (move.getDrain() / 100)))
    if not move.getPower():
        for statChange in move.getStatChanges():
            if -6 < pokemonInBattleStats[statChange["name"]] < 6 and -6 < targetBattleStats[statChange["name"]] < 6:
                if statChange["change"] == 1:
                    pokemonInBattleStats[statChange["name"]] += statChange["change"]
                    print(f"{pokemon.getName()}'s {statChange['name']} rose!")
                elif statChange["change"] == 2:
                    pokemonInBattleStats[statChange["name"]] += statChange["change"]
                    print(f"{pokemon.getName()}'s {statChange['name']} sharply rose!")
                elif statChange["change"] == 3:
                    pokemonInBattleStats[statChange["name"]] += statChange["change"]
                    print(f"{pokemon.getName()}'s {statChange['name']} rose drastically!")
                elif statChange["change"] == -1:
                    targetBattleStats[statChange["name"]] += statChange["change"]
                    print(f"{target.getName()}'s {statChange['name']} fell!")
                elif statChange["change"] == -2:
                    targetBattleStats[statChange["name"]] += statChange["change"]
                    print(f"{target.getName()}'s {statChange['name']} harshly fell!")
                elif statChange["change"] == -3:
                    targetBattleStats[statChange["name"]] += statChange["change"]
                    print(f"{target.getName()}'s {statChange['name']} severely fell!")
            else:
                print("nothing happened!")
        pokemon.setBattleStats(pokemonInBattleStats)
        target.setBattleStats(targetBattleStats)


def attackTurn(pokemon, target, move):
    if not move.getMultiHitType() == "single":
        if move.getMultiHitType() == "double":
            hits = 2
        else:
            randHit = random.randint(1, 100)
            if randHit <= 35:
                hits = 2
            elif randHit <= 70:
                hits = 3
            elif randHit <= 85:
                hits = 4
            else:
                hits = 5
    else:
        hits = 1
    hitCount = 1
    stopHit = False
    flinch = False
    while hitCount <= hits and not stopHit:
        damage, hit, flinch = calculateDamage(pokemon, move, target)
        if hit == 1:
            if damage > 0:
                print(damage)
                target.lowerHp(damage)
            hitCount += 1
            calculateStatChanges(move, pokemon, target, damage)
        elif hit == 0:
            print("attack missed")
            stopHit = True
    if hits > 1:
        print("it hit", hitCount - 1, "time(s)")
    return flinch


def battleMenu(pokemon1, pokemon2, moves):
    print()
    print("|__________________________________________________________|")
    print("| Your Pokemon:", pokemon1.getName().ljust(15), "lv",
          str(pokemon1.getLevel()).ljust(3), "      ", str(pokemon1.getHp()).ljust(5), "       |")
    print("| Enemy Pokemon:", pokemon2.getName().ljust(14), "lv",
          str(pokemon2.getLevel()).ljust(3), "      ", str(pokemon2.getHp()).ljust(5), "       |")
    print("|__________________________________________________________|")
    print("| Moves:                                                   |")
    for move in moves:
        print("|", moves[move].getName().ljust(15), "     ", str(moves[move].getPower()).ljust(5),
              "                             |")
    print("|__________________________________________________________|")
    choice = int(input(">"))
    while not (0 < choice < 5 and moves["move" + str(choice)].getPp() > 0):
        choice = int(input(">"))
    return "move" + str(choice)
