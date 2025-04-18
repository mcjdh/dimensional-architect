# resources.py

from colorama import Fore, Style
import random
from rich.table import Table
from rich.console import Console

console = Console()

class ResourceManager:
    def __init__(self):
        self.resources = {
            "Light": 100,
            "Water": 100,
            "Land": 0,
            "Energy": 50,
            "Metal": 0,
            "Food": 0,
            "Technology": 0
        }
        self.gather_count = 0  # Tracks the number of times resources have been gathered

    def gather(self):
        console.print("[bold yellow]\n[Action] Gathering resources...[/bold yellow]")
        # Define possible resource gains
        possible_gains = {
            "Light": (5, 15),       # Gain between 5 to 15 Light
            "Water": (10, 20),      # Gain between 10 to 20 Water
            "Energy": (5, 10),      # Gain between 5 to 10 Energy
            "Food": (0, 5)          # Occasionally gain Food
        }
        # Randomly determine gains
        light_gained = random.randint(*possible_gains["Light"])
        water_gained = random.randint(*possible_gains["Water"])
        energy_gained = random.randint(*possible_gains["Energy"])
        food_gained = random.randint(*possible_gains["Food"])

        # Update resources
        self.resources["Light"] += light_gained
        self.resources["Water"] += water_gained
        self.resources["Energy"] += energy_gained
        self.resources["Food"] += food_gained
        self.gather_count += 1

        # Display gains
        gains = []
        if light_gained > 0:
            gains.append(f"+{light_gained} {self.get_resource_symbol('Light')} Light")
        if water_gained > 0:
            gains.append(f"+{water_gained} {self.get_resource_symbol('Water')} Water")
        if energy_gained > 0:
            gains.append(f"+{energy_gained} {self.get_resource_symbol('Energy')} Energy")
        if food_gained > 0:
            gains.append(f"+{food_gained} {self.get_resource_symbol('Food')} Food")

        gains_str = ", ".join(gains) if gains else "No resources gained this turn."
        console.print(f"[bold green][Resource Modification]{gains_str}[/bold green]")

    def generate_automatic_resources(self, population, buildings):
        # Base generation
        light_generated = population.current_population * 2
        water_generated = population.current_population * 1
        energy_generated = int(population.current_population * 0.5)
        metal_generated = population.current_population * 0.5
        food_generated = population.current_population * 1.5
        tech_generated = population.current_population * 0.2

        # Apply building effects
        building_effects = buildings.get_building_effects()
        for building, count in buildings.list_buildings().items():
            if building in building_effects:
                effect = building_effects[building]
                for resource, bonus in effect.items():
                    if resource in self.resources:
                        additional = bonus * count
                        self.resources[resource] += additional
                        console.print(f"[bold magenta][Building Effect]{building} provides +{additional} {self.get_resource_symbol(resource)} {resource}.[/bold magenta]")

        # Now, add the base resource generation
        self.resources["Light"] += light_generated
        self.resources["Water"] += water_generated
        self.resources["Energy"] += energy_generated
        self.resources["Metal"] += metal_generated
        self.resources["Food"] += food_generated
        self.resources["Technology"] += tech_generated

        # Display auto-generated resources
        auto_gains = [
            f"+{light_generated} {self.get_resource_symbol('Light')} Light",
            f"+{water_generated} {self.get_resource_symbol('Water')} Water",
            f"+{energy_generated} {self.get_resource_symbol('Energy')} Energy",
            f"+{metal_generated} {self.get_resource_symbol('Metal')} Metal",
            f"+{food_generated} {self.get_resource_symbol('Food')} Food",
            f"+{tech_generated} {self.get_resource_symbol('Technology')} Technology"
        ]
        auto_gains_str = ", ".join(auto_gains)
        console.print(f"[bold green][Auto-Generated]{auto_gains_str}[/bold green]")

    def spend_resources(self, costs):
        for resource, amount in costs.items():
            if self.resources.get(resource, 0) < amount:
                console.print(f"[bold red][Resource Spend] Not enough {resource}. Required: {amount}, Available: {self.resources.get(resource, 0)}.[/bold red]")
                return False
        for resource, amount in costs.items():
            self.resources[resource] -= amount
        spent_resources = ", ".join([f"{self.get_resource_symbol(res)} {res}: {amt}" for res, amt in costs.items()])
        console.print(f"[bold green][Resource Spend] Spent resources: {spent_resources}.[/bold green]")
        return True

    def add_resources(self, gains):
        for resource, amount in gains.items():
            self.resources[resource] = self.resources.get(resource, 0) + amount
            console.print(f"[bold green][Resource Modification] +{amount} {self.get_resource_symbol(resource)} {resource}.[/bold green]")

    def modify_resource(self, resource, amount):
        if resource in self.resources:
            self.resources[resource] += amount
            if self.resources[resource] < 0:
                self.resources[resource] = 0
            change = f"+{amount}" if amount >= 0 else f"{amount}"
            console.print(f"[bold magenta][Resource Modification] {self.get_resource_symbol(resource)} {resource} changed by {change}. New value: {self.resources[resource]}.[/bold magenta]")

    def get_resources(self):
        return self.resources.copy()

    def get_gather_count(self):
        return self.gather_count

    def get_resource_symbol(self, resource):
        symbols = {
            "Light": "✨",
            "Water": "💧",
            "Land": "🌍",
            "Energy": "⚡",
            "Metal": "🔩",
            "Food": "🍖",
            "Technology": "💻"
        }
        return symbols.get(resource, "")

    def to_dict(self):
        return self.resources.copy()

    def from_dict(self, data):
        self.resources = data.copy()
