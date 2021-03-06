
class Trainer:
    def __init__(self, discordId, name=None, profilePicture=None):
        self.name = name
        self.pokemonList = []
        self.carryPokemonList = []
        self.inventoryList = []
        self.discordId = discordId
        self.profilePicture = profilePicture

    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name

    def getPokemonList(self):
        return self.pokemonList

    def getCarryPokemonList(self):
        return self.carryPokemonList

    def switchCarryPokemon(self, pokemon2, pokemon1=0):
        if self.carryPokemonList[pokemon2].getHp() > 0:
            self.carryPokemonList[pokemon1], self.carryPokemonList[pokemon2] = self.carryPokemonList[pokemon2], self.carryPokemonList[pokemon1]
            for pokemon in self.carryPokemonList:
                print(pokemon.getName())
            return True
        return False

    def depositCarryPokemon(self, pokemon):
        if len(self.carryPokemonList) < 6:
            if pokemon in self.pokemonList:
                if pokemon not in self.carryPokemonList:
                    self.carryPokemonList.append(pokemon)
                else:
                    print("This pokemon is already in your party")
            else:
                print("You don't have this pokemon")
        else:
            print("You carry already 6 pokemon")

    def getInventoryList(self):
        return self.inventoryList

    def addPokemon(self, pokemon):
        self.pokemonList.append(pokemon)
        if len(self.carryPokemonList) < 6:
            self.carryPokemonList.append(pokemon)

    def getDiscordId(self):
        return self.discordId

    def setDiscordId(self, identifier):
        self.discordId = identifier

    def getProfilePicture(self):
        return self.profilePicture

    def setProfilePicture(self, url):
        self.profilePicture = url
