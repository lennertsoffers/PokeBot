import random
from PokeBot.classes.Pokemon import Pokemon
from PokeBot.oldVersion.battleComponents import attackTurn, calculateExperience, battleMenu


def wildBattle(trainerPokemon):
    wildPokemon = Pokemon(
        random.randint(10, 100),
        random.randint(trainerPokemon.getLevel() - 5, trainerPokemon.getLevel())
    )
    while wildPokemon.getHp() > 0 and trainerPokemon.getHp() > 0:
        if trainerPokemon.getBattleStats()["speed"] >= wildPokemon.getBattleStats()["speed"]:
            move = trainerPokemon.getMoves()[battleMenu(trainerPokemon, wildPokemon, trainerPokemon.getMoves())]
            flinch = attackTurn(trainerPokemon, wildPokemon, move)
            if wildPokemon.getHp() > 0:
                if not flinch:
                    move = wildPokemon.getMoves()["move" + str(random.randint(1, len(wildPokemon.getMoves())))]
                    attackTurn(wildPokemon, trainerPokemon, move)
                else:
                    print(f"{wildPokemon.getName()} flinched")
        else:
            move = wildPokemon.getMoves()["move" + str(random.randint(1, len(wildPokemon.getMoves())))]
            flinch = attackTurn(wildPokemon, trainerPokemon, move)
            if trainerPokemon.getHp() > 0:
                if not flinch:
                    move = trainerPokemon.getMoves()[battleMenu(trainerPokemon, wildPokemon, trainerPokemon.getMoves())]
                    attackTurn(trainerPokemon, wildPokemon, move)
                else:
                    print(f"{trainerPokemon.getName()} flinched")

    trainerPokemon.setBattleStats({"attack": 0,
                                   "defense": 0,
                                   "special-attack": 0,
                                   "special-defense": 0,
                                   "speed": 0,
                                   "accuracy": 0,
                                   "evasion": 0,
                                   "criticalHitRate": 0})
    if wildPokemon.getHp() == 0:
        print(wildPokemon.getName(), "fainted")
        experience = calculateExperience(trainerPokemon, wildPokemon)
        print(trainerPokemon.getName(), "gained", experience, "xp")
        trainerPokemon.addExperience(experience)
    else:
        print(trainerPokemon.getName(), "fainted")
