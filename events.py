# events.py

import random
from colorama import Fore, Style
from rich.console import Console

console = Console()

class EventManager:
    def __init__(self):
        self.events = [
            {
                "name": "Resource Surge",
                "description": "A sudden surge in Light resources boosts your civilization.",
                "effect": lambda game: game.resources.add_resources({"Light": 50}),
                "chance": 0.1  # 10% chance each turn
            },
            {
                "name": "Water Scarcity",
                "description": "Water resources are scarce this turn.",
                "effect": lambda game: game.resources.modify_resource("Water", -30),
                "chance": 0.05  # 5% chance
            },
            {
                "name": "Energy Boost",
                "description": "An energy boost increases your civilization's efficiency.",
                "effect": lambda game: game.resources.add_resources({"Energy": 30}),
                "chance": 0.1
            },
            {
                "name": "Population Boom",
                "description": "A sudden boom in population due to favorable conditions.",
                "effect": lambda game: game.population.modify_population(10),
                "chance": 0.05
            },
            {
                "name": "Land Expansion",
                "description": "New lands have been discovered, expanding your civilization's territory.",
                "effect": lambda game: game.resources.add_resources({"Land": 100}),
                "chance": 0.07
            },
            {
                "name": "Energy Drain",
                "description": "A mysterious energy drain affects your civilization.",
                "effect": lambda game: game.resources.modify_resource("Energy", -40),
                "chance": 0.05
            },
            {
                "name": "Technological Advancement",
                "description": "A technological breakthrough improves resource generation.",
                "effect": lambda game: game.resources.add_resources({"Light": 20, "Energy": 20}),
                "chance": 0.08
            },
            {
                "name": "Metal Rush",
                "description": "A surge in demand for Metal resources boosts your Metal production.",
                "effect": lambda game: game.resources.add_resources({"Metal": 50}),
                "chance": 0.06
            },
            {
                "name": "Food Festival",
                "description": "A grand food festival enhances your Food resources.",
                "effect": lambda game: game.resources.add_resources({"Food": 100}),
                "chance": 0.04
            },
            {
                "name": "Tech Breakthrough",
                "description": "A breakthrough in technology accelerates your Technology research.",
                "effect": lambda game: game.resources.add_resources({"Technology": 50}),
                "chance": 0.05
            },
            {
                "name": "Meteor Strike",
                "description": "A meteor strike damages your civilization, reducing resources.",
                "effect": lambda game: game.resources.modify_resource("Land", -50),
                "chance": 0.03
            },
            {
                "name": "Trade Agreement",
                "description": "A trade agreement boosts your resource imports.",
                "effect": lambda game: game.resources.add_resources({"Metal": 25, "Technology": 25}),
                "chance": 0.07
            },
            {
                "name": "Natural Disaster",
                "description": "A natural disaster has struck, reducing your population.",
                "effect": lambda game: game.population.modify_population(-5),
                "chance": 0.04
            },
            {
                "name": "Cultural Renaissance",
                "description": "A cultural renaissance boosts your population's happiness.",
                "effect": lambda game: game.population.modify_population(5),
                "chance": 0.05
            },
            {
                "name": "Scientific Breakthrough",
                "description": "A scientific breakthrough significantly enhances your Technology production.",
                "effect": lambda game: game.resources.add_resources({"Technology": 100}),
                "chance": 0.02
            },
            {
                "name": "Economic Boom",
                "description": "An economic boom increases your resource generation rates.",
                "effect": lambda game: game.resources.add_resources({"Light": 20, "Water": 20, "Energy": 20}),
                "chance": 0.03
            }
        ]

    def trigger_event(self, game):
        triggered = False
        for event in self.events:
            if random.random() < event["chance"]:
                console.print(f"\n[bold cyan][Event] {event['name']}:[/bold cyan] {event['description']}")
                event["effect"](game)
                triggered = True
        if not triggered:
            console.print("[bold cyan]\n[Event] No events this turn.[/bold cyan]")
