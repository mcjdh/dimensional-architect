# achievements.py

from colorama import Fore, Style
from rich.console import Console
from rich.table import Table

console = Console()

class AchievementManager:
    def __init__(self):
        self.achievements = {
            "First Harvest": {
                "unlocked": False,
                "description": "Gather resources for the first time.",
                "reward": {
                    "type": "resource",
                    "resource": "Energy",
                    "value": 20,
                    "turns": 3,
                    "description": "Gain +20 Energy for the next 3 turns."
                }
            },
            "First Building": {
                "unlocked": False,
                "description": "Construct your first building.",
                "reward": {
                    "type": "population",
                    "value": 5,
                    "turns": 2,
                    "description": "Gain +5 Population for the next 2 turns."
                }
            },
            "Level 3 Achieved": {  # New Achievement
                "unlocked": False,
                "description": "Reach level 3.",
                "reward": {
                    "type": "resource",
                    "resource": "Light",
                    "value": 30,
                    "turns": 2,
                    "description": "Gain +30 Light for the next 2 turns."
                }
            },
            "Population Growth": {
                "unlocked": False,
                "description": "Reach a population of 50.",
                "reward": {
                    "type": "resource",
                    "resource": "Light",
                    "value": 50,
                    "turns": 1,
                    "description": "Gain +50 Light for the next turn."
                }
            },
            "Resource Master": {
                "unlocked": False,
                "description": "Accumulate 500 of each resource.",
                "reward": {
                    "type": "resource",
                    "resource": "Food",
                    "value": 100,
                    "turns": 2,
                    "description": "Gain +100 Food for the next 2 turns."
                }
            },
            "Master Builder": {
                "unlocked": False,
                "description": "Construct all types of buildings.",
                "reward": {
                    "type": "population",
                    "value": 10,
                    "turns": 3,
                    "description": "Gain +10 Population for the next 3 turns."
                }
            },
            "Technological Breakthrough": {
                "unlocked": False,
                "description": "Construct the Dimensional Gate.",
                "reward": {
                    "type": "resource",
                    "resource": "Technology",
                    "value": 50,
                    "turns": 1,
                    "description": "Gain +50 Technology for the next turn."
                }
            },
            "Metal Tycoon": {
                "unlocked": False,
                "description": "Accumulate 300 Metal.",
                "reward": {
                    "type": "resource",
                    "resource": "Metal",
                    "value": 75,
                    "turns": 2,
                    "description": "Gain +75 Metal for the next 2 turns."
                }
            },
            "Food Sovereign": {
                "unlocked": False,
                "description": "Accumulate 200 Food.",
                "reward": {
                    "type": "resource",
                    "resource": "Food",
                    "value": 50,
                    "turns": 3,
                    "description": "Gain +50 Food for the next 3 turns."
                }
            },
            "Tech Guru": {
                "unlocked": False,
                "description": "Accumulate 100 Technology.",
                "reward": {
                    "type": "resource",
                    "resource": "Technology",
                    "value": 30,
                    "turns": 4,
                    "description": "Gain +30 Technology for the next 4 turns."
                }
            },
            "Energy Overlord": {
                "unlocked": False,
                "description": "Accumulate 200 Energy.",
                "reward": {
                    "type": "resource",
                    "resource": "Energy",
                    "value": 100,
                    "turns": 2,
                    "description": "Gain +100 Energy for the next 2 turns."
                }
            },
            "Mission Accomplished": {  # Achievement for completing missions
                "unlocked": False,
                "description": "Complete 3 missions.",
                "reward": {
                    "type": "population",
                    "value": 15,
                    "turns": 3,
                    "description": "Gain +15 Population for the next 3 turns."
                }
            },
            "Resource Hoarder": {  # Achievement for resource accumulation
                "unlocked": False,
                "description": "Accumulate 1000 Light.",
                "reward": {
                    "type": "resource",
                    "resource": "Energy",
                    "value": 50,
                    "turns": 2,
                    "description": "Gain +50 Energy for the next 2 turns."
                }
            },
            "Technocrat": {  # Achievement for Technology accumulation
                "unlocked": False,
                "description": "Accumulate 200 Technology.",
                "reward": {
                    "type": "resource",
                    "resource": "Technology",
                    "value": 70,
                    "turns": 3,
                    "description": "Gain +70 Technology for the next 3 turns."
                }
            },
            "Victory": {  # Updated condition
                "unlocked": False,
                "description": "Unlock all achievements and build the Dimensional Gate.",
                "reward": {
                    "type": "resource",
                    "resource": "Technology",
                    "value": 100,
                    "turns": 5,
                    "description": "Gain +100 Technology for the next 5 turns."
                }
            }
        }

    def check_achievements(self, game):
        # Iterate through achievements to check if any can be unlocked
        for name, details in self.achievements.items():
            if not details["unlocked"]:
                if self.meets_conditions(name, game):
                    self.unlock_achievement(name, game)

    def meets_conditions(self, name, game):
        if name == "First Harvest":
            return game.resources.get_gather_count() >= 1
        elif name == "First Building":
            return len(game.buildings.buildings) >= 1
        elif name == "Level 3 Achieved":
            return game.player.level >= 3
        elif name == "Population Growth":
            return game.population.current_population >= 50
        elif name == "Resource Master":
            return all(amount >= 500 for amount in game.resources.resources.values())
        elif name == "Master Builder":
            required_buildings = ["Land Formation", "Settlement", "Farm", "Metal Mine", "Technology Lab", "Dimensional Gate"]
            return all(game.buildings.buildings.get(building, 0) >= 1 for building in required_buildings)
        elif name == "Technological Breakthrough":
            return "Dimensional Gate" in game.buildings.buildings and game.buildings.buildings["Dimensional Gate"] >= 1
        elif name == "Metal Tycoon":
            return game.resources.resources.get("Metal", 0) >= 300
        elif name == "Food Sovereign":
            return game.resources.resources.get("Food", 0) >= 200
        elif name == "Tech Guru":
            return game.resources.resources.get("Technology", 0) >= 100
        elif name == "Energy Overlord":
            return game.resources.resources.get("Energy", 0) >= 200
        elif name == "Mission Accomplished":
            completed_missions = len([m for m in game.missions if m['completed']])
            return completed_missions >= 3  # Change from 5 to 3
        elif name == "Resource Hoarder":
            return game.resources.resources.get("Light", 0) >= 1000
        elif name == "Technocrat":
            return game.resources.resources.get("Technology", 0) >= 200
        elif name == "Victory":
            # Victory condition: All achievements except "Victory" are unlocked and Dimensional Gate is built
            all_unlocked = all(details["unlocked"] for ach, details in self.achievements.items() if ach != "Victory")
            dim_gate_built = "Dimensional Gate" in game.buildings.buildings and game.buildings.buildings["Dimensional Gate"] >= 1
            return all_unlocked and dim_gate_built
        return False

    def unlock_achievement(self, name, game):
        self.achievements[name]["unlocked"] = True
        console.print(f"\n[bold yellow]🎖️ Achievement Unlocked: {name}! {self.achievements[name]['description']}[/bold yellow]")
        self.apply_reward(name, game)

    def apply_reward(self, name, game):
        reward = self.achievements[name]["reward"]
        if reward["type"] == "population":
            game.add_buff(
                name=f"Achievement Reward: {reward['description']}",
                buff_type="population",
                description=reward['description'],
                value=reward['value'],
                turns=reward['turns']
            )
        elif reward["type"] == "resource":
            game.add_buff(
                name=f"Achievement Reward: {reward['description']}",
                buff_type="resource",
                description=reward['description'],
                value=reward['value'],
                turns=reward['turns'],
                resource=reward.get("resource")
            )

    def get_achieved(self):
        return [name for name, details in self.achievements.items() if details["unlocked"]]

    def display_achievements(self):
        console.print("\n[bold yellow]=== Achievements ===[/bold yellow]")
        achievements_table = Table(show_header=True, header_style="bold blue")
        achievements_table.add_column("Achievement", style="cyan")
        achievements_table.add_column("Status", style="magenta")
        achievements_table.add_column("Description", style="green")
        for name, details in self.achievements.items():
            status = "[green]Unlocked[/green]" if details["unlocked"] else "[red]Locked[/red]"
            emoji = "🏆" if details["unlocked"] else "🔒"
            achievements_table.add_row(f"{emoji} {name}", status, details['description'])
        console.print(achievements_table)
        console.print("[bold yellow]====================[/bold yellow]\n")
