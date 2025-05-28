// Dimensional Architect - Web Edition
// Game Logic ported from Python version

class Player {
    constructor(name = "Leader") {
        this.name = name;
        this.level = 1;
        this.experience = 0;
    }

    gainExperience(amount) {
        this.experience += amount;
        game.log(`${this.name} gains ${amount} experience points.`, 'achievement');
        
        while (this.experience >= this.level * 100) {
            this.levelUp();
        }
        this.updateDisplay();
    }

    levelUp() {
        this.level += 1;
        this.experience -= (this.level - 1) * 100;
        game.log(`${this.name} has reached level ${this.level}!`, 'achievement');
        
        // Check for level achievements
        game.achievements.checkAchievement('Level 3 Achieved', () => this.level >= 3);
    }

    updateDisplay() {
        document.getElementById('player-name').textContent = this.name;
        document.getElementById('player-level').textContent = this.level;
        document.getElementById('experience-current').textContent = this.experience;
        document.getElementById('experience-next').textContent = this.level * 100;
        
        const percentage = (this.experience / (this.level * 100)) * 100;
        document.getElementById('experience-fill').style.width = `${percentage}%`;
    }
}

class ResourceManager {
    constructor() {
        this.resources = {
            "Light": 100,
            "Water": 100,
            "Land": 0,
            "Energy": 50,
            "Metal": 0,
            "Food": 0,
            "Technology": 0
        };
        this.gatherCount = 0;
        this.symbols = {
            "Light": "✨",
            "Water": "💧",
            "Land": "🌍",
            "Energy": "⚡",
            "Metal": "🔩",
            "Food": "🍖",
            "Technology": "💻"
        };
    }

    gather() {
        game.log("Gathering resources...", 'action');
        
        const possibleGains = {
            "Light": [5, 15],
            "Water": [10, 20],
            "Energy": [5, 10],
            "Food": [0, 5]
        };

        const gains = {};
        for (const [resource, range] of Object.entries(possibleGains)) {
            const gained = this.randomInt(range[0], range[1]);
            if (gained > 0) {
                gains[resource] = gained;
                this.resources[resource] += gained;
            }
        }

        this.gatherCount += 1;
        
        // Display gains
        const gainTexts = [];
        for (const [resource, amount] of Object.entries(gains)) {
            gainTexts.push(`+${amount} ${this.symbols[resource]} ${resource}`);
        }
        
        if (gainTexts.length > 0) {
            game.log(`Gathered: ${gainTexts.join(', ')}`, 'resource-gain');
        } else {
            game.log("No resources gained this turn.", 'action');
        }

        // Check for first harvest achievement
        game.achievements.checkAchievement('First Harvest', () => this.gatherCount >= 1);

        this.updateDisplay();
        game.player.gainExperience(5);
    }

    generateAutomaticResources(population, buildings) {
        const lightGenerated = population.currentPopulation * 2;
        const waterGenerated = population.currentPopulation * 1;
        const energyGenerated = Math.floor(population.currentPopulation * 0.5);
        const metalGenerated = population.currentPopulation * 0.5;
        const foodGenerated = population.currentPopulation * 1.5;
        const techGenerated = population.currentPopulation * 0.2;

        // Apply building effects
        const buildingEffects = buildings.getBuildingEffects();
        for (const [building, count] of Object.entries(buildings.buildings)) {
            if (buildingEffects[building]) {
                for (const [resource, bonus] of Object.entries(buildingEffects[building])) {
                    if (this.resources.hasOwnProperty(resource)) {
                        const additional = bonus * count;
                        this.resources[resource] += additional;
                        game.log(`${building} provides +${additional} ${this.symbols[resource]} ${resource}`, 'resource-gain');
                    }
                }
            }
        }

        // Add base resource generation
        this.resources["Light"] += lightGenerated;
        this.resources["Water"] += waterGenerated;
        this.resources["Energy"] += energyGenerated;
        this.resources["Metal"] += metalGenerated;
        this.resources["Food"] += foodGenerated;
        this.resources["Technology"] += techGenerated;

        // Display auto-generated resources
        const autoGains = [
            `+${lightGenerated} ${this.symbols['Light']} Light`,
            `+${waterGenerated} ${this.symbols['Water']} Water`,
            `+${energyGenerated} ${this.symbols['Energy']} Energy`,
            `+${metalGenerated} ${this.symbols['Metal']} Metal`,
            `+${foodGenerated} ${this.symbols['Food']} Food`,
            `+${techGenerated} ${this.symbols['Technology']} Technology`
        ];
        
        game.log(`Auto-Generated: ${autoGains.join(', ')}`, 'resource-gain');
        this.updateDisplay();
    }

