//
//  MainGameView.swift
//  IDL RPG Shared
//
//  Created by MyKey on 11/17/25.
//

import SwiftUI

/// Main game view with tab navigation
struct MainGameView: View {
    @StateObject private var viewModel = GameViewModel()
    @State private var selectedTab = 0
    
    var body: some View {
        TabView(selection: $selectedTab) {
            BattleView(viewModel: BattleViewModel(gameStateManager: viewModel.gameStateManager))
                .tabItem {
                    Label("Battle", systemImage: "sword")
                }
                .tag(0)
            
            CharacterView(viewModel: CharacterViewModel(gameStateManager: viewModel.gameStateManager))
                .tabItem {
                    Label("Character", systemImage: "person.fill")
                }
                .tag(1)
            
            InventoryView(viewModel: CharacterViewModel(gameStateManager: viewModel.gameStateManager))
                .tabItem {
                    Label("Inventory", systemImage: "bag.fill")
                }
                .tag(2)
            
            SettingsView(gameStateManager: viewModel.gameStateManager)
                .tabItem {
                    Label("Settings", systemImage: "gearshape.fill")
                }
                .tag(3)
        }
        .accentColor(AppConstants.Colors.primary)
        .onAppear {
            // Check for offline rewards
            if viewModel.gameStateManager.offlineRewards != nil {
                showOfflineRewards()
            }
        }
        .sheet(item: Binding(
            get: { viewModel.gameStateManager.offlineRewards != nil ? OfflineRewardsWrapper(viewModel.gameStateManager.offlineRewards!) : nil },
            set: { _ in viewModel.gameStateManager.offlineRewards = nil }
        )) { wrapper in
            OfflineRewardsView(rewards: wrapper.rewards) {
                viewModel.applyOfflineRewards()
            }
        }
    }
    
    private func showOfflineRewards() {
        // Sheet will be shown automatically via binding
    }
}

struct OfflineRewardsWrapper: Identifiable {
    let id = UUID()
    let rewards: OfflineRewards
}

