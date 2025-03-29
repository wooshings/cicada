# cicada

An easy to use python library for creating Escape Room puzzles using Raspberry Pi, built to feel like a Game Engine.

## Install

```
pip install git+https://github.com/wooshdude/cicada
```

## How to use

### Nodes

Cicada uses Nodes (called Nymphs), which are decorated subclasses.

```python
from Cicada import Nymph, Node

@Node
class Main(Nymph):
    def _ready(self):

    def _process(self):
```

Cicada exposes several functions through the Nymph class, but the two most important are `_ready` and `_process`.

**Ready**
`_ready()`

- Runs exactly once at the start of the program.
- Used to declare variables or setup pins.

**Process**
`_process()`

- Runs once every tick.
  - One tick is 1/20th of a second.
- Used for code that needs to be run repeatedly.

### Pins

Cicada also allows for easy use of the Raspberry Pi's GPIO pins, using the Pin class. Creating a pin takes two parameters, the pin number, and the mode.

```python
from Cicada import Pin

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
- is_pressed()
  - Checks if the input is 1, returns a boolean
- is_just_pressed()
  - The same as is_pressed, but only triggers once per input

### Network Node

Cicada has optional support for MQTT using the NetworkNode decorator.

```python
from Cicada import Nymph, NetworkNode

topics = ["topics to subscribe to go here"]
@NetworkNode("localhost", 1883, topics)
class Main(Nymph):
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
from Cicada import Nymph, Node, Pin

@Node
class Main(Nymph):
    # Runs once at the start of the programm
    def _ready(self):
        self.led = Pin(4, Pin.OUT)
        self.led.off()

        self.input = Pin(7, Pin.IN)

    # Runs every tick
    def _process(self):
        if self.input.is_pressed():
            self.led.on()
        else:
            self.led.off()
```

### NetworkNode Example

```python
from Cicada import Nymph, Node, Pin

topics = ["test/one", "test/two"]
@NetworkNode("localhost", 1883, topics)
class Main(Nymph):
    # Runs once at the start of the programm
    def _ready(self):
        self.led = Pin(4, Pin.OUT)
        self.led.off()

        self.input = Pin(7, Pin.IN)

    # Runs every tick
    def _process(self):
        if self.input.is_pressed():
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
