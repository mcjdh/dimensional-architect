# main.py

from game_loop import GameLoop
from player import Player
from agents import AdvisingAgent
from population import Population
from resources import ResourceManager
from buildings import BuildingManager
from events import EventManager
from achievements import AchievementManager
from colorama import init, Fore, Style

def main():
    # Initialize colorama
    init(autoreset=True)
    
    # Prompt player for their name
    player_name = input(Fore.CYAN + "Enter your name, Leader of the Civilization: " + Style.RESET_ALL).strip()
    if not player_name:
        player_name = "Leader"
        print(Fore.YELLOW + "No name entered. Defaulting to 'Leader'." + Style.RESET_ALL)
    
    # Initialize game components
    player = Player(name=player_name)
    agent = AdvisingAgent()
    population = Population()
    resources = ResourceManager()
    buildings = BuildingManager()
    event_manager = EventManager()
    achievements = AchievementManager()
    
    # Initialize game loop
    game = GameLoop(player, agent, population, resources, buildings, event_manager, achievements)
    game.start()

if __name__ == "__main__":
    main()
