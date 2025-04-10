import paho.mqtt.client as mqtt
from time import sleep
import asyncio
import RPi.GPIO as GPIO

processes = []
def add_process():
    def wrapper(func):
        processes.append(func)
        return func
    return wrapper

async def run_process():
    for p in processes:
        p()
asyncio.run(run_process())

class Nymph():
    def __init__(self, host: str, port: int, topics: list) -> None:
        self.host = host
        self.port = port
        self.topics = topics 
        self.mqttc = mqtt.Client()
        self.tick_speed = 20
        
        self.start()
        self._ready()
        asyncio.run(self.start_process())

    def start(self):
        if self.host == "": return
        self.mqttc.connect(self.host, self.port, 60)

        self.mqttc.on_connect = self.connect_callback
        self.mqttc.on_message = self.message_callback

    @add_process()
    async def start_process(self):
        try:
            self.mqttc.loop_read()
            self._process()
            self.mqttc.loop_write()
            sleep(1/self.tick_speed)
        except KeyboardInterrupt:
            print("\nStopping program. Goodbye!")
            quit()

    def _ready(self):
        pass

    def _process(self):
        pass

    def _on_connect(self):
        pass

    def _on_message(self, msg):
        pass

    def publish(self, topic, msg):
        if self.host == "": print("Cannot publish using type Node. Try creating a NetworkNode instead.")
        self.mqttc.publish(topic, msg)

    def connect_callback(self, client, userdata, flags, reason_code):
        print(f"Connected with result code {reason_code}")
        for topic in self.topics:
            client.subscribe(topic)
        self._on_connect()

    def message_callback(self, client, userdata, msg):
        self._on_message(msg)

class Property():
    def __init__(self, default) -> None:
        self.default = default
        self.value = default

    def reset(self):
        self.value = self.default
    
    def get_value(self):
        return str(self.value)

def NetworkNode(host="localhost", port=1883, topics=[]):
    def wrapper(cls):
        new_node = cls(host, port, topics)
        return new_node
    return wrapper

def Node():
    def wrapper(cls):
        new_node = cls("", 0, [])
        return new_node
    return wrapper


class Pin():
    IN = GPIO.IN
    OUT = GPIO.OUT

    def __init__(self, pin, mode) -> None:
        self.pin = pin
        self.mode = mode
        self.pressed = False
        self.released = True
        self.is_on = True

        GPIO.setmode(GPIO.BCM)
        if mode == GPIO.IN:
            GPIO.setup(pin, mode, pull_up_down=GPIO.PUD_UP)
        else:
            GPIO.setup(pin, mode)
            self.on()

    def on(self):
        if self.mode == self.IN: print(f"Pin {self.pin} is not an output."); return
        self.is_on = True
        GPIO.output(self.pin, 1)

    def off(self):
        if self.mode == self.IN: print(f"Pin {self.pin} is not an output."); return
        self.is_on = False
        GPIO.output(self.pin, 0)

    def toggle(self):
        if self.is_on:
            self.off()
        elif not self.is_on:
            self.on()

    def value(self):
        if self.mode != GPIO.IN: print(f"Pin {self.pin} is not an input."); return
        if GPIO.input(self.pin): return 1
        return 0

    def is_pressed(self):
        if self.value() == 0:
            return True
        return False

    def is_just_pressed(self):
        if self.is_pressed() and self.pressed: return False

        if self.is_pressed() and not self.pressed:
            self.pressed = True
            return True

        elif not self.is_pressed() and self.pressed:
            self.pressed = False
            return False
    
    def is_just_released(self):
        if self.is_pressed() and self.released:
            self.released = False
            return False

        elif not self.is_pressed() and not self.released:
            self.released = True
            return True






