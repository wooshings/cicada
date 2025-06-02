from machine import Pin as GPIO
from utime import sleep
import network
import uasyncio


processes:list = []

class Cicada():
	def __init__(self, host: str, port: int, topics: list) -> None:
		self.host = host
		self.port = port
		self.topics = topics 
		self.mqttc = MQTTClient(client_id="1", server=self.host)
		self.tick_speed = 20
		
		self.start()

	def start(self):
		if self.host == "": return
		self._ready()
		while True:
			try:
				self.mqttc.connect()
				break
			except OSError:
				print("Connection to broker failed. Attempting to reconnect.")
		self.mqttc.set_callback(self.message_callback)

		for topic in self.topics:
			self.mqttc.subscribe(topic)
		self._on_connect()
			
	async def start_process(self):
		try:
			while True:
				self._process()
				self.mqttc.check_msg()
				await uasyncio.sleep(1/self.tick_speed)
		except KeyboardInterrupt:
			print("\nStopping program. Goodbye!")
			quit()

	def _ready(self):
		pass

	def _process(self):
		pass

	def _on_connect(self):
		pass

	def _on_message(self, msg):
		pass

	def publish(self, topic, payload):
		if self.host == "": print("Cannot publish using type Node. Try creating a NetworkNode instead.")
		self.mqttc.publish(topic, payload)

	def message_callback(self, topic, payload):
		print('received message')
		self._on_message(Msg(topic, payload))


class Network():
	def __init__(self, ssid, password) -> None:
		self.wlan = network.WLAN(network.STA_IF)
		self.wlan.active(True)
		self.wlan.connect(ssid, password)
		while self.wlan.isconnected() == False:
			print('Waiting for connection...')
			sleep(1)
		print("Connected to WiFi")
def NetworkNode(host="localhost", port=1883, topics=[]):
    def wrapper(cls):
        new_node = cls(host, port, topics)
        return new_node
    return wrapper

def Node():
    def wrapper(cls):
        new_node = cls("", 0, [])
        return new_node
    return wrapper

class Pin(GPIO):
	def __init__(self, pin, mode) -> None:
		if mode == GPIO.OUT:
			super().__init__(pin, mode)
		else:
			super().__init__(pin, mode, GPIO.PULL_UP)
		self.pin = pin
		self.mode = mode
		self.pressed = False
		self.released = True
		self.is_on = True

	def on(self):
		if self.mode == self.IN: print(f"Pin {self.pin} is not an output."); return
		self.is_on = True
		return super().on()

	def off(self):
		if self.mode == self.IN: print(f"Pin {self.pin} is not an output."); return
		self.is_on = False
		return super().off()

	def value(self):
		if self.mode != GPIO.IN: print(f"Pin {self.pin} is not an input."); return
		return super().value()


class Msg():
	def __init__(self, topic, payload) -> None:
		self.topic = topic
		self.payload = payload


import socket
import struct
from binascii import hexlify


class MQTTException(Exception):
    pass


