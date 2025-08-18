# cicada

> :warning: This library is still in early development and updating your projects may cause breaking changes.

<br>

<img src="banner.png" alt="cicada logo"/>

<br>
An easy to use python library for creating Escape Room puzzles using Raspberry Pi, built to feel like a Game Engine.

## Install

Using Python-pip

```
pip install "git+https://github.com/wooshdude/cicada[all]"
```

Using UV

```
uv add "git+https://github.com/wooshdude/cicada[all]"
```

If you want to write your script on a machine that isn't a Raspberry Pi, you can install Cicada with fallback dependencies.

```
pip install "git+https://github.com/wooshdude/cicada[fallback]"
    -- or --
uv add "git+https://github.com/wooshdude/cicada[fallback]"
```

## How to use

### Nodes

Cicada uses Nodes (called Cidadas), which are decorated subclasses.

```python
from Cicada.RPi import Cicada, Node

@Node
class Main(Cicada):
    def _ready(self):

    def _process(self):
```

Cicada exposes several functions through the Cicadaclass, but the two most important are `_ready` and `_process`.

**Ready**
`_ready()`

- Runs exactly once at the start of the program.
- Used to declare variables or setup pins.

**Process**
`_process()`

- Runs once every tick.
  - One tick is 1/20th of a second.
  - Can be adjusted with `self.tick_speed`
- Used for code that needs to be run repeatedly.

### Pins

Cicada also allows for easy use of the Raspberry Pi's GPIO pins, using the Pin class. Creating a pin takes two parameters, the pin number, and the mode.

```python
from Cicada.RPi import Pin

pin = 4         # The GPIO pin on the raspberry pi
mode = Pin.OUT  # The pin mode, IN for input, OUT for output
new_pin = Pin(pin, mode)
```

Pins have several helpful methods:

- on()
  - Turns the pin on
- off()
  - Turns the pin off
- toggle()
  - Toggles the pin on/off
- value()
  - Returns the current value of the pin, 1 or 0

#### Inputs

##### Button

Buttons are one of the most common typs of inputs used for aany escape game, and Cicada makes it easy to set up and use new buttons with the Button class.

```python
from Cicada.Inputs import Button

pin = 4
new_button = Button(4)
```

- is_pressed()
  - Returns True or False if the button is pressed every tick
- is_just_pressed()
  - The same as is_pressed() but only returns on the initial press
- is_just_released()
  - The opposite of is_just_pressed()

### Network Node

Cicada has optional support for MQTT using the NetworkNode decorator.

```python
from Cicada.RPi import Cicada, NetworkNode

topics = ["topics to subscribe to go here"]
@NetworkNode("localhost", 1883, topics)
class Main(Cicada):
    def _on_connect():

    def _on_message(msg):
```

A Network Node works the same as a Node, but offers a few extra functions tailored for MQTT.

**On Message**
`_on_message(msg)`

- Triggered when a subscribed topic receives a message. Carries the msg object.

**On Connect**
`_on_connect()`

- Triggered when the Node connects to the broker.

**Publish**
`publish(topic, payload)`

- Publishes a payload to a specified topic.

## Examples

### Node Example

```python
from Cicada.RPi import Cicada, Node, Pin

@Node
class Main(Cicada):
    # Runs once at the start of the programm
    def _ready(self):
        self.led = Pin(4, Pin.OUT)
        self.led.off()

        self.input = Pin(7, Pin.IN)

    # Runs every tick
    def _process(self):
        if self.input.value() == 1:
            self.led.on()
        else:
            self.led.off()
```

### NetworkNode Example

```python
from Cicada.RPi import Cicada, Node, Pin

topics = ["test/one", "test/two"]
@NetworkNode("localhost", 1883, topics)
class Main(Cicada):
    # Runs once at the start of the programm
    def _ready(self):
        self.led = Pin(4, Pin.OUT)
        self.led.off()

        self.input = Pin(7, Pin.IN)

    # Runs every tick
    def _process(self):
        if self.input.value() == 1:
            self.led.on()
        else:
            self.led.off()

    def _on_connect():
        print("Connected to MQTT broker.")
        self.publish("test/one", "hello world")

    def _on_message(msg):
        if msg.topic == "test/one":
            print(f"{msg.topic}: {msg.payload}")
            self.publish("test/two", "hello back")

```

## Service

More than likely, your Raspberry Pi will be frequently rebooted. In that case, scripts should automatically be run once the device has fully booted.
Cicada offers a simple python script that generates a service file.

You can clone the repository and run `serve.py`, or..

```
curl https://raw.githubusercontent.com/wooshings/cicada/refs/heads/main/serve.py | python3
```

## TODO
- Modularize creating new processes
- Smart dial inputs
- Screw all everything and convert backend to C for arduino support (kill me)
- Add immdiate-mode support for when all you need is to check if a button is pressed and turn on an output
