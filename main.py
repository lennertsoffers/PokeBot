from classes.Pokemon import Pokemon
from classes.Trainer import Trainer
from battleNew import wildBattle
from battleNew import playerBattle
import random


# Create trainer and starter pokemon
def createTrainer():
    trainer = Trainer("test")
    # trainer = Trainer(input("Name: "))
    trainer.addPokemon(chooseStarter())
    return trainer


def chooseStarter():
    choice = "3"
    # choice = input("Choose your starter: ").lower()
    # while choice not in ["charmander", "bulbasaur", "squirtle", "rotom", "1", "4", "7"]:
    #     choice = input("Choose your starter: ").lower()
    starter = Pokemon(choice, level=30)
    return starter


trainer1 = createTrainer()
trainer1.addPokemon(Pokemon(random.randint(1, 500), 30))
# trainer1.addPokemon(Pokemon(random.randint(1, 500), 30))
# trainer1.addPokemon(Pokemon(random.randint(1, 500), 30))
# trainer1.addPokemon(Pokemon(random.randint(1, 500), 30))
# trainer1.addPokemon(Pokemon(random.randint(1, 500), 30))
for PKM in trainer1.getPokemonList():
    trainer1.depositCarryPokemon(trainer1.getPokemonList()[PKM])

# trainer2 = createTrainer()
# trainer2.addPokemon(Pokemon(random.randint(1, 500), 30))
# # trainer2.addPokemon(Pokemon(random.randint(1, 500), 30))
# # trainer2.addPokemon(Pokemon(random.randint(1, 500), 30))
# # trainer2.addPokemon(Pokemon(random.randint(1, 500), 30))
# # trainer2.addPokemon(Pokemon(random.randint(1, 500), 30))
# for PKM in trainer2.getPokemonList():
#     trainer2.depositCarryPokemon(trainer2.getPokemonList()[PKM])

wildBattle(trainer1)
