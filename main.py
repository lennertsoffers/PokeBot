from PokeBot.classes.Pokemon import Pokemon
from PokeBot.classes.Trainer import Trainer
from PokeBot.battleNew import wildBattle


# Create trainer and starter pokemon
def createTrainer():
    trainer = Trainer("test")
    # trainer = Trainer(input("Name: "))
    trainer.addPokemon(chooseStarter())
    return trainer


def chooseStarter():
    choice = "magnemite"
    # choice = input("Choose your starter: ").lower()
    # while choice not in ["charmander", "bulbasaur", "squirtle", "rotom", "1", "4", "7"]:
    #     choice = input("Choose your starter: ").lower()
    starter = Pokemon(choice, level=35)
    return starter


newTrainer = createTrainer()
newTrainer.addPokemon(Pokemon(1, 1))
newTrainer.addPokemon(Pokemon(2, 1))
newTrainer.addPokemon(Pokemon(3, 1))
newTrainer.addPokemon(Pokemon(4, 1))
newTrainer.addPokemon(Pokemon(5, 1))
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



