//
//  BattleView.swift
//  IDL RPG Shared
//
//  Created by MyKey on 11/17/25.
//

import SwiftUI
import SpriteKit
#if os(iOS)
import UIKit
#endif
#if os(OSX)
import AppKit
#endif

/// Main battle view with SpriteKit visualization
struct BattleView: View {
    @ObservedObject var viewModel: BattleViewModel
    @State private var showBattleScene = true
    
    var body: some View {
        ZStack {
            AppConstants.Colors.background
                .ignoresSafeArea()
            
            VStack(spacing: 0) {
                // Player Stats Bar
                PlayerStatsBar(player: viewModel.player)
                    .padding(.horizontal, AppConstants.Spacing.medium)
                    .padding(.top, AppConstants.Spacing.medium)
                
                // Battle Scene
                if showBattleScene {
                    SpriteKitBattleScene(
                        player: viewModel.player,
                        enemy: viewModel.enemy,
                        battleState: viewModel.battleState
                    )
                    .frame(maxWidth: .infinity, maxHeight: .infinity)
                }
                
                // Enemy Stats Bar
                if let enemy = viewModel.enemy {
                    EnemyStatsBar(enemy: enemy)
                        .padding(.horizontal, AppConstants.Spacing.medium)
                        .padding(.bottom, AppConstants.Spacing.medium)
                }
                
                // Battle Controls
                BattleControlsView(
                    battleState: viewModel.battleState,
                    isBattleActive: viewModel.isBattleActive,
                    onStartBattle: { viewModel.startBattle() },
                    onPauseBattle: { viewModel.pauseBattle() },
                    onResumeBattle: { viewModel.resumeBattle() }
                )
                .padding(.horizontal, AppConstants.Spacing.medium)
                .padding(.bottom, AppConstants.Spacing.medium)
            }
        }
    }
}

/// Player stats display bar
struct PlayerStatsBar: View {
    let player: Player
    
    var body: some View {
        VStack(alignment: .leading, spacing: AppConstants.Spacing.small) {
            HStack {
                Text(player.name)
                    .font(.headline)
                    .foregroundColor(AppConstants.Colors.textPrimary)
                
                Spacer()
                
                Text("Lv. \(player.level)")
                    .font(.subheadline)
                    .foregroundColor(AppConstants.Colors.textSecondary)
            }
            
            // Health Bar
            HealthBar(current: player.currentHealth, max: player.maxHealth, color: AppConstants.Colors.success)
            
            // Stats
            HStack(spacing: AppConstants.Spacing.medium) {
                StatBadge(icon: "sword", value: player.attack)
                StatBadge(icon: "shield", value: player.defense)
                StatBadge(icon: "bolt", value: player.speed)
            }
        }
        .padding(AppConstants.Spacing.medium)
        .background(
            RoundedRectangle(cornerRadius: AppConstants.CornerRadius.medium)
                .fill(Color.black.opacity(0.3))
        )
    }
}

/// Enemy stats display bar
struct EnemyStatsBar: View {
    let enemy: Enemy
    
    var body: some View {
        VStack(alignment: .leading, spacing: AppConstants.Spacing.small) {
            HStack {
                Text(enemy.name)
                    .font(.headline)
                    .foregroundColor(AppConstants.Colors.textPrimary)
                
                Spacer()
                
                Text("Lv. \(enemy.level)")
                    .font(.subheadline)
                    .foregroundColor(AppConstants.Colors.textSecondary)
            }
            
            // Health Bar
            HealthBar(current: enemy.currentHealth, max: enemy.maxHealth, color: AppConstants.Colors.accent)
        }
        .padding(AppConstants.Spacing.medium)
        .background(
            RoundedRectangle(cornerRadius: AppConstants.CornerRadius.medium)
                .fill(Color.black.opacity(0.3))
        )
    }
}

/// Health bar component
struct HealthBar: View {
    let current: Int
    let max: Int
    let color: Color
    
    private var percentage: CGFloat {
        guard max > 0 else { return 0 }
        return CGFloat(current) / CGFloat(max)
    }
    
    var body: some View {
        GeometryReader { geometry in
            ZStack(alignment: .leading) {
                // Background
                RoundedRectangle(cornerRadius: 4)
                    .fill(Color.black.opacity(0.3))
                
                // Health fill
                RoundedRectangle(cornerRadius: 4)
                    .fill(color)
                    .frame(width: geometry.size.width * percentage)
                
                // Text overlay
                HStack {
                    Text("\(current)/\(max)")
                        .font(.caption)
                        .foregroundColor(.white)
                        .bold()
                    Spacer()
                }
                .padding(.horizontal, 4)
            }
        }
        .frame(height: 24)
    }
}

