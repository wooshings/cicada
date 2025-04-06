from Cicada.RPi import Nymph, Node, Pin
import random
from enum import Enum
from time import sleep

class Turn(Enum):
    game = 0
    user = 1
    done = 2

class LedButton():
    def __init__(self, in_pin, out_pin):
        self.input = Pin(in_pin, Pin.IN)
        self.output = Pin(out_pin, Pin.OUT)
        self.output.off()

@Node()
class Puzzle1(Nymph):
    def _ready(self):
        self.buttons = {"white": LedButton(17, 27), "green": LedButton(16, 20), "blue": LedButton(26, 19), "yellow": LedButton(23, 24)}

        self.output_code = []
        self.input_code = []
        self.steps = 1
        self.finished = False
        self.turn = Turn.game
        self.failed = False

    def _process(self):
        match (self.turn):
            case Turn.game: self.game_turn()
            case Turn.user: self.user_turn()

    def user_turn(self):
        self.failed = False
        for color in self.buttons.keys():
            button = self.buttons[color]

            if button.input.is_pressed():
                button.output.on()
            else:
                button.output.off()

            if button.input.is_just_pressed():
                print(f"{color} just pressed")
                self.input_code.append(color)
                print(self.input_code)

                if len(self.input_code) == len(self.output_code):
                    print(self.input_code)
                    print(self.output_code)
                    for i in range(len(self.output_code)):
                        if self.input_code[i] != self.output_code[i]:
                            self.output_code.clear()
                            self.input_code.clear()
                            print("game failed")

                    print("game turn")
                    button.output.on()
                    sleep(0.2)
                    button.output.off()
                    sleep(2)
                    self.turn = Turn.game

    def game_turn(self):
        if not self.failed and len(self.output_code) == 6:
            for button in self.buttons.values():
                button.output.on()
            return
        self.output_code.append(list(self.buttons.keys())[random.randint(0, 3)])
        output_icons = ""
        for i in self.output_code:
            output_icons += self.color_to_icon(i)
        print(output_icons)

        for color in self.output_code:
            self.buttons[color].output.on()
            sleep(1)
            self.buttons[color].output.off()
            sleep(0.5)

        self.input_code.clear()
        self.turn = Turn.user

    def color_to_icon(self, color) -> str:
        match color:
            case "white":
                return "⚪"
            case "blue":
                return "🔵"
            case "green":
                return "🟢"
            case "yellow":
                return "🟡"
        return "⚫"
