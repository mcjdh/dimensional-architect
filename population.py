# population.py

from colorama import Fore, Style
from rich.console import Console

console = Console()

class Population:
    def __init__(self):
        self.current_population = 10
        self.max_population = 100
        self.accumulated_growth = 0.0  # To handle fractional growth

    def grow(self):
        growth_rate = 0.05  # 5% growth per turn
        growth = self.current_population * growth_rate
        self.accumulated_growth += growth
        new_members = int(self.accumulated_growth)
        if new_members >= 1:
            if self.current_population + new_members <= self.max_population:
                self.current_population += new_members
                console.print(f"[bold green][Population] Population has grown by {new_members} to {self.current_population}.[/bold green]")
            else:
                new_members = self.max_population - self.current_population
                self.current_population = self.max_population
                console.print(f"[bold green][Population] Population has grown by {new_members} to reach the maximum limit of {self.max_population}.[/bold green]")
            self.accumulated_growth -= new_members
        else:
            console.print(f"[bold yellow][Population] Population has grown by 0. Current population: {self.current_population}.[/bold yellow]")

    def upgrade_population(self, resources):
        upgrade_cost = {"Light": 100, "Energy": 50}
        if resources.spend_resources(upgrade_cost):
            self.max_population += 50
            console.print(f"[bold green][Population] Population capacity increased to {self.max_population}.[/bold green]")
            return True
        else:
            console.print("[bold red]Insufficient resources to upgrade population capacity.[/bold red]")
            return False

    def modify_population(self, amount):
        self.current_population = min(self.current_population + amount, self.max_population)
        console.print(f"[bold magenta][Population] Population has {'increased' if amount >=0 else 'decreased'} by {abs(amount)} to {self.current_population}.[/bold magenta]")

    def to_dict(self):
        return {
            "current_population": self.current_population,
            "max_population": self.max_population,
            "accumulated_growth": self.accumulated_growth
        }

    def from_dict(self, data):
        self.current_population = data.get("current_population", 10)
        self.max_population = data.get("max_population", 100)
        self.accumulated_growth = data.get("accumulated_growth", 0.0)
