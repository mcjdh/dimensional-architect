# buildings.py
from rich.prompt import Prompt
from rich.prompt import Confirm
from colorama import Fore, Style
from rich.console import Console
from rich.table import Table
from tqdm import tqdm
import time

console = Console()

class BuildingManager:
    def __init__(self):
        self.buildings = {}
        self.building_emojis = {
            "Land Formation": "🌱",
            "Settlement": "🏘️",
            "Farm": "🌾",
            "Metal Mine": "⛏️",
            "Technology Lab": "🔬",
            "Dimensional Gate": "🌀"
        }

    def build_structure(self, resources, population):
        available_buildings = self.list_available_buildings()
        if not available_buildings:
            console.print("[bold yellow]No buildings available to construct at this time.[/bold yellow]")
            return False

        console.print("\n[bold yellow]Available Buildings to Construct:[/bold yellow]")
        building_table = Table(show_header=True, header_style="bold blue")
        building_table.add_column("Number", style="cyan", no_wrap=True)
        building_table.add_column("Building", style="magenta")
        building_table.add_column("Cost", style="green")
        building_table.add_column("Affordability", style="yellow")

        for idx, building in enumerate(available_buildings, start=1):
            cost_str = ", ".join([f"{resources.get_resource_symbol(res)} {res}: {amt}" for res, amt in building['cost'].items()])
            can_afford = self.can_afford_building(building, resources)
            affordability = "[green]Yes[/green]" if can_afford else "[red]No[/red]"
            building_table.add_row(str(idx), f"{building['emoji']} {building['name']}", cost_str, affordability)

        console.print(building_table)

        choice = Prompt.ask("Enter the number of the building you want to construct", default="1")
        try:
            choice = int(choice)
            if 1 <= choice <= len(available_buildings):
                selected = available_buildings[choice - 1]
                if self.can_afford_building(selected, resources):
                    if resources.spend_resources(selected["cost"]):
                        # Simulate building time with tqdm
                        console.print(f"\n[bold magenta]Constructing {selected['name']}...[/bold magenta]")
                        for _ in tqdm(range(10), desc="Building", unit="step"):
                            time.sleep(0.1)
                        self.buildings[selected["name"]] = self.buildings.get(selected["name"], 0) + 1
                        console.print(f"[bold green]{selected['name']} constructed successfully.[/bold green]")
                        return True  # Exit after one construction
                else:
                    console.print(f"[bold red]You do not have enough resources to construct {selected['name']}.[/bold red]")
            else:
                console.print("[bold red]Invalid choice.[/bold red]")
        except ValueError:
            console.print("[bold red]Invalid input. Please enter a number.[/bold red]")

        return False  # Exit function if no valid structure is built




    def can_afford_building(self, building, resources):
        for res, amt in building['cost'].items():
            if resources.resources.get(res, 0) < amt:
                return False
        return True

    def list_buildings(self):
        return self.buildings

    def list_available_buildings(self):
        # Define available buildings and their costs with emojis
        return [
            {"name": "Land Formation", "cost": {"Light": 50, "Energy": 20}, "emoji": self.get_building_emoji("Land Formation")},
            {"name": "Settlement", "cost": {"Light": 100, "Water": 50, "Energy": 30}, "emoji": self.get_building_emoji("Settlement")},
            {"name": "Farm", "cost": {"Land": 50, "Energy": 20}, "emoji": self.get_building_emoji("Farm")},
            {"name": "Metal Mine", "cost": {"Land": 100, "Energy": 40, "Metal": 50}, "emoji": self.get_building_emoji("Metal Mine")},
            {"name": "Technology Lab", "cost": {"Metal": 100, "Energy": 50, "Technology": 20}, "emoji": self.get_building_emoji("Technology Lab")},
            {"name": "Dimensional Gate", "cost": {"Land": 200, "Energy": 100, "Light": 150, "Technology": 50}, "emoji": self.get_building_emoji("Dimensional Gate")}
        ]

    def get_building_effects(self):
        # Returns a dictionary with building names as keys and their effects
        # For example, Farm increases Light and Water generation per population
        effects = {
            "Land Formation": {"Land": 100},  # Each Land Formation adds 100 Land
            "Settlement": {"Energy": 10},      # Settlement increases Energy generation by 10 per turn
            "Farm": {"Light": 1, "Water": 0.5, "Food": 2},
            "Metal Mine": {"Metal": 5},
            "Technology Lab": {"Technology": 2},
            "Dimensional Gate": {"Light": 5, "Energy": 5}  # Placeholder for end-game effects
        }
        return effects

    def upgrade_building(self, building_name, resources):
        if building_name not in self.buildings or self.buildings[building_name] <= 0:
            console.print(f"[bold red]You don't have any {building_name} to upgrade.[/bold red]")
            return False
        upgrade_cost = self.get_upgrade_cost(building_name)
        if not upgrade_cost:
            console.print(f"[bold yellow]{building_name} cannot be upgraded.[/bold yellow]")
            return False
        if self.can_upgrade_building(building_name, resources):  # Use the existing method here
            console.print(f"\n[bold yellow]Upgrade Cost for {building_name}:[/bold yellow]")
            upgrade_table = Table(show_header=False, show_edge=False)
            upgrade_table.add_column("Cost", style="green")
            upgrade_table.add_row(", ".join([f"{resources.get_resource_symbol(res)} {res}: {amt}" for res, amt in upgrade_cost.items()]))
            console.print(upgrade_table)
            
            confirm = Confirm.ask("Do you want to proceed with the upgrade?")
            if confirm:
                if resources.spend_resources(upgrade_cost):
                    # Simulate upgrading time with tqdm
                    console.print(f"\n[bold magenta]Upgrading {building_name}...[/bold magenta]")
                    for _ in tqdm(range(10), desc="Upgrading", unit="step"):
                        time.sleep(0.1)
                    self.buildings[building_name] += 1
                    console.print(f"[bold green]{building_name} has been upgraded successfully.[/bold green]")
                    return True
            else:
                console.print("[bold yellow]Upgrade action canceled.[/bold yellow]")
        else:
            console.print(f"[bold red]Insufficient resources to upgrade {building_name}.[/bold red]")
        return False

    def can_upgrade_building(self, building_name, resources):
        upgrade_cost = self.get_upgrade_cost(building_name)
        for res, amt in upgrade_cost.items():
            if resources.resources.get(res, 0) < amt:
                return False
        return True

    def get_upgrade_cost(self, building_name):
        # Define upgrade costs for each building
        upgrade_costs = {
            "Farm": {"Light": 30, "Water": 20},
            "Settlement": {"Light": 50, "Water": 30, "Energy": 20},
            "Metal Mine": {"Metal": 50, "Energy": 30},
            "Technology Lab": {"Technology": 30, "Energy": 20},
            "Land Formation": {"Light": 20, "Energy": 10},
            "Dimensional Gate": {"Light": 100, "Energy": 50, "Technology": 50}
        }
        return upgrade_costs.get(building_name, {})

    def get_building_emoji(self, building_name):
        return self.building_emojis.get(building_name, "")

    def to_dict(self):
        return self.buildings.copy()

    def from_dict(self, data):
        self.buildings = data.copy()
