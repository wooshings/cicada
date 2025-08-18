import os
import os.path
import argparse
import sys

parser = argparse.ArgumentParser(prog="Cicada service file creator.", description="Create and apply service files to automatically run your scripts.")
args = parser.parse_args()

name: str = ""
apply: str = ""


def get_input():
    global name
    global apply
    name = input("Choose name for service: ")
    apply = input(
        "Would you like the service to be automatically applied?: [y/n] ")


def create():
    if os.path.exists(f"{name}.service"):
        os.remove(f"{name}.service")

    python_path: str = ''
    if os.path.exists("bin/python3"):
        python_path = "bin/python3"
    elif os.path.exists(".venv/bin/python3"):
        python_path = ".venv/bin/python3"
    print(f"Found path to Python virtual environment at {python_path}")
        
    with open(f"{name}.service", "w") as f:
        f.write(f'''[Unit]
Description=Start {name}
After=network-online.target
Wants=network-online.target

[Service]
ExecStart={python_path} /home/pi/myscript.py
WorkingDirectory={os.getcwd()}
StandardOutput=journal
Restart=always
User={os.getlogin()}

[Install]
WantedBy=multi-user.target''')


def enable():
    if not apply == "y":
        return

    os.system(
        f"sudo mv {name}.service /etc/systemd/system/{name}.service")
    os.system("sudo systemctl daemon-reload")
    os.system(f"sudo systemctl enable {name}.service")
    os.system(f"sudo systemctl start {name}.service")


if __name__ == "__main__":
    get_input()
    create()
    enable()
    if args.temp:
        os.remove(sys.argv[0])
