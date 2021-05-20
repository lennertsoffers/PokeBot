import requests
import json
import random


class Stat:
    def __init__(self, identifier, baseStat, level):
        data = json.loads(str(requests.get(f"https://pokeapi.co/api/v2/stat/{identifier}").text))
        self.id = data["id"]
        self.name = data["name"]
        try:
            self.damageClass = data["move_damage_class"]["name"]
        except TypeError:
            self.damageClass = "none"
        self.baseStat = baseStat
        self.iv = random.randint(0, 15)
        if self.id == 1:
            self.statValue = round(((2 * baseStat + self.iv) * level) / 100 + level + 10)
        else:
            self.statValue = round(((2 * baseStat + self.iv) * level) / 100 + 5)
        self.previousStat = self.statValue

    def getId(self):
        return self.id

    def getName(self):
        return self.name

    def getDamageClass(self):
        return self.damageClass

    def getBaseStat(self):
        return self.baseStat

    def getStatValue(self):
        return self.statValue

    def getPreviousStat(self):
        return self.previousStat

    def levelUp(self, level):
        self.previousStat = self.statValue
        if self.id == 1:
            self.statValue = round(((2 * self.baseStat + self.iv) * level) / 100 + level + 10)
        else:
            self.statValue = round(((2 * self.baseStat + self.iv) * level) / 100 + 5)


