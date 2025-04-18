# player.py
from rich.console import Console  # Add this import at the top of the file

class Player:
    def __init__(self, name):
        self.name = name
        self.level = 1
        self.experience = 0

    def gain_experience(self, amount):
        self.experience += amount
        console = Console()
        console.print(f"[bold yellow][Player]{self.name} gains {amount} experience points.[/bold yellow]")
        while self.experience >= self.level * 100:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.experience -= (self.level - 1) * 100
        console = Console()
        console.print(f"[bold green][Player]{self.name} has reached level {self.level}![/bold green]")

    def to_dict(self):
        return {
            "name": self.name,
            "level": self.level,
            "experience": self.experience
        }

    def from_dict(self, data):
        self.name = data["name"]
        self.level = data["level"]
        self.experience = data["experience"]
