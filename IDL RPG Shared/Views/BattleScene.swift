//
//  BattleScene.swift
//  IDL RPG Shared
//
//  Created by MyKey on 11/17/25.
//

import SpriteKit

/// SpriteKit scene for battle visualization
class BattleScene: SKScene {
    var player: Player?
    var enemy: Enemy?
    var battleState: BattleState = .idle
    
    private var playerNode: SKSpriteNode?
    private var enemyNode: SKSpriteNode?
    private var backgroundNode: SKSpriteNode?
    
    override func didMove(to view: SKView) {
        setupScene()
    }
    
    func setupScene() {
        // Set background color
        backgroundColor = SKColor(red: 0.1, green: 0.1, blue: 0.18, alpha: 1.0)
        
        // Create background
        createBackground()
        
        // Create player and enemy sprites
        updateSprites()
    }
    
    func createBackground() {
        // Simple gradient background
        let background = SKSpriteNode(color: SKColor(red: 0.1, green: 0.1, blue: 0.18, alpha: 1.0), size: size)
        background.position = CGPoint(x: size.width / 2, y: size.height / 2)
        background.zPosition = -1
        addChild(background)
        backgroundNode = background
    }
    
    func updateSprites() {
        // Remove existing sprites
        playerNode?.removeFromParent()
        enemyNode?.removeFromParent()
        
        guard let player = player else { return }
        
        // Create player sprite (placeholder - use actual sprite if available)
        let playerSprite = SKSpriteNode(color: SKColor.blue, size: CGSize(width: 60, height: 60))
        playerSprite.position = CGPoint(x: size.width * 0.25, y: size.height / 2)
        playerSprite.zPosition = 1
        addChild(playerSprite)
        playerNode = playerSprite
        
        // Add player label
        let playerLabel = SKLabelNode(text: player.name)
        playerLabel.fontSize = 16
        playerLabel.fontColor = SKColor.white
        playerLabel.position = CGPoint(x: 0, y: -40)
        playerSprite.addChild(playerLabel)
        
        if let enemy = enemy {
            // Create enemy sprite
            let enemySprite = SKSpriteNode(color: SKColor.red, size: CGSize(width: 60, height: 60))
            enemySprite.position = CGPoint(x: size.width * 0.75, y: size.height / 2)
            enemySprite.zPosition = 1
            addChild(enemySprite)
            enemyNode = enemySprite
            
            // Add enemy label
            let enemyLabel = SKLabelNode(text: enemy.name)
            enemyLabel.fontSize = 16
            enemyLabel.fontColor = SKColor.white
            enemyLabel.position = CGPoint(x: 0, y: -40)
            enemySprite.addChild(enemyLabel)
        }
        
        // Add battle state indicator
        updateBattleState()
    }
    
    func updateBattleState() {
        // Remove existing state label
        childNode(withName: "battleState")?.removeFromParent()
        
        let stateLabel = SKLabelNode(text: battleStateText)
        stateLabel.name = "battleState"
        stateLabel.fontSize = 24
        stateLabel.fontColor = SKColor.white
        stateLabel.position = CGPoint(x: size.width / 2, y: size.height * 0.8)
        stateLabel.zPosition = 10
        addChild(stateLabel)
    }
    
    private var battleStateText: String {
        switch battleState {
        case .idle:
            return "Ready to Battle"
        case .fighting:
            return "Fighting!"
        case .victory:
            return "Victory!"
        case .defeat:
            return "Defeat"
        case .paused:
            return "Paused"
        }
    }
    
    override func update(_ currentTime: TimeInterval) {
        // Update sprites if needed
        if playerNode == nil || enemyNode == nil {
            updateSprites()
        }
    }
    
    /// Animates player attack
    func animatePlayerAttack(completion: @escaping () -> Void) {
        guard let playerNode = playerNode else {
            completion()
            return
        }
        
        let originalPosition = playerNode.position
        let attackPosition = CGPoint(x: originalPosition.x + 30, y: originalPosition.y)
        
        let moveForward = SKAction.move(to: attackPosition, duration: 0.1)
        let moveBack = SKAction.move(to: originalPosition, duration: 0.1)
        let sequence = SKAction.sequence([moveForward, moveBack])
        
        playerNode.run(sequence) {
            completion()
        }
    }
    
    /// Animates enemy attack
    func animateEnemyAttack(completion: @escaping () -> Void) {
        guard let enemyNode = enemyNode else {
            completion()
            return
        }
        
        let originalPosition = enemyNode.position
        let attackPosition = CGPoint(x: originalPosition.x - 30, y: originalPosition.y)
        
        let moveForward = SKAction.move(to: attackPosition, duration: 0.1)
        let moveBack = SKAction.move(to: originalPosition, duration: 0.1)
        let sequence = SKAction.sequence([moveForward, moveBack])
        
        enemyNode.run(sequence) {
            completion()
        }
    }
    
    /// Shows damage number
    func showDamage(_ amount: Int, at position: CGPoint, isPlayer: Bool) {
        let damageLabel = SKLabelNode(text: "-\(amount)")
        damageLabel.fontSize = 20
        damageLabel.fontColor = isPlayer ? SKColor.red : SKColor.orange
        damageLabel.position = position
        damageLabel.zPosition = 5
        
        addChild(damageLabel)
        
        let moveUp = SKAction.moveBy(x: 0, y: 50, duration: 0.5)
        let fadeOut = SKAction.fadeOut(withDuration: 0.5)
        let remove = SKAction.removeFromParent()
        let sequence = SKAction.sequence([SKAction.group([moveUp, fadeOut]), remove])
        
        damageLabel.run(sequence)
    }
}

