from Cicada.RPi import Pin, Node, Nymph

@Node()
class Main(Nymph):
	def _ready(self):
		self.button = Pin(1, Pin.IN)
	
	def _process(self):
		if self.button.is_pressed():
			print("i am a button being held down!")
		
		if self.button.is_just_pressed():
			print("i am a button being pressed once!")