    spendResources(costs) {
        // Check if can afford
        for (const [resource, amount] of Object.entries(costs)) {
            if ((this.resources[resource] || 0) < amount) {
                game.log(`Not enough ${resource}. Required: ${amount}, Available: ${this.resources[resource] || 0}`, 'resource-spend');
                return false;
            }
        }

        // Spend resources
        for (const [resource, amount] of Object.entries(costs)) {
            this.resources[resource] -= amount;
        }

        const spentTexts = [];
        for (const [resource, amount] of Object.entries(costs)) {
            spentTexts.push(`${this.symbols[resource]} ${resource}: ${amount}`);
        }
        game.log(`Spent: ${spentTexts.join(', ')}`, 'resource-spend');
        
        this.updateDisplay();
        return true;
    }

    addResources(gains) {
        for (const [resource, amount] of Object.entries(gains)) {
            this.resources[resource] = (this.resources[resource] || 0) + amount;
            game.log(`+${amount} ${this.symbols[resource]} ${resource}`, 'resource-gain');
        }
        this.updateDisplay();
    }

    modifyResource(resource, amount) {
        if (this.resources.hasOwnProperty(resource)) {
            this.resources[resource] += amount;
            if (this.resources[resource] < 0) {
                this.resources[resource] = 0;
            }
            const change = amount >= 0 ? `+${amount}` : `${amount}`;
            game.log(`${this.symbols[resource]} ${resource} changed by ${change}. New value: ${this.resources[resource]}`, 'event');
        }
        this.updateDisplay();
    }

    updateDisplay() {
        for (const [resource, value] of Object.entries(this.resources)) {
            const element = document.getElementById(`resource-${resource.toLowerCase()}`);
            if (element) {
                element.textContent = Math.floor(value);
            }
        }

        // Check resource-based achievements
        game.achievements.checkAchievement('Metal Tycoon', () => this.resources.Metal >= 300);
        game.achievements.checkAchievement('Food Sovereign', () => this.resources.Food >= 200);
    }

    randomInt(min, max) {
        return Math.floor(Math.random() * (max - min + 1)) + min;
    }
}

class Population {
    constructor() {
        this.currentPopulation = 10;
        this.maxPopulation = 100;
        this.accumulatedGrowth = 0.0;
    }

    grow() {
        const growthRate = 0.05; // 5% growth per turn
        const growth = this.currentPopulation * growthRate;
        this.accumulatedGrowth += growth;
        const newMembers = Math.floor(this.accumulatedGrowth);
        
        if (newMembers >= 1) {
            if (this.currentPopulation + newMembers <= this.maxPopulation) {
                this.currentPopulation += newMembers;
                game.log(`Population has grown by ${newMembers} to ${this.currentPopulation}`, 'event');
            } else {
                const actualNewMembers = this.maxPopulation - this.currentPopulation;
                this.currentPopulation = this.maxPopulation;
                game.log(`Population has grown by ${actualNewMembers} to reach the maximum limit of ${this.maxPopulation}`, 'event');
            }
            this.accumulatedGrowth -= newMembers;
        }

        // Check population achievements
        game.achievements.checkAchievement('Population Growth', () => this.currentPopulation >= 50);
        game.achievements.checkAchievement('Megalopolis', () => this.currentPopulation >= 200);
        
        this.updateDisplay();
    }

