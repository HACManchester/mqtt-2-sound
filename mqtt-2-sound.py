#!/usr/bin/python
import mosquitto
import yaml
import pygame
import os

config_f = open('config.yaml')
config = yaml.safe_load(config_f)
config_f.close()

# set up the mixer at 44100 frequency, with 16 signed bits per sample, 1 channel, with a 2048 sample buffer
pygame.mixer.init(44100, -16, 1, 2048)
# set volume to maximum
pygame.mixer.music.set_volume(1.0)

currently_playing_file = ""


def on_message(obj, msg):
    print "Received %s on topic %s" % (msg.payload, msg.topic)
    if msg.topic == 'door/inner/opened/username':
        play("audio/%s_announce.ogg" % msg.payload)
    elif msg.topic == 'door/outer/buzzer':
        play("audio/buzzer.ogg")
    elif msg.topic == 'door/outer/opened/username':
        play("audio/outer_door_opened.ogg")
    elif msg.topic == 'door/inner/doorbell':
        play("audio/doorbell.ogg")


def play(filename):
    global currently_playing_file
    if os.path.isfile(filename):
        if (not pygame.mixer.music.get_busy()) or (currently_playing_file is not filename):
            print "Playing %s" % filename
            currently_playing_file = filename
            pygame.mixer.music.load(filename)
            pygame.mixer.music.play()


mqttc = mosquitto.Mosquitto(config['mqtt']['name'])
mqttc.connect(config['mqtt']['server'], 1883, 60, True)

mqttc.subscribe("door/outer/buzzer")
mqttc.subscribe("door/outer/opened/username")

mqttc.subscribe("door/inner/doorbell")
mqttc.subscribe("door/inner/opened/username")
mqttc.on_message = on_message

while mqttc.loop(timeout=100) == 0:
    pass

