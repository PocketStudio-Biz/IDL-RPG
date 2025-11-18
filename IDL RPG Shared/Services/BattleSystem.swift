//
//  BattleSystem.swift
//  IDL RPG Shared
//
//  Created by MyKey on 11/17/25.
//

import Foundation
import Combine

/// Handles automatic combat calculations and battle logic
class BattleSystem: ObservableObject {
    @Published var battleLog: [BattleEvent] = []
    @Published var isBattleActive: Bool = false
    
    private var battleTimer: Timer?
    private var currentBattleState: BattleState = .idle
    
    /// Executes a single turn of combat
    func executeTurn(player: inout Player, enemy: inout Enemy) -> BattleResult {
        let turnOrder = ProgressionSystem.determineTurnOrder(
            playerSpeed: player.speed,
            enemySpeed: enemy.speed
        )
        
        var events: [BattleEvent] = []
        
        // Player turn
        if turnOrder == .playerFirst || turnOrder == .playerFirst {
            let playerDamage = ProgressionSystem.calculateDamage(
                attackerAttack: player.attack,
                defenderDefense: enemy.defense
            )
            let enemyDefeated = enemy.takeDamage(playerDamage)
            events.append(.playerAttack(damage: playerDamage, enemyHealth: enemy.currentHealth))
            
            if enemyDefeated {
                return .victory(events: events)
            }
        }
        
        // Enemy turn
        let enemyDamage = ProgressionSystem.calculateDamage(
            attackerAttack: enemy.attack,
            defenderDefense: player.defense
        )
        player.currentHealth = max(0, player.currentHealth - enemyDamage)
        events.append(.enemyAttack(damage: enemyDamage, playerHealth: player.currentHealth))
        
        if player.currentHealth <= 0 {
            return .defeat(events: events)
        }
        
        // Player turn (if enemy went first)
        if turnOrder == .enemyFirst {
            let playerDamage = ProgressionSystem.calculateDamage(
                attackerAttack: player.attack,
                defenderDefense: enemy.defense
            )
            let enemyDefeated = enemy.takeDamage(playerDamage)
            events.append(.playerAttack(damage: playerDamage, enemyHealth: enemy.currentHealth))
            
            if enemyDefeated {
                return .victory(events: events)
            }
        }
        
        return .ongoing(events: events)
    }
    
    /// Starts automatic battle
    func startAutoBattle(player: inout Player, enemy: inout Enemy, speed: BattleSpeed = .normal) {
        isBattleActive = true
        currentBattleState = .fighting
        battleLog.removeAll()
        
        let interval = 1.0 / speed.multiplier
        
        battleTimer = Timer.scheduledTimer(withTimeInterval: interval, repeats: true) { [weak self] _ in
            guard let self = self else { return }
            
            let result = self.executeTurn(player: &player, enemy: &enemy)
            
            switch result {
            case .victory(let events):
                self.battleLog.append(contentsOf: events)
                self.endBattle(result: .victory(events: events))
                
            case .defeat(let events):
                self.battleLog.append(contentsOf: events)
                self.endBattle(result: .defeat(events: events))
                
            case .ongoing(let events):
                self.battleLog.append(contentsOf: events)
            }
        }
    }
    
    /// Stops the automatic battle
    func stopBattle() {
        battleTimer?.invalidate()
        battleTimer = nil
        isBattleActive = false
        currentBattleState = .idle
    }
    
    private func endBattle(result: BattleResult) {
        stopBattle()
        currentBattleState = result.isVictory ? .victory : .defeat
    }
}

/// Battle events for logging and visualization
enum BattleEvent {
    case playerAttack(damage: Int, enemyHealth: Int)
    case enemyAttack(damage: Int, playerHealth: Int)
    case playerLevelUp(newLevel: Int)
    case enemyDefeated
    case playerDefeated
    case lootObtained(equipment: Equipment?, gold: Int)
}

/// Result of a battle turn or complete battle
enum BattleResult {
    case victory(events: [BattleEvent])
    case defeat(events: [BattleEvent])
    case ongoing(events: [BattleEvent])
    
    var isVictory: Bool {
        if case .victory = self {
            return true
        }
        return false
    }
    
    var isDefeat: Bool {
        if case .defeat = self {
            return true
        }
        return false
    }
}

