from Cicada.RPi import Node, Nymph

@Node()
class Main(Nymph):
    def _process(self):
        print("balls")
