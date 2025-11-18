//
//  IdleCalculator.swift
//  IDL RPG Shared
//
//  Created by MyKey on 11/17/25.
//

import Foundation

/// Calculates offline rewards with safety caps
class IdleCalculator {
    /// Maximum offline time to calculate rewards for (in seconds)
    /// Default: 24 hours
    static let maxOfflineTime: TimeInterval = 24 * 60 * 60
    
    /// Maximum number of enemies that can be defeated offline
    static let maxOfflineEnemies: Int = 100
    
    /// Average time per battle (in seconds)
    static let averageBattleTime: TimeInterval = 5.0
    
    /// Calculates rewards for offline time
    static func calculateOfflineRewards(
        player: Player,
        lastSaveTime: Date,
        currentTime: Date = Date()
    ) -> OfflineRewards {
        let timeAway = currentTime.timeIntervalSince(lastSaveTime)
        
        // Cap the offline time
        let cappedTime = min(timeAway, maxOfflineTime)
        
        guard cappedTime > 60 else { // Less than 1 minute, no rewards
            return OfflineRewards(
                timeAway: timeAway,
                enemiesDefeated: 0,
                experienceGained: 0,
                goldGained: 0,
                lootObtained: []
            )
        }
        
        // Estimate battles based on time
        let estimatedBattles = Int(cappedTime / averageBattleTime)
        let battlesToProcess = min(estimatedBattles, maxOfflineEnemies)
        
        // Simulate battles (simplified calculation)
        var totalExperience = 0
        var totalGold = 0
        var lootItems: [Equipment] = []
        
        for _ in 0..<battlesToProcess {
            // Create enemy scaled to player level
            let enemy = Enemy.createForLevel(player.level)
            
            // Assume player wins (simplified - in reality would need battle simulation)
            // For offline, we assume player wins based on their stats
            let playerWinChance = calculateWinChance(player: player, enemy: enemy)
            
            if Double.random(in: 0...1) < playerWinChance {
                totalExperience += enemy.experienceReward
                totalGold += enemy.goldReward
                
                // Check for loot
                for lootItem in enemy.lootTable {
                    if Double.random(in: 0...1) < lootItem.dropChance {
                        if let equipment = lootItem.equipment {
                            lootItems.append(equipment)
                        }
                    }
                }
            }
        }
        
        return OfflineRewards(
            timeAway: timeAway,
            enemiesDefeated: battlesToProcess,
            experienceGained: totalExperience,
            goldGained: totalGold,
            lootObtained: lootItems
        )
    }
    
    /// Calculates win chance based on player and enemy stats
    private static func calculateWinChance(player: Player, enemy: Enemy) -> Double {
        let playerPower = Double(player.attack + player.defense + player.maxHealth / 10)
        let enemyPower = Double(enemy.attack + enemy.defense + enemy.maxHealth / 10)
        
        let totalPower = playerPower + enemyPower
        guard totalPower > 0 else { return 0.5 }
        
        return playerPower / totalPower
    }
}

/// Represents rewards earned while offline
struct OfflineRewards: Codable {
    var timeAway: TimeInterval
    var enemiesDefeated: Int
    var experienceGained: Int
    var goldGained: Int
    var lootObtained: [Equipment]
    
    var formattedTimeAway: String {
        let hours = Int(timeAway) / 3600
        let minutes = (Int(timeAway) % 3600) / 60
        
        if hours > 0 {
            return "\(hours)h \(minutes)m"
        } else {
            return "\(minutes)m"
        }
    }
}

