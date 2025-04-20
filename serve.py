import argparse
import os
import sys

parser = argparse.ArgumentParser(description="Generate Service File.")
parser.add_argument("name", help="Service name")

args = parser.parse_args()


def main():
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


if __name__ == "__main__":
    main()

# sudo mv /etc/systemd/system/myscript.service
# sudo systemctl daemon-reload
# sudo systemctl enable myscript.service
# sudo systemctl start myscript.service
