import requests
import json


class Type:
    def __init__(self, identifier):
        data = json.loads(str(requests.get(f"https://pokeapi.co/api/v2/type/{identifier}").text))
        self.id = data["id"]
        self.name = data["name"]
        damageRelations = data["damage_relations"]
        self.noDamageTo = []
        for entry in damageRelations["no_damage_to"]:
            self.noDamageTo.append(entry["name"])
        self.halfDamageTo = []
        for entry in damageRelations["half_damage_to"]:
            self.halfDamageTo.append(entry["name"])
        self.doubleDamageTo = []
        for entry in damageRelations["double_damage_to"]:
            self.doubleDamageTo.append(entry["name"])
        self.noDamageFrom = []
        for entry in damageRelations["no_damage_from"]:
            self.noDamageFrom.append(entry["name"])
        self.halfDamageFrom = []
        for entry in damageRelations["half_damage_from"]:
            self.halfDamageFrom.append(entry["name"])
        self.doubleDamageFrom = []
        for entry in damageRelations["double_damage_from"]:
            self.doubleDamageFrom.append(entry["name"])

    def getId(self):
        return self.id

    def getName(self):
        return self.name

    def getNoDamageTo(self):
        return self.noDamageTo

    def getHalfDamageTo(self):
        return self.halfDamageTo

    def getDoubleDamageTo(self):
        return self.doubleDamageTo

    def getNoDamageFrom(self):
        return self.noDamageFrom

    def getHalfDamageFrom(self):
        return self.halfDamageFrom

    def getDoubleDamageFrom(self):
        return self.doubleDamageFrom
