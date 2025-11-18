//
//  InventoryView.swift
//  IDL RPG Shared
//
//  Created by MyKey on 11/17/25.
//

import SwiftUI

/// Inventory management view
struct InventoryView: View {
    @ObservedObject var viewModel: CharacterViewModel
    
    var body: some View {
        ScrollView {
            VStack(spacing: AppConstants.Spacing.medium) {
                // Gold Display
                GoldDisplay(gold: viewModel.player.gold)
                
                // Inventory Items
                if viewModel.inventory.isEmpty {
                    EmptyInventoryView()
                } else {
                    LazyVGrid(columns: [GridItem(.flexible()), GridItem(.flexible())], spacing: AppConstants.Spacing.medium) {
                        ForEach(viewModel.inventory) { item in
                            InventoryItemCard(item: item) {
                                viewModel.equipItem(item)
                            }
                        }
                    }
                }
            }
            .padding(AppConstants.Spacing.medium)
        }
        .background(AppConstants.Colors.background)
    }
}

struct GoldDisplay: View {
    let gold: Int
    
    var body: some View {
        HStack {
            Image(systemName: "dollarsign.circle.fill")
                .font(.title2)
                .foregroundColor(AppConstants.Colors.success)
            
            Text("\(gold)")
                .font(.title)
                .bold()
                .foregroundColor(AppConstants.Colors.textPrimary)
            
            Text("Gold")
                .font(.subheadline)
                .foregroundColor(AppConstants.Colors.textSecondary)
        }
        .frame(maxWidth: .infinity)
        .padding()
        .background(
            RoundedRectangle(cornerRadius: AppConstants.CornerRadius.medium)
                .fill(Color.black.opacity(0.3))
        )
    }
}

struct EmptyInventoryView: View {
    var body: some View {
        VStack(spacing: AppConstants.Spacing.medium) {
            Image(systemName: "bag")
                .font(.system(size: 60))
                .foregroundColor(AppConstants.Colors.textSecondary)
            
            Text("Inventory Empty")
                .font(.headline)
                .foregroundColor(AppConstants.Colors.textSecondary)
            
            Text("Defeat enemies to collect equipment!")
                .font(.caption)
                .foregroundColor(AppConstants.Colors.textSecondary)
                .multilineTextAlignment(.center)
        }
        .frame(maxWidth: .infinity)
        .padding(AppConstants.Spacing.xLarge)
    }
}

struct InventoryItemCard: View {
    let item: Equipment
    let onEquip: () -> Void
    
    var body: some View {
        VStack(alignment: .leading, spacing: AppConstants.Spacing.small) {
            // Item Name
            Text(item.name)
                .font(.headline)
                .foregroundColor(Color(hex: item.rarity.colorHex))
                .lineLimit(2)
            
            // Item Type
            Text(item.type.displayName)
                .font(.caption)
                .foregroundColor(AppConstants.Colors.textSecondary)
            
            // Stat Bonuses
            VStack(alignment: .leading, spacing: 4) {
                if item.attackBonus > 0 {
                    StatRow(icon: "sword", value: "+\(item.attackBonus)")
                }
                if item.defenseBonus > 0 {
                    StatRow(icon: "shield", value: "+\(item.defenseBonus)")
                }
                if item.healthBonus > 0 {
                    StatRow(icon: "heart", value: "+\(item.healthBonus)")
                }
            }
            
            Spacer()
            
            // Equip Button
            Button(action: onEquip) {
                Text("Equip")
                    .font(.caption)
                    .bold()
                    .frame(maxWidth: .infinity)
                    .padding(.vertical, 8)
                    .background(AppConstants.Colors.primary)
                    .foregroundColor(.white)
                    .cornerRadius(AppConstants.CornerRadius.small)
            }
            .accessibilityLabel("Equip \(item.name)")
            .accessibilityHint("Equips this \(item.type.displayName) to your character")
        }
        .padding()
        .frame(maxWidth: .infinity)
        .background(
            RoundedRectangle(cornerRadius: AppConstants.CornerRadius.medium)
                .fill(Color.black.opacity(0.3))
                .overlay(
                    RoundedRectangle(cornerRadius: AppConstants.CornerRadius.medium)
                        .stroke(Color(hex: item.rarity.colorHex), lineWidth: 2)
                )
        )
    }
}

struct StatRow: View {
    let icon: String
    let value: String
    
    var body: some View {
        HStack(spacing: 4) {
            Image(systemName: icon)
                .font(.caption2)
            Text(value)
                .font(.caption2)
        }
        .foregroundColor(AppConstants.Colors.textSecondary)
    }
}

