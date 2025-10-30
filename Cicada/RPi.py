import paho.mqtt.client as mqtt
from time import sleep
import asyncio
import importlib.util
import sys
import traceback

try:
    importlib.util.find_spec("RPi.GPIO")
except ImportError:
    import fake_rpi
    sys.modules['RPi'] = fake_rpi.RPi     # Fake RPi
    sys.modules['RPi.GPIO'] = fake_rpi.RPi.GPIO # Fake GPIO

import RPi.GPIO as GPIO


class Cicada():
    def __init__(self, host: str, port: int, topics: list) -> None:
        self.host = host
        self.port = port
        self.topics = topics
        self.mqttc = mqtt.Client()
        self.tick_speed = 20

        self.start()

    def start(self):
        if not self.host == "":
            self.mqttc.connect(self.host, self.port, 60)

            self.mqttc.on_connect = self.connect_callback
            self.mqttc.on_message = self.message_callback
        self._ready()
        asyncio.run(self.start_process())

    async def start_process(self):
        try: 
            while True:
                self.mqttc.loop_read()
                self._process()
                self.mqttc.loop_write()
                sleep(1/self.tick_speed)
        except Exception:
            print(traceback.format_exc())
        except KeyboardInterrupt:
            print("\nStopping program. Goodbye!")
        finally:
            GPIO.cleanup()
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
        if self.host == "":
            print("Cannot publish using type Node. Try creating a NetworkNode instead.")
        self.mqttc.publish(topic, msg)

    def connect_callback(self, client, userdata, flags, reason_code):
        if reason_code != 0:
            print(f"Could not connect. Code {reason_code}")
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


def NetworkNode(host="localhost", port=1883, topics=None):
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
        if self.mode == self.IN:
            print(f"Pin {self.pin} is not an output.")
            return
        self.is_on = True
        GPIO.output(self.pin, 1)

    def off(self):
        if self.mode == self.IN:
            print(f"Pin {self.pin} is not an output.")
            return
        self.is_on = False
        GPIO.output(self.pin, 0)

    def toggle(self):
        if self.is_on:
            self.off()
        elif not self.is_on:
            self.on()

    def value(self):
        if self.mode != GPIO.IN:
            print(f"Pin {self.pin} is not an input.")
            return
        if GPIO.input(self.pin):
            return 1
        return 0

