#!/bin/bash
# write an English text string as an audio file using Google Translate
# usage: en2audio.sh <text>
# from here:  http://stackoverflow.com/questions/9163988/download-mp3-from-google-translate-text-to-speech
wget -q -U Mozilla -O "$*.mp3" "http://translate.google.com/translate_tts?ie=UTF-8&tl=en&q=$*"