//
//  Player.swift
//  IDL RPG Shared
//
//  Created by MyKey on 11/17/25.
//

import Foundation

/// Represents the player character with stats, level, equipment, and currency
struct Player: Codable, Identifiable {
    let id: UUID
    var name: String
    var level: Int
    var experience: Int
    var experienceToNextLevel: Int
    
    // Core Stats
    var baseHealth: Int
    var baseAttack: Int
    var baseDefense: Int
    var baseSpeed: Int
    
    // Current Stats (base + equipment bonuses)
    var currentHealth: Int
    var maxHealth: Int
    var attack: Int
    var defense: Int
    var speed: Int
    
    // Currency
    var gold: Int
    
    // Equipment
    var equippedWeapon: Equipment?
    var equippedArmor: Equipment?
    
    // Timestamps
    var lastSaveTime: Date
    var totalPlayTime: TimeInterval
    
    init(
        id: UUID = UUID(),
        name: String = "Hero",
        level: Int = 1,
        experience: Int = 0,
        baseHealth: Int = 100,
        baseAttack: Int = 10,
        baseDefense: Int = 5,
        baseSpeed: Int = 10,
        gold: Int = 0
    ) {
        self.id = id
        self.name = name
        self.level = level
        self.experience = experience
        self.baseHealth = baseHealth
        self.baseAttack = baseAttack
        self.baseDefense = baseDefense
        self.baseSpeed = baseSpeed
        self.gold = gold
        
        // Calculate derived stats
        self.experienceToNextLevel = ProgressionSystem.experienceForLevel(level + 1)
        self.currentHealth = baseHealth
        self.maxHealth = baseHealth
        self.attack = baseAttack
        self.defense = baseDefense
        self.speed = baseSpeed
        
        self.equippedWeapon = nil
        self.equippedArmor = nil
        self.lastSaveTime = Date()
        self.totalPlayTime = 0
    }
    
    /// Recalculates stats based on level and equipment
    mutating func recalculateStats() {
        // Base stats scale with level
        let levelMultiplier = 1.0 + (Double(level - 1) * 0.1)
        
        let calculatedBaseHealth = Int(Double(baseHealth) * levelMultiplier)
        let calculatedBaseAttack = Int(Double(baseAttack) * levelMultiplier)
        let calculatedBaseDefense = Int(Double(baseDefense) * levelMultiplier)
        let calculatedBaseSpeed = Int(Double(baseSpeed) * levelMultiplier)
        
        // Add equipment bonuses
        var weaponBonus = 0
        var armorBonus = 0
        var healthBonus = 0
        
        if let weapon = equippedWeapon {
            weaponBonus += weapon.attackBonus
            healthBonus += weapon.healthBonus
        }
        
        if let armor = equippedArmor {
            armorBonus += armor.defenseBonus
            healthBonus += armor.healthBonus
        }
        
        // Set final stats
        self.maxHealth = calculatedBaseHealth + healthBonus
        self.attack = calculatedBaseAttack + weaponBonus
        self.defense = calculatedBaseDefense + armorBonus
        self.speed = calculatedBaseSpeed
        
        // Ensure current health doesn't exceed max
        if currentHealth > maxHealth {
            currentHealth = maxHealth
        }
    }
    
    /// Adds experience and handles level ups
    mutating func addExperience(_ amount: Int) -> Bool {
        var leveledUp = false
        
        experience += amount
        
        while experience >= experienceToNextLevel {
            experience -= experienceToNextLevel
            level += 1
            experienceToNextLevel = ProgressionSystem.experienceForLevel(level + 1)
            leveledUp = true
            
            // Increase base stats on level up
            baseHealth += 10
            baseAttack += 2
            baseDefense += 1
            baseSpeed += 1
        }
        
        if leveledUp {
            recalculateStats()
            // Restore health on level up
            currentHealth = maxHealth
        }
        
        return leveledUp
    }
    
    /// Equips an item
    mutating func equip(_ item: Equipment) {
        switch item.type {
        case .weapon:
            equippedWeapon = item
        case .armor:
            equippedArmor = item
        }
        recalculateStats()
    }
    
    /// Unequips an item
    mutating func unequip(_ item: Equipment) {
        switch item.type {
        case .weapon:
            equippedWeapon = nil
        case .armor:
            equippedArmor = nil
        }
        recalculateStats()
    }
}

