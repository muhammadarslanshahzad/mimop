#!/usr/bin/env python3
"""
Quick test script for MiMoMop personality system
Run this to test if Ollama connection works and personalities generate correctly
"""

import sys
import os

# Add controller to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'controllers', 'mimomop_controller'))

from personality.personality_system import PersonalitySystem


def test_personalities():
    """Test all personality modes"""
    print("🧪 Testing MiMoMop Personality System\n")
    print("=" * 60)
    
    personalities = ['sarcastic', 'cute', 'drill_sergeant', 'proud', 'chill']
    
    for personality in personalities:
        print(f"\n🎭 Testing: {personality.upper()}")
        print("-" * 60)
        
        ps = PersonalitySystem(initial_mode=personality)
        
        # Test greeting
        greeting = ps.generate_greeting()
        print(f"Greeting: {greeting}")
        
        # Test comments
        for i in range(2):
            comment = ps.generate_comment(
                sensor_data={'distance': 0.5},
                action={'type': 'move'}
            )
            if comment:
                print(f"Comment {i+1}: {comment}")
        
        print()
    
    print("=" * 60)
    print("\n✅ All personalities tested!")
    print("\nNext: Try LLM-generated responses (requires Ollama running)")
    print("Run: ollama serve &")


def test_ollama_connection():
    """Test Ollama connection"""
    print("\n🦙 Testing Ollama Connection\n")
    print("=" * 60)
    
    from brain.mimomop_brain import MiMoMopBrain
    
    brain = MiMoMopBrain()
    
    # Test query
    print("\nAsking MiMoMop a question...")
    response = brain.query_llm(
        "You are MiMoMop, a sarcastic cleaning robot. "
        "You just saw a huge pile of dust. React in 10 words or less."
    )
    
    print(f"MiMoMop: {response}")
    print("\n" + "=" * 60)
    
    if "[LLM Error" in response:
        print("\n⚠️  Ollama connection failed!")
        print("Make sure Ollama is running: ollama serve &")
    else:
        print("\n✅ Ollama connection working!")


if __name__ == "__main__":
    print("\n🤖 MiMoMop Component Tests\n")
    
    # Test personalities (template-based, doesn't need Ollama)
    test_personalities()
    
    # Test Ollama (requires Ollama running)
    try:
        test_ollama_connection()
    except Exception as e:
        print(f"\n⚠️  Ollama test skipped: {e}")
        print("Start Ollama with: ollama serve &")
    
    print("\n✨ Testing complete!\n")