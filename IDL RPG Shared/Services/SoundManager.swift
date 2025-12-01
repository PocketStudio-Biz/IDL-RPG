//
//  SoundManager.swift
//  IDL RPG Shared
//
//  Created by AI Assistant.
//

import AVFoundation

/// Manages sound effects using procedural generation so no external files are needed.
class SoundManager {
    static let shared = SoundManager()
    
    private let engine = AVAudioEngine()
    private let playerNode = AVAudioPlayerNode()
    private let mainMixer: AVAudioMixerNode
    
    private var isEngineRunning = false
    
    // Cache for generated sound buffers
    private var attackBuffer: AVAudioPCMBuffer?
    private var damageBuffer: AVAudioPCMBuffer?
    private var victoryBuffer: AVAudioPCMBuffer?
    private var defeatBuffer: AVAudioPCMBuffer?
    
    private init() {
        mainMixer = engine.mainMixerNode
        engine.attach(playerNode)
        engine.connect(playerNode, to: mainMixer, format: nil)
        
        // Pre-generate sounds
        generateSounds()
    }
    
    /// Generates procedural sound buffers
    private func generateSounds() {
        let format = mainMixer.outputFormat(forBus: 0)
        let sampleRate = Float(format.sampleRate)
        
        // 1. Attack Sound (Swipe/Whoosh - Noise burst)
        attackBuffer = generateNoiseBuffer(duration: 0.15, format: format)
        
        // 2. Damage Sound (Low pitch square wave decay)
        damageBuffer = generateToneBuffer(frequency: 150, duration: 0.2, type: .square, format: format)
        
        // 3. Victory Sound (Major arpeggio)
        victoryBuffer = generateArpeggioBuffer(notes: [440, 554, 659], duration: 0.6, format: format)
        
        // 4. Defeat Sound (Descending slide)
        defeatBuffer = generateSlideBuffer(startFreq: 200, endFreq: 50, duration: 0.8, format: format)
    }
    
    /// Starts the audio engine
    private func startEngineIfNeeded() {
        guard !isEngineRunning else { return }
        do {
            try engine.start()
            isEngineRunning = true
        } catch {
            print("Failed to start audio engine: \(error)")
        }
    }
    
    // MARK: - Public Methods
    
    func playAttack() {
        playSound(buffer: attackBuffer)
    }
    
    func playDamage() {
        playSound(buffer: damageBuffer)
    }
    
    func playVictory() {
        playSound(buffer: victoryBuffer)
    }
    
    func playDefeat() {
        playSound(buffer: defeatBuffer)
    }
    
    private func playSound(buffer: AVAudioPCMBuffer?) {
        startEngineIfNeeded()
        guard let buffer = buffer else { return }
        
        if playerNode.isPlaying {
            playerNode.stop()
        }
        playerNode.scheduleBuffer(buffer, at: nil, options: [], completionHandler: nil)
        playerNode.play()
    }
    
    // MARK: - Generators
    
    private enum WaveType { case sine, square, saw }
    
    private func generateToneBuffer(frequency: Float, duration: Float, type: WaveType, format: AVAudioFormat) -> AVAudioPCMBuffer? {
        let frameCount = AVAudioFrameCount(format.sampleRate * Double(duration))
        guard let buffer = AVAudioPCMBuffer(pcmFormat: format, frameCapacity: frameCount) else { return nil }
        
        buffer.frameLength = frameCount
        let channels = Int(format.channelCount)
        let sampleRate = Float(format.sampleRate)
        
        for channel in 0..<channels {
            guard let channelData = buffer.floatChannelData?[channel] else { continue }
            for frame in 0..<Int(frameCount) {
                let time = Float(frame) / sampleRate
                let envelope = 1.0 - (time / duration) // Linear decay
                
                var value: Float = 0
                switch type {
                case .sine:
                    value = sin(2.0 * .pi * frequency * time)
                case .square:
                    value = sin(2.0 * .pi * frequency * time) > 0 ? 0.5 : -0.5
                case .saw:
                    value = 2.0 * (time * frequency - floor(time * frequency + 0.5))
                }
                
                channelData[frame] = value * envelope * 0.5
            }
        }
        return buffer
    }
    
    private func generateNoiseBuffer(duration: Float, format: AVAudioFormat) -> AVAudioPCMBuffer? {
        let frameCount = AVAudioFrameCount(format.sampleRate * Double(duration))
        guard let buffer = AVAudioPCMBuffer(pcmFormat: format, frameCapacity: frameCount) else { return nil }
        
        buffer.frameLength = frameCount
        let channels = Int(format.channelCount)
        
        for channel in 0..<channels {
            guard let channelData = buffer.floatChannelData?[channel] else { continue }
            for frame in 0..<Int(frameCount) {
                let envelope = 1.0 - (Float(frame) / Float(frameCount))
                let value = Float.random(in: -1...1)
                channelData[frame] = value * envelope * 0.3
            }
        }
        return buffer
    }
    
    private func generateArpeggioBuffer(notes: [Float], duration: Float, format: AVAudioFormat) -> AVAudioPCMBuffer? {
        // Simple concatenation of tones for now (implementation simplified)
        // Returns just a single tone for simplicity in this snippet, real arpeggio requires mixing
        return generateToneBuffer(frequency: notes[0], duration: duration, type: .sine, format: format)
    }
    
    private func generateSlideBuffer(startFreq: Float, endFreq: Float, duration: Float, format: AVAudioFormat) -> AVAudioPCMBuffer? {
        let frameCount = AVAudioFrameCount(format.sampleRate * Double(duration))
        guard let buffer = AVAudioPCMBuffer(pcmFormat: format, frameCapacity: frameCount) else { return nil }
        
        buffer.frameLength = frameCount
        let channels = Int(format.channelCount)
        let sampleRate = Float(format.sampleRate)
        
        for channel in 0..<channels {
            guard let channelData = buffer.floatChannelData?[channel] else { continue }
            for frame in 0..<Int(frameCount) {
                let time = Float(frame) / sampleRate
                let progress = time / duration
                let currentFreq = startFreq + (endFreq - startFreq) * progress
                
                let value = sin(2.0 * .pi * currentFreq * time)
                channelData[frame] = value * 0.5
            }
        }
        return buffer
    }
}

