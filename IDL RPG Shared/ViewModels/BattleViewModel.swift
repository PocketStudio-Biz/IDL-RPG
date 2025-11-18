//
//  BattleViewModel.swift
//  IDL RPG Shared
//
//  Created by MyKey on 11/17/25.
//

import Foundation
import Combine
import SwiftUI

/// View model for battle view
class BattleViewModel: ObservableObject {
    @Published var player: Player
    @Published var enemy: Enemy?
    @Published var battleState: BattleState = .idle
    @Published var battleLog: [BattleEvent] = []
    @Published var isBattleActive: Bool = false
    
    private let gameStateManager: GameStateManager
    private let battleSystem: BattleSystem
    private var cancellables = Set<AnyCancellable>()
    
    init(gameStateManager: GameStateManager) {
        self.gameStateManager = gameStateManager
        self.player = gameStateManager.gameState.player
        self.enemy = gameStateManager.gameState.currentEnemy
        self.battleState = gameStateManager.gameState.battleState
        self.battleSystem = BattleSystem()
        
        observeGameState()
    }
    
    /// Starts a battle
    func startBattle() {
        gameStateManager.startBattle()
    }
    
    /// Pauses the battle
    func pauseBattle() {
        battleSystem.stopBattle()
        gameStateManager.gameState.battleState = .paused
    }
    
    /// Resumes the battle
    func resumeBattle() {
        guard let enemy = enemy else { return }
        var player = self.player
        battleSystem.startAutoBattle(
            player: &player,
            enemy: &enemy,
            speed: gameStateManager.gameState.gameSettings.battleSpeed
        )
        self.player = player
    }
    
    /// Observes game state changes
    private func observeGameState() {
        gameStateManager.$gameState
            .sink { [weak self] state in
                self?.player = state.player
                self?.enemy = state.currentEnemy
                self?.battleState = state.battleState
            }
            .store(in: &cancellables)
        
        battleSystem.$battleLog
            .assign(to: &$battleLog)
        
        battleSystem.$isBattleActive
            .assign(to: &$isBattleActive)
    }
}

