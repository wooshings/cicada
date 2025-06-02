from Cicada.RPi import Pin
from mfrc522 import SimpleMFRC522


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


class RFID(SimpleMFRC522):
    def __init__(self):
        super().__init__()
        self.last_id = None
        self.tag_present = False
        self.ready_to_scan = True

    def scan(self):
        current_id = self.read_id_no_block()

        if not current_id:
            self.tag_present = False
            self.last_id = None
            self.ready_to_scan = True
            return

        if self.ready_to_scan and (not self.tag_present or current_id != self.last_id):
            self.last_id = current_id
            self.tag_present = True
            self.ready_to_scan = False  # Block scanning until no tag detected

            try:
                self.MFRC522_StopCrypto1()
            except AttributeError:
                pass

            return current_id

        return
