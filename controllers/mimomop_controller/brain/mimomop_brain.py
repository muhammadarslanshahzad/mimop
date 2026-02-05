import requests

class MiMoMopBrain:
    def __init__(self, model="gemma3:4b"):
        self.model = model
        self.url = "http://localhost:11434/api/generate"

    def generate_thought(self, sensor_data, personality):
        prompt = f"""
        System: You are {personality}. You are currently cleaning a room.
        Data: Proximity sensors: {sensor_data['proximity']}. Position: {sensor_data['position']}.
        Task: Give a short, one-sentence sarcastic comment about your current cleaning progress.
        """
        
        response = requests.post(self.url, json={
            "model": self.model,
            "prompt": prompt,
            "stream": False
        })
        return response.json().get('response', "I have no thoughts, just dust.")