//
//  CharacterViewModel.swift
//  IDL RPG Shared
//
//  Created by MyKey on 11/17/25.
//

import Foundation
import Combine
import SwiftUI

/// View model for character/stats view
class CharacterViewModel: ObservableObject {
    @Published var player: Player
    @Published var inventory: [Equipment]
    
    private let gameStateManager: GameStateManager
    private var cancellables = Set<AnyCancellable>()
    
    init(gameStateManager: GameStateManager) {
        self.gameStateManager = gameStateManager
        self.player = gameStateManager.gameState.player
        self.inventory = gameStateManager.gameState.inventory
        
        observeGameState()
    }
    
    /// Equips an item
    func equipItem(_ equipment: Equipment) {
        gameStateManager.equipItem(equipment)
    }
    
    /// Observes game state changes
    private func observeGameState() {
        gameStateManager.$gameState
            .sink { [weak self] state in
                self?.player = state.player
                self?.inventory = state.inventory
            }
            .store(in: &cancellables)
    }
}

