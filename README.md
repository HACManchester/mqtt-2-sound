mqtt-2-sound
============

This is a python script that connects our MQTT network at Hackspace Manchester to the audio announcements when people enter the space.

To add an announce theme for yourself (that plays when you enter the door), create an ogg file with under a second of audio, and call it '''YourNickName_announce.ogg'''.  Put it in the '''audio/''' directory, and send a pull request.  Assuming its ok, i'll pull and launch it.

To change the sounds for other things, switch out the audio to your own ogg file, and send a PR:
* door_outer_opened.ogg = outer door has been opened
* buzzer.ogg = intercom buzzer has been pressed
* doorbell.ogg = inner doorbell has been pressed
