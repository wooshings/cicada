from Cicada.RPi import Pin, Node, Cicada
from time import sleep

@Node()
class Main(Cicada):
	def _ready(self):
		self.led = Pin(1, Pin.OUT)
		self.led.on()

	def _process(self):
		self.led.toggle()
		sleep(1)

