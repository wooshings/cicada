from Cicada.RPi import Node, Cicada
from Cicada.Inputs import Button

@Node()
class Main(Cicada):
	def _ready(self):
		self.button = Button(1)
	
	def _process(self):
		if self.button.is_pressed():
			print("i am a button being held down!")
		
		if self.button.is_just_pressed():
			print("i am a button being pressed once!")
