# from naoqi import ALProxy
from PIL import Image
from motion import photo_motion
import os

# string of the directory to save photos
DIRECTORY = "./cameras/photos"
# the name of the file
FILENAME = "/test_"
# the name of the file to save
PHOTONAME = "instant_photo"

# settings of the device to take a picture
RESOLUTION = 2
COLORSPACE = 11
FPS = 20
TYPE = "png"


class Photo:
    def __init__(self, srv):
        self.srv = srv
        self.directory = DIRECTORY
        self.filename = FILENAME
        self.photo_name = None
        self.count = 0

    def motion(self):
        photo_motion.take_picture(self.srv)  # motion

    def ready(self):
        photo_motion.stand(self.srv)

    def save(self):
        video_service = self.srv['video_device']
        id = video_service.subscribe("rgb_t", RESOLUTION, COLORSPACE, FPS)

        for i in range(self.count, self.count + 1):
            pepper_img = video_service.getImageRemote(id)
            width, height = pepper_img[0], pepper_img[1]
            array = pepper_img[6]
            img_str = str(bytearray(array))
            im = Image.frombytes("RGB", (width, height), img_str)
            self.photo_name = self.filename + str(i) + '.png'
            im.save(self.directory + self.photo_name, "PNG")

        self.count += 1
        video_service.unsubscribe(id)

    def take(self):
        self.ready()  # make the robot get ready
        self.save()  # save the photo
        self.motion()
        command = 'sshpass -p "1847!" scp ' + self.directory + self.photo_name \
                  + ' nao@192.168.1.188:/opt/aldebaran/www/apps/bi-html/html/src/' + PHOTONAME + '.png'
        # print(command)
        os.system(command)
