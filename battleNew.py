import random
from PokeBot.classes.Pokemon import Pokemon


def moveMenu(trainer):
    moves = trainer.getCarryPokemonList()[0].getMoves()
    moveIndex = 1
    print("|------------------------------|")
    for moveKey in moves:
        move = moves[moveKey]
        print(f"| {moveIndex}: {move.getName().ljust(15)}   {str(move.getPower()).ljust(8)}|")
        moveIndex += 1
    print("|------------------------------|")
    moveIndex = input("| > ")
    while moveIndex not in ["1", "2", "3", "4"]:
        moveIndex = input("| > ")
    return moves["move" + str(moveIndex)]


def battleMenu(trainer, target):
    def printPokemons(trainerToPrint):
        carryPokemonIndex = 1
        for carryPokemon in trainerToPrint.getCarryPokemonList():
            print("| " + str(carryPokemonIndex) + ": "
                  + carryPokemon.getName().ljust(15) + str(carryPokemon.getHp()).ljust(11) + "|")
            carryPokemonIndex += 1

    menuOutput = {
        "move": None,
        "run": False,
        "switch": False,
        "useItem": False,
        "displayMenu": False
    }
    print("|------------------------------|")
    print("| 1: Fight                     |")
    print("| 2: Run                       |")
    print("| 3: Pokemon                   |")
    print("| 4: Bag                       |")
    print("|------------------------------|")
    action = input("| > ")
    while action not in ["1", "2", "3", "4"]:
        action = input("| > ")
    if action == "1":
        menuOutput["move"] = moveMenu(trainer)
    elif action == "2":
        if trainer.getCarryPokemonList()[0].getStat("speed").getStatValue() < target.getStat("speed").getStatValue():
            print("| Cannot escape                |")
            menuOutput["displayMenu"] = True
        else:
            menuOutput["run"] = True
    elif action == "3":
        menuOutput["switch"] = True
        printPokemons(trainer)
        trainer.switchCarryPokemon((int(input("| first pokemon: ")) - 1), (int(input("| second pokemon: ")) - 1))
        printPokemons(trainer)
    elif action == "4":
        menuOutput["useItem"] = True
    return menuOutput


def attackTurn(trainer, wildPokemon):
    def canAttack(pokemon, target, move):
        nvStatus = pokemon.getNonVolatileStatus()
        vStatus = pokemon.getVolatileStatus()
        print(vStatus)
        mAccuracy = move.getAccuracy()
        pAccuracy = pokemon.getBattleStats()["accuracy"]
        pEvasion = pokemon.getBattleStats()["evasion"]

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
        if random.randint(1, 100) <= round(t):
            canAttackOutput = {"attack": True, "message": "", "before": False}
        else:
            canAttackOutput = {"attack": False, "message": pokemon.getName() + " missed", "before": False}

        if nvStatus["PAR"]:
            canAttackOutput = {"attack": False, "message": pokemon.getName() + " is paralyzed and can't move", "before": True}
        elif nvStatus["SLP"] != -1:
            if nvStatus["SLP"] > 0:
                canAttackOutput = {"attack": False, "message": pokemon.getName() + " is fast asleep", "before": True}
                nvStatus["SLP"] -= 1
            else:
                canAttackOutput = {"attack": True, "message": pokemon.getName() + " woke up!", "before": True}
                nvStatus["SLP"] -= 1
        elif nvStatus["FRZ"] != -1:
            if nvStatus["FRZ"] > 0:
                canAttackOutput = {"attack": False, "message": pokemon.getName() + " if frozen solid", "before": True}
                nvStatus["FRZ"] -= 1
            else:
                canAttackOutput = {"attack": True, "message": pokemon.getName() + " broke free!", "before": True}
        elif vStatus["flinch"]:
            canAttackOutput = {"attack": False, "message": pokemon.getName() + " flinched", "before": False}
            vStatus["flinch"] = False

        pokemon.setVolatileStatus(vStatus)
        pokemon.setNonVolatileStatus(nvStatus)
        return canAttackOutput

    trainerAction = battleMenu(trainer, wildPokemon)
    while trainerAction["displayMenu"]:
        trainerAction = battleMenu(trainer, wildPokemon)
    if trainerAction["run"]:
        print("Got away safely")
        return -1
    elif trainerAction["useItem"]:
        print("Use item")
        return -1
    elif trainerAction["move"]:
        trainerPokemon = trainer.getCarryPokemonList()[0]
        # if trainerPokemon.getStat("speed").getStatValue() > wildPokemon.getStat("speed").getStatValue():
        print(canAttack(trainerPokemon, wildPokemon, trainerAction["move"]))


def wildBattle(trainer):
    wildPokemon = Pokemon(random.randint(1, 500), 100)
    print(trainer.getName(), "uses", trainer.getCarryPokemonList()[0].getName())
    while True:
        attackTurn(trainer, wildPokemon)
