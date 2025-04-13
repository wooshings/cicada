from os import path
import subprocess

class Media():
	def __init__(self, path:str, loop:bool = False) -> None:
		self.path = path
		self.loop = loop

	def play(self):
		if not path.exists(self.path): print(f"Path is not valid: {self.path}"); return
		
		print("Started playback.")
		subprocess.run(["vlc", 
				  "--fullscreen", 
				  "--video-on-top", 
				  "--no-video-title-show",
				  "--mouse-hide-timeout", "0",
				  "--loop" if self.loop else "--no-loop", 
				  "--play-and-stop", 
				  self.path])

