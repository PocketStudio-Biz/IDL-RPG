//
//  Enemy.swift
//  IDL RPG Shared
//
//  Created by MyKey on 11/17/25.
//

import Foundation

/// Represents an enemy with stats and loot table
struct Enemy: Codable, Identifiable {
    let id: UUID
    var name: String
    var level: Int
    
    // Stats
    var maxHealth: Int
    var currentHealth: Int
    var attack: Int
    var defense: Int
    var speed: Int
    
    // Rewards
    var experienceReward: Int
    var goldReward: Int
    var lootTable: [LootItem]
    
    // Visual
    var spriteName: String
    
    init(
        id: UUID = UUID(),
        name: String,
        level: Int,
        maxHealth: Int,
        attack: Int,
        defense: Int,
        speed: Int,
        experienceReward: Int,
        goldReward: Int,
        lootTable: [LootItem] = [],
        spriteName: String = "enemy_default"
    ) {
        self.id = id
        self.name = name
        self.level = level
        self.maxHealth = maxHealth
        self.currentHealth = maxHealth
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.experienceReward = experienceReward
        self.goldReward = goldReward
        self.lootTable = lootTable
        self.spriteName = spriteName
    }
    
    /// Creates a scaled enemy based on player level
    static func createForLevel(_ playerLevel: Int, enemyType: EnemyType = .normal) -> Enemy {
        let level = max(1, playerLevel + Int.random(in: -2...3))
        let levelMultiplier = Double(level) * 0.5
        
        let baseHealth = Int(50 + (levelMultiplier * 20))
        let baseAttack = Int(5 + (levelMultiplier * 2))
        let baseDefense = Int(2 + (levelMultiplier * 1))
        let baseSpeed = Int(5 + (levelMultiplier * 1))
        
        let expReward = Int(10 + (levelMultiplier * 5))
        let goldReward = Int(5 + (levelMultiplier * 3))
        
        var lootTable: [LootItem] = []
        if Double.random(in: 0...1) < 0.3 { // 30% chance for loot
            lootTable.append(LootItem.randomEquipment(for: level))
        }
        
        return Enemy(
            name: enemyType.name(for: level),
            level: level,
            maxHealth: baseHealth,
            attack: baseAttack,
            defense: baseDefense,
            speed: baseSpeed,
            experienceReward: expReward,
            goldReward: goldReward,
            lootTable: lootTable,
            spriteName: enemyType.spriteName
        )
    }
    
    /// Takes damage and returns if enemy is defeated
    mutating func takeDamage(_ amount: Int) -> Bool {
        let actualDamage = max(1, amount - defense)
        currentHealth = max(0, currentHealth - actualDamage)
        return currentHealth <= 0
    }
}

/// Enemy types with different characteristics
enum EnemyType: String, Codable {
    case normal
    case elite
    case boss
    
    func name(for level: Int) -> String {
        switch self {
        case .normal:
            return "Goblin Lv.\(level)"
        case .elite:
            return "Elite Orc Lv.\(level)"
        case .boss:
            return "Boss Lv.\(level)"
        }
    }
    
    var spriteName: String {
        switch self {
        case .normal:
            return "enemy_goblin"
        case .elite:
            return "enemy_orc"
        case .boss:
            return "enemy_boss"
        }
    }
}

/// Represents a loot item that can drop from enemies
struct LootItem: Codable {
    var equipment: Equipment?
    var gold: Int
    var dropChance: Double // 0.0 to 1.0
    
    static func randomEquipment(for level: Int) -> LootItem {
        let equipment = Equipment.random(for: level)
        return LootItem(equipment: equipment, gold: 0, dropChance: 0.3)
    }
}

