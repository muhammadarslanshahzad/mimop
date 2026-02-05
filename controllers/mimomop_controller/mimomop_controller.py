#!/usr/bin/env python3
"""
MiMoMop Main Controller
Entry point for the robot controller in Webots
"""

import sys
import os

# Add controller path to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.robot_interface import MiMoMopRobot
from brain.mimomop_brain import MiMoMopBrain
from personality.personality_system import PersonalitySystem


def main():
    """Main control loop"""
    print("🤖 MiMoMop booting up...")
    
    # Initialize robot interface
    robot = MiMoMopRobot()
    
    # Initialize brain (LLM + planning)
    brain = MiMoMopBrain()
    
    # Initialize personality system
    personality = PersonalitySystem(initial_mode="sarcastic")
    
    # Say hello
    greeting = personality.generate_greeting()
    print(f"💬 MiMoMop: {greeting}")
    
    # Main control loop
    timestep = int(robot.getBasicTimeStep())
    
    while robot.step(timestep) != -1:
        # Get sensor data
        sensor_data = robot.get_sensor_data()
        
        # Brain processes sensor data and decides action
        action = brain.decide_action(sensor_data)
        
        # Execute action
        robot.execute_action(action)
        
        # Personality commentary (occasional)
        if robot.get_time() % 10 < timestep / 1000.0:  # Every 10 seconds
            comment = personality.generate_comment(sensor_data, action)
            if comment:
                print(f"💬 MiMoMop: {comment}")
    
    print("🤖 MiMoMop shutting down...")


if __name__ == "__main__":
    main()