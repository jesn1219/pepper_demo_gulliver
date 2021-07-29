import time
from random import randint
from data_list import *

# the string of responses
UP = "Up"
DOWN = "Down"
CORRECT = "That's correct!"
ERROR = "Error occurs."  # error statement


class UpDown:
    def __init__(self, srv):
        self.answer = randint(1, 10 + 1)
        self.tts = srv['tts']
        self.asr = srv['asr']
        srv['asr'].setLanguage("English")
        self.exit_flag = False

    def asr_callback(self, msg):
        # Threshold
        if msg[1] > 0.4:
            print(msg[0], msg[1], " is returned")
            self.ret['type'] = 'speech'
            self.ret['word'] = msg[0]
            self.exit_flag = True

    def correct(self, number):
        return self.answer == number

    def response(self, number):
        is_right = self.correct(number)
        if is_right:
            return CORRECT
        elif self.answer > number:
            return UP
        elif self.answer < number:
            return DOWN
        return ERROR  # invalid case

    def show_result(self, correct):
        if correct:
            return "You loose."
        return "Exceeded the number of attempts. Game over."

    def play(self, input_ret):
        tts = self.tts
        tts.say("Hello!")

        # initialization
        correct = False
        count = 0
        while count < 3:
            tts.say("Say the number between 1 to 10. If you want to stop the game, say 'Stop'.")
            while input_ret['type'] != 'speech':
                time.sleep(0.01)
            value = input_ret['word']
            # check if user wants to stop the game
            if value == 'stop':
                tts.say("The game ends.")
                return  # stop the game

            try:
                int_value = NUMBERS[value]
                if int_value not in NUMBERS.values():
                    raise ValueError
            except (ValueError, KeyError):
                tts.say("Invalid. Try again.")
                continue

            response = self.response(int_value)
            tts.say(response)
            correct = self.correct(int_value)  # update the result
            if correct:
                break  # the game ends if the answer is correct
            count += 1

        tts.say(self.show_result(correct))