    upgradePopulation(resources) {
        const upgradeCost = {"Light": 100, "Energy": 50};
        if (resources.spendResources(upgradeCost)) {
            this.maxPopulation += 50;
            game.log(`Population capacity increased to ${this.maxPopulation}`, 'achievement');
            this.updateDisplay();
            game.player.gainExperience(10);
            return true;
        } else {
            game.log("Insufficient resources to upgrade population capacity", 'resource-spend');
            return false;
        }
    }

    modifyPopulation(amount) {
        this.currentPopulation = Math.min(this.currentPopulation + amount, this.maxPopulation);
        const change = amount >= 0 ? 'increased' : 'decreased';
        game.log(`Population has ${change} by ${Math.abs(amount)} to ${this.currentPopulation}`, 'event');
        this.updateDisplay();
    }

    updateDisplay() {
        document.getElementById('population-current').textContent = this.currentPopulation;
        document.getElementById('population-max').textContent = this.maxPopulation;
    }
}

class BuildingManager {
    constructor() {
        this.buildings = {};
        this.buildingEmojis = {
            "Land Formation": "🌱",
            "Settlement": "🏘️",
            "Farm": "🌾",
            "Metal Mine": "⛏️",
            "Technology Lab": "🔬",
            "Dimensional Gate": "🌀"
        };
    }

    getAvailableBuildings() {
        return [
            {"name": "Land Formation", "cost": {"Light": 50, "Energy": 20}, "emoji": this.buildingEmojis["Land Formation"]},
            {"name": "Settlement", "cost": {"Light": 100, "Water": 50, "Energy": 30}, "emoji": this.buildingEmojis["Settlement"]},
            {"name": "Farm", "cost": {"Land": 50, "Energy": 20}, "emoji": this.buildingEmojis["Farm"]},
            {"name": "Metal Mine", "cost": {"Land": 100, "Energy": 40, "Metal": 50}, "emoji": this.buildingEmojis["Metal Mine"]},
            {"name": "Technology Lab", "cost": {"Metal": 100, "Energy": 50, "Technology": 20}, "emoji": this.buildingEmojis["Technology Lab"]},
            {"name": "Dimensional Gate", "cost": {"Land": 200, "Energy": 100, "Light": 150, "Technology": 50}, "emoji": this.buildingEmojis["Dimensional Gate"]}
        ];
    }

    getBuildingEffects() {
        return {
            "Land Formation": {"Land": 100},
            "Settlement": {"Energy": 10},
            "Farm": {"Light": 1, "Water": 0.5, "Food": 2},
            "Metal Mine": {"Metal": 5},
            "Technology Lab": {"Technology": 2},
            "Dimensional Gate": {"Light": 5, "Energy": 5}
        };
    }

    canAffordBuilding(building, resources) {
        for (const [resource, amount] of Object.entries(building.cost)) {
            if ((resources.resources[resource] || 0) < amount) {
                return false;
            }
        }
        return true;
    }

    buildStructure(buildingName, resources) {
        const availableBuildings = this.getAvailableBuildings();
        const building = availableBuildings.find(b => b.name === buildingName);
        
        if (!building) {
            game.log(`Building ${buildingName} not found`, 'action');
            return false;
        }

        if (this.canAffordBuilding(building, resources)) {
            if (resources.spendResources(building.cost)) {
                this.buildings[building.name] = (this.buildings[building.name] || 0) + 1;
                game.log(`${building.name} constructed successfully!`, 'achievement');
                
                // Check achievements
                game.achievements.checkAchievement('First Building', () => this.getTotalBuildings() >= 1);
                game.achievements.checkAchievement('Technological Breakthrough', () => this.buildings["Dimensional Gate"] >= 1);
                
                this.updateDisplay();
                game.player.gainExperience(15);
                return true;
            }
        } else {
            game.log(`You do not have enough resources to construct ${building.name}`, 'resource-spend');
        }
        return false;
    }

