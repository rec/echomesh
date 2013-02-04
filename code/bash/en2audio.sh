#!/bin/bash
# write an English text string as an audio file using Google Translate
# usage: en2audio.sh <text>
# from:  http://stackoverflow.com/questions/9163988/download-mp3-from-google-translate-text-to-speech
# see also: http://elinux.org/RPi_Text_to_Speech_(Speech_Synthesis)
wget -q -U Mozilla -O "$*.mp3" "http://translate.google.com/translate_tts?ie=UTF-8&tl=en&q=$*"

curl --output foo.mp3 --user-agent Mozilla "http://translate.google.com/translate_tts?ie=UTF-8&tl=en&q=who+am+I"