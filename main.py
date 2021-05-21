from PokeBot.classes.Pokemon import Pokemon
from PokeBot.classes.Trainer import Trainer
from PokeBot.battleNew import wildBattle
import random


# Create trainer and starter pokemon
def createTrainer():
    trainer = Trainer("test")
    # trainer = Trainer(input("Name: "))
    trainer.addPokemon(chooseStarter())
    return trainer


def chooseStarter():
    choice = "sandshrew"
    # choice = input("Choose your starter: ").lower()
    # while choice not in ["charmander", "bulbasaur", "squirtle", "rotom", "1", "4", "7"]:
    #     choice = input("Choose your starter: ").lower()
    starter = Pokemon(choice, level=38)
    starter.lowerHp(starter.getHp() - 1)
    return starter


newTrainer = createTrainer()
pkm2 = Pokemon(random.randint(1, 500), 30)
pkm2.lowerHp(pkm2.getHp() - 1)
newTrainer.addPokemon(pkm2)
# newTrainer.addPokemon(Pokemon(random.randint(1, 500), 30))
# newTrainer.addPokemon(Pokemon(random.randint(1, 500), 30))
# newTrainer.addPokemon(Pokemon(random.randint(1, 500), 30))
# newTrainer.addPokemon(Pokemon(random.randint(1, 500), 30))
for PKM in newTrainer.getPokemonList():
    newTrainer.depositCarryPokemon(newTrainer.getPokemonList()[PKM])
wildBattle(newTrainer)
# newTrainer.addPokemon(Pokemon(random.randint(10, 500)))
# for PKM in newTrainer.getPokemonList():
#     print(newTrainer.getPokemonList()[PKM].getName())
# selectedPokemon = newTrainer.getPokemonList()[input("Pokemon: ")]
# action = input("action: ")
# while action == "" and selectedPokemon.getHp() > 0:
#     wildBattle(selectedPokemon)
#     action = input("action: ")



