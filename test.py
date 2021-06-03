from classes.Pokemon import Pokemon
from classes.Trainer import Trainer
from battle.battle import wildBattle
from battle.battle import playerBattle

trainer = Trainer(discordId=1, name='test')
pokemon = Pokemon(identifier=1, level=5)
pokemon2 = Pokemon(identifier=5, level=5)
trainer.addPokemon(pokemon)
trainer.depositCarryPokemon(pokemon)
trainer.depositCarryPokemon(pokemon2)
print(trainer.getCarryPokemonList())