    upgradeBuilding(buildingName, resources) {
        if (!this.buildings[buildingName] || this.buildings[buildingName] <= 0) {
            game.log(`You don't have any ${buildingName} to upgrade`, 'action');
            return false;
        }

        const upgradeCost = this.getUpgradeCost(buildingName);
        if (!upgradeCost || Object.keys(upgradeCost).length === 0) {
            game.log(`${buildingName} cannot be upgraded`, 'action');
            return false;
        }

        if (this.canUpgradeBuilding(buildingName, resources)) {
            if (resources.spendResources(upgradeCost)) {
                this.buildings[buildingName] += 1;
                game.log(`${buildingName} has been upgraded successfully!`, 'achievement');
                this.updateDisplay();
                game.player.gainExperience(10);
                return true;
            }
        } else {
            game.log(`Insufficient resources to upgrade ${buildingName}`, 'resource-spend');
        }
        return false;
    }

    canUpgradeBuilding(buildingName, resources) {
        const upgradeCost = this.getUpgradeCost(buildingName);
        for (const [resource, amount] of Object.entries(upgradeCost)) {
            if ((resources.resources[resource] || 0) < amount) {
                return false;
            }
        }
        return true;
    }

    getUpgradeCost(buildingName) {
        const upgradeCosts = {
            "Farm": {"Light": 30, "Water": 20},
            "Settlement": {"Light": 50, "Water": 30, "Energy": 20},
            "Metal Mine": {"Metal": 50, "Energy": 30},
            "Technology Lab": {"Technology": 30, "Energy": 20},
            "Land Formation": {"Light": 20, "Energy": 10},
            "Dimensional Gate": {"Light": 100, "Energy": 50, "Technology": 50}
        };
        return upgradeCosts[buildingName] || {};
    }

    getTotalBuildings() {
        return Object.values(this.buildings).reduce((sum, count) => sum + count, 0);
    }

    updateDisplay() {
        const buildingsList = document.getElementById('buildings-list');
        buildingsList.innerHTML = '';

        for (const [building, count] of Object.entries(this.buildings)) {
            if (count > 0) {
                const buildingElement = document.createElement('div');
                buildingElement.className = 'building-item';
                buildingElement.innerHTML = `
                    <div class="building-info">
                        <div class="building-name">${this.buildingEmojis[building]} ${building}</div>
                    </div>
                    <div class="building-count">${count}</div>
                `;
                buildingsList.appendChild(buildingElement);
            }
        }

        if (Object.keys(this.buildings).length === 0) {
            buildingsList.innerHTML = '<div class="building-item">No buildings constructed yet</div>';
        }
    }
}

class AchievementManager {
    constructor() {
        this.achievements = {
            "First Harvest": {
                "unlocked": false,
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
                "unlocked": false,
                "description": "Construct your first building.",
                "reward": {
                    "type": "population",
                    "value": 5,
                    "turns": 2,
                    "description": "Gain +5 Population for the next 2 turns."
                }
            },
            "Level 3 Achieved": {
                "unlocked": false,
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
                "unlocked": false,
                "description": "Reach a population of 50.",
                "reward": {
                    "type": "resource",
                    "resource": "Light",
                    "value": 50,
                    "turns": 3,
                    "description": "Gain +50 Light for the next 3 turns."
                }
            },
            "Technological Breakthrough": {
                "unlocked": false,
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
                "unlocked": false,
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
                "unlocked": false,
                "description": "Accumulate 200 Food.",
                "reward": {
                    "type": "resource",
                    "resource": "Food",
                    "value": 50,
                    "turns": 2,
                    "description": "Gain +50 Food for the next 2 turns."
                }
            },
            "Megalopolis": {
                "unlocked": false,
                "description": "Reach a population of 200.",
                "reward": {
                    "type": "population",
                    "value": 10,
                    "turns": 3,
                    "description": "Gain +10 Population for the next 3 turns."
                }
            },
            "Victory": {
                "unlocked": false,
                "description": "Unlock all achievements and build the Dimensional Gate.",
                "reward": {
                    "type": "resource",
                    "resource": "Technology",
                    "value": 100,
                    "turns": 5,
                    "description": "Gain +100 Technology for the next 5 turns."
                }
            }
        };
        this.activeBuffs = [];
    }

