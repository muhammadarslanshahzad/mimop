
import sys
from core.robot_interface import MiMoMopRobot
from brain.mimomop_brain import MiMoMopBrain
from brain.memory_manager import MiMoMemory
from personality.personality_system import PersonalitySystem

def main():
    robot = MiMoMopRobot()
    brain = MiMoMopBrain()
    memory = MiMoMemory()

    robot_personality = PersonalitySystem(initial_mode='cute')
    
    print("🚀 MiMoMop Connected!")
    print("🎮 CONTROL: Use ARROW KEYS in the Webots window.")
    
    last_memory_time = -2.0
    last_thought_time = -20.0 # Track the last time the brain spoke

    # while robot.step() != -1:
    #     current_time = robot.get_time()
        
    #     # 1. READ KEYBOARD & MOVE
    #     cmd = robot.get_keyboard_command()
    #     if cmd == 'forward': robot.move_forward()
    #     elif cmd == 'backward': robot.move_backward()
    #     elif cmd == 'left': robot.move_left()
    #     elif cmd == 'right': robot.move_right()
    #     else: robot.stop()

    #     # 2. SENSE THE WORLD
    #     sensor_data = robot.get_sensor_data()

    #     # 3. SAVE TO QDRANT (Every 5 seconds - less frequent logs)
    #     if current_time - last_memory_time >= 5.0:
    #         memory.record_cleaning(
    #             position=sensor_data['position'], 
    #             sensor_data=sensor_data['proximity'],
    #             mood="Dynamic"
    #         )
    #         last_memory_time = current_time
    #         print(f"📍 Location {sensor_data['position']} logged.")

    #     # 4. DYNAMIC LLM COMMENTARY (Every 20 seconds)
    #     # 4. DYNAMIC PERSONALITY TRIGGER
    #     if sensor_data['obstacle_ahead']:
    #         robot_personality.switch_personality('drill_sergeant')
    #         context_str = "A WALL IS BLOCKING ME! MOVE IT!"
    #     elif cmd == 'forward':
    #         robot_personality.switch_personality('cute')
    #         context_str = "Zooming around cleaning everything! ✨"
    #     else:
    #         robot_personality.switch_personality('sarcastic')
    #         context_str = "Just sitting here collecting dust."


    #     if current_time - last_thought_time >= 20.0:
    #         # IMPORTANT: Call the LLM method using the STRING, not the dict
    #         thought = robot_personality.generate_llm_comment(context_str)
    #         print(f"💬 {robot_personality.current_personality.upper()}: {thought}")
    #         last_thought_time = current_time
    last_comment_time = 0
    comment_duration = 2.0  # Seconds to keep the comment visible
    current_comment = ""
    while robot.step() != -1:
        current_time = robot.get_time()
        
        # 1. READ KEYBOARD & MOVE
        cmd = robot.get_keyboard_command()
        action_taken = {}
        if cmd == 'forward': 
            robot.move_forward()
            action_taken = {'type': 'move'}
        elif cmd == 'backward': 
            robot.move_backward()
            action_taken = {'type': 'move'}
        elif cmd in ['left', 'right']: 
            if cmd == 'left': robot.move_left()
            else: robot.move_right()
            action_taken = {'type': 'rotate'}
        else: 
            robot.stop()


        if current_time - last_comment_time >= comment_duration:
            
            if cmd is not None:
                # Generate a new comment only if the previous one is finished
                new_comment = robot_personality.generate_comment(sensor_data, action_taken)
                
                if new_comment:
                    # Update Webots visual label
                    robot.setLabel(0, f"{new_comment}", 0.05, 0.05, 0.08, 0x00FF00, 0.0)
                    print(f"💬 {robot_personality.current_personality.upper()}: {new_comment}")
                    
                    # Reset the timers
                    current_comment = new_comment
                    last_comment_time = current_time
            # else:
            #     # Optional: Clear the label if no key is pressed and 2s passed
            #     robot.setLabel(0, "", 0.05, 0.05, 0.08, 0x00FF00, 0.0)
        # if cmd is not None:
        #     # Use the local template comments for instant speed
        #     new_comment = robot_personality.generate_comment(sensor_data, action_taken)
        #     if new_comment:
        #         current_comment = new_comment
        #         print(f"💬 {robot_personality.current_personality.upper()}: {current_comment}")
        #         robot.setLabel(
        #             0,                          # ID (0-65534)
        #             f"{robot_personality.current_personality.upper()}: {current_comment}", 
        #             0.05, 0.05,                 # X and Y position (0.0 to 1.0)
        #             0.1,                        # Text size
        #             0x00FF00,                   # Color (Hex: Green)
        #             0.0,                        # Transparency (0.0 = solid)
        #             "Arial"                     # Font
        #         )


        # 2. SENSE & DYNAMIC LOGIC
        sensor_data = robot.get_sensor_data()

        # Update personality but let the class handle the "spam" prevention
        if sensor_data['obstacle_ahead']:
            robot_personality.switch_personality('drill_sergeant')
            context_str = "A WALL IS BLOCKING ME! MOVE IT!"
        elif cmd == 'forward':
            robot_personality.switch_personality('cute')
            context_str = "Zooming around cleaning everything! ✨"
        else:
            robot_personality.switch_personality('sarcastic')
            context_str = "Just sitting here collecting dust."

        # 3. SAVE TO QDRANT (Every 5 seconds)
        if current_time - last_memory_time >= 5.0:
            memory.record_cleaning(
                position=sensor_data['position'], 
                sensor_data=sensor_data['proximity'],
                mood=robot_personality.current_personality
            )
            last_memory_time = current_time
            print(f"📍 Location {sensor_data['position']} logged.")

        # 4. LLM COMMENTARY (Every 20 seconds)
        if current_time - last_thought_time >= 20.0:
            thought = robot_personality.generate_llm_comment(context_str)
            print(f"💬 {robot_personality.current_personality.upper()}: {thought}")
            last_thought_time = current_time

if __name__ == "__main__":
    main()
