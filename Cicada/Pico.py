from machine import Pin as GPIO
from simple import MQTTClient
from utime import sleep
import network
import uasyncio

class Nymph():
	def __init__(self, host: str, port: int, topics: list) -> None:
		self.host = host
		self.port = port
		self.topics = topics 
		self.mqttc = MQTTClient(client_id="1", server=self.host)
		self.tick_speed = 20
		
		self.start()
		uasyncio.run(self.start_process())

	def start(self):
		if self.host == "": return
		while True:
			try:
				self.mqttc.connect()
				break
			except OSError:
				print("Connection to broker failed. Attempting to reconnect.")
		self.mqttc.set_callback(self.message_callback)

		for topic in self.topics:
			self.mqttc.subscribe(topic)
		self._on_connect()
			
	async def start_process(self):
		self._ready()
		while True:
			try:
				self._process()
				self.mqttc.check_msg()
				await uasyncio.sleep(1/self.tick_speed)
			except KeyboardInterrupt:
				print("\nStopping program. Goodbye!")
				break

	def _ready(self):
		pass

	def _process(self):
		pass

	def _on_connect(self):
		pass

	def _on_message(self, msg):
		pass

	def publish(self, topic, payload):
		if self.host == "": print("Cannot publish using type Node. Try creating a NetworkNode instead.")
		self.mqttc.publish(topic, payload)

	def message_callback(self, topic, payload):
		print('received message')
		self._on_message(Msg(topic, payload))


class Network():
	def __init__(self, ssid, password) -> None:
		self.wlan = network.WLAN(network.STA_IF)
		self.wlan.active(True)
		self.wlan.connect(ssid, password)
		while self.wlan.isconnected() == False:
			print('Waiting for connection...')
			sleep(1)
		print("Connected to WiFi")

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

class Pin(GPIO):
	def __init__(self, pin, mode) -> None:
		if mode == GPIO.OUT:
			super().__init__(pin, mode)
		else:
			super().__init__(pin, mode, GPIO.PULL_UP)
		self.pin = pin
		self.mode = mode
		self.pressed = False
		self.released = True
		self.is_on = True

	def on(self):
		if self.mode == self.IN: print(f"Pin {self.pin} is not an output."); return
		self.is_on = True
		return super().on()

	def off(self):
		if self.mode == self.IN: print(f"Pin {self.pin} is not an output."); return
		self.is_on = False
		return super().off()

	def value(self):
		if self.mode != GPIO.IN: print(f"Pin {self.pin} is not an input."); return
		return super().value()


class Msg():
	def __init__(self, topic, payload) -> None:
		self.topic = topic
		self.payload = payload
