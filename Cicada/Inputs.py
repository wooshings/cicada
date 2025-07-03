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

class Keypad3():
    def __init__(self, c1: int, c2: int, c3: int, r1: int, r2: int, r3: int, r4: int) -> None:
        self.c1: Pin = Pin(c1, Pin.IN)
        self.c2: Pin = Pin(c2, Pin.IN)
        self.c3: Pin = Pin(c3, Pin.IN)
        self.r1: Pin = Pin(r1, Pin.IN)
        self.r2: Pin = Pin(r2, Pin.IN)
        self.r3: Pin = Pin(r3, Pin.IN)
        self.r4: Pin = Pin(r4, Pin.IN)

        self.rows = [self.r1, self.r2, self.r3, self.r4]
        self.cols = [self.c1, self.c2, self.c3]
 
        self.nums = {
            1: (Button(r1), Button(c1)),
            2: (Button(r1), Button(c2)),
            3: (Button(r1), Button(c3)),
            4: (Button(r2), Button(c1)),
            5: (Button(r2), Button(c2)),
            6: (Button(r2), Button(c3)),
            7: (Button(r3), Button(c1)),
            8: (Button(r3), Button(c2)),
            9: (Button(r3), Button(c3)),
            0: (Button(r4), Button(c2)),
        }

        self.sym = {
            "*": (Button(r4), Button(c1)),
            "#": (Button(r4), Button(c3))
        }

    def get_num_just_pressed(self):
        for k,v in self.nums.items():
            if v[0].is_just_pressed() and v[1].is_just_pressed():
                return k




