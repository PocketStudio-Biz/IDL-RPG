//
//  ProgressionSystem.swift
//  IDL RPG Shared
//
//  Created by MyKey on 11/17/25.
//

import Foundation

/// Handles character progression, leveling, and stat growth
class ProgressionSystem {
    /// Applies rewards after defeating an enemy
    static func applyVictoryRewards(player: inout Player, enemy: Enemy) -> [BattleEvent] {
        var events: [BattleEvent] = []
        
        // Add experience
        let leveledUp = player.addExperience(enemy.experienceReward)
        if leveledUp {
            events.append(.playerLevelUp(newLevel: player.level))
        }
        
        // Add gold
        player.gold += enemy.goldReward
        
        // Handle loot
        for lootItem in enemy.lootTable {
            if Double.random(in: 0...1) < lootItem.dropChance {
                if let equipment = lootItem.equipment {
                    events.append(.lootObtained(equipment: equipment, gold: 0))
                }
                if lootItem.gold > 0 {
                    player.gold += lootItem.gold
                    events.append(.lootObtained(equipment: nil, gold: lootItem.gold))
                }
            }
        }
        
        return events
    }
    
    /// Calculates stat growth for a level up
    static func calculateLevelUpStats(baseStats: (health: Int, attack: Int, defense: Int, speed: Int), level: Int) -> (health: Int, attack: Int, defense: Int, speed: Int) {
        let growthMultiplier = 1.0 + (Double(level - 1) * 0.1)
        
        return (
            health: Int(Double(baseStats.health) * growthMultiplier),
            attack: Int(Double(baseStats.attack) * growthMultiplier),
            defense: Int(Double(baseStats.defense) * growthMultiplier),
            speed: Int(Double(baseStats.speed) * growthMultiplier)
        )
    }
    
    /// Validates if player can afford an equipment purchase
    static func canAfford(player: Player, equipment: Equipment) -> Bool {
        return player.gold >= equipment.goldCost
    }
    
    /// Purchases equipment (removes gold, adds to inventory)
    static func purchaseEquipment(player: inout Player, equipment: Equipment) -> Bool {
        guard canAfford(player: player, equipment: equipment) else {
            return false
        }
        
        player.gold -= equipment.goldCost
        return true
    }
}

