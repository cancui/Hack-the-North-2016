import os
import json
from os.path import join, dirname
from dotenv import load_dotenv
from watson_developer_cloud import SpeechToTextV1 as SpeechToText
from watson_developer_cloud import AlchemyLanguageV1 as AlchemyLanguage

from recorder import Recorder

import pyaudio
import wave
import subprocess

def record_audio(file_name):
	#This block records audio into a .wav file
	recorder = Recorder(str(file_name))
	print("Please say something nice into the microphone\n")
	recorder.record_to_file()

def speech2text(file_name):
	returned_json = ""
	username = os.environ.get("BLUEMIX_USERNAME_S2T")
	password = os.environ.get("BLUEMIX_PASSWORD_S2T")
	speech_to_text = SpeechToText(username=username, password=password)
    #print join(dirname(__file__), path_to_audio_file)
	with open((str(file_name)), 'rb') as audio_file: #with open("/home/can/workspace/speech-sentiment-python/speech.wav", 'rb') as audio_file: 
		returned_json = speech_to_text.recognize(audio_file, content_type='audio/wav')
	#extracts the actual transcript
	transcript_text = returned_json['results'][0]['alternatives'][0]['transcript']	#(((returned_json.split("u'transcript': u'"))[0]).split("'}],"))[0]
	return transcript_text

def text2speech(text_to_say):
	#length_of_text = len(text_to_say.split())
	#print length_of_text

	username = os.environ.get("BLUEMIX_USERNAME_T2S")
	password = os.environ.get("BLUEMIX_PASSWORD_T2S")

	part1 = 'curl -X POST -u ' + username + ':' + password + ' '
	part2 = '--header "Content-Type: application/json" --header "Accept: audio/wav" '
	part3 = '--data "{\\\"text\\\":\\\"' + text_to_say + '\\\"}" '
	part4 = '--output returned_speech.wav "https://stream.watsonplatform.net/text-to-speech/api/v1/synthesize"'

	bash_command = part1 + part2 + part3 + part4

	#execute command in Bash, requesting a .wav speech file by giving a text file to the text to speech API
	#subprocess.call([bash_command], shell=True)
	process = subprocess.Popen([bash_command], shell = True, stdout=subprocess.PIPE)
	output = process.communicate()[0]







	#define stream chunk   
	chunk = 1024  

	#open a wav format music  
	f = wave.open("returned_speech.wav","rb")  
	


	#instantiate PyAudio  
	p = pyaudio.PyAudio()  
	#open stream  
	stream = p.open(format = p.get_format_from_width(f.getsampwidth()), channels = f.getnchannels(), rate = f.getframerate(), output = True)  
	#read data  
	data = f.readframes(chunk)  

	#paly stream  
	while data != '':  
	    stream.write(data)  
	    data = f.readframes(chunk)  

	#stop stream  
	stream.stop_stream()  
	stream.close()  

	#close PyAudio  
	p.terminate()  

def main():

	#This block records audio into a .wav file
	#record_audio("speech.wav")

	#This block called Watson Speech to Text API to convert a .wav into text
	returned_text = speech2text("speech.wav")

	text2speech(returned_text)


	

#Makes file executable via command line
if __name__ == '__main__':
	dotenv_path = join(dirname(__file__), '.env')
	load_dotenv(dotenv_path)

	main()
