import requests
import json
from classes.Type import Type


class Move:
    def __init__(self, identifier):
        data = json.loads(str(requests.get(f"https://pokeapi.co/api/v2/move/{identifier}").text))
        self.id = data["id"]
        self.name = data["name"]
        self.accuracy = data["accuracy"]
        self.flinchChance = data["meta"]["flinch_chance"]

        ailmentName = "-1"
        ailmentChance = "-1"
        if data["meta"]["ailment"]["name"]:
            ailment = data["meta"]["ailment"]["name"]
            ailmentChance = data["meta"]["ailment_chance"]
            if ailment == "paralysis":
                ailmentName = "PAR"
            elif ailment == "burn":
                ailmentName = "BRN"
            elif ailment == "freeze":
                ailmentName = "FRZ"
            elif ailment == "poison":
                ailmentName = "PSN"
            elif ailment == "sleep":
                ailmentName = "SLP"
            elif ailment == "confusion":
                ailmentName = "confusion"
        self.ailment = {"name": ailmentName, "chance": ailmentChance}
        self.criticalRate = data["meta"]["crit_rate"]
        self.pp = data["pp"]
        self.power = data["power"]
        self.damageClass = data["damage_class"]["name"]
        self.type = Type(data["type"]["name"])
        self.drain = data["meta"]["drain"]
        self.healing = data["meta"]["healing"]
        if data["meta"]["min_hits"]:
            if data["meta"]["min_hits"] == data["meta"]["max_hits"]:
                self.multiHitType = "double"
            else:
                self.multiHitType = "random"
        else:
            self.multiHitType = "single"
        self.bound = [data["meta"]["min_turns"], data["meta"]["max_turns"]]
        self.statChanges = []
        for statChange in data["stat_changes"]:
            self.statChanges.append({"name": statChange["stat"]["name"], "change": statChange["change"]})

    def getId(self):
        return self.id

    def getName(self):
        return self.name

    def getAccuracy(self):
        return self.accuracy

    def getFlinchChance(self):
        return self.flinchChance

    def getAilment(self):
        return self.ailment

    def getCriticalRate(self):
        return self.criticalRate

    def getPp(self):
        return self.pp

    def getPower(self):
        return self.power

    def getDamageClass(self):
        return self.damageClass

    def getType(self):
        return self.type

    def getDrain(self):
        return self.drain

    def getHealing(self):
        return self.healing

    def getMultiHitType(self):
        return self.multiHitType

    def getStatChanges(self):
        return self.statChanges
