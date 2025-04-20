from Cicada.RPi import Pin, add_process

class Dial():
	def __init__(self, pin1, pin2) -> None:
		self.left_pin = Pin(pin1, Pin.IN)
		self.right_pin = Pin(pin2, Pin.IN)

	@add_process()
	def process(self):
		if self.left_pin.is_just_pressed():
			self._on_rotation(-1)
		elif self.right_pin.is_just_pressed():
			self._on_rotation(1)

	def _on_rotation(self, dir):
		pass

