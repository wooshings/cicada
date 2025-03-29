import paho.mqtt.client as mqtt
from time import sleep
import asyncio
import RPi.GPIO as GPIO

class Nymph():
    host: str
    port: int
    topics: list[str]
    mqttc: mqtt.Client

    def __init__(self, host: str, port: int, topics: list) -> None:
        self.host = host
        self.port = port
        self.topics = topics 
        self.mqttc = mqtt.Client()
        
        self.start()
        asyncio.run(self.start_process())

    def start(self):
        self.mqttc.connect(self.host, self.port, 60)

        self.mqttc.on_connect = self.connect_callback
        self.mqttc.on_message = self.message_callback

    async def start_process(self):
        self._ready()
        while True:
            self.mqttc.loop_read()
            self._process()
            self.mqttc.loop_write()
            sleep(0.05)

    def _ready(self):
        pass

    def _process(self):
        pass

    def _on_connect(self):
        pass

    def _on_message(self, msg):
        pass

    def publish(self, topic, msg):
        self.mqttc.publish(topic, msg)

    def connect_callback(self, client, userdata, flags, reason_code):
        print(f"Connected with result code {reason_code}")
        for topic in self.topics:
            client.subscribe(topic)
        self._on_connect()

    def message_callback(self, client, userdata, msg):
        self._on_message(msg)

class Property():
    default = 0
    value = 0

    def __init__(self, default) -> None:
        self.default = default
        self.value = default

    def reset(self):
        self.value = self.default
    
    def get_value(self):
        return str(self.value)

def Node(host="localhost", port=1883, topics=[]):
    def wrapper(cls):
        new_node = cls(host, port, topics)
        return new_node
    return wrapper


class Pin():
    pressed:bool = False

    def __init__(self, pin, mode) -> None:
        self.pin = pin
        self.mode = mode

        GPIO.setmode(GPIO.BCM)
        if mode == GPIO.IN:
            GPIO.setup(pin, mode, pull_up_down=GPIO.PUD_UP)
        else:
            GPIO.setup(pin, mode)

    def value(self):
        if self.mode != GPIO.IN: print(f"Pin {self.pin} is not an input")
        if GPIO.input(self.pin): return 0
        return 1

    def is_pressed(self):
        if self.value() == 1:
            return True
        return False

    def is_just_pressed(self):
        if self.value() == 0 and self.pressed: return False

        if self.value() == 0 and not self.pressed:
            self.pressed = True
            return True
        elif self.value() == 1 and self.pressed:
            self.pressed = False
            return False






