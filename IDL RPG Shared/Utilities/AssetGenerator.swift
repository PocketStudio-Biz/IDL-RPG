//
//  AssetGenerator.swift
//  IDL RPG Shared
//
//  Created by AI Assistant.
//

import SpriteKit

/// Generates procedural textures for game assets so we don't need external image files.
class AssetGenerator {
    
    static let shared = AssetGenerator()
    
    private init() {}
    
    /// Generates a hero/player texture
    func playerTexture(size: CGSize = CGSize(width: 64, height: 64)) -> SKTexture {
        let shape = SKShapeNode()
        let path = CGMutablePath()
        
        // Draw a simple helmet/knight shape
        let w = size.width
        let h = size.height
        
        // Head/Helmet
        path.addArc(center: CGPoint(x: 0, y: h * 0.2), radius: w * 0.25, startAngle: 0, endAngle: CGFloat.pi * 2, clockwise: true)
        
        // Body/Armor
        path.move(to: CGPoint(x: -w * 0.2, y: 0))
        path.addLine(to: CGPoint(x: -w * 0.25, y: -h * 0.3)) // Left shoulder
        path.addLine(to: CGPoint(x: w * 0.25, y: -h * 0.3))  // Right shoulder
        path.addLine(to: CGPoint(x: w * 0.2, y: 0))          // Neck right
        path.closeSubpath()
        
        shape.path = path
        shape.fillColor = SKColor(red: 0.2, green: 0.6, blue: 1.0, alpha: 1.0) // Blueish armor
        shape.strokeColor = .white
        shape.lineWidth = 2
        
        return view.texture(from: shape) ?? SKTexture()
    }
    
    /// Generates an enemy/monster texture
    func enemyTexture(size: CGSize = CGSize(width: 64, height: 64)) -> SKTexture {
        let shape = SKShapeNode()
        let path = CGMutablePath()
        
        // Draw a spiky blob/monster
        let w = size.width
        let h = size.height
        
        path.move(to: CGPoint(x: 0, y: h * 0.3))
        path.addLine(to: CGPoint(x: w * 0.3, y: h * 0.1))
        path.addLine(to: CGPoint(x: w * 0.4, y: -h * 0.1))
        path.addLine(to: CGPoint(x: 0, y: -h * 0.4))
        path.addLine(to: CGPoint(x: -w * 0.4, y: -h * 0.1))
        path.addLine(to: CGPoint(x: -w * 0.3, y: h * 0.1))
        path.closeSubpath()
        
        shape.path = path
        shape.fillColor = SKColor(red: 1.0, green: 0.2, blue: 0.2, alpha: 1.0) // Red monster
        shape.strokeColor = SKColor(red: 0.5, green: 0.0, blue: 0.0, alpha: 1.0)
        shape.lineWidth = 2
        
        return view.texture(from: shape) ?? SKTexture()
    }
    
    /// Generates a background texture
    func backgroundTexture(size: CGSize) -> SKTexture {
        // Gradient background
        let texture = SKTexture(size: size)
        // Since we can't easily do complex gradients into a texture without a View context in this helper easily,
        // we'll return a texture meant to be tiled or just let the scene handle the gradient node.
        // For now, let's return a noise pattern or similar if possible, but Gradient is better handled by SKShapeNode/SKSpriteNode with shader.
        // We'll leave this simple.
        return texture
    }
    
    // Helper view for rendering nodes to textures
    private let view = SKView()
}

// Extension to make it easier to use
extension SKTexture {
    static var player: SKTexture {
        return AssetGenerator.shared.playerTexture()
    }
    
    static var enemy: SKTexture {
        return AssetGenerator.shared.enemyTexture()
    }
}

