import random
import hashlib
import socketserver
import os

class XDRHandler(socketserver.StreamRequestHandler):
    def challenge(self):
        rng = random.SystemRandom()
        chars = "QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm0123456789_-"
        return "".join(rng.choice(chars) for i in range(16))

    def send(self, data):
        self.wfile.write(bytes(str(data) + '\n', 'ascii', 'ignore'))

    def hash(self, salt):
        m = hashlib.sha1()
        m.update(bytes(salt, 'ascii'))
        m.update(bytes(self.server.get_password(), 'ascii'))
        return m.hexdigest()

    def hello(self):
        self.send("M%d\nY%d\nT%d\nD%d\nA%d\nF%d\nZ%d\nG%02d\nV%d\nQ%d\nC%d\nI%d,%d" % (self.server.get_tuner_mode(), self.server.get_tuner_volume(), self.server.get_tuner_freq(), self.server.get_tuner_deemphasis(), self.server.get_tuner_agc(), self.server.get_tuner_filter(), self.server.get_tuner_ant(), self.server.get_tuner_gain(), self.server.get_tuner_daa(), self.server.get_tuner_squelch(), self.server.get_tuner_rotator(), self.server.get_tuner_sampling(), self.server.get_tuner_detector()))

    def parse(self, data):
        if(data[0] == "x"):
            self.send("OK")
        elif(data[0] == "X"):
            return False
        elif(data[0] == "T"):
            self.server.set_tuner_freq(int(data[1:]))
            os.system("pgrep -f \"nc -l -u 12345\" | xargs kill -9")
            os.system("pgrep -f \"nc -u 127.0.0.1 52005\" | xargs kill -9")
            #os.system("kill -9 `pidof nc`")
        elif(data[0] == "B"):
            self.server.set_tuner_forced_mono(int(data[1:]))
        elif(data[0] == "D"):
            self.server.set_tuner_deemphasis(int(data[1:]))
        elif(data[0] == "F"):
            self.server.set_tuner_filter(int(data[1:]))

        return True

    def handle(self):
        self.guest = False
        salt = self.challenge()
        self.send(salt)

        data = self.rfile.readline().strip().lower().decode()
        localhash = self.hash(salt)

        if(not data or len(data) != 40):
            return

        if localhash != data:
            allow_guests = self.server.get_allow_guests()
            self.guest = True
            self.send("a"+str(int(allow_guests)))
            if not allow_guests:
                return

        self.hello()
        self.server.add_user(self)

        while True:
            data = self.rfile.readline().strip().decode()
            if not data:
                break
            if not self.guest:
                if not self.parse(data):
                    break

        self.server.remove_user(self)
