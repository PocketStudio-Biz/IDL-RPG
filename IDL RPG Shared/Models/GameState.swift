//
//  GameState.swift
//  IDL RPG Shared
//
//  Created by MyKey on 11/17/25.
//

import Foundation

/// Complete game state for save/load functionality
struct GameState: Codable {
    var player: Player
    var currentEnemy: Enemy?
    var battleState: BattleState
    var inventory: [Equipment]
    var gameSettings: GameSettings
    var lastUpdateTime: Date
    var version: String // For migration purposes
    
    init(
        player: Player = Player(),
        currentEnemy: Enemy? = nil,
        battleState: BattleState = .idle,
        inventory: [Equipment] = [],
        gameSettings: GameSettings = GameSettings(),
        lastUpdateTime: Date = Date(),
        version: String = "1.0"
    ) {
        self.player = player
        self.currentEnemy = currentEnemy
        self.battleState = battleState
        self.inventory = inventory
        self.gameSettings = gameSettings
        self.lastUpdateTime = lastUpdateTime
        self.version = version
    }
}

enum BattleState: String, Codable {
    case idle
    case fighting
    case victory
    case defeat
    case paused
}

/// Game settings and preferences
struct GameSettings: Codable {
    var soundEnabled: Bool
    var musicEnabled: Bool
    var notificationsEnabled: Bool
    var autoBattleEnabled: Bool
    var battleSpeed: BattleSpeed
    
    init(
        soundEnabled: Bool = true,
        musicEnabled: Bool = true,
        notificationsEnabled: Bool = true,
        autoBattleEnabled: Bool = true,
        battleSpeed: BattleSpeed = .normal
    ) {
        self.soundEnabled = soundEnabled
        self.musicEnabled = musicEnabled
        self.notificationsEnabled = notificationsEnabled
        self.autoBattleEnabled = autoBattleEnabled
        self.battleSpeed = battleSpeed
    }
}

enum BattleSpeed: String, Codable {
    case slow
    case normal
    case fast
    
    var multiplier: Double {
        switch self {
        case .slow:
            return 0.5
        case .normal:
            return 1.0
        case .fast:
            return 2.0
        }
    }
}

