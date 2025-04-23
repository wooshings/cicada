from Cicada.RPi import Pin


class Button(Pin):
    def __init__(self, pin) -> None:
        super().__init__(pin, Pin.IN)

    def is_pressed(self):
        if self.value() == 0:
            return True
        return False

    def is_just_pressed(self):
        if self.is_pressed() and self.pressed: return False

        if self.is_pressed() and not self.pressed:
            self.pressed = True
            return True

        elif not self.is_pressed() and self.pressed:
            self.pressed = False
            return False

    def is_just_released(self):
        if self.is_pressed() and self.released:
            self.released = False
            return False

        elif not self.is_pressed() and not self.released:
            self.released = True
            return True
