//
//  GameStateManager.swift
//  IDL RPG Shared
//
//  Created by MyKey on 11/17/25.
//

import Foundation
import Combine

/// Central coordinator for game state management
class GameStateManager: ObservableObject {
    @Published var gameState: GameState
    @Published var offlineRewards: OfflineRewards?
    
    private let saveManager = SaveManager()
    private let battleSystem = BattleSystem()
    private var cancellables = Set<AnyCancellable>()
    
    init() {
        // Try to load existing game state, otherwise create new
        if let loadedState = try? saveManager.load() {
            self.gameState = loadedState
            
            // Calculate offline rewards if applicable
            if gameState.battleState == .idle {
                calculateOfflineRewards()
            }
        } else {
            self.gameState = GameState()
        }
        
        // Auto-save periodically
        setupAutoSave()
    }
    
    /// Calculates and applies offline rewards
    func calculateOfflineRewards() {
        let rewards = IdleCalculator.calculateOfflineRewards(
            player: gameState.player,
            lastSaveTime: gameState.player.lastSaveTime
        )
        
        // Only show rewards if there are meaningful gains
        if rewards.experienceGained > 0 || rewards.goldGained > 0 || !rewards.lootObtained.isEmpty {
            offlineRewards = rewards
        }
    }
    
    /// Applies offline rewards to the game state
    func applyOfflineRewards() {
        guard let rewards = offlineRewards else { return }
        
        // Add experience
        _ = gameState.player.addExperience(rewards.experienceGained)
        
        // Add gold
        gameState.player.gold += rewards.goldGained
        
        // Add loot to inventory
        gameState.inventory.append(contentsOf: rewards.lootObtained)
        
        // Clear rewards
        offlineRewards = nil
        
        // Save after applying rewards
        save()
    }
    
    /// Starts a new battle
    func startBattle() {
        guard gameState.battleState == .idle else { return }
        
        gameState.currentEnemy = Enemy.createForLevel(gameState.player.level)
        gameState.battleState = .fighting
        
        // Start auto-battle
        var player = gameState.player
        if var enemy = gameState.currentEnemy {
            battleSystem.startAutoBattle(
                player: &player,
                enemy: &enemy,
                speed: gameState.gameSettings.battleSpeed
            )
            
            gameState.player = player
            gameState.currentEnemy = enemy
        }
        
        save()
    }
    
    /// Handles battle victory
    func handleVictory() {
        guard let enemy = gameState.currentEnemy else { return }
        
        let events = ProgressionSystem.applyVictoryRewards(
            player: &gameState.player,
            enemy: enemy
        )
        
        // Add loot to inventory
        for event in events {
            if case .lootObtained(let equipment, _) = event, let equipment = equipment {
                gameState.inventory.append(equipment)
            }
        }
        
        gameState.currentEnemy = nil
        gameState.battleState = .idle
        
        save()
    }
    
    /// Handles battle defeat
    func handleDefeat() {
        gameState.battleState = .defeat
        gameState.currentEnemy = nil
        
        // Restore player health to 50% on defeat
        gameState.player.currentHealth = gameState.player.maxHealth / 2
        
        save()
    }
    
    /// Equips an item from inventory
    func equipItem(_ equipment: Equipment) {
        // Remove from inventory
        gameState.inventory.removeAll { $0.id == equipment.id }
        
        // Unequip current item of same type if exists
        if equipment.type == .weapon, let currentWeapon = gameState.player.equippedWeapon {
            gameState.inventory.append(currentWeapon)
        } else if equipment.type == .armor, let currentArmor = gameState.player.equippedArmor {
            gameState.inventory.append(currentArmor)
        }
        
        // Equip new item
        gameState.player.equip(equipment)
        
        save()
    }
    
    /// Saves the current game state
    func save() {
        saveManager.autoSave(gameState)
    }
    
    /// Sets up automatic saving
    private func setupAutoSave() {
        // Auto-save every 30 seconds
        Timer.publish(every: 30, on: .main, in: .common)
            .autoconnect()
            .sink { [weak self] _ in
                self?.save()
            }
            .store(in: &cancellables)
    }
}

