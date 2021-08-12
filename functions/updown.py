import time
from random import randint
from data_list import *

# the string of responses
UP = "Up"
DOWN = "Down"
CORRECT = "That's correct!"
ERROR = "Error occurs."  # error statement

VALID = 0.4


class UpDown:
    def __init__(self, srv):
        self.answer = randint(1, 10 + 1)  # range of numbers
        self.tts = srv['tts']
        self.asr = srv['asr']
        srv['asr'].setLanguage("English")
        self.exit_flag = False

    def asr_callback(self, msg):
        # Threshold
        if msg[1] > VALID:
            print(msg[0], msg[1], " is returned")
            self.ret['type'] = 'speech'
            self.ret['word'] = msg[0]
            self.exit_flag = True

    def response(self, number):
        tts = self.tts
        is_right = self.answer == number
        if is_right:
            tts.say(CORRECT)
        elif self.answer > number:
            tts.say(UP)
        elif self.answer < number:
            tts.say(DOWN)
        return is_right
