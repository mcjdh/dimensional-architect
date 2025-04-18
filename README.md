# Dimensional Architect

Dimensional Architect is a turn-based civilization simulation implemented in Python. Features resource management, population development, building construction, event handling, and achievement unlocking, Eventually ends in the construction of the Dimensional Gate. 🏗️

---

## Overview

Key features:
- Resource management (Energy, Light, Food, Metal, Technology)
- Population growth and leveling
- Building construction and upgrades
- Random events affecting gameplay
- Achievement tracking with temporary buffs
- Mission completion for additional rewards

The main loop advances one turn at a time. Each turn includes:
1. Resource gathering and spending
2. Building actions
3. Event resolution
4. Achievement checks and applying rewards
5. Population updates and level progression

---

## Getting Started

### Requirements

- Python 3.x
- colorama
- rich
## Game Guide

- Gather initial resources to unlock **First Harvest**  
    • Gain an early Energy boost ⚡

- Construct core buildings:  
    • **Settlements**  
        – Increases population and available actions 👥  
    • **Farms**  
        – Secures your Food supply 🌾

- Accumulate resources to trigger achievements:  
    • **Metal Tycoon**: 300 Metal 🥇  
    • **Food Sovereign**: 200 Food 🍽️  
    • **Resource Hoarder**: 1,000 Light 💡

- Build a **Technology Lab** to:  
    • Enhance Technology production  
    • Unlock higher‑level achievements

- Complete random **missions** for bonus rewards:  
    • Additional population boosts  
    • Extra resource grants 🎲

- Final objective:  
    • Unlock all achievements  
    • Construct the **Dimensional Gate** 🚀

## Achievements

Achievement conditions and temporary bonuses:

- First Harvest: Gather resources → +20 Energy (3 turns)
- First Building: Construct a building → +5 Population (2 turns)
- Level 3 Achieved: Reach player level 3 → +30 Light (2 turns)
- Population Growth: 50 population → +50 Light (1 turn)
- Resource Master: 500+ of each resource → +100 Food (2 turns)
- Master Builder: Construct every building type → +10 Population (3 turns)
- Metal Tycoon: 300 Metal → +75 Metal (2 turns)
- Food Sovereign: 200 Food → +50 Food (3 turns)
- Tech Guru: 100 Technology → +30 Technology (4 turns)
- Energy Overlord: 200 Energy → +100 Energy (2 turns)
- Resource Hoarder: 1000 Light → +50 Energy (2 turns)
- Technocrat: 200 Technology → +70 Technology (3 turns)
- Technological Breakthrough: Build Dimensional Gate → +50 Technology (1 turn)
- Victory: All achievements unlocked and Dimensional Gate built → +100 Technology (5 turns)

---

## Code Structure

```text
.
├─ main.py           # Entry point: initializes components and starts the game loop
├─ game_loop.py      # Turn-based loop, user interactions, and display (uses rich tables)
├─ player.py         # Player data model, experience, and leveling logic
├─ resources.py      # ResourceManager: tracks and updates resource values
├─ population.py     # Population model and growth calculations
├─ buildings.py      # BuildingManager: definitions, costs, and construction logic
├─ events.py         # EventManager: random event generation and handling
├─ achievements.py   # AchievementManager: conditions and reward application
└─ utils.py          # Utility functions (e.g., printing separators)
```

---

## Strategies

- Balance resource types to avoid bottlenecks.
- Grow population early for more available actions per turn.
- Time your Technology Lab upgrades after securing Food and Metal supplies.
- Use achievement rewards strategically around major constructions.
- Maintain a reserve of resources to mitigate negative events.
- Aim to construct the Dimensional Gate as soon as achievement prerequisites are met.
