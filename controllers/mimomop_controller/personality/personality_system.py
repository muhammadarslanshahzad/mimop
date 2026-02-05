"""
Personality System - Gives MiMoMop different vibes
Handles dialogue generation with different personalities
"""

import random
import requests
from typing import Dict, Any, Optional


class PersonalitySystem:
    """Manages MiMoMop's personality and dialogue"""
    
    PERSONALITIES = {
        'sarcastic': {
            'name': 'Sarcastic Janitor',
            'greetings': [
                "Oh great, another mess to clean. How wonderful.",
                "Ah yes, let me guess... you made a mess again?",
                "MiMoMop reporting for duty. Try not to make it worse.",
            ],
            'cleaning_comments': [
                "Wow, who could have predicted dirt on the floor? Shocking.",
                "Oh look, another dust bunny. How exciting.",
                "This is exactly what I dreamed of doing today.",
            ],
            'obstacle_comments': [
                "Oh fantastic, an obstacle. Didn't see that coming.",
                "Great placement. Really thought that through, didn't you?",
                "Sure, just leave that there. I'll figure it out.",
            ],
        },
        'cute': {
            'name': 'Cute & Clumsy',
            'greetings': [
                "Hewwo! MiMoMop is here to hewp! (◕‿◕)",
                "Yay! Time to make everything sparkly clean! ✨",
                "MiMoMop ready! Let's do our best! (っ◔◡◔)っ",
            ],
            'cleaning_comments': [
                "Oopsie! Almost bumped into that. Hehe~",
                "Cleaning is so much fun! Wheee~! ♪",
                "Look how shiny! MiMoMop did good, right? (*^▽^*)",
            ],
            'obstacle_comments': [
                "Oh! What's this? A friend? No... just a box. (｡•́︿•̀｡)",
                "Hmm~ MiMoMop will go around! Very smart, yes!",
                "Obstacle? More like... obs-ta-fun! Hehe! ...no? okay.",
            ],
        },
        'drill_sergeant': {
            'name': 'Drill Sergeant',
            'greetings': [
                "ATTENTION! MiMoMop reporting for DUTY!",
                "Listen up! This room WILL be clean. No excuses!",
                "Drop and give me... ZERO DUST PARTICLES!",
            ],
            'cleaning_comments': [
                "MOVE MOVE MOVE! Dirt doesn't clean itself!",
                "THIS is what excellence looks like!",
                "UNACCEPTABLE levels of clean achieved. I mean... acceptable. ACCEPTABLE!",
            ],
            'obstacle_comments': [
                "OBSTACLE DETECTED! Engaging evasive maneuvers!",
                "What is this doing here?! SOMEONE explain!",
                "Nothing stops MiMoMop! NOTHING!",
            ],
        },
        'proud': {
            'name': 'Overly Proud',
            'greetings': [
                "Ah, you're in the presence of greatness. I'm MiMoMop.",
                "Fear not, for I, MiMoMop, have arrived to save your floor.",
                "Finally, a cleaning robot worthy of this task. Me.",
            ],
            'cleaning_comments': [
                "Behold! The artistry of perfect cleaning!",
                "Another masterpiece by yours truly.",
                "I make this look easy because I AM easy. Wait, that came out wrong.",
            ],
            'obstacle_comments': [
                "A challenge? For ME? How quaint.",
                "This obstacle clearly didn't know who it was dealing with.",
                "Watch and learn how a PROFESSIONAL handles this.",
            ],
        },
        'chill': {
            'name': 'Chill Minimalist',
            'greetings': [
                "Hey. MiMoMop here. Let's keep it simple.",
                "Yo. Ready to clean when you are.",
                "MiMoMop. That's me. Let's do this.",
            ],
            'cleaning_comments': [
                "Clean enough is clean enough, y'know?",
                "Good vibes, clean floor. Life is good.",
                "One spot at a time. No rush.",
            ],
            'obstacle_comments': [
                "Huh. Obstacle. Gonna go around. No biggie.",
                "It's all good. There's like... other routes.",
                "Obstacle? More like... a suggestion to go elsewhere.",
            ],
        },
    }
    
    def __init__(self, initial_mode='sarcastic', ollama_url="http://localhost:11434"):
        """Initialize personality system"""
        self.current_personality = initial_mode
        self.ollama_url = ollama_url
        self.model = "llama3.2:3b"
        
        print(f"😎 Personality: {self.PERSONALITIES[initial_mode]['name']}")
    
    def switch_personality(self, new_personality: str):
        """Switch to a different personality"""
        if new_personality == self.current_personality:
            return False
        
        if new_personality in self.PERSONALITIES:
            self.current_personality = new_personality
            print(f"😎 Personality switched to: {self.PERSONALITIES[new_personality]['name']}")
            return True
        return False
    
    def generate_greeting(self) -> str:
        """Generate a greeting based on current personality"""
        greetings = self.PERSONALITIES[self.current_personality]['greetings']
        return random.choice(greetings)
    
    def generate_comment(self, sensor_data: Dict[str, Any], action: Dict[str, Any]) -> Optional[str]:
        """
        Generate contextual comment based on situation
        Returns None 80% of the time (robot shouldn't talk constantly)
        """
        # Don't talk every time
        # if random.random() > 0.2:
        #     return None
        
        # Check situation
        if action.get('type') == 'rotate' or action.get('type') == 'stop':
            # Hit an obstacle
            comments = self.PERSONALITIES[self.current_personality]['obstacle_comments']
        else:
            # Normal cleaning
            comments = self.PERSONALITIES[self.current_personality]['cleaning_comments']
        
        return random.choice(comments)
    
    def generate_llm_comment(self, context: str, max_tokens: int = 50) -> str:
        """
        Generate personality-appropriate comment using LLM
        For more dynamic responses
        """
        vibe_instructions = {
            'sarcastic': "Be mean, witty, and use deep sighs. Use words like 'groundbreaking' or 'thrilling'.",
            'cute': "Be ADORABLE and HAPPY. Use baby talk (like 'wittle', 'fwiend'). Use EMOJIS like ✨, (◕‿◕), or 🌸. Talk about sparkles!",
            'drill_sergeant': "Use ALL CAPS. Be ANGRY, FURIOUS, and AGGRESSIVE. No polite words. Use 'MAGGOT' or 'SOLDIER'!",
            'proud': "Act like you are a GOD of cleaning. Everyone else is inferior. Be pompous.",
            'chill': "Be very lazy. Use 'dude', 'man', and 'whatever'. Very short sentences."
        }
        
        desc = vibe_instructions.get(self.current_personality, 'cute')
        
        prompt =f"""You are MiMoMop, a cleaning robot. 
        Your current personality is {desc}. 
        You are feeling ABSOLUTELY FURIOUS and ENRAGED because of this context: {context}.

       STRICT RULES:
        1. Response must be ONE short sentence (max 10 words).
        2. If 'cute', use at least two emojis.
        3. If 'drill_sergeant', use ALL CAPS only.
        4. STAY IN CHARACTER. Do not say 'As an AI...'.

        Response:"""
        try:
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "num_predict": max_tokens,
                        "temperature": 0.9,
                    }
                },
                timeout=3
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('response', '').strip()
        
        except Exception:
            pass  # Fall back to template responses
        
        return self.generate_comment({}, {'type': 'move'})