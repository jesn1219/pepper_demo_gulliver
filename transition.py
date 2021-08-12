import time
from naoqi import ALProxy

from data_list import *
from cameras import take_photo
from functions import updown
from functions.play_music import *


aas_configuration = {"bodyLanguageMode": "contextual"}


class Transition:
    def __init__(self):
        pass

    def get_html_address(self, file_name):
        name = file_name
        if len(name) > 5 and name[-5:] == '.html':
            name = name[:-5]
        return "http://198.18.0.1/apps/bi-html/" + name + '.html'

    def tour_iot(self, srv):
        next_scene = 'tour_iot'
        srv['tts'].setParameter("defaultVoiceSpeed", 100)
        srv['tablet'].showWebview(self.get_html_address(next_scene))
        srv['aas'].say(
            "This room is a smart space built by an IoT platform. This IoT platform looks at the IoT environment based on service, not device. Users can build their own smart space from the perspective of a combination of services through a easy script language.",
            aas_configuration)

        # add the scene to introduce
        next_scene = 'tour_iot'  # NEED TO FIX THIS
        # srv['tablet'].showWebview(self.get_html_address(next_scene))
        srv['aas'].say(
            "Currently, entrance management, indoor environment management, and plant management are being performed through the IoT.",
            aas_configuration)

        # add the scene to introduce
        next_scene = 'tour_iot'  # NEED TO FIX THIS
        # srv['tablet'].showWebview(self.get_html_address(next_scene))
        srv['aas'].say(
            "We use heat sensor, camera, and motion sensor to guide people's entrance in accordance with the corona prevention rules.",
            aas_configuration)

        # add the scene to introduce
        next_scene = 'tour_iot'  # NEED TO FIX THIS
        # srv['tablet'].showWebview(self.get_html_address(next_scene))
        srv['aas'].say(
            "And, It is sensing environmental information through air quality sensors and some more sensors installed in three places in the room, and takes appropriate actions such as operating air conditioner and air purifier.",
            aas_configuration)

        # add the scene to introduce
        # next_scene = 'tour_iot'  # NEED TO FIX THIS
        srv['tablet'].showWebview(self.get_html_address(next_scene))
        srv['aas'].say(
            "Near the window, you can see a smart pot management. Measuring the soil humidity of each pot, it supplies water and light appropriately.",
            aas_configuration)

        # add the scene to introduce
        srv['aas'].say(
            "All IoT sensor data in this room is collected on a local server, and when an abnormality is detected, it can be checked on the dashboard.",
            aas_configuration)

        srv['tts'].setParameter("defaultVoiceSpeed", 70)
        next_scene = 'tour'
        srv['tablet'].showWebview(self.get_html_address(next_scene))
        return next_scene

    def tour_arm(self, srv):
        next_scene = 'tour_armrobot'
        srv['tts'].setParameter("defaultVoiceSpeed", 100)
        srv['tablet'].showWebview(self.get_html_address(next_scene))
        srv['aas'].say("Let me explain the arm robot space.", aas_configuration)
        srv['aas'].say("Here you can see the kinova gen3 lite, an arm robot for working and studying.", aas_configuration)

        # add the scene to introduce
        srv['aas'].say("This arm robot have a 6 joints and a two-finger gripper that can grip objects up to 500g.", aas_configuration)
        # add the scene to introduce
        srv['aas'].say("By mounting an rgbd camera named Realsense, it is possible to understanding the environments using vision module.",
                       aas_configuration)
        # add the scene to introduce
        srv['aas'].say(
            "The demo prepared by our researcher is a task of categorizing and tidying up the objects.",
            aas_configuration)
        # add the scene to introduce
        srv['aas'].say(
            "In addition, you can experience a remote control using vr service that allows you to perform tasks remotely using a robot arm by connecting to the oculus quest2.",
            aas_configuration)

        next_scene = 'tour_armrobot2'
        srv['tablet'].showWebview(self.get_html_address(next_scene))
        srv['aas'].say(
            "If you have any other questions or inquiries, please refer to the following website or contact us.",
            aas_configuration)

        srv['tts'].setParameter("defaultVoiceSpeed", 70)
        next_scene = 'tour'
        srv['tablet'].showWebview(self.get_html_address(next_scene))
        return next_scene

    def updown_game(self, srv, input_ret):
        tts = srv['tts']
        tts.say("Hello!")

        game = updown.UpDown(srv)
        correct = False

        trial = 3  # number of trials
        while trial > 0:
            tts.say("Say the number between 1 to 10. If you want to stop the game, say 'Stop'.")
            time.sleep(0.01)
            tts.say("The number of remaining attempts is only %d" % trial)
            while input_ret['type'] != 'speech':
                time.sleep(0.01)
            value = input_ret['word']
            # check if user wants to stop the game
            if value == 'stop':
                tts.say("The game ends.")
                return SCENES['entertain2']  # stop the game
            try:
                int_value = NUMBERS[value]
                if int_value not in NUMBERS.values():
                    raise ValueError
            except (ValueError, KeyError):
                tts.say("Invalid. Try again.")
                continue
            if game.response(int_value):
                correct = True
                break
            else:
                trial -= 1

        if correct:
            tts.say("You Win! Congratulations!")
        else:
            tts.say("You lose. Game over.")

        return SCENES['entertain2']

    def do_elephant(self, srv):
        file_path = "/opt/aldebaran/www/apps/bi-sound/elephant.ogg"
        player = ALProxy("ALAudioPlayer", PEPPER_IP, 9559)
        player.post.playFileFromPosition(file_path, 0)
        entertain.elephant(srv)
        player.post.stopAll()

    def play_music(self, srv, mode):
        try:
            player = Play(srv, mode, PEPPER_IP)
            player.motion()
        except KeyError:
            print("KeyError occurs.")  # for debugging
            return

    # initial screen
    def home(self, srv, input_ret):
        if input_ret['type'] == 'touch':
            if input_ret['touch_position'] == 'BUTTON_MIDDLE_DOWN':
                next_scene = 'first_menu'
                srv['tablet'].showWebview(self.get_html_address(next_scene))
                srv['tts'].say("next menu")
                return SCENES[next_scene]

        elif input_ret['type'] == 'speech':
            if input_ret['word'] == 'hello':
                next_scene = 'first_menu'
                srv['aas'].say("Hello, Nice to meet you!", aas_configuration)
                srv['tablet'].showWebview(self.get_html_address(next_scene))
                return SCENES[next_scene]

            elif input_ret['word'] == 'pepper':
                next_scene = 'home'
                srv['aas'].say("Yep! Hello?!", aas_configuration)
                return SCENES[next_scene]

    def first(self, srv, input_ret):
        if input_ret['type'] == 'touch':
            if input_ret['touch_position'] == 'BUTTON_LEFT':
                next_scene = 'tour'
                srv['tablet'].showWebview(self.get_html_address(next_scene))
                srv['aas'].say("What would you like me to introduce?")
                return SCENES[next_scene]

            elif input_ret['touch_position'] == 'BUTTON_RIGHT':
                next_scene = 'entertain'
                srv['tablet'].showWebview(self.get_html_address(next_scene))
                srv['tts'].say("What should we do? Please choose one")
                return SCENES[next_scene]

            elif input_ret['touch_position'] == 'BUTTON_LEFT_DOWN':
                srv['tts'].say("Bye-bye!")
                next_scene = 'exit'
                return SCENES[next_scene]

            elif input_ret['touch_position'] == 'BUTTON_MIDDLE_DOWN':
                next_scene = 'home'
                srv['tablet'].showWebview(self.get_html_address(next_scene))
                srv['aas'].say("To the initial screen")
                return SCENES[next_scene]

            elif input_ret['touch_position'] == 'BUTTON_RIGHT_DOWN':
                next_scene = 'first_menu'
                srv['tts'].setParameter("defaultVoiceSpeed", 100)
                srv['aas'].say(
                    "Are you curious about me? I am Pepper. It is a humanoid robot made by Softbank, and can use artificial intelligence. It is characterized by a cute appearance, and is introduced in various fields such as finance, bookstore, medical care, and distribution fields in Korea")
                srv['tts'].setParameter("defaultVoiceSpeed", 70)
                return SCENES[next_scene]

        elif input_ret['type'] == 'speech':
            say = None
            if input_ret['word'] == 'back':
                next_scene = 'home'
            elif input_ret['word'] == 'about':
                next_scene = 'tour'
                say = "What would you like me to introduce?"
            elif input_ret['word'] == 'play':
                next_scene = 'entertain'
                say = "What should we do? Please choose one"
            elif input_ret['word'] == 'bye':
                next_scene = 'exit'
                say = "Bye-bye!"
            else:
                next_scene = 'first_menu'

            srv['tablet'].showWebview(self.get_html_address(next_scene))
            if say is not None:
                srv['aas'].say(say)
            return SCENES[next_scene]

    def tour(self, srv, input_ret):
        if input_ret['type'] == 'touch':
            if input_ret['touch_position'] == 'BUTTON_RIGHT':
                next_scene = self.tour_iot(srv)

            elif input_ret['touch_position'] == 'BUTTON_LEFT':
                next_scene = self.tour_arm(srv)

            elif input_ret['touch_position'] == 'BUTTON_MIDDLE_DOWN':
                next_scene = 'home'
                srv['tablet'].showWebview(self.get_html_address(next_scene))
                srv['aas'].say("To the initial screen", aas_configuration)

            elif input_ret['touch_position'] == 'BUTTON_LEFT_DOWN':
                next_scene = 'first_menu'
                srv['tablet'].showWebview(self.get_html_address(next_scene))
                srv['tts'].say("previous menu")

            elif input_ret['touch_position'] == 'BUTTON_RIGHT_DOWN':
                next_scene = 'tour'
                srv['tts'].setParameter("defaultVoiceSpeed", 110)
                srv['aas'].say(
                    "Are you curious about me? I am Pepper. It is a humanoid robot made by Softbank, and can use artificial intelligence. It is characterized by a cute appearance, and is introduced in various fields such as finance, bookstore, medical care, and distribution fields in Korea",
                    aas_configuration)
                srv['tts'].setParameter("defaultVoiceSpeed", 70)

            else:
                next_scene = 'tour'

            return SCENES[next_scene]

        elif input_ret['type'] == 'speech':
            if input_ret['word'] == 'robot':
                next_scene = self.tour_robot(srv)
            elif input_ret['word'] == 'lab':
                next_scene = self.tour_lab(srv)
            elif input_ret['word'] == 'back':
                next_scene = 'first_menu'
                srv['tablet'].showWebview(self.get_html_address(next_scene))
                srv['aas'].say("Okay. What should we do then?")
            else:
                next_scene = 'tour'

            return SCENES[next_scene]

    def entertain(self, srv, input_ret):
        if input_ret['type'] == 'touch':
            if input_ret['touch_position'] == 'BUTTON_MIDDLE_DOWN':
                next_scene = 'home'
                srv['tablet'].showWebview(self.get_html_address(next_scene))
                srv['tts'].say("To the initial screen")
                return SCENES[next_scene]

            elif input_ret['touch_position'] == 'BUTTON_LEFT_DOWN':
                next_scene = 'first_menu'
                srv['tablet'].showWebview(self.get_html_address(next_scene))
                srv['tts'].say("previous menu")
                return SCENES[next_scene]

            elif input_ret['touch_position'] == 'BUTTON_LEFT':
                self.do_elephant(srv)

            elif input_ret['touch_position'] == 'BUTTON_RIGHT':
                next_scene = 'dance_1'
                srv['tablet'].showWebview(self.get_html_address(next_scene))
                srv['tts'].say("Next menu. Please choose one to play.")
                return SCENES[next_scene]

            elif input_ret['touch_position'] == 'BUTTON_RIGHT_DOWN':
                next_scene = 'entertain2'
                srv['tablet'].showWebview(self.get_html_address(next_scene))
                srv['tts'].say("next menu")
                return SCENES[next_scene]
            
        elif input_ret['type'] == 'speech':
            if input_ret['word'] == 'elephant':
                self.do_elephant(srv)

            elif input_ret['word'] == 'music':
                next_scene = 'dance_1'
                srv['tablet'].showWebview(self.get_html_address(next_scene))
                srv['tts'].say("Okay. Please choose one to play.")
                return SCENES[next_scene]

            elif input_ret['word'] == 'back':
                next_scene = 'first_menu'
                srv['tablet'].showWebview(self.get_html_address(next_scene))
                srv['aas'].say("Okay. What should we do then?")
                return SCENES[next_scene]

            elif input_ret['word'] == 'next':
                next_scene = 'entertain2'
                srv['tablet'].showWebview(self.get_html_address(next_scene))
                srv['tts'].say("next menu")
                return SCENES[next_scene]

    # fix after implementation
    def entertain2(self, srv, input_ret):
        if input_ret['type'] == 'touch':
            if input_ret['touch_position'] == 'BUTTON_MIDDLE_DOWN':
                next_scene = 'home'
                srv['tablet'].showWebview(self.get_html_address(next_scene))
                srv['tts'].say("To the initial screen")
                return SCENES[next_scene]

            elif input_ret['touch_position'] == 'BUTTON_LEFT_DOWN':
                next_scene = 'first_menu'
                srv['tablet'].showWebview(self.get_html_address(next_scene))
                srv['tts'].say("previous menu")
                return SCENES[next_scene]

            elif input_ret['touch_position'] == 'BUTTON_LEFT':
                # srv['tts'].say("Say cheese")
                # if input_ret['type'] == 'speech' and input_ret['word'] == 'cheese':
                photo_test = take_photo.Photo(srv)
                photo_test.take()
                srv['tablet'].showWebview(self.get_html_address('photo_screen'))
                time.sleep(3)
                srv['tablet'].showWebview(self.get_html_address('entertain2'))

            elif input_ret['touch_position'] == 'BUTTON_RIGHT':
                srv['tts'].say("You must say the number in English." \
                               + "Other languages are not allowed.")
                time.sleep(0.1)  # wait for making sound not to overlap
                srv['tts'].say("Touch anywhere to start the game.")
                time.sleep(1)  # wait for a second
                next_scene = 'updown'
                return SCENES[next_scene]

            elif input_ret['touch_position'] == 'BUTTON_RIGHT_DOWN':
                next_scene = 'entertain'
                srv['tablet'].showWebview(self.get_html_address(next_scene))
                srv['tts'].say("next menu")
                return SCENES[next_scene]

    def dance1(self, srv, input_ret):
        if input_ret['type'] == 'touch':
            if input_ret['touch_position'] == 'BUTTON_MIDDLE_DOWN':
                next_scene = 'home'
                srv['tablet'].showWebview(self.get_html_address(next_scene))
                srv['tts'].say("To the initial screen")
                return SCENES[next_scene]

            elif input_ret['touch_position'] == 'BUTTON_LEFT_DOWN':
                next_scene = 'entertain'
                srv['tablet'].showWebview(self.get_html_address(next_scene))
                srv['tts'].say("previous menu")
                return SCENES[next_scene]

            elif input_ret['touch_position'] == 'BUTTON_LEFT':
                self.play_music(srv, "disco")

            elif input_ret['touch_position'] == 'BUTTON_RIGHT':
                self.play_music(srv, "bang")
                # raise ValueError

            elif input_ret['touch_position'] == 'BUTTON_RIGHT_DOWN':
                next_scene = 'dance_2'
                srv['tablet'].showWebview(self.get_html_address(next_scene))
                srv['tts'].say("next menu")
                return SCENES[next_scene]

    def dance2(self, srv, input_ret):
        if input_ret['type'] == 'touch':
            if input_ret['touch_position'] == 'BUTTON_MIDDLE_DOWN':
                next_scene = 'home'
                srv['tablet'].showWebview(self.get_html_address(next_scene))
                srv['tts'].say("To the initial screen")
                return SCENES[next_scene]

            elif input_ret['touch_position'] == 'BUTTON_LEFT_DOWN':
                next_scene = 'dance_1'
                srv['tablet'].showWebview(self.get_html_address(next_scene))
                srv['tts'].say("previous menu")
                return SCENES[next_scene]

            elif input_ret['touch_position'] == 'BUTTON_LEFT':
                self.play_music(srv, "guitar")

            elif input_ret['touch_position'] == 'BUTTON_RIGHT':
                self.play_music(srv, "saxophone")

            elif input_ret['touch_position'] == 'BUTTON_RIGHT_DOWN':
                pass  # need to implement this

    # return the object of the next scene
    def switch(self, srv, scene, input_ret):
        if scene == "home":
            return self.home(srv, input_ret)
        elif scene == "first_menu":
            return self.first(srv, input_ret)
        elif scene == "tour":
            return self.tour(srv, input_ret)
        elif scene == "entertain":
            return self.entertain(srv, input_ret)
        elif scene == "entertain2":
            return self.entertain2(srv, input_ret)
        elif scene == "dance_1":
            return self.dance1(srv, input_ret)
        elif scene == "dance_2":
            return self.dance2(srv, input_ret)
        elif scene == "updown":
            return self.updown_game(srv, input_ret)
