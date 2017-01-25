#!/usr/bin/python
import mosquitto
import yaml
import pygame
import time
import os
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(3, GPIO.OUT)
GPIO.output(3, GPIO.LOW)

config_f = open('config.yaml')
config = yaml.safe_load(config_f)
config_f.close()

# set up the mixer at 44100 frequency, with 16 signed bits per sample, 1 channel, with a 2048 sample buffer
#pygame.mixer.init(44100, -16, 1, 2048)

currently_playing_file = ""


def on_message(obj, udata, msg):
    print "Received %s on topic %s" % (msg.payload, msg.topic)
    if msg.topic == 'door/inner/doorbell':
        GPIO.output(3, GPIO.HIGH)
        os.system("ogg123 audio/doorbell.ogg")
        time.sleep(5)
        GPIO.output(3, GPIO.LOW)
    elif msg.topic == 'door/inner/opened/username':
        os.system("ogg123 audio/outer_door_opened.ogg")
        time.sleep(1)
        print "Person: %s has arrived." % (msg.payload)
        os.system("pico2wave -w /tmp/test.wav \"Attention, " + msg.payload + " has arrived.\"; aplay /tmp/test.wav; rm /tmp/test.wav");

def play(filename,level = 1.0):
    global currently_playing_file
    if os.path.isfile(filename):
        if (not pygame.mixer.music.get_busy()) or (currently_playing_file is not filename):
            print "Playing %s" % filename
            currently_playing_file = filename
            pygame.mixer.music.load(filename)
            pygame.mixer.music.set_volume(level)
            pygame.mixer.music.play()


mqttc = mosquitto.Mosquitto(config['mqtt']['name'])
mqttc.connect(config['mqtt']['server'], 1883, 60, True)

mqttc.subscribe("door/outer/buzzer")
mqttc.subscribe("door/outer/opened/username")

mqttc.subscribe("door/inner/doorbell")
mqttc.subscribe("door/inner/opened/username")
mqttc.on_message = on_message

while mqttc.loop() == 0:
    pass

