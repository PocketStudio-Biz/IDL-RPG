//
//  GameViewController.swift
//  IDL RPG iOS
//
//  Created by MyKey on 11/17/25.
//

import UIKit
import SwiftUI

class GameViewController: UIHostingController<MainGameView> {

    override func viewDidLoad() {
        super.viewDidLoad()
        
        // Set root view to MainGameView
        rootView = MainGameView()
    }

    override var supportedInterfaceOrientations: UIInterfaceOrientationMask {
        if UIDevice.current.userInterfaceIdiom == .phone {
            return .allButUpsideDown
        } else {
            return .all
        }
    }

    override var prefersStatusBarHidden: Bool {
        return false
    }
}
