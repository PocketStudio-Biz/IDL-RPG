//
//  CharacterView.swift
//  IDL RPG Shared
//
//  Created by MyKey on 11/17/25.
//

import SwiftUI

/// Character stats and progression view
struct CharacterView: View {
    @ObservedObject var viewModel: CharacterViewModel
    
    var body: some View {
        ScrollView {
            VStack(spacing: AppConstants.Spacing.large) {
                // Character Header
                CharacterHeader(player: viewModel.player)
                
                // Stats Section
                StatsSection(player: viewModel.player)
                
                // Equipment Section
                EquipmentSection(player: viewModel.player)
                
                // Progression Section
                ProgressionSection(player: viewModel.player)
            }
            .padding(AppConstants.Spacing.medium)
        }
        .background(AppConstants.Colors.background)
    }
}

struct CharacterHeader: View {
    let player: Player
    
    var body: some View {
        VStack(spacing: AppConstants.Spacing.medium) {
            // Character Avatar/Icon
            Circle()
                .fill(AppConstants.Colors.primary.opacity(0.3))
                .frame(width: 100, height: 100)
                .overlay(
                    Image(systemName: "person.fill")
                        .font(.system(size: 50))
                        .foregroundColor(AppConstants.Colors.primary)
                )
            
            Text(player.name)
                .font(.title)
                .bold()
                .foregroundColor(AppConstants.Colors.textPrimary)
                .accessibilityLabel("Character name: \(player.name)")
            
            Text("Level \(player.level)")
                .font(.title2)
                .foregroundColor(AppConstants.Colors.textSecondary)
                .accessibilityLabel("Level \(player.level)")
        }
        .padding()
        .frame(maxWidth: .infinity)
        .background(
            RoundedRectangle(cornerRadius: AppConstants.CornerRadius.large)
                .fill(Color.black.opacity(0.3))
        )
    }
}

struct StatsSection: View {
    let player: Player
    
    var body: some View {
        VStack(alignment: .leading, spacing: AppConstants.Spacing.medium) {
            Text("Stats")
                .font(.headline)
                .foregroundColor(AppConstants.Colors.textPrimary)
            
            LazyVGrid(columns: [GridItem(.flexible()), GridItem(.flexible())], spacing: AppConstants.Spacing.medium) {
                StatCard(title: "Health", value: "\(player.currentHealth)/\(player.maxHealth)", icon: "heart.fill", color: AppConstants.Colors.accent)
                StatCard(title: "Attack", value: "\(player.attack)", icon: "sword", color: AppConstants.Colors.primary)
                StatCard(title: "Defense", value: "\(player.defense)", icon: "shield", color: AppConstants.Colors.secondary)
                StatCard(title: "Speed", value: "\(player.speed)", icon: "bolt", color: AppConstants.Colors.success)
            }
        }
    }
}

struct StatCard: View {
    let title: String
    let value: String
    let icon: String
    let color: Color
    
    var body: some View {
        VStack(spacing: AppConstants.Spacing.small) {
            Image(systemName: icon)
                .font(.title2)
                .foregroundColor(color)
            
            Text(title)
                .font(.caption)
                .foregroundColor(AppConstants.Colors.textSecondary)
            
            Text(value)
                .font(.headline)
                .bold()
                .foregroundColor(AppConstants.Colors.textPrimary)
        }
        .frame(maxWidth: .infinity)
        .padding()
        .background(
            RoundedRectangle(cornerRadius: AppConstants.CornerRadius.medium)
                .fill(Color.black.opacity(0.3))
        )
    }
}

struct EquipmentSection: View {
    let player: Player
    
    var body: some View {
        VStack(alignment: .leading, spacing: AppConstants.Spacing.medium) {
            Text("Equipment")
                .font(.headline)
                .foregroundColor(AppConstants.Colors.textPrimary)
            
            VStack(spacing: AppConstants.Spacing.small) {
                EquipmentRow(title: "Weapon", equipment: player.equippedWeapon)
                EquipmentRow(title: "Armor", equipment: player.equippedArmor)
            }
        }
    }
}

struct EquipmentRow: View {
    let title: String
    let equipment: Equipment?
    
    var body: some View {
        HStack {
            Text(title)
                .foregroundColor(AppConstants.Colors.textSecondary)
            
            Spacer()
            
            if let equipment = equipment {
                Text(equipment.name)
                    .foregroundColor(AppConstants.Colors.textPrimary)
                    .bold()
            } else {
                Text("None")
                    .foregroundColor(AppConstants.Colors.textSecondary)
            }
        }
        .padding()
        .background(
            RoundedRectangle(cornerRadius: AppConstants.CornerRadius.medium)
                .fill(Color.black.opacity(0.3))
        )
    }
}

struct ProgressionSection: View {
    let player: Player
    
    private var experienceProgress: Double {
        guard player.experienceToNextLevel > 0 else { return 0 }
        return Double(player.experience) / Double(player.experienceToNextLevel)
    }
    
    var body: some View {
        VStack(alignment: .leading, spacing: AppConstants.Spacing.medium) {
            Text("Progression")
                .font(.headline)
                .foregroundColor(AppConstants.Colors.textPrimary)
            
            VStack(alignment: .leading, spacing: AppConstants.Spacing.small) {
                HStack {
                    Text("Experience")
                        .foregroundColor(AppConstants.Colors.textSecondary)
                    Spacer()
                    Text("\(player.experience) / \(player.experienceToNextLevel)")
                        .foregroundColor(AppConstants.Colors.textPrimary)
                        .bold()
                }
                
                GeometryReader { geometry in
                    ZStack(alignment: .leading) {
                        RoundedRectangle(cornerRadius: 8)
                            .fill(Color.black.opacity(0.3))
                        
                        RoundedRectangle(cornerRadius: 8)
                            .fill(AppConstants.Colors.primary)
                            .frame(width: geometry.size.width * experienceProgress)
                    }
                }
                .frame(height: 20)
            }
            .padding()
            .background(
                RoundedRectangle(cornerRadius: AppConstants.CornerRadius.medium)
                    .fill(Color.black.opacity(0.3))
            )
        }
    }
}

