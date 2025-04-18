# agents.py

import random
from rich.console import Console

console = Console()

class AdvisingAgent:
    def __init__(self):
        self.introductory_messages = [
            "Welcome, {name}. Your journey begins in the void.",
            "Establish Light and Land to start creating your civilization.",
            "Manage your resources wisely to grow your population and build structures.",
            "Remember, the ultimate goal is to create a thriving world and build a Dimensional Gate."
        ]
        self.tip_messages = [
            "Tip: Building a Settlement will allow you to manage your population more effectively.",
            "Tip: Farms can increase your resource generation each turn.",
            "Tip: Upgrading your population capacity lets you support a larger civilization.",
            "Tip: Keep an eye on your Energy levels to ensure continuous growth.",
            "Tip: Don't neglect Water resources; they are essential for sustaining life.",
            "Tip: Land Formation increases your available land for building structures.",
            "Tip: Dimensional Gates are the key to completing your civilization.",
            "Tip: Efficient resource management is crucial for your civilization's growth.",
            "Tip: Monitor your resource levels to prevent depletion.",
            "Tip: Constructing multiple Farms can significantly boost your resource output.",
            "Tip: Technology Labs enhance your Technology generation, unlocking advanced buildings.",
            "Tip: Metal Mines provide the Metal needed for constructing robust structures.",
            "Tip: Research in Technology Labs can unlock new capabilities.",
            "Tip: Balancing resource generation ensures sustainable growth.",
            "Tip: Completing missions can grant you valuable rewards and buffs.",
            "Tip: Upgrading buildings can provide significant advantages to your civilization.",
            "Tip: Explore new lands to discover additional resources.",
            "Tip: Diversify your building portfolio to maximize resource efficiency.",
            "Tip: Keep your population happy to prevent unrest and decline.",
            "Tip: Strategic planning is key to overcoming unforeseen challenges."
        ]
        self.current_intro_message = 0
        self.player_name = "Leader"

    def set_player_name(self, name):
        self.player_name = name

    def introduce(self):
        console.print("\n[bold magenta][Advising Agent] Greetings, Leader of the Civilization.[/bold magenta]")
        self.provide_introductory_message()

    def provide_introductory_message(self):
        if self.current_intro_message < len(self.introductory_messages):
            message = self.introductory_messages[self.current_intro_message].format(name=self.player_name)
            console.print(f"[bold magenta][Advising Agent]: {message}[/bold magenta]")
            self.current_intro_message += 1

    def provide_tip(self):
        # Randomly select a tip from tip_messages
        tip = random.choice(self.tip_messages)
        console.print(f"[bold green][Advising Agent]: {tip}[/bold green]")
