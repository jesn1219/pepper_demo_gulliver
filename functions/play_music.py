from naoqi import ALProxy
from motion import entertain, photo_motion


PATH = {"disco": "UrbanStreet.mp3", "bang": "", "guitar": "guitar_bgm.mp3", "saxophone": "epicsax.ogg"}
BASE_PATH = "/opt/aldebaran/www/apps/bi-sound/"


class Play:
    def __init__(self, srv, mode, ip):
        self.srv = srv
        self.mode = mode
        self.path = BASE_PATH + PATH[self.mode]
        self.ip = ip
        self.modes = PATH.keys()

    def motion(self):
        mode = self.mode
        modes = self.modes
        srv = self.srv

        player = ALProxy("ALAudioPlayer", self.ip, 9559)
        player.post.playFileFromPosition(self.path, 0)
        if mode == modes[0]:
            entertain.disco(srv)
        elif mode == modes[1]:
            entertain.bang(srv)
        elif mode == modes[2]:
            entertain.guitar(srv)
        elif mode == modes[3]:
            entertain.saxophone(srv)
        player.post.stopAll()
        photo_motion.stand(srv)
