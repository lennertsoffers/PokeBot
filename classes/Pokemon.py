import requests
import json
import random
from PokeBot.classes.Specie import Specie
from PokeBot.classes.Stat import Stat
from PokeBot.classes.Move import Move
from PokeBot.classes.Type import Type


class Pokemon:
    def __init__(self, identifier, level=-1):
        data = json.loads(str(requests.get(f"https://pokeapi.co/api/v2/pokemon/{identifier}").text))
        self.id = data["id"]
        self.name = data["name"]
        self.specie = Specie(identifier)
        if level == -1:
            self.level = random.randint(1, 100)
        else:
            self.level = level

        self.baseExperience = data["base_experience"]
        self.totalExperience = self.calculateTotalXp(self.level, self.specie.getGrowthRate())
        self.nextLevelExperience = self.calculateTotalXp(self.level + 1, self.specie.getGrowthRate())
        self.possibleMoves = []
        self.moves = {}
        moveSets = []
        for pokemonAbleMove in data["moves"]:
            moveName = pokemonAbleMove["move"]["name"]
            learnAt = pokemonAbleMove["version_group_details"][0]["level_learned_at"]
            learnMethod = pokemonAbleMove["version_group_details"][0]["move_learn_method"]["name"]
            moveAddDict = {"name": moveName, "learnAt": learnAt, "method": learnMethod}
            if learnMethod != "egg":
                self.possibleMoves.append(moveAddDict)
            if int(learnAt) <= self.level and learnMethod == "level-up":
                moveSets.append(moveAddDict)
        moveSets = sorted(moveSets, key=lambda x: x["learnAt"])
        moveSets = moveSets[-4:]
        moveIndex = 0
        while moveIndex < len(moveSets):
            self.moves.update({"move" + str(moveIndex + 1): Move(moveSets[moveIndex]["name"])})
            moveIndex += 1

        self.stats = {}
        for stat in data["stats"]:
            newStat = Stat(stat["stat"]["name"], stat["base_stat"], self.level)
            self.stats.update({newStat.getName(): newStat})
        self.hp = self.stats["hp"].getStatValue()
        self.typeList = []
        for pokemonTypeIndex in range(len(data["types"])):
            self.typeList.append(Type(data["types"][pokemonTypeIndex]["type"]["name"]))
        self.inBattleStats = {"attack": 0, "defense": 0, "special-attack": 0, "special-defense": 0, "speed": 0, "accuracy": 0, "evasion": 0, "criticalHitRate": 0}
        self.nonVolatileStatus = {
            "BRN": False,
            "FRZ": False,
            "PAR": False,
            "PSN": False,
            "SLP": False
        }
        self.volatileStatus = {
            "bound": False,
            "cantEscape": False,
            "confusion": False,
            "curse": False,
            "flinch": False,
            "encore": False,
            "identified": False,
            "infatuation": False,
            "leechSeed": False,
            "nightmare": False,
            "telekinesis": False
        }
        self.volatileBattleStatus = {
            "aquaRing": False,
            "chargingTurn": False,
            "defenseCurl": False,
            "rooting": False,
            "magicLevitation": False,
            "protection": False,
            "recharging": False
        }

    def getId(self):
        return self.id

    def getName(self):
        return self.name

    def getBaseExperience(self):
        return self.baseExperience

    def getTotalExperience(self):
        return self.totalExperience

    def getNextLevelExperience(self):
        return self.nextLevelExperience

    def getExperienceDifference(self):
        return self.nextLevelExperience - self.totalExperience

    def addExperience(self, experience):
        self.totalExperience += experience
        if self.totalExperience >= self.nextLevelExperience:
            self.levelUp()

    def getLevel(self):
        return self.level

    def levelUp(self):
        while self.totalExperience >= self.nextLevelExperience:
            self.level += 1
            self.nextLevelExperience = self.calculateTotalXp(self.level, self.specie.getGrowthRate())
            print("-----------------------------------")
            print(self.name, "leveled up to level", self.level)
            for selectedStat in self.stats:
                self.stats[selectedStat].levelUp(self.level)
                print(str(self.stats[selectedStat].getName()).ljust(15), ":\t", self.stats[selectedStat].getPreviousStat(), "\t->\t", self.stats[selectedStat].getStatValue())
            cont = input(">")
            while cont != "":
                cont = input(">")

    def getSpecie(self):
        return self.specie

    def getMoves(self):
        return self.moves

    def addMove(self, moveName):
        moveNameList = []
        for move in self.moves:
            moveNameList.append(self.moves[move].getName())
        if any(dictItem["name"] == moveName for dictItem in self.possibleMoves) and moveName not in moveNameList:
            if len(self.moves) == 4:
                print("Choose move to delete:")
                for move in self.moves:
                    print(move, "\t", self.moves[move].getName(), "\t", self.moves[move].getPower())
                toChange = input("Choose move: ")
                self.moves["move" + str(toChange)] = Move(moveName)
            else:
                self.moves["move" + str(len(self.moves) + 1)] = Move(moveName)
        else:
            print(f"{self.name} cannot learn {moveName}")

    def getPossibleMoves(self):
        return self.possibleMoves

    def getStats(self):
        return self.stats

    def getStat(self, statName):
        return self.stats[statName]

    def calculateTotalXp(self, level, growthRate):
        if growthRate == "slow":
            xp = (5 * (level ** 3)) / 4
        elif growthRate == "medium":
            xp = level ** 3
        elif growthRate == "fast":
            xp = (4 * (level ** 3)) / 5
        elif growthRate == "medium slow":
            xp = ((6 / 5) * (level ** 3)) - (15 * (level ** 2)) + (100 * level) - 140
        elif growthRate == "slow then very fast":
            if level < 50:
                xp = ((level ** 3) * (100 - level)) / 50
            elif 50 <= level < 68:
                xp = ((level ** 3) * (150 - level)) / 100
            elif 68 <= level < 98:
                xp = ((level ** 3) * ((1911 - (10 * level)) / 3)) / 500
            else:
                xp = ((level ** 3) * (160 - level)) / 100
        else:
            if level < 15:
                xp = (level ** 3) * ((((level + 1) / 3) + 24) / 50)
            elif 15 <= level < 36:
                xp = (level ** 3) * ((level + 14) / 50)
            else:
                xp = (level ** 3) * (((level / 2) + 32) / 50)
        return round(xp)

    def getHp(self):
        return self.hp

    def addHp(self, amount):
        if amount < 0:
            self.lowerHp(abs(amount))
            print(self.name, "got", abs(amount), "recoil")
        else:
            hpDifference = self.stats["hp"].getStatValue() - self.hp
            if hpDifference > amount:
                self.hp += amount
                print(self.name, "healed", amount, "hp")
            else:
                self.hp = self.stats["hp"].getStatValue()
                print(self.name, "healed", hpDifference, "hp")

    def lowerHp(self, amount):
        self.hp -= amount
        if self.hp < 0:
            self.hp = 0

    def getTypes(self):
        return self.typeList

    def getBattleStats(self):
        return self.inBattleStats

    def setBattleStats(self, inBattleStats):
        self.inBattleStats = inBattleStats

    def getNonVolatileStatus(self):
        return self.nonVolatileStatus