    checkAchievement(name, condition) {
        if (this.achievements[name] && !this.achievements[name].unlocked && condition()) {
            this.unlockAchievement(name);
        }
    }

    unlockAchievement(name) {
        if (this.achievements[name] && !this.achievements[name].unlocked) {
            this.achievements[name].unlocked = true;
            game.log(`🏆 Achievement Unlocked: ${name}!`, 'achievement');
            game.log(`${this.achievements[name].description}`, 'achievement');
            
            // Apply reward as buff
            const reward = this.achievements[name].reward;
            if (reward) {
                this.addBuff(name, reward.type, reward.description, reward.value, reward.turns, reward.resource);
            }

            this.updateDisplay();
            this.checkVictoryCondition();
        }
    }

    addBuff(name, buffType, description, value, turns, resource = null) {
        const buff = {
            name,
            type: buffType,
            description,
            value,
            remainingTurns: turns,
            resource
        };
        this.activeBuffs.push(buff);
        game.log(`Buff Active: ${description}`, 'achievement');
    }

    applyActiveBuffs() {
        for (let i = this.activeBuffs.length - 1; i >= 0; i--) {
            const buff = this.activeBuffs[i];
            
            if (buff.type === 'resource' && buff.resource) {
                game.resources.resources[buff.resource] += buff.value;
                game.log(`Buff: +${buff.value} ${game.resources.symbols[buff.resource]} ${buff.resource}`, 'resource-gain');
            } else if (buff.type === 'population') {
                game.population.modifyPopulation(buff.value);
            }

            buff.remainingTurns--;
            if (buff.remainingTurns <= 0) {
                game.log(`Buff expired: ${buff.description}`, 'achievement');
                this.activeBuffs.splice(i, 1);
            }
        }
    }

    checkVictoryCondition() {
        const unlockedCount = Object.values(this.achievements).filter(a => a.unlocked).length;
        const totalCount = Object.keys(this.achievements).length - 1; // Exclude Victory itself
        
        if (unlockedCount >= totalCount && game.buildings.buildings["Dimensional Gate"] >= 1) {
            this.checkAchievement('Victory', () => true);
        }
    }

    updateDisplay() {
        const achievementsList = document.getElementById('achievements-list');
        achievementsList.innerHTML = '';

        for (const [name, achievement] of Object.entries(this.achievements)) {
            const achievementElement = document.createElement('div');
            achievementElement.className = 'achievement-item';
            achievementElement.innerHTML = `
                <div class="achievement-info">
                    <div class="achievement-name">${name}</div>
                    <div class="achievement-description">${achievement.description}</div>
                </div>
                ${achievement.unlocked ? '<div class="achievement-unlocked">✓ Unlocked</div>' : ''}
            `;
            achievementsList.appendChild(achievementElement);
        }
    }
}

class EventManager {
    constructor() {
        this.events = [
            {
                "name": "Resource Surge",
                "description": "A sudden surge in Light resources boosts your civilization.",
                "effect": (game) => game.resources.addResources({"Light": 50}),
                "chance": 0.1
            },
            {
                "name": "Water Scarcity",
                "description": "Water resources are scarce this turn.",
                "effect": (game) => game.resources.modifyResource("Water", -30),
                "chance": 0.05
            },
            {
                "name": "Energy Boost",
                "description": "An energy boost increases your civilization's efficiency.",
                "effect": (game) => game.resources.addResources({"Energy": 30}),
                "chance": 0.1
            },
            {
                "name": "Population Boom",
                "description": "A sudden boom in population due to favorable conditions.",
                "effect": (game) => game.population.modifyPopulation(10),
                "chance": 0.05
            },
            {
                "name": "Land Expansion",
                "description": "New lands have been discovered, expanding your civilization's territory.",
                "effect": (game) => game.resources.addResources({"Land": 100}),
                "chance": 0.07
            },
            {
                "name": "Energy Drain",
                "description": "A mysterious energy drain affects your civilization.",
                "effect": (game) => game.resources.modifyResource("Energy", -40),
                "chance": 0.05
            },
            {
                "name": "Technological Advancement",
                "description": "A technological breakthrough improves resource generation.",
                "effect": (game) => game.resources.addResources({"Light": 20, "Energy": 20}),
                "chance": 0.08
            },
            {
                "name": "Metal Rush",
                "description": "A surge in demand for Metal resources boosts your Metal production.",
                "effect": (game) => game.resources.addResources({"Metal": 50}),
                "chance": 0.06
            },
            {
                "name": "Food Festival",
                "description": "A grand food festival enhances your Food resources.",
                "effect": (game) => game.resources.addResources({"Food": 100}),
                "chance": 0.04
            },
            {
                "name": "Tech Breakthrough",
                "description": "A breakthrough in technology accelerates your Technology research.",
                "effect": (game) => game.resources.addResources({"Technology": 50}),
                "chance": 0.05
            }
        ];
    }

