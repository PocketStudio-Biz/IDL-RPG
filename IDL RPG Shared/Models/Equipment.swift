//
//  Equipment.swift
//  IDL RPG Shared
//
//  Created by MyKey on 11/17/25.
//

import Foundation

/// Represents equipment items (weapons and armor) with stat bonuses
struct Equipment: Codable, Identifiable {
    let id: UUID
    var name: String
    var type: EquipmentType
    var rarity: Rarity
    
    // Stat Bonuses
    var attackBonus: Int
    var defenseBonus: Int
    var healthBonus: Int
    var speedBonus: Int
    
    // Cost
    var goldCost: Int
    
    // Visual
    var spriteName: String
    
    init(
        id: UUID = UUID(),
        name: String,
        type: EquipmentType,
        rarity: Rarity,
        attackBonus: Int = 0,
        defenseBonus: Int = 0,
        healthBonus: Int = 0,
        speedBonus: Int = 0,
        goldCost: Int = 0,
        spriteName: String = "equipment_default"
    ) {
        self.id = id
        self.name = name
        self.type = type
        self.rarity = rarity
        self.attackBonus = attackBonus
        self.defenseBonus = defenseBonus
        self.healthBonus = healthBonus
        self.speedBonus = speedBonus
        self.goldCost = goldCost
        self.spriteName = spriteName
    }
    
    /// Creates random equipment scaled to level
    static func random(for level: Int) -> Equipment {
        let rarityRoll = Double.random(in: 0...1)
        let rarity: Rarity
        
        if rarityRoll < 0.05 {
            rarity = .legendary
        } else if rarityRoll < 0.20 {
            rarity = .epic
        } else if rarityRoll < 0.50 {
            rarity = .rare
        } else {
            rarity = .common
        }
        
        let type: EquipmentType = Bool.random() ? .weapon : .armor
        let levelMultiplier = Double(level) * 0.3
        let rarityMultiplier = rarity.statMultiplier
        
        let baseStat = Int(levelMultiplier * rarityMultiplier)
        
        if type == .weapon {
            return Equipment(
                name: "\(rarity.displayName) \(type.displayName)",
                type: type,
                rarity: rarity,
                attackBonus: baseStat + Int.random(in: 1...5),
                healthBonus: baseStat / 2,
                goldCost: Int(baseStat * 10),
                spriteName: "weapon_\(rarity.rawValue)"
            )
        } else {
            return Equipment(
                name: "\(rarity.displayName) \(type.displayName)",
                type: type,
                rarity: rarity,
                defenseBonus: baseStat + Int.random(in: 1...5),
                healthBonus: baseStat,
                goldCost: Int(baseStat * 10),
                spriteName: "armor_\(rarity.rawValue)"
            )
        }
    }
}

enum EquipmentType: String, Codable {
    case weapon
    case armor
    
    var displayName: String {
        switch self {
        case .weapon:
            return "Sword"
        case .armor:
            return "Armor"
        }
    }
}

enum Rarity: String, Codable, CaseIterable {
    case common
    case rare
    case epic
    case legendary
    
    var displayName: String {
        switch self {
        case .common:
            return "Common"
        case .rare:
            return "Rare"
        case .epic:
            return "Epic"
        case .legendary:
            return "Legendary"
        }
    }
    
    var statMultiplier: Double {
        switch self {
        case .common:
            return 1.0
        case .rare:
            return 1.5
        case .epic:
            return 2.0
        case .legendary:
            return 3.0
        }
    }
    
    var colorHex: String {
        switch self {
        case .common:
            return "#FFFFFF" // White
        case .rare:
            return "#1E90FF" // Blue
        case .epic:
            return "#9370DB" // Purple
        case .legendary:
            return "#FFD700" // Gold
        }
    }
}

