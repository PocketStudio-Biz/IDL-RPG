//
//  Progression.swift
//  IDL RPG Shared
//
//  Created by MyKey on 11/17/25.
//

import Foundation

/// Progression formulas and calculations
struct ProgressionSystem {
    /// Calculates experience required for a given level
    /// Uses exponential curve: XP = base * (multiplier ^ (level - 1))
    static func experienceForLevel(_ level: Int) -> Int {
        guard level > 1 else { return 0 }
        
        let baseXP = 100
        let multiplier = 1.5
        
        // Sum of geometric series
        var totalXP = 0
        for lvl in 2...level {
            let xpForThisLevel = Int(Double(baseXP) * pow(multiplier, Double(lvl - 2)))
            totalXP += xpForThisLevel
        }
        
        return totalXP
    }
    
    /// Calculates stat growth per level
    static func statGrowth(level: Int, baseStat: Int) -> Int {
        let growthRate = 1.0 + (Double(level - 1) * 0.1)
        return Int(Double(baseStat) * growthRate)
    }
    
    /// Calculates damage dealt in combat
    static func calculateDamage(attackerAttack: Int, defenderDefense: Int) -> Int {
        let baseDamage = attackerAttack
        let mitigatedDamage = max(1, baseDamage - defenderDefense)
        
        // Add random variance (80% to 120%)
        let variance = Double.random(in: 0.8...1.2)
        return max(1, Int(Double(mitigatedDamage) * variance))
    }
    
    /// Determines turn order based on speed
    static func determineTurnOrder(playerSpeed: Int, enemySpeed: Int) -> TurnOrder {
        if playerSpeed > enemySpeed {
            return .playerFirst
        } else if enemySpeed > playerSpeed {
            return .enemyFirst
        } else {
            // Tie breaker: random
            return Bool.random() ? .playerFirst : .enemyFirst
        }
    }
    
    /// Calculates gold reward based on enemy level
    static func goldReward(for enemyLevel: Int) -> Int {
        let baseGold = 5
        let levelBonus = enemyLevel * 3
        let randomBonus = Int.random(in: 0...5)
        return baseGold + levelBonus + randomBonus
    }
    
    /// Calculates experience reward based on enemy level
    static func experienceReward(for enemyLevel: Int, playerLevel: Int) -> Int {
        let baseXP = 10
        let levelBonus = enemyLevel * 5
        
        // Bonus for defeating higher level enemies
        let levelDifference = enemyLevel - playerLevel
        let difficultyBonus = max(0, levelDifference * 10)
        
        return baseXP + levelBonus + difficultyBonus
    }
}

enum TurnOrder {
    case playerFirst
    case enemyFirst
}

