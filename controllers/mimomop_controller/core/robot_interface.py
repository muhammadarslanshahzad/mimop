from controller import Robot, Keyboard, Supervisor
import numpy as np

class MiMoMopRobot:
    def __init__(self):
        self.robot = Supervisor()
        self.timestep = int(self.robot.getBasicTimeStep())
        
        # --- Thymio II Motors ---
        # Official Webots names for Thymio II motors
        self.left_motor = self.robot.getDevice('motor.left')
        self.right_motor = self.robot.getDevice('motor.right')
        
        self.left_motor.setPosition(float('inf'))
        self.right_motor.setPosition(float('inf'))
        self.left_motor.setVelocity(0.0)
        self.right_motor.setVelocity(0.0)
        
        self.keyboard = Keyboard()
        self.keyboard.enable(self.timestep)

        # --- Thymio II Proximity Sensors ---
        # Thymio has 7 horizontal sensors: 5 front, 2 back
        self.prox_sensors = []
        for i in range(7):
            # Official names: prox.horizontal.0 to prox.horizontal.6
            ps = self.robot.getDevice(f'prox.horizontal.{i}')
            if ps:
                ps.enable(self.timestep)
                self.prox_sensors.append(ps)
        
        # --- Optional Navigation ---
        self.gps = self.robot.getDevice('gps')
        if self.gps: self.gps.enable(self.timestep)
        
        print(f"✅ Thymio II initialized with {len(self.prox_sensors)} proximity sensors")

    def get_sensor_data(self):
        """Prepares data for Ollama and Qdrant"""
        # Thymio proximity sensors return values between 0 (far) and ~4000 (close)
        prox_values = [ps.getValue() for ps in self.prox_sensors]
        
        return {
            'timestamp': self.robot.getTime(),
            'position': self.gps.getValues() if self.gps else [0, 0, 0],
            'proximity': prox_values,
            # Identify if any front sensor (0-4) is triggered
            'obstacle_ahead': any(v > 1000 for v in prox_values[:5])
        }

    def set_velocities(self, left, right):
        # Thymio II max speed is approximately 9.53 rad/s
        max_speed = 9.53
        self.left_motor.setVelocity(np.clip(left, -max_speed, max_speed))
        self.right_motor.setVelocity(np.clip(right, -max_speed, max_speed))

    def get_keyboard_command(self):
        """Translates Webots key codes into movement strings"""
        key = self.keyboard.getKey()
        
        if key == Keyboard.UP:
            return 'forward'
        elif key == Keyboard.DOWN:
            return 'backward'
        elif key == Keyboard.LEFT:
            return 'left'
        elif key == Keyboard.RIGHT:
            return 'right'
        
        return None

    def get_time(self):
        """Returns the current simulation time in seconds"""
        return self.robot.getTime()
    
    def move_forward(self):
        # Drive both wheels forward
        self.set_velocities(5.0, 5.0)

    def move_backward(self):
        # Drive both wheels backward
        self.set_velocities(-5.0, -5.0)

    def move_left(self):
        # Tank turn: left wheel back, right wheel forward
        self.set_velocities(-3.0, 3.0)

    def move_right(self):
        # Tank turn: left wheel forward, right wheel back
        self.set_velocities(3.0, -3.0)

    def step(self):
        return self.robot.step(self.timestep)

    def stop(self):
        self.set_velocities(0.0, 0.0)


    def setLabel(self, id, text, x, y, size, color, transparency, font="Arial"):
        """Wrapper to call the native Webots setLabel method"""
        self.robot.setLabel(id, text, x, y, size, color, transparency, font)