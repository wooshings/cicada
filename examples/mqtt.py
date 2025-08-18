from Cicada.RPi import NetworkNode, Cicada

topics = ["example/topic"]
@NetworkNode("localhost", 1883, topics)
class Main(Cicada):
	def _on_connect(self):
		print("Connected to MQTT broker.")
		self.publish("test/topics", "this is a example message!")
	
	def _on_message(self, msg):
		print(f"{msg.topic}: {msg.payload}")
	
