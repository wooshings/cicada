import argparse
import os

parser = argparse.ArgumentParser(description="Generate Service File.")
parser.add_argument("name", help="Service name")
parser.add_argument("--apply", action="store_true", help="Apply service")

args = parser.parse_args()


def create():
    if os.path.exists(f"{args.name}.service"):
        os.remove(f"{args.name}.service")
    with open(f"{args.name}.service", "w") as f:
        f.write(f'''[Unit]
Description=Start {args.name}
After=network-online.target
Wants=network-online.target

[Service]
ExecStart=/bin/python3 /home/pi/myscript.py
WorkingDirectory={os.getcwd()}
StandardOutput=journal
Restart=always
User=pi

[Install]
WantedBy=multi-user.target''')


def enable():
    if not args.apply:
        return

    os.system(
        f"sudo mv {args.name}.service /etc/systemd/system/{args.name}.service")
    os.system("sudo systemctl daemon-reload")
    os.system(f"sudo systemctl enable {args.name}.service")
    os.system(f"sudo systemctl start {args.name}.service")


if __name__ == "__main__":
    create()
    enable()
