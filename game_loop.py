# game_loop.py

from utils import print_separator
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, Confirm
from tqdm import tqdm
import time
import random
from colorama import Fore, Style

console = Console()

class GameLoop:
    def __init__(self, player, agent, population, resources, buildings, event_manager, achievements):
        self.player = player
        self.agent = agent
        self.population = population
        self.resources = resources
        self.buildings = buildings
        self.event_manager = event_manager
        self.achievements = achievements
        self.turn = 1
        self.game_over = False
        self.active_buffs = []  # List to hold active buffs
        self.missions = []  # List to hold active missions

    def start(self):
        self.agent.set_player_name(self.player.name)
        self.agent.introduce()
        while not self.game_over:
            self.display_turn_separator()
            console.print(f"[bold magenta]=== Turn {self.turn} ===[/bold magenta]")
            self.agent.provide_tip()
            self.display_status()
            self.player_turn()
            self.display_action_outcomes()
            self.update_game_state()
            self.apply_active_buffs()
            self.event_manager.trigger_event(self)
            self.achievements.check_achievements(self)
            self.check_end_conditions()
            self.manage_missions()
            input(Fore.GREEN + "\nPress Enter to continue to the next turn..." + Style.RESET_ALL)
            self.turn += 1

    def display_turn_separator(self):
        print_separator()

    def display_status(self):
        resources = self.resources.get_resources()
        table = Table(title="Resources", show_header=True, header_style="bold blue")
        table.add_column("Resource", style="cyan", no_wrap=True)
        table.add_column("Amount", style="magenta", justify="right")
        
        for resource, amount in resources.items():
            symbol = self.get_resource_symbol(resource)
            table.add_row(f"{symbol} {resource}", f"{amount}")
        
        console.print(table)
        
        # Display Population
        population_text = f"[bold green]Population:[/bold green] {self.population.current_population}/{self.population.max_population}"
        console.print(population_text)
        
        # Display Buildings
        buildings = self.buildings.list_buildings()
        if buildings:
            building_table = Table(title="Buildings", show_header=True, header_style="bold blue")
            building_table.add_column("Building", style="cyan", no_wrap=True)
            building_table.add_column("Count", style="magenta", justify="right")
            for building, count in buildings.items():
                emoji = self.buildings.get_building_emoji(building)
                building_table.add_row(f"{emoji} {building}", f"{count}")
            console.print(building_table)
        else:
            console.print("[bold yellow]Buildings:[/bold yellow] None")
        
        # Display Player Level
        level_text = f"[bold green]Player Level:[/bold green] {self.player.level}"
        console.print(level_text)
        
        # Display Achievements
        achieved = self.achievements.get_achieved()
        achievements_text = f"[bold green]Achievements Unlocked:[/bold green] {', '.join(achieved) if achieved else 'None'}"
        console.print(achievements_text)
        
        # Display Active Buffs
        if self.active_buffs:
            buffs_table = Table(title="Active Buffs", show_header=True, header_style="bold blue")
            buffs_table.add_column("Buff", style="cyan", no_wrap=True)
            buffs_table.add_column("Description", style="magenta")
            buffs_table.add_column("Turns Left", style="green", justify="right")
            for buff in self.active_buffs:
                buffs_table.add_row(buff['name'], buff['description'], str(buff['turns_left']))
            console.print(buffs_table)
        
        # Display Active Missions
        if self.missions:
            missions_table = Table(title="Active Missions", show_header=True, header_style="bold blue")
            missions_table.add_column("Mission", style="cyan", no_wrap=True)
            missions_table.add_column("Description", style="magenta")
            missions_table.add_column("Status", style="green")
            for mission in self.missions:
                status = "Completed" if mission['completed'] else f"Turns Left: {mission['turns_left']}"
                missions_table.add_row(mission['name'], mission['description'], status)
            console.print(missions_table)
        print_separator()

    def player_turn(self):
        console.print("\n[bold yellow]Choose an action:[/bold yellow]")
        # Define the main menu options with emojis
        actions = [
            {"number": "1", "description": "Gather Resources 🌾", "action": self.gather_resources},
            {"number": "2", "description": "Build a Structure 🏗️", "action": self.build_structure},
            {"number": "3", "description": "Upgrade Population 👥", "action": self.upgrade_population},
            {"number": "4", "description": "View Achievements 🏆", "action": self.view_achievements},
            {"number": "5", "description": "View Active Missions 📜", "action": self.view_active_missions},
            {"number": "6", "description": "Accept Mission ✉️", "action": self.accept_mission},
            {"number": "7", "description": "Upgrade Building 🔧", "action": self.upgrade_building},
            {"number": "8", "description": "Quit Game 🚪", "action": self.quit_game}
        ]

        # If Victory is achieved, add a new option
        if self.achievements.achievements.get("Victory", {}).get("unlocked", False):
            actions.append({"number": "9", "description": "Use Portal 🎉", "action": self.use_portal})

        # Display the menu with colors and emojis
        for option in actions:
            console.print(f"[green]{option['number']}.[/green] {option['description']}")

        choice = Prompt.ask("Enter the number of your choice", default="1")

        # Map choice to action
        for option in actions:
            if choice == option["number"]:
                option["action"]()
                return  # Ensure the player turn ends after performing one action to avoid repeating
        console.print("[red]Invalid choice. Please try again.[/red]")

    def gather_resources(self):
        # Preview potential gains
        preview = self.preview_gather()
        console.print("[bold cyan]\nPotential Resource Gains this turn:[/bold cyan]")
        preview_table = Table(show_header=False, show_edge=False)
        for resource, amount in preview.items():
            symbol = self.resources.get_resource_symbol(resource)
            preview_table.add_row(f"{symbol} {resource}", f"+{amount}")
        console.print(preview_table)
        
        confirm = Confirm.ask("Do you want to proceed with gathering resources?")
        if confirm:
            self.resources.gather()
            self.player.gain_experience(10)  # Example experience gain
            self.record_action("Gather Resources")
        else:
            console.print("[bold yellow]Gather Resources action canceled.[/bold yellow]")

    def preview_gather(self):
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

        # Create a dictionary of potential gains
        preview = {
            "Light": light_gained,
            "Water": water_gained,
            "Energy": energy_gained,
            "Food": food_gained
        }
        return preview

    def build_structure(self):
        available_buildings = self.buildings.list_available_buildings()
        if not available_buildings:
            console.print("[bold yellow]No buildings available to construct at this time.[/bold yellow]")
            return

        console.print("\n[bold yellow]Available Buildings to Construct:[/bold yellow]")
        building_table = Table(show_header=True, header_style="bold blue")
        building_table.add_column("Number", style="cyan", no_wrap=True)
        building_table.add_column("Building", style="magenta")
        building_table.add_column("Cost", style="green")
        building_table.add_column("Affordability", style="yellow")

        for idx, building in enumerate(available_buildings, start=1):
            cost_str = ", ".join([f"{self.resources.get_resource_symbol(res)} {res}: {amt}" for res, amt in building['cost'].items()])
            can_afford = self.buildings.can_afford_building(building, self.resources)
            affordability = "[green]Yes[/green]" if can_afford else "[red]No[/red]"
            building_table.add_row(str(idx), f"{building['emoji']} {building['name']}", cost_str, affordability)

        console.print(building_table)

        choice = Prompt.ask("Enter the number of the building you want to construct", default="1")
        try:
            choice = int(choice)
            if 1 <= choice <= len(available_buildings):
                selected = available_buildings[choice - 1]
                if self.buildings.can_afford_building(selected, self.resources):
                    if self.resources.spend_resources(selected["cost"]):
                        # Simulate building time with tqdm
                        console.print(f"\n[bold magenta]Constructing {selected['name']}...[/bold magenta]")
                        for _ in tqdm(range(10), desc="Building", unit="step"):
                            time.sleep(0.1)
                        self.buildings.buildings[selected["name"]] = self.buildings.buildings.get(selected["name"], 0) + 1
                        console.print(f"[bold green]{selected['name']} constructed successfully.[/bold green]")
                        self.player.gain_experience(15)
                        
                        # Check achievements after construction
                        self.achievements.check_achievements(self)

                        return  # Ensure the function exits after one construction
                else:
                    console.print(f"[bold red]You do not have enough resources to construct {selected['name']}.[/bold red]")
            else:
                console.print("[bold red]Invalid choice.[/bold red]")
        except ValueError:
            console.print("[bold red]Invalid input. Please enter a number.[/bold red]")

        return  # Ensure the function exits if no valid action is taken

    def upgrade_population(self):
        upgrade_cost = {"Light": 100, "Energy": 50}
        console.print("\n[bold yellow]Upgrade Population Capacity:[/bold yellow]")
        upgrade_table = Table(show_header=False, show_edge=False)
        upgrade_table.add_column("Cost", style="green")
        upgrade_table.add_row(", ".join([f"{self.resources.get_resource_symbol(res)} {res}: {amt}" for res, amt in upgrade_cost.items()]))
        console.print(upgrade_table)

        confirm = Confirm.ask("Do you want to proceed with upgrading population capacity?")
        if confirm:
            if self.population.upgrade_population(self.resources):
                # Simulate upgrading time with tqdm
                console.print(f"\n[bold magenta]Upgrading Population Capacity...[/bold magenta]")
                for _ in tqdm(range(5), desc="Upgrading", unit="step"):
                    time.sleep(0.2)
                console.print(f"[bold green]Population capacity increased to {self.population.max_population}.[/bold green]")
                self.player.gain_experience(20)  # Example experience gain
                self.record_action("Upgrade Population")
            else:
                console.print("[bold red]Insufficient resources to upgrade population capacity.[/bold red]")
        else:
            console.print("[bold yellow]Upgrade Population action canceled.[/bold yellow]")

    def view_achievements(self):
        self.achievements.display_achievements()
        input("\nPress Enter to continue...")  # Pause to allow the player to view the achievements
        self.record_action("View Achievements")

    def view_active_missions(self):
        if not self.missions:
            console.print("\n[bold cyan]You have no active missions.[/bold cyan]")
            return
        console.print("\n[bold cyan]Active Missions:[/bold cyan]")
        missions_table = Table(show_header=True, header_style="bold blue")
        missions_table.add_column("Mission", style="cyan")
        missions_table.add_column("Description", style="magenta")
        missions_table.add_column("Status", style="green")
        for mission in self.missions:
            status = "Completed" if mission['completed'] else f"Turns Left: {mission['turns_left']}"
            missions_table.add_row(mission['name'], mission['description'], status)
        console.print(missions_table)

    def accept_mission(self):
        available_missions = self.get_available_missions()
        if not available_missions:
            console.print("\n[bold yellow]No missions available at this time.[/bold yellow]")
            return
        console.print("\n[bold yellow]Available Missions to Accept:[/bold yellow]")
        missions_table = Table(show_header=True, header_style="bold blue")
        missions_table.add_column("Number", style="cyan")
        missions_table.add_column("Mission", style="magenta")
        missions_table.add_column("Description", style="green")
        for idx, mission in enumerate(available_missions, start=1):
            missions_table.add_row(str(idx), mission['name'], mission['description'])
        console.print(missions_table)

        choice = Prompt.ask("Enter the number of the mission you want to accept", default="1")
        try:
            choice = int(choice)
            if 1 <= choice <= len(available_missions):
                selected = available_missions[choice - 1]
                self.missions.append({
                    "name": selected['name'],
                    "description": selected['description'],
                    "reward": selected['reward'],
                    "turns_left": selected['duration'],
                    "completed": False
                })
                console.print(f"\n[bold magenta]Mission '{selected['name']}' has been accepted![/bold magenta]")
                self.record_action("Accept Mission")
            else:
                console.print("[bold red]Invalid choice.[/bold red]")
        except ValueError:
            console.print("[bold red]Invalid input. Please enter a number.[/bold red]")

    def upgrade_building(self):
        buildings = self.buildings.list_buildings()
        if not buildings:
            console.print("[bold yellow]\nYou have no buildings to upgrade.[/bold yellow]")
            return
        console.print("\n[bold yellow]Your Buildings:[/bold yellow]")
        building_table = Table(show_header=True, header_style="bold blue")
        building_table.add_column("Number", style="cyan")
        building_table.add_column("Building", style="magenta")
        building_table.add_column("Count", style="green", justify="right")
        for idx, (building, count) in enumerate(buildings.items(), start=1):
            emoji = self.buildings.get_building_emoji(building)
            building_table.add_row(str(idx), f"{emoji} {building}", str(count))
        console.print(building_table)

        choice = Prompt.ask("Enter the number of the building you want to upgrade", default="1")
        try:
            choice = int(choice)
            if 1 <= choice <= len(buildings):
                selected_building = list(buildings.keys())[choice - 1]
                if self.buildings.can_upgrade_building(selected_building, self.resources):
                    # Simulate upgrading time with tqdm
                    console.print(f"\n[bold magenta]Upgrading {selected_building}...[/bold magenta]")
                    for _ in tqdm(range(10), desc="Upgrading", unit="step"):
                        time.sleep(0.1)
                    if self.buildings.upgrade_building(selected_building, self.resources):
                        console.print(f"[bold green]{selected_building} has been upgraded successfully.[/bold green]")
                        self.player.gain_experience(25)  # Example experience gain
                        self.record_action("Upgrade Building")
                    else:
                        console.print(f"[bold red]Failed to upgrade {selected_building} due to insufficient resources.[/bold red]")
                else:
                    console.print(f"[bold red]You do not have enough resources to upgrade {selected_building}.[/bold red]")
            else:
                console.print("[bold red]Invalid choice.[/bold red]")
        except ValueError:
            console.print("[bold red]Invalid input. Please enter a number.[/bold red]")

    def quit_game(self):
        self.game_over = True
        console.print("[bold red]Thank you for playing![/bold red]")

    def use_portal(self):
        console.print("\n[bold green]🌟 You have used the Dimensional Gate to traverse dimensions successfully! 🌟[/bold green]")
        console.print("[bold green]🎉 Congratulations! You have completed your journey and won the game![/bold green]")
        input(Fore.GREEN + "\nPress Enter to close the game..." + Style.RESET_ALL)  # Pause for the player to press Enter
        self.game_over = True

    def record_action(self, action_name):
        # Placeholder for any future action recording or logging
        pass

    def display_action_outcomes(self):
        # Print separation bar after player action
        print_separator()
        time.sleep(0.5)  # Small pause for readability

    def update_game_state(self):
        # Automatically generate resources each turn, considering buildings
        self.resources.generate_automatic_resources(self.population, self.buildings)
        self.population.grow()

    def apply_active_buffs(self):
        # Apply buffs at the start of the turn
        for buff in self.active_buffs[:]:
            if buff['type'] == 'population':
                self.population.current_population += buff['value']
                console.print(f"[bold magenta][Buff] {buff['name']} applied: +{buff['value']} Population.[/bold magenta]")
            elif buff['type'] == 'resource':
                resource = buff['resource']
                self.resources.modify_resource(resource, buff['value'])
                operation = "+" if buff['value'] >= 0 else ""
                console.print(f"[bold magenta][Buff] {buff['name']} applied: {operation}{buff['value']} {resource}.[/bold magenta]")
            # Decrement turns left
            buff['turns_left'] -= 1
            if buff['turns_left'] <= 0:
                console.print(f"[bold blue][Buff] {buff['name']} has expired.[/bold blue]")
                self.active_buffs.remove(buff)

    def add_buff(self, name, buff_type, description, value, turns, resource=None):
        buff = {
            "name": name,
            "type": buff_type,  # 'population' or 'resource'
            "description": description,
            "value": value,
            "turns_left": turns
        }
        if resource:
            buff["resource"] = resource
        self.active_buffs.append(buff)
        console.print(f"\n[bold magenta][Buff] {name} has been activated: {description} for {turns} turns.[/bold magenta]")

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

    def get_resource_color(self, resource):
        colors = {
            "Light": Fore.YELLOW,
            "Water": Fore.BLUE,
            "Land": Fore.GREEN,
            "Energy": Fore.RED,
            "Metal": Fore.CYAN,
            "Food": Fore.MAGENTA,
            "Technology": Fore.WHITE
        }
        return colors.get(resource, Fore.WHITE)

    def check_end_conditions(self):
        # Define end conditions, e.g., reaching a certain level
        # Now, check if "Victory" achievement is unlocked
        if self.achievements.achievements.get("Victory", {}).get("unlocked", False):
            # Show new menu option to use portal
            # Or automatically end the game
            # Here, the new menu option is already added, so continue
            pass
        elif self.resources.resources["Light"] <= 0 or self.resources.resources["Water"] <= 0:
            console.print("\n[bold red]☠️ Resources depleted! Your civilization cannot survive.[/bold red]")
            self.game_over = True

    def manage_missions(self):
        for mission in self.missions[:]:
            if not mission['completed']:
                # Check if mission is completed
                if mission['name'] == "Resource Gathering":
                    if self.resources.resources["Light"] >= 100 and self.resources.resources["Water"] >= 100:
                        mission['completed'] = True
                        console.print(f"\n[bold green]🎯 Mission Completed: {mission['name']}! Reward: {mission['reward']['description']}[/bold green]")
                        self.apply_mission_reward(mission['reward'])
                        self.achievements.check_achievements(self)  # Add here

                elif mission['name'] == "Technological Research":
                    if self.buildings.buildings.get("Technology Lab", 0) >= 2:
                        mission['completed'] = True
                        console.print(f"\n[bold green]🎯 Mission Completed: {mission['name']}! Reward: {mission['reward']['description']}[/bold green]")
                        self.apply_mission_reward(mission['reward'])
                        self.achievements.check_achievements(self)  # Add here

                elif mission['name'] == "Agricultural Expansion":
                    if self.buildings.buildings.get("Farm", 0) >= 3:
                        mission['completed'] = True
                        console.print(f"\n[bold green]🎯 Mission Completed: {mission['name']}! Reward: {mission['reward']['description']}[/bold green]")
                        self.apply_mission_reward(mission['reward'])
                        self.achievements.check_achievements(self)  # Add here

                elif mission['name'] == "Metal Mining":
                    if self.resources.resources.get("Metal", 0) >= 200:
                        mission['completed'] = True
                        console.print(f"\n[bold green]🎯 Mission Completed: {mission['name']}! Reward: {mission['reward']['description']}[/bold green]")
                        self.apply_mission_reward(mission['reward'])
                        self.achievements.check_achievements(self)  # Add here

                elif mission['name'] == "Technological Prowess":
                    if self.resources.resources.get("Technology", 0) >= 150:
                        mission['completed'] = True
                        console.print(f"\n[bold green]🎯 Mission Completed: {mission['name']}! Reward: {mission['reward']['description']}[/bold green]")
                        self.apply_mission_reward(mission['reward'])
                        self.achievements.check_achievements(self)  # Add here

            # Decrement turns left
            mission['turns_left'] -= 1
            if mission['turns_left'] <= 0 and not mission['completed']:
                console.print(f"\n[bold red]🚫 Mission Failed: {mission['name']}.[/bold red]")
                self.missions.remove(mission)

        # Check for "Mission Accomplished" achievement
        if not self.achievements.achievements.get("Mission Accomplished", {}).get("unlocked", False):
            completed_missions = len([m for m in self.missions if m['completed']])
            if completed_missions >= 5:
                self.achievements.unlock_achievement("Mission Accomplished", self)


    def apply_mission_reward(self, reward):
        if reward["type"] == "population":
            self.add_buff(
                name=f"Mission Reward: {reward['description']}",
                buff_type="population",
                description=reward['description'],
                value=reward['value'],
                turns=reward['turns']
            )
        elif reward["type"] == "resource":
            self.add_buff(
                name=f"Mission Reward: {reward['description']}",
                buff_type="resource",
                description=reward['description'],
                value=reward['value'],
                turns=reward['turns'],
                resource=reward.get("resource")
            )

    def get_available_missions(self):
        # Define a list of missions
        all_missions = [
            {
                "name": "Resource Gathering",
                "description": "Gather at least 100 Light and 100 Water.",
                "reward": {
                    "type": "resource",
                    "resource": "Food",
                    "value": 50,
                    "turns": 2,
                    "description": "Gain +50 Food for the next 2 turns."
                },
                "requirements": lambda game: game.resources.resources["Light"] >= 100 and game.resources.resources["Water"] >= 100,
                "duration": 3
            },
            {
                "name": "Technological Research",
                "description": "Build 2 Technology Labs.",
                "reward": {
                    "type": "resource",
                    "resource": "Technology",
                    "value": 30,
                    "turns": 3,
                    "description": "Gain +30 Technology for the next 3 turns."
                },
                "requirements": lambda game: game.buildings.buildings.get("Technology Lab", 0) >= 2,
                "duration": 4
            },
            {
                "name": "Agricultural Expansion",
                "description": "Build 3 Farms.",
                "reward": {
                    "type": "population",
                    "value": 10,
                    "turns": 2,
                    "description": "Gain +10 Population for the next 2 turns."
                },
                "requirements": lambda game: game.buildings.buildings.get("Farm", 0) >= 3,
                "duration": 3
            },
            {
                "name": "Metal Mining",
                "description": "Accumulate 200 Metal.",
                "reward": {
                    "type": "resource",
                    "resource": "Metal",
                    "value": 75,
                    "turns": 2,
                    "description": "Gain +75 Metal for the next 2 turns."
                },
                "requirements": lambda game: game.resources.resources.get("Metal", 0) >= 200,
                "duration": 3
            },
            {
                "name": "Technological Prowess",
                "description": "Accumulate 150 Technology.",
                "reward": {
                    "type": "resource",
                    "resource": "Technology",
                    "value": 50,
                    "turns": 3,
                    "description": "Gain +50 Technology for the next 3 turns."
                },
                "requirements": lambda game: game.resources.resources.get("Technology", 0) >= 150,
                "duration": 4
            },
            {
                "name": "Cultural Renaissance",
                "description": "Build 1 Settlement and 2 Farms.",
                "reward": {
                    "type": "resource",
                    "resource": "Light",
                    "value": 40,
                    "turns": 3,
                    "description": "Gain +40 Light for the next 3 turns."
                },
                "requirements": lambda game: game.buildings.buildings.get("Settlement", 0) >= 1 and game.buildings.buildings.get("Farm", 0) >= 2,
                "duration": 4
            }
        ]
        # Filter missions that are not already active and meet requirements
        active_mission_names = [mission['name'] for mission in self.missions]
        available = [m for m in all_missions if m['name'] not in active_mission_names and m['requirements'](self)]
        return available  # Ensure that the full list of available missions is returned