from pathlib import Path
import subprocess

class Media():
    def __init__(self, path: str, loop: bool = False) -> None:
        self.path = path
        self.loop = loop

    def play(self):
        if not Path(self.path).exists():
            print(f"Path is not valid: {self.path}")
            return

        print("Started playback.")
        cmd = [
            "mpv",
            "--fs",
            "--no-border",
            "--hwdec=auto",
            "--vo=gpu"
        ]
        if self.loop:
            cmd.append("--loop")
        cmd.append(self.path)
        subprocess.run(cmd)

