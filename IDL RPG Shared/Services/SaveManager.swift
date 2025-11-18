//
//  SaveManager.swift
//  IDL RPG Shared
//
//  Created by MyKey on 11/17/25.
//

import Foundation

/// Manages game state persistence using UserDefaults
class SaveManager {
    private let saveKey = "IDLRPG_GameState"
    private let encoder = JSONEncoder()
    private let decoder = JSONDecoder()
    
    init() {
        encoder.dateEncodingStrategy = .iso8601
        decoder.dateDecodingStrategy = .iso8601
    }
    
    /// Saves game state to UserDefaults
    func save(_ gameState: GameState) throws {
        var stateToSave = gameState
        stateToSave.lastUpdateTime = Date()
        stateToSave.player.lastSaveTime = Date()
        
        let data = try encoder.encode(stateToSave)
        UserDefaults.standard.set(data, forKey: saveKey)
        UserDefaults.standard.synchronize()
    }
    
    /// Loads game state from UserDefaults
    func load() throws -> GameState? {
        guard let data = UserDefaults.standard.data(forKey: saveKey) else {
            return nil
        }
        
        let gameState = try decoder.decode(GameState.self, from: data)
        return gameState
    }
    
    /// Deletes saved game state
    func delete() {
        UserDefaults.standard.removeObject(forKey: saveKey)
        UserDefaults.standard.synchronize()
    }
    
    /// Checks if a save file exists
    func hasSaveFile() -> Bool {
        return UserDefaults.standard.data(forKey: saveKey) != nil
    }
    
    /// Auto-saves game state (non-throwing version for convenience)
    func autoSave(_ gameState: GameState) {
        do {
            try save(gameState)
        } catch {
            print("Auto-save failed: \(error.localizedDescription)")
        }
    }
}

