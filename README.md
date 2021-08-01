# PokeBot

A Python that brings the old school mechanics of Pokémon on the Nintendo DS to Discord

## Description

The goal of this PokeBot is to make a Pokémon game with the same mechanics as the games on game consoles. It is written in Python and makes use of the PokéAPI.

You control the bot with adding reactions and not with commands which makes it easy to use.

Mechanics included in the Bot:
* Trainers with inventory
* Leveling system
* Learning your Pokémon new moves
* Battles vs randomly generated Pokémon including status effects, life steal and more of the original battle mechanics
* PvP (work in progress)


## Set up this Bot yourself

* Clone this repository
* Insert your Discord Bot token in the bot/bot.py file
* Open a shell and change directory to the PokeBot folder
* Create these text channels:
    * new-players
    * free-roam
    * battle-requests
* Run `python3 bot.py` or `py bot.py` on Windows
