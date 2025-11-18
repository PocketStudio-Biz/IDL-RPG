//
//  OfflineRewardsView.swift
//  IDL RPG Shared
//
//  Created by MyKey on 11/17/25.
//

import SwiftUI

/// View for displaying and claiming offline rewards
struct OfflineRewardsView: View {
    let rewards: OfflineRewards
    let onClaim: () -> Void
    
    var body: some View {
        VStack(spacing: AppConstants.Spacing.large) {
            // Header
            VStack(spacing: AppConstants.Spacing.small) {
                Image(systemName: "clock.fill")
                    .font(.system(size: 50))
                    .foregroundColor(AppConstants.Colors.primary)
                
                Text("Welcome Back!")
                    .font(.title)
                    .bold()
                    .foregroundColor(AppConstants.Colors.textPrimary)
                
                Text("You were away for \(rewards.formattedTimeAway)")
                    .font(.subheadline)
                    .foregroundColor(AppConstants.Colors.textSecondary)
            }
            
            // Rewards Summary
            VStack(spacing: AppConstants.Spacing.medium) {
                RewardRow(
                    icon: "figure.walk",
                    title: "Enemies Defeated",
                    value: "\(rewards.enemiesDefeated)"
                )
                
                RewardRow(
                    icon: "star.fill",
                    title: "Experience Gained",
                    value: "\(rewards.experienceGained)"
                )
                
                RewardRow(
                    icon: "dollarsign.circle.fill",
                    title: "Gold Earned",
                    value: "\(rewards.goldGained)"
                )
                
                if !rewards.lootObtained.isEmpty {
                    RewardRow(
                        icon: "bag.fill",
                        title: "Items Found",
                        value: "\(rewards.lootObtained.count)"
                    )
                }
            }
            .padding()
            .background(
                RoundedRectangle(cornerRadius: AppConstants.CornerRadius.large)
                    .fill(Color.black.opacity(0.3))
            )
            
            // Claim Button
            Button(action: onClaim) {
                Text("Claim Rewards")
                    .font(.headline)
                    .foregroundColor(.white)
                    .frame(maxWidth: .infinity)
                    .padding()
                    .background(AppConstants.Colors.primary)
                    .cornerRadius(AppConstants.CornerRadius.medium)
            }
        }
        .padding(AppConstants.Spacing.large)
        .background(AppConstants.Colors.background)
    }
}

struct RewardRow: View {
    let icon: String
    let title: String
    let value: String
    
    var body: some View {
        HStack {
            Image(systemName: icon)
                .font(.title3)
                .foregroundColor(AppConstants.Colors.primary)
                .frame(width: 30)
            
            Text(title)
                .foregroundColor(AppConstants.Colors.textSecondary)
            
            Spacer()
            
            Text(value)
                .font(.headline)
                .foregroundColor(AppConstants.Colors.textPrimary)
        }
    }
}