class MQTTClient:
    def __init__(
        self,
        client_id,
        server,
        port=0,
        user=None,
        password=None,
        keepalive=0,
        ssl=None,
    ):
        if port == 0:
            port = 8883 if ssl else 1883
        self.client_id = client_id
        self.server = server
        self.port = port
        self.ssl = ssl
        self.pid = 0
        self.cb = None
        self.user = user
        self.pswd = password
        self.keepalive = keepalive
        self.lw_topic = None
        self.lw_msg = None
        self.lw_qos = 0
        self.lw_retain = False

    def _send_str(self, s):
        self.sock.write(struct.pack("!H", len(s)))
        self.sock.write(s)

    def _recv_len(self):
        n = 0
        sh = 0
        while 1:
            b = self.sock.read(1)[0]
            n |= (b & 0x7F) << sh
            if not b & 0x80:
                return n
            sh += 7

    def set_callback(self, f):
        self.cb = f

    def set_last_will(self, topic, msg, retain=False, qos=0):
        assert 0 <= qos <= 2
        assert topic
        self.lw_topic = topic
        self.lw_msg = msg
        self.lw_qos = qos
        self.lw_retain = retain

    def connect(self, clean_session=True, timeout=None):
        self.sock = socket.socket()
        self.sock.settimeout(timeout)
        addr = socket.getaddrinfo(self.server, self.port)[0][-1]
        self.sock.connect(addr)
        if self.ssl:
            self.sock = self.ssl.wrap_socket(self.sock, server_hostname=self.server)
        premsg = bytearray(b"\x10\0\0\0\0\0")
        msg = bytearray(b"\x04MQTT\x04\x02\0\0")

        sz = 10 + 2 + len(self.client_id)
        msg[6] = clean_session << 1
        if self.user:
            sz += 2 + len(self.user) + 2 + len(self.pswd)
            msg[6] |= 0xC0
        if self.keepalive:
            assert self.keepalive < 65536
            msg[7] |= self.keepalive >> 8
            msg[8] |= self.keepalive & 0x00FF
        if self.lw_topic:
            sz += 2 + len(self.lw_topic) + 2 + len(self.lw_msg)
            msg[6] |= 0x4 | (self.lw_qos & 0x1) << 3 | (self.lw_qos & 0x2) << 3
            msg[6] |= self.lw_retain << 5

        i = 1
        while sz > 0x7F:
            premsg[i] = (sz & 0x7F) | 0x80
            sz >>= 7
            i += 1
        premsg[i] = sz

        self.sock.write(premsg, i + 2)
        self.sock.write(msg)
        # print(hex(len(msg)), hexlify(msg, ":"))
        self._send_str(self.client_id)
        if self.lw_topic:
            self._send_str(self.lw_topic)
            self._send_str(self.lw_msg)
        if self.user:
            self._send_str(self.user)
            self._send_str(self.pswd)
        resp = self.sock.read(4)
        assert resp[0] == 0x20 and resp[1] == 0x02
        if resp[3] != 0:
            raise MQTTException(resp[3])
        return resp[2] & 1

    def disconnect(self):
        self.sock.write(b"\xe0\0")
        self.sock.close()

    def ping(self):
        self.sock.write(b"\xc0\0")

    def publish(self, topic, msg, retain=False, qos=0):
        pkt = bytearray(b"\x30\0\0\0")
        pkt[0] |= qos << 1 | retain
        sz = 2 + len(topic) + len(msg)
        if qos > 0:
            sz += 2
        assert sz < 2097152
        i = 1
        while sz > 0x7F:
            pkt[i] = (sz & 0x7F) | 0x80
            sz >>= 7
            i += 1
        pkt[i] = sz
        # print(hex(len(pkt)), hexlify(pkt, ":"))
        self.sock.write(pkt, i + 1)
        self._send_str(topic)
        if qos > 0:
            self.pid += 1
            pid = self.pid
            struct.pack_into("!H", pkt, 0, pid)
            self.sock.write(pkt, 2)
        self.sock.write(msg)
        if qos == 1:
            while 1:
                op = self.wait_msg()
                if op == 0x40:
                    sz = self.sock.read(1)
                    assert sz == b"\x02"
                    rcv_pid = self.sock.read(2)
                    rcv_pid = rcv_pid[0] << 8 | rcv_pid[1]
                    if pid == rcv_pid:
                        return
        elif qos == 2:
            assert 0

    def subscribe(self, topic, qos=0):
        assert self.cb is not None, "Subscribe callback is not set"
        pkt = bytearray(b"\x82\0\0\0")
        self.pid += 1
        struct.pack_into("!BH", pkt, 1, 2 + 2 + len(topic) + 1, self.pid)
        # print(hex(len(pkt)), hexlify(pkt, ":"))
        self.sock.write(pkt)
        self._send_str(topic)
        self.sock.write(qos.to_bytes(1, "little"))
        while 1:
            op = self.wait_msg()
            if op == 0x90:
                resp = self.sock.read(4)
                # print(resp)
                assert resp[1] == pkt[2] and resp[2] == pkt[3]
                if resp[3] == 0x80:
                    raise MQTTException(resp[3])
                return

    # Wait for a single incoming MQTT message and process it.
    # Subscribed messages are delivered to a callback previously
    # set by .set_callback() method. Other (internal) MQTT
    # messages processed internally.
    def wait_msg(self):
        res = self.sock.read(1)
        self.sock.setblocking(True)
        if res is None:
            return None
        if res == b"":
            raise OSError(-1)
        if res == b"\xd0":  # PINGRESP
            sz = self.sock.read(1)[0]
            assert sz == 0
            return None
        op = res[0]
        if op & 0xF0 != 0x30:
            return op
        sz = self._recv_len()
        topic_len = self.sock.read(2)
        topic_len = (topic_len[0] << 8) | topic_len[1]
        topic = self.sock.read(topic_len)
        sz -= topic_len + 2
        if op & 6:
            pid = self.sock.read(2)
            pid = pid[0] << 8 | pid[1]
            sz -= 2
        msg = self.sock.read(sz)
        self.cb(topic, msg)
        if op & 6 == 2:
            pkt = bytearray(b"\x40\x02\0\0")
            struct.pack_into("!H", pkt, 2, pid)
            self.sock.write(pkt)
        elif op & 6 == 4:
            assert 0
        return op

    # Checks whether a pending message from server is available.
    # If not, returns immediately with None. Otherwise, does
    # the same processing as wait_msg.
    def check_msg(self):
        self.sock.setblocking(False)
        return self.wait_msg()


__version__ = '1.5.0'