/// Stat badge component
struct StatBadge: View {
    let icon: String
    let value: Int
    
    var body: some View {
        HStack(spacing: 4) {
            Image(systemName: icon)
                .font(.caption)
            Text("\(value)")
                .font(.caption)
                .bold()
        }
        .foregroundColor(AppConstants.Colors.textPrimary)
        .padding(.horizontal, 8)
        .padding(.vertical, 4)
        .background(
            Capsule()
                .fill(Color.white.opacity(0.2))
        )
    }
}

/// Battle controls view
struct BattleControlsView: View {
    let battleState: BattleState
    let isBattleActive: Bool
    let onStartBattle: () -> Void
    let onPauseBattle: () -> Void
    let onResumeBattle: () -> Void
    
    var body: some View {
        HStack(spacing: AppConstants.Spacing.medium) {
            switch battleState {
            case .idle:
            Button(action: onStartBattle) {
                HStack {
                    Image(systemName: "play.fill")
                    Text("Start Battle")
                }
                .frame(maxWidth: .infinity)
                .padding()
                .background(AppConstants.Colors.primary)
                .foregroundColor(.white)
                .cornerRadius(AppConstants.CornerRadius.medium)
            }
            .accessibilityLabel("Start Battle")
            .accessibilityHint("Begins automatic combat with an enemy")
                
            case .fighting, .paused:
                if isBattleActive {
                    Button(action: onPauseBattle) {
                        HStack {
                            Image(systemName: "pause.fill")
                            Text("Pause")
                        }
                        .frame(maxWidth: .infinity)
                        .padding()
                        .background(AppConstants.Colors.accent)
                        .foregroundColor(.white)
                        .cornerRadius(AppConstants.CornerRadius.medium)
                    }
                } else {
                    Button(action: onResumeBattle) {
                        HStack {
                            Image(systemName: "play.fill")
                            Text("Resume")
                        }
                        .frame(maxWidth: .infinity)
                        .padding()
                        .background(AppConstants.Colors.success)
                        .foregroundColor(.white)
                        .cornerRadius(AppConstants.CornerRadius.medium)
                    }
                }
                
            case .victory:
                VStack(spacing: AppConstants.Spacing.small) {
                    Text("Victory!")
                        .font(.title2)
                        .bold()
                        .foregroundColor(AppConstants.Colors.success)
                    
                    Button(action: onStartBattle) {
                        Text("Next Battle")
                            .frame(maxWidth: .infinity)
                            .padding()
                            .background(AppConstants.Colors.primary)
                            .foregroundColor(.white)
                            .cornerRadius(AppConstants.CornerRadius.medium)
                    }
                }
                
            case .defeat:
                VStack(spacing: AppConstants.Spacing.small) {
                    Text("Defeat")
                        .font(.title2)
                        .bold()
                        .foregroundColor(AppConstants.Colors.accent)
                    
                    Button(action: onStartBattle) {
                        Text("Try Again")
                            .frame(maxWidth: .infinity)
                            .padding()
                            .background(AppConstants.Colors.primary)
                            .foregroundColor(.white)
                            .cornerRadius(AppConstants.CornerRadius.medium)
                    }
                }
            }
        }
    }
}

/// SpriteKit battle scene wrapper
struct SpriteKitBattleScene: UIViewRepresentable {
    let player: Player
    let enemy: Enemy?
    let battleState: BattleState
    
    func makeUIView(context: Context) -> SKView {
        let view = SKView()
        view.ignoresSiblingOrder = true
        view.showsFPS = false
        view.showsNodeCount = false
        
        let scene = BattleScene()
        scene.scaleMode = .aspectFill
        scene.player = player
        scene.enemy = enemy
        scene.battleState = battleState
        
        view.presentScene(scene)
        return view
    }
    
    func updateUIView(_ uiView: SKView, context: Context) {
        if let scene = uiView.scene as? BattleScene {
            scene.player = player
            scene.enemy = enemy
            scene.battleState = battleState
        }
    }
}

#if os(OSX)
extension SpriteKitBattleScene: NSViewRepresentable {
    func makeNSView(context: Context) -> SKView {
        let view = SKView()
        view.ignoresSiblingOrder = true
        view.showsFPS = false
        view.showsNodeCount = false
        
        let scene = BattleScene()
        scene.scaleMode = .aspectFill
        scene.player = player
        scene.enemy = enemy
        scene.battleState = battleState
        
        view.presentScene(scene)
        return view
    }
    
    func updateNSView(_ nsView: SKView, context: Context) {
        if let scene = nsView.scene as? BattleScene {
            scene.player = player
            scene.enemy = enemy
            scene.battleState = battleState
        }
    }
}
#endif

