
class Trainer:
    def __init__(self, name=None):
        self.name = name
        self.pokemonList = {}
        self.carryPokemonList = []
        self.inventoryList = []

    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name

    def getPokemonList(self):
        return self.pokemonList

    def getCarryPokemonList(self):
        return self.carryPokemonList

    def switchCarryPokemon(self, pokemon1, pokemon2):
        self.carryPokemonList[pokemon1], self.carryPokemonList[pokemon2] = self.carryPokemonList[pokemon2], self.carryPokemonList[pokemon1]

    def depositCarryPokemon(self, pokemon):
        if len(self.carryPokemonList) < 6:
            self.carryPokemonList.append(pokemon)
        else:
            print("You carry already 6 pokemon")

    def getInventoryList(self):
        return self.inventoryList

    def addPokemon(self, pokemon):
        self.pokemonList.update({pokemon.getName(): pokemon})
