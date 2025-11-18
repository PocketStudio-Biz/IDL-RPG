//
//  SettingsView.swift
//  IDL RPG Shared
//
//  Created by MyKey on 11/17/25.
//

import SwiftUI

/// Settings and preferences view
struct SettingsView: View {
    @ObservedObject var gameStateManager: GameStateManager
    @State private var showResetConfirmation = false
    
    var body: some View {
        Form {
            Section(header: Text("Audio")) {
                Toggle("Sound Effects", isOn: Binding(
                    get: { gameStateManager.gameState.gameSettings.soundEnabled },
                    set: { gameStateManager.gameState.gameSettings.soundEnabled = $0; gameStateManager.save() }
                ))
                
                Toggle("Music", isOn: Binding(
                    get: { gameStateManager.gameState.gameSettings.musicEnabled },
                    set: { gameStateManager.gameState.gameSettings.musicEnabled = $0; gameStateManager.save() }
                ))
            }
            
            Section(header: Text("Gameplay")) {
                Toggle("Auto Battle", isOn: Binding(
                    get: { gameStateManager.gameState.gameSettings.autoBattleEnabled },
                    set: { gameStateManager.gameState.gameSettings.autoBattleEnabled = $0; gameStateManager.save() }
                ))
                
                Picker("Battle Speed", selection: Binding(
                    get: { gameStateManager.gameState.gameSettings.battleSpeed },
                    set: { gameStateManager.gameState.gameSettings.battleSpeed = $0; gameStateManager.save() }
                )) {
                    Text("Slow").tag(BattleSpeed.slow)
                    Text("Normal").tag(BattleSpeed.normal)
                    Text("Fast").tag(BattleSpeed.fast)
                }
            }
            
            Section(header: Text("Notifications")) {
                Toggle("Enable Notifications", isOn: Binding(
                    get: { gameStateManager.gameState.gameSettings.notificationsEnabled },
                    set: { gameStateManager.gameState.gameSettings.notificationsEnabled = $0; gameStateManager.save() }
                ))
            }
            
            Section(header: Text("Data")) {
                Button(action: { showResetConfirmation = true }) {
                    HStack {
                        Image(systemName: "trash")
                        Text("Reset Game Data")
                            .foregroundColor(AppConstants.Colors.accent)
                    }
                }
            }
            
            Section(header: Text("About")) {
                HStack {
                    Text("Version")
                    Spacer()
                    Text("1.0")
                        .foregroundColor(AppConstants.Colors.textSecondary)
                }
            }
        }
        .background(AppConstants.Colors.background)
        .alert("Reset Game Data", isPresented: $showResetConfirmation) {
            Button("Cancel", role: .cancel) { }
            Button("Reset", role: .destructive) {
                resetGameData()
            }
        } message: {
            Text("This will delete all your progress. This action cannot be undone.")
        }
    }
    
    private func resetGameData() {
        gameStateManager.gameState = GameState()
        gameStateManager.save()
    }
}