    triggerEvent() {
        let triggered = false;
        for (const event of this.events) {
            if (Math.random() < event.chance) {
                game.log(`🌟 Event: ${event.name} - ${event.description}`, 'event');
                event.effect(game);
                triggered = true;
                break; // Only trigger one event per turn
            }
        }
        if (!triggered) {
            game.log("No events this turn.", 'event');
        }
    }
}

class Game {
    constructor() {
        this.player = new Player();
        this.resources = new ResourceManager();
        this.population = new Population();
        this.buildings = new BuildingManager();
        this.achievements = new AchievementManager();
        this.events = new EventManager();
        this.turnCounter = 1;
        this.gameOver = false;
    }

    start() {
        this.log("🌌 Welcome to Dimensional Architect!", 'achievement');
        this.log("Your journey begins in the void. Build your civilization and reach for the stars!", 'achievement');
        
        // Set player name
        const playerName = prompt("Enter your name, Leader of the Civilization:") || "Leader";
        this.player.name = playerName;
        
        this.updateAllDisplays();
        this.setupEventListeners();
    }

    setupEventListeners() {
        // Action buttons
        document.getElementById('gather-btn').addEventListener('click', () => this.gatherResources());
        document.getElementById('build-btn').addEventListener('click', () => this.showBuildModal());
        document.getElementById('upgrade-population-btn').addEventListener('click', () => this.upgradePopulation());
        document.getElementById('view-achievements-btn').addEventListener('click', () => this.toggleAchievementsPanel());
        document.getElementById('upgrade-building-btn').addEventListener('click', () => this.showUpgradeModal());
        document.getElementById('next-turn-btn').addEventListener('click', () => this.nextTurn());

        // Modal close buttons
        document.querySelectorAll('.close').forEach(closeBtn => {
            closeBtn.addEventListener('click', (e) => {
                e.target.closest('.modal').style.display = 'none';
            });
        });

        // Close modals when clicking outside
        window.addEventListener('click', (e) => {
            if (e.target.classList.contains('modal')) {
                e.target.style.display = 'none';
            }
        });
    }

    gatherResources() {
        this.resources.gather();
        this.log("Turn completed.", 'action');
    }

    showBuildModal() {
        const modal = document.getElementById('build-modal');
        const buildingOptions = document.getElementById('building-options');
        buildingOptions.innerHTML = '';

        const availableBuildings = this.buildings.getAvailableBuildings();
        
        availableBuildings.forEach(building => {
            const canAfford = this.buildings.canAffordBuilding(building, this.resources);
            const option = document.createElement('div');
            option.className = `building-option ${canAfford ? 'affordable' : 'unaffordable'}`;
            
            const costTexts = [];
            for (const [resource, amount] of Object.entries(building.cost)) {
                costTexts.push(`${this.resources.symbols[resource]} ${resource}: ${amount}`);
            }
            
            option.innerHTML = `
                <div class="option-header">
                    <span class="option-title">${building.emoji} ${building.name}</span>
                </div>
                <div class="option-cost">Cost: ${costTexts.join(', ')}</div>
            `;
            
            if (canAfford) {
                option.addEventListener('click', () => {
                    this.buildings.buildStructure(building.name, this.resources);
                    modal.style.display = 'none';
                });
            }
            
            buildingOptions.appendChild(option);
        });

        modal.style.display = 'block';
    }

