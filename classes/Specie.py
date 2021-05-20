import requests
import json


class Specie:
    def __init__(self, identifier):
        data = json.loads(str(requests.get(f"https://pokeapi.co/api/v2/pokemon-species/{identifier}").text))
        self.genderRate = data["gender_rate"]
        self.captureRate = data["capture_rate"]
        self.isLegendary = data["is_legendary"]
        self.isMythical = data["is_mythical"]
        self.hatchCounter = data["hatch_counter"]
        self.growthRate = data["growth_rate"]

    def getGenderRate(self):
        return self.genderRate

    def getCaptureRate(self):
        return self.captureRate

    def getIsLegendary(self):
        return self.isLegendary

    def getIsMythical(self):
        return self.isMythical

    def getHatchCounter(self):
        return self.hatchCounter

    def getGrowthRate(self):
        return self.growthRate
