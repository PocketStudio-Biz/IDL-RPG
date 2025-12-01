//
//  GameViewController.swift
//  IDL RPG macOS
//
//  Created by MyKey on 11/17/25.
//

import Cocoa
import SwiftUI
import SpriteKit
import GameplayKit

class GameViewController: NSViewController {

    override func viewDidLoad() {
        super.viewDidLoad()
        
        // Initialize the main game view with SwiftUI
        let mainGameView = MainGameView()
        let hostingController = NSHostingController(rootView: mainGameView)
        
        // Add hosting controller as child
        addChild(hostingController)
        hostingController.view.translatesAutoresizingMaskIntoConstraints = false
        view.addSubview(hostingController.view)
        
        // Set constraints to fill the window
        NSLayoutConstraint.activate([
            hostingController.view.topAnchor.constraint(equalTo: view.topAnchor),
            hostingController.view.bottomAnchor.constraint(equalTo: view.bottomAnchor),
            hostingController.view.leadingAnchor.constraint(equalTo: view.leadingAnchor),
            hostingController.view.trailingAnchor.constraint(equalTo: view.trailingAnchor)
        ])
    }
}