    showUpgradeModal() {
        const modal = document.getElementById('upgrade-modal');
        const upgradeOptions = document.getElementById('upgrade-options');
        upgradeOptions.innerHTML = '';

        for (const [buildingName, count] of Object.entries(this.buildings.buildings)) {
            if (count > 0) {
                const upgradeCost = this.buildings.getUpgradeCost(buildingName);
                if (Object.keys(upgradeCost).length > 0) {
                    const canAfford = this.buildings.canUpgradeBuilding(buildingName, this.resources);
                    const option = document.createElement('div');
                    option.className = `upgrade-option ${canAfford ? 'affordable' : 'unaffordable'}`;
                    
                    const costTexts = [];
                    for (const [resource, amount] of Object.entries(upgradeCost)) {
                        costTexts.push(`${this.resources.symbols[resource]} ${resource}: ${amount}`);
                    }
                    
                    option.innerHTML = `
                        <div class="option-header">
                            <span class="option-title">${this.buildings.buildingEmojis[buildingName]} ${buildingName}</span>
                        </div>
                        <div class="option-cost">Upgrade Cost: ${costTexts.join(', ')}</div>
                    `;
                    
                    if (canAfford) {
                        option.addEventListener('click', () => {
                            this.buildings.upgradeBuilding(buildingName, this.resources);
                            modal.style.display = 'none';
                        });
                    }
                    
                    upgradeOptions.appendChild(option);
                }
            }
        }

        if (upgradeOptions.children.length === 0) {
            upgradeOptions.innerHTML = '<div class="upgrade-option">No buildings available for upgrade</div>';
        }

        modal.style.display = 'block';
    }

    upgradePopulation() {
        this.population.upgradePopulation(this.resources);
    }

    toggleAchievementsPanel() {
        const panel = document.querySelector('.achievements-panel');
        panel.style.display = panel.style.display === 'none' ? 'block' : 'none';
    }

    nextTurn() {
        this.turnCounter++;
        this.log(`--- Turn ${this.turnCounter} ---`, 'action');
        
        // Apply active buffs
        this.achievements.applyActiveBuffs();
        
        // Generate automatic resources
        this.resources.generateAutomaticResources(this.population, this.buildings);
        
        // Population growth
        this.population.grow();
        
        // Random events
        this.events.triggerEvent();
        
        // Check end conditions
        this.checkEndConditions();
        
        // Update turn counter
        document.getElementById('turn-counter').textContent = this.turnCounter;
        
        this.log("Turn completed.", 'action');
    }

    checkEndConditions() {
        if (this.achievements.achievements["Victory"].unlocked) {
            this.log("🎉 Victory! You have completed your journey and won the game!", 'achievement');
            // Could add portal button or end game here
        } else if (this.resources.resources["Light"] <= 0 || this.resources.resources["Water"] <= 0) {
            this.log("☠️ Resources depleted! Your civilization cannot survive.", 'action');
            this.gameOver = true;
        }
    }

    updateAllDisplays() {
        this.player.updateDisplay();
        this.resources.updateDisplay();
        this.population.updateDisplay();
        this.buildings.updateDisplay();
        this.achievements.updateDisplay();
    }

    log(message, type = 'info') {
        const gameLog = document.getElementById('game-log');
        const logEntry = document.createElement('div');
        logEntry.className = `log-entry ${type}`;
        logEntry.textContent = `[${new Date().toLocaleTimeString()}] ${message}`;
        gameLog.appendChild(logEntry);
        gameLog.scrollTop = gameLog.scrollHeight;
    }
}

// Initialize game when page loads
let game;
document.addEventListener('DOMContentLoaded', () => {
    game = new Game();
    game.start();
});