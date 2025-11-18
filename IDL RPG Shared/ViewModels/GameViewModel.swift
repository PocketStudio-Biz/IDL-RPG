//
//  GameViewModel.swift
//  IDL RPG Shared
//
//  Created by MyKey on 11/17/25.
//

import Foundation
import Combine
import SwiftUI

/// Main game view model coordinating all game systems
class GameViewModel: ObservableObject {
    @Published var gameStateManager: GameStateManager
    @Published var currentView: GameView = .battle
    
    init(gameStateManager: GameStateManager = GameStateManager()) {
        self.gameStateManager = gameStateManager
        
        // Observe battle system
        observeBattleSystem()
    }
    
    /// Starts a new battle
    func startBattle() {
        gameStateManager.startBattle()
    }
    
    /// Handles battle result
    func handleBattleResult(_ result: BattleResult) {
        if result.isVictory {
            gameStateManager.handleVictory()
        } else if result.isDefeat {
            gameStateManager.handleDefeat()
        }
    }
    
    /// Applies offline rewards
    func applyOfflineRewards() {
        gameStateManager.applyOfflineRewards()
    }
    
    /// Observes battle system for updates
    private func observeBattleSystem() {
        // Battle system updates will be handled through GameStateManager
    }
}

enum GameView {
    case battle
    case character
    case inventory
    case shop
    case settings
}

